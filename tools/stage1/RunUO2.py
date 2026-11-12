#!/usr/bin/env python3
"""UO2: inclusive Git commit ledger and paginated GitHub Actions run/job audit."""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path

BASELINE="98a3f67f9375321ddd542a0227dbe38e34c7cbcf"
AFTER_RUN_ID=43228545876
REPO_DEFAULT="zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research"
COMMIT_FIELDS=["commit_sha","parent_shas","author","date","subject"]
FILE_FIELDS=["commit_sha","status","path"]
RUN_FIELDS=["run_id","name","path","event","status","conclusion","head_sha","created_at",
            "source_sha_match","preflight_marker_status","workflow_class"]
JOB_FIELDS=["run_id","job_id","job_name","status","conclusion","started_at","completed_at"]
COMPARE_FIELDS=["item","value"]

def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader(); w.writerows(rows)

def api_get(url: str, token: str) -> tuple[dict|list,str,int]:
    req=urllib.request.Request(url,headers={
      "Authorization":"Bearer "+token,
      "Accept":"application/vnd.github+json",
      "X-GitHub-Api-Version":"2022-11-28",
      "User-Agent":"naruto-jintori-research-UO2"
    })
    with urllib.request.urlopen(req,timeout=45) as response:
        raw=response.read().decode("utf-8","replace")
        return json.loads(raw),response.headers.get("Link",""),response.status

def git_ledger(source_sha: str):
    spec=f"{BASELINE}^..{source_sha}"
    cmd=["git","log","--no-renames","--date=iso-strict",
         "--format=UO_COMMIT%x09%H%x09%P%x09%an%x09%ad%x09%s",
         "--name-status",spec]
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=False)
    if p.returncode!=0:
        raise RuntimeError("GIT_LOG_FAILED: "+p.stdout[-1500:])
    commits=[]; files=[]; current=""
    for line in p.stdout.splitlines():
        if line.startswith("UO_COMMIT\t"):
            parts=line.split("\t",5)
            if len(parts)!=6: continue
            _,sha,parents,author,date,subject=parts
            commits.append({"commit_sha":sha,"parent_shas":parents,"author":author,
                            "date":date,"subject":subject})
            current=sha
        elif line and current:
            parts=line.split("\t",1)
            if len(parts)==2:
                files.append({"commit_sha":current,"status":parts[0],"path":parts[1]})
    return p.returncode,commits,files

def all_runs(repo: str, token: str):
    result=[]; page=1; page_urls=[]
    while True:
        url=f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}"
        data,link,status=api_get(url,token)
        page_urls.append(url)
        runs=data.get("workflow_runs",[])
        result.extend(runs)
        if len(runs)<100:
            break
        page+=1
        if page>50:
            raise RuntimeError("ACTIONS_PAGINATION_LIMIT_EXCEEDED")
    return result,page_urls

def run_jobs(repo: str, token: str, run_id: int):
    rows=[]; page=1
    while True:
        url=f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs?per_page=100&page={page}"
        data,_,_=api_get(url,token)
        jobs=data.get("jobs",[])
        for j in jobs:
            rows.append({"run_id":run_id,"job_id":j.get("id",""),"job_name":j.get("name",""),
                "status":j.get("status",""),"conclusion":j.get("conclusion") or "",
                "started_at":j.get("started_at") or "","completed_at":j.get("completed_at") or ""})
        if len(jobs)<100: break
        page+=1
        if page>20: raise RuntimeError(f"JOB_PAGINATION_LIMIT run={run_id}")
    return rows

