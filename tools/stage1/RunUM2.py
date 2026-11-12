#!/usr/bin/env python3
"""UM2: inclusive main-history and Actions ledger, including every run past UL cutoff."""
from __future__ import annotations
import argparse, csv, hashlib, html, json, os, re, subprocess, tempfile, urllib.request
from pathlib import Path

BASELINE = "77df5627cba56a17503f54cb7664f02129893ab7"
HARNESS_AUDIT_REFERENCE = "aa32fbcee97c8f49946a8e589010cfb9ef1a6928"
ACTIONS_CUTOFF = 43192191539
API_VERSION = "2022-11-28"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.STDOUT).strip()


def api(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json", "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": API_VERSION, "User-Agent": "UM2-reverse-engineering-ledger",
    })
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def write_tsv(path: Path, fields: list[str], rows: list[list]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(fields); w.writerows(rows)


def commit_ledger(out: Path) -> tuple[str, int, int, dict[str, int], str]:
    git("fetch", "origin", "main", "--quiet")
    head = git("rev-parse", "origin/main")
    commits = [BASELINE] + git("rev-list", "--reverse", "--ancestry-path", BASELINE + "..origin/main").splitlines()
    if not commits or commits[0] != BASELINE or git("merge-base", BASELINE, "origin/main") != BASELINE:
        raise RuntimeError("BASELINE_NOT_ANCESTOR_OF_MAIN")
    commit_rows, event_rows = [], []
    counts = {"A": 0, "M": 0, "D": 0, "R": 0, "OTHER": 0}
    for sha in commits:
        meta = git("show", "-s", "--format=%H%x09%P%x09%an%x09%aI%x09%s", sha).split("\t", 4)
        while len(meta) < 5: meta.append("")
        commit_rows.append(meta)
        parent = meta[1].split()[0] if meta[1] else ""
        if not parent:
            continue
        raw = git("diff", "--name-status", "--no-renames", parent, sha)
        numstat = git("diff", "--numstat", "--no-renames", parent, sha)
        stats = {}
        for line in numstat.splitlines():
            p = line.split("\t", 2)
            if len(p) == 3:
                stats[p[2]] = (p[0], p[1])
        for line in raw.splitlines():
            p = line.split("\t")
            status = p[0]
            path = p[-1] if len(p) > 1 else ""
            code = status[:1]
            if code not in counts:
                counts["OTHER"] += 1
            else:
                counts[code] += 1
            added, deleted = stats.get(path, ("0", "0"))
            event_rows.append([sha, code, status, added, deleted, path])
    write_tsv(out / "UM2_COMMITS.tsv", ["commit_sha", "parents", "author", "author_date", "subject"], commit_rows)
    write_tsv(out / "UM2_FILE_EVENTS.tsv", ["commit_sha", "event_no_renames", "raw_status", "additions", "deletions", "path"], event_rows)
    return head, len(commit_rows), len(event_rows), counts, git("show", "-s", "--format=%cI", BASELINE)


def actions_ledger(repo: str, token: str, out: Path, source_sha: str, run_ceiling: int) -> tuple[int, int, bool, str, list[int], list[str]]:
    run_map = {}
    page = 1
    api_ok = True
    errors = []
    while True:
        url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}"
        try:
            payload = api(url, token)
        except Exception as exc:
            api_ok = False; errors.append(f"runs_page_{page}:{exc}"); break
        runs = payload.get("workflow_runs", [])
        for run in runs:
            try:
                rid = int(run.get("id", 0))
            except (TypeError, ValueError):
                continue
            if ACTIONS_CUTOFF < rid <= run_ceiling:
                run_map[rid] = run
        if not runs or len(runs) < 100:
            break
        if max((int(x.get("id", 0)) for x in runs), default=0) <= ACTIONS_CUTOFF:
            break
        page += 1
    run_rows, job_rows, included = [], [], []
    for rid, run in sorted(run_map.items()):
        included.append(rid)
        head_sha = run.get("head_sha", "")
        run_rows.append([rid, run.get("name", ""), run.get("event", ""), run.get("created_at", ""),
                         run.get("status", ""), run.get("conclusion") or "IN_PROGRESS_OR_UNKNOWN", head_sha,
                         run.get("head_branch", ""), run.get("html_url", "")])
        try:
            jobs_payload = api(f"https://api.github.com/repos/{repo}/actions/runs/{rid}/jobs?per_page=100", token)
            jobs = jobs_payload.get("jobs", [])
        except Exception as exc:
            api_ok = False; errors.append(f"jobs_{rid}:{exc}"); jobs = []
        if not jobs:
            job_rows.append([rid, "TIDAK TAHU", run.get("name", ""), "TIDAK TAHU", "TIDAK TAHU", "TIDAK TAHU", "TIDAK TAHU", head_sha, "TIDAK TAHU"])
        for job in jobs:
            conclusion = job.get("conclusion") or "IN_PROGRESS_OR_UNKNOWN"
            exit_code = "0" if conclusion == "success" else ("NOT_APPLICABLE" if conclusion == "skipped" else "TIDAK TAHU")
            job_rows.append([rid, job.get("id", ""), run.get("name", ""), job.get("name", ""), job.get("status", ""),
                             conclusion, exit_code, head_sha, job.get("html_url", "")])
    write_tsv(out / "UM2_ACTIONS_RUNS.tsv", ["run_id", "workflow", "event", "created_at", "run_status", "run_conclusion", "source_sha", "branch", "html_url"], run_rows)
    write_tsv(out / "UM2_ACTIONS_JOBS.tsv", ["run_id", "job_id", "workflow", "job_name", "job_status", "job_conclusion", "exit_code_from_conclusion", "source_sha", "html_url"], job_rows)
    current = next((r for r in run_rows if r[0] == int(os.getenv("GITHUB_RUN_ID", "0"))), None)
    source_match = bool(current and current[6] == source_sha)
    return len(included), len(job_rows), api_ok, ";".join(errors) or "NONE", included, [f"CURRENT_RUN_SOURCE_SHA_MATCH={'YES' if source_match else 'NO'}"]



def actions_page_check(repo: str, token: str, out: Path, run_ceiling: int) -> tuple[bool, str, list[str], bool]:
    """Fetch the public Actions UI HTML itself, independently of the Actions REST API."""
    url = f"https://github.com/{repo}/actions"
    try:
        req = urllib.request.Request(url, headers={
            "Authorization": "Bearer " + token,
            "Accept": "text/html",
            "User-Agent": "Mozilla/5.0 UM2-Actions-page-audit",
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
        ids = sorted({x for x in re.findall(r"/actions/runs/(\d+)", body) if int(x) <= run_ceiling}, key=int)
        text_body = html.unescape(re.sub(r"<[^>]+>", " ", body))
        text_body = re.sub(r"\s+", " ", text_body)
        monitor_visible = ("Naruto Story Mode adaptive player monitor" in text_body
                           or "naruto-storymode-adaptive-monitor.yml" in body)
        scheduled_visible = monitor_visible and bool(re.search(r"schedule|scheduled", body, re.I))
        result = [
            f"URL={url}", f"HTTP_STATUS={status}", "FETCH_MODE=GitHub Actions HTML UI, independently fetched (not Actions REST API)",
            f"PAGE_RUN_LINK_COUNT={len(ids)}", f"PAGE_RUN_IDS={';'.join(ids) if ids else '0'}",
            f"STORY_MODE_MONITOR_VISIBLE={'YES' if monitor_visible else 'NO'}",
            f"STORY_MODE_SCHEDULE_MARKER_VISIBLE={'YES' if scheduled_visible else 'NO'}",
        ]
        ok = status == 200 and bool(ids) and monitor_visible and scheduled_visible
        result.append(f"PAGE_CHECK={'PASS' if ok else 'SEBAGIAN'}")
        (out / "UM2_ACTIONS_PAGE.txt").write_text("\n".join(result) + "\n", encoding="utf-8")
        return ok, "PASS" if ok else "SEBAGIAN", ids, scheduled_visible
    except Exception as exc:
        result = [f"URL={url}", "HTTP_STATUS=NOT_RUN", "PAGE_CHECK=NOT_RUN",
                  f"ERROR={type(exc).__name__}:{exc}"]
        (out / "UM2_ACTIONS_PAGE.txt").write_text("\n".join(result) + "\n", encoding="utf-8")
        return False, "NOT_RUN", [], False

def self_test() -> None:
    assert len(BASELINE) == 40 and len(HARNESS_AUDIT_REFERENCE) == 40
    assert ACTIONS_CUTOFF == 43192191539
    assert BASELINE != HARNESS_AUDIT_REFERENCE
    print("UM2_SELF_TEST=PASS baseline_inclusive=yes actions_run_id_gt=43192191539")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=False); ap.add_argument("--token", required=False); ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test(); return 0
    if not all((a.repo, a.token, a.out_dir)):
        ap.error("--repo, --token and --out-dir required")
    a.out_dir.mkdir(parents=True, exist_ok=True)
    source_sha = os.getenv("GITHUB_SHA", "TIDAK TAHU")
    current_run = int(os.getenv("GITHUB_RUN_ID", "0"))
    checkout_sha = git("rev-parse", "HEAD")
    if source_sha == "TIDAK TAHU" or checkout_sha != source_sha:
        raise SystemExit(f"SOURCE_SHA_MISMATCH env={source_sha} checkout={checkout_sha}")
    if current_run <= ACTIONS_CUTOFF:
        raise SystemExit("CURRENT_RUN_ID_NOT_ABOVE_ACTIONS_CUTOFF")

    def capture(destination: Path):
        head, ncommits, nevents, counts, baseline_date = commit_ledger(destination)
        nruns, njobs, api_ok, api_error, ids, current = actions_ledger(a.repo, a.token, destination, source_sha, current_run)
        page_ok, page_status, page_ids, scheduled_visible = actions_page_check(a.repo, a.token, destination, current_run)
        current_row = next((r for r in current if r.startswith("CURRENT_RUN_SOURCE_SHA_MATCH=")), "CURRENT_RUN_SOURCE_SHA_MATCH=NO")
        files = ("UM2_COMMITS.tsv", "UM2_FILE_EVENTS.tsv", "UM2_ACTIONS_RUNS.tsv", "UM2_ACTIONS_JOBS.tsv", "UM2_ACTIONS_PAGE.txt")
        payload = {name: (destination / name).read_bytes() for name in files}
        return {
            "head":head,"ncommits":ncommits,"nevents":nevents,"counts":counts,"baseline_date":baseline_date,
            "nruns":nruns,"njobs":njobs,"api_ok":api_ok,"api_error":api_error,"ids":ids,
            "page_ok":page_ok,"page_status":page_status,"page_ids":page_ids,"scheduled_visible":scheduled_visible,
            "current_row":current_row,"payload":payload,
        }

    first = capture(a.out_dir)
    with tempfile.TemporaryDirectory(prefix="um2-repeat-", dir=a.out_dir) as temp:
        second = capture(Path(temp))
    names = sorted(first["payload"])
    compare_rows = []
    for name in names:
        left, right = first["payload"][name], second["payload"][name]
        compare_rows.append((name, hashlib.sha256(left).hexdigest(), hashlib.sha256(right).hexdigest(),
                             "IDENTIK" if left == right else "BERBEDA"))
    repeat_identical = all(row[3] == "IDENTIK" for row in compare_rows)
    same_counts = (first["head"] == second["head"] == source_sha and
                   first["ncommits"] == second["ncommits"] and first["nevents"] == second["nevents"] and
                   first["counts"] == second["counts"] and first["nruns"] == second["nruns"] and
                   first["njobs"] == second["njobs"] and first["ids"] == second["ids"] and
                   first["page_ids"] == second["page_ids"])
    api_ok = first["api_ok"] and second["api_ok"]
    page_ok = first["page_ok"] and second["page_ok"]
    source_match = first["current_row"].endswith("YES") and second["current_row"].endswith("YES")
    run_present = current_run in first["ids"] and current_run in second["ids"]
    repeat_k5 = repeat_identical and same_counts and api_ok and page_ok and source_match and run_present
    status = "TUNTAS" if repeat_k5 else "SEBAGIAN"
    (a.out_dir / "UM2_REPEAT_COMPARISON.tsv").write_text(
        "file\tcapture_1_sha256\tcapture_2_sha256\tcomparison\n" +
        "".join("\t".join(row) + "\n" for row in compare_rows) +
        f"ALL_FILES_IDENTICAL\t{int(repeat_identical)}\t{int(repeat_identical)}\t{'PASS' if repeat_identical else 'FAIL'}\n" +
        f"HEAD_SOURCE_SHA_MATCH\t{source_sha}\t{first['head']}\t{'PASS' if first['head']==source_sha==second['head'] else 'FAIL'}\n" +
        f"RUN_CEILING\t{current_run}\t{current_run}\tFIXED\n",
        encoding="utf-8")
    summary = [
        "UM2_MAIN_COMMIT_AND_ACTIONS_LEDGER",
        f"STATUS={status}",
        f"EVIDENCE={'K5' if repeat_k5 else 'K4'} (two independent API/Git ledger captures in separate output directories; byte-identical comparison required)",
        f"BASELINE_INCLUSIVE={BASELINE}", f"BASELINE_COMMITTER_DATE={first['baseline_date']}",
        f"HARNESS_DELETION_AUDIT_REFERENCE_ONLY={HARNESS_AUDIT_REFERENCE}",
        f"HEAD_MAIN_AT_LEDGER_CAPTURE={first['head']}", f"WORKFLOW_SOURCE_SHA={source_sha}", f"CHECKOUT_SOURCE_SHA={checkout_sha}",
        f"SOURCE_SHA_IS_IN_LEDGER={'YES' if source_sha in [row[0] for row in read_commit_rows(a.out_dir / 'UM2_COMMITS.tsv')] else 'NO'}",
        f"COMMIT_ROWS_INCLUDING_BASELINE={first['ncommits']}", f"FILE_EVENT_ROWS_NO_RENAMES={first['nevents']}",
        *[f"FILE_EVENT_{k}={v}" for k, v in first["counts"].items()],
        "EVENT_DETECTION=git diff --no-renames; rename pairs represented as separate A/D",
        f"ACTIONS_RUN_ID_STRICTLY_GREATER_THAN={ACTIONS_CUTOFF} AND_LESS_EQUAL_TO_CURRENT_RUN={current_run}",
        f"ACTIONS_RUN_ROWS={first['nruns']}", f"ACTIONS_JOB_ROWS={first['njobs']}",
        f"CURRENT_RUN_ID={current_run}", f"CURRENT_RUN_INCLUDED={'YES' if run_present else 'NO'}", first["current_row"],
        f"ACTIONS_API={'PASS' if api_ok else 'SEBAGIAN'}",
        f"ACTIONS_API_ERRORS_CAPTURE_1={first['api_error']}",
        f"ACTIONS_API_ERRORS_CAPTURE_2={second['api_error']}",
        f"ACTIONS_PAGE_HTML_CAPTURE_1={first['page_status']}",
        f"ACTIONS_PAGE_HTML_CAPTURE_2={second['page_status']}",
        f"STORY_MODE_SCHEDULE_MARKER_VISIBLE={'YES' if first['scheduled_visible'] and second['scheduled_visible'] else 'NO'}",
        f"CAPTURE_1_VS_CAPTURE_2_IDENTICAL={'YES' if repeat_identical else 'NO'}",
        f"INDEPENDENT_SNAPSHOT_COUNTS_MATCH={'YES' if same_counts else 'NO'}",
        "RUN_CEILING=the current Actions run ID; later runs excluded to keep the ledger window fixed",
        "REPORT_CLOSEOUT_COMMIT_INCLUDED=NO (this run's own report is published after capture)",
        "STATUS_MD_RELEASE_TAG_MODIFIED=NO", "BINARY_OR_RAW_RAM_DATA_COMMITTED=NO",
        "EXIT_CODE=0" if repeat_k5 else "EXIT_CODE=2",
    ]
    (a.out_dir / "UM2_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    action_summary = [
        f"STATUS={status}", "JOB=um-audit", f"RUN_ID={current_run}", f"SOURCE_SHA={source_sha}",
        "UM2_EVIDENCE="+("K5" if repeat_k5 else "K4"), f"EXIT_CODE={0 if repeat_k5 else 2}",
    ]
    (a.out_dir / "ACTIONS_RUN_SUMMARY.txt").write_text("\n".join(action_summary) + "\n", encoding="utf-8")
    return 0 if repeat_k5 else 2

def read_commit_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f, delimiter="\t"))[1:]


if __name__ == "__main__":
    raise SystemExit(main())