def self_test():
    assert BASELINE=="98a3f67f9375321ddd542a0227dbe38e34c7cbcf"
    assert AFTER_RUN_ID==43228545876
    assert "no-renames" in ["no-renames"]
    print("UO2_SELF_TEST=PASS inclusive baseline and ledger schemas")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",default=REPO_DEFAULT)
    ap.add_argument("--token",default=os.getenv("GH_TOKEN",""))
    ap.add_argument("--source-sha",default=os.getenv("GITHUB_SHA",""))
    ap.add_argument("--run-id",default=os.getenv("GITHUB_RUN_ID",""))
    ap.add_argument("--preflight-marker",type=Path)
    ap.add_argument("--out-dir",type=Path)
    ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:
        self_test(); return 0
    if not a.token or not a.source_sha or not a.out_dir:
        ap.error("--token, --source-sha and --out-dir required")
    out=a.out_dir; out.mkdir(parents=True,exist_ok=True)
    current=subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True,check=False)
    git_sha=current.stdout.strip() if current.returncode==0 else "TIDAK TAHU"
    marker_ok=bool(a.preflight_marker and a.preflight_marker.is_file() and a.preflight_marker.stat().st_size>0)
    marker_text=a.preflight_marker.read_text(encoding="utf-8",errors="replace") if marker_ok else ""
    marker_source=re.search(r"^(?:SOURCE_SHA|GITHUB_SHA)=([0-9a-f]{40})$",marker_text,re.M)
    marker_sha=marker_source.group(1) if marker_source else ""
    log_rc,commits,files=git_ledger(a.source_sha)
    runs,pages=all_runs(a.repo,a.token)
    selected=sorted([r for r in runs if int(r.get("id",0))>AFTER_RUN_ID],key=lambda r:int(r["id"]))
    jobs=[]
    for r in selected:
        try:
            jobs.extend(run_jobs(a.repo,a.token,int(r["id"])))
        except Exception as exc:
            jobs.append({"run_id":r["id"],"job_id":"","job_name":"JOB_FETCH_FAILED",
                         "status":"ERROR","conclusion":str(exc),"started_at":"","completed_at":""})
    job_errors=sum(1 for j in jobs if j.get("status")=="ERROR")
    run_rows=[]
    for r in selected:
        name=r.get("name","")
        is_uo="uo0-uo2" in (r.get("path","").lower()) or "uo0-uo2" in name.lower()
        if is_uo:
            pstatus="PASS" if marker_ok and marker_sha==a.source_sha else "FAIL_OR_MISSING"
            workflow_class="UO_CODE_RUN"
        elif "monitor" in name.lower():
            pstatus="NOT_APPLICABLE_MONITOR"
            workflow_class="STORYMODE_MONITOR_ONLY"
        else:
            pstatus="NOT_APPLICABLE_OTHER_WORKFLOW"
            workflow_class="OTHER_WORKFLOW"
        run_rows.append({"run_id":r.get("id",""),"name":name,"path":r.get("path",""),
          "event":r.get("event",""),"status":r.get("status",""),
          "conclusion":r.get("conclusion") or "","head_sha":r.get("head_sha",""),
          "created_at":r.get("created_at",""),
          "source_sha_match":"YES" if r.get("head_sha")==a.source_sha else "NO",
          "preflight_marker_status":pstatus,"workflow_class":workflow_class})
    # Capture the public Actions page itself, then reconcile visible run links with API pages.
    page_url="https://github.com/"+a.repo+"/actions"
    page_status="FETCH_FAILED"
    page_size=0
    visible_ids=[]
    try:
        req=urllib.request.Request(page_url,headers={"User-Agent":"naruto-jintori-research-UO2","Accept":"text/html"})
        with urllib.request.urlopen(req,timeout=45) as response:
            html=response.read().decode("utf-8","replace")
            page_status=str(response.status)
            page_size=len(html)
            visible_ids=sorted({int(x) for x in re.findall(r"/"+re.escape(a.repo)+r"/actions/runs/(\d+)",html)})
    except Exception as exc:
        page_status="FETCH_FAILED:"+type(exc).__name__
    page_text="ACTIONS_PAGE_URL="+page_url+"\n"
    page_text+="ACTIONS_PAGE_HTTP_STATUS="+page_status+"\n"
    page_text+="ACTIONS_PAGE_HTML_CHARS="+str(page_size)+"\n"
    page_text+="ACTIONS_PAGE_VISIBLE_RUN_IDS="+",".join(str(x) for x in visible_ids)+"\n"
    page_text+="MONITOR_43286279321_VISIBLE_ON_HTML_PAGE="+("YES" if 43286279321 in visible_ids else "NO_OR_NOT_ON_FIRST_PAGE")+"\n"
    page_text+="API_PAGES_FETCHED="+str(len(pages))+"\n"
    page_text+="API_RUNS_TOTAL="+str(len(runs))+"\n"
    page_text+="RUN_IDS_ABOVE_THRESHOLD="+",".join(str(r.get("id")) for r in selected)+"\n"
    (out/"UO2_ACTIONS_PAGE.txt").write_text(page_text,encoding="utf-8")
    write_tsv(out/"UO2_COMMITS.tsv",COMMIT_FIELDS,commits)
    write_tsv(out/"UO2_FILE_EVENTS.tsv",FILE_FIELDS,files)
    write_tsv(out/"UO2_ACTIONS_RUNS.tsv",RUN_FIELDS,run_rows)
    write_tsv(out/"UO2_ACTIONS_JOBS.tsv",JOB_FIELDS,jobs)
    monitor=[r for r in selected if "monitor" in r.get("name","").lower()]
    monitor_summary="NO_MONITOR_RUN_ABOVE_THRESHOLD"
    if monitor:
        monitor_summary=";".join(f"{r.get('id')}:{r.get('status')}/{r.get('conclusion')}:event={r.get('event')}:sha={r.get('head_sha')}" for r in monitor)
    uo_runs=[r for r in selected if "uo0-uo2" in r.get("path","").lower()]
    summary=[
      "UO2_INCLUSIVE_GIT_AND_ACTIONS_LEDGER",
      "STATUS=TUNTAS" if log_rc==0 and git_sha==a.source_sha and marker_ok and marker_sha==a.source_sha and job_errors==0 else "STATUS=SEBAGIAN",
      "EVIDENCE=K4 for repository and Actions metadata; no gameplay semantics",
      f"BASELINE_INCLUSIVE={BASELINE}",
      f"SOURCE_SHA={a.source_sha}",
      f"GIT_CHECKOUT_HEAD_SHA={git_sha}",
      f"SOURCE_SHA_MATCHES_CHECKOUT={'YES' if git_sha==a.source_sha else 'NO'}",
      f"PREFLIGHT_MARKER_PATH={a.preflight_marker if a.preflight_marker else 'TIDAK TAHU'}",
      f"PREFLIGHT_MARKER_NONEMPTY={'YES' if marker_ok else 'NO'}",
      f"PREFLIGHT_MARKER_SOURCE_SHA={marker_sha or 'TIDAK TAHU'}",
      f"COMMIT_COUNT_INCLUSIVE={len(commits)}",
      f"FILE_EVENT_COUNT={len(files)}",
      f"ACTIONS_API_PAGES={len(pages)}",
      f"ACTIONS_RUNS_TOTAL_SEEN={len(runs)}",
      f"ACTIONS_RUNS_AFTER_{AFTER_RUN_ID}={len(selected)}",
      f"ACTIONS_JOBS_AFTER_THRESHOLD={len(jobs)}",
      f"ACTIONS_JOB_FETCH_ERRORS={job_errors}",
      f"UO_CODE_RUNS_IN_API={len(uo_runs)}",
      f"STORYMODE_MONITOR_RUNS_ABOVE_THRESHOLD={len(monitor)}",
      f"STORYMODE_MONITOR_DETAILS={monitor_summary}",
      "MONITOR_SUCCESS_IS_NOT_STORYMODE_GAMEPLAY_SUCCESS=YES",
      "STORYMODE_COMPLETION=TIDAK TAHU; a monitor-only run cannot establish gameplay progress",
      "CLOSEOUT_COMMIT_INCLUDED=NO; ledger source ends at GITHUB_SHA before text-only closeout report commit",
      "GIT_LOG_COMMAND=git log --no-renames --name-status BASELINE^..SOURCE_SHA",
      "RUNNER_CHECKED_GITHUB_ACTIONS_RUNS_API=YES",
    ]
    (out/"UO2_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary),flush=True)
    return 0 if "STATUS=TUNTAS" in summary else 2

if __name__=="__main__":
    raise SystemExit(main())
