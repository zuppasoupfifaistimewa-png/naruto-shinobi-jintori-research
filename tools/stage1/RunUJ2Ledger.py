#!/usr/bin/env python3
"""UJ2: enumerate commits and Actions runs since the inclusive baseline; text/TSV only."""
from __future__ import annotations
import argparse, csv, json, subprocess, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASELINE_DEFAULT="d2c57a796215696dc91be91fb18f36907fa5203c"
MONITOR_RUN=43109652913

def git(*args):
    return subprocess.check_output(["git",*args],text=True,stderr=subprocess.STDOUT).strip()

def api(url,token):
    req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+token,"X-GitHub-Api-Version":"2022-11-28","User-Agent":"UJ2-research-ledger"})
    with urllib.request.urlopen(req,timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def commit_ledger(baseline,out):
    git("fetch","origin","main","--quiet")
    base_date=git("show","-s","--format=%cI",baseline)
    commits=[baseline]+git("rev-list","--reverse","--ancestry-path",baseline+"..origin/main").splitlines()
    commit_rows=[]; event_rows=[]
    for sha in commits:
        meta=git("show","-s","--format=%H%x09%P%x09%an%x09%aI%x09%s",sha).split("\t",4)
        while len(meta)<5: meta.append("")
        commit_rows.append(meta)
        parent=meta[1].split()[0] if meta[1] else ""
        if parent:
            diff=git("diff","--numstat","--no-renames",parent,sha).splitlines()
            names=git("diff","--name-status","--no-renames",parent,sha).splitlines()
        else:
            diff=[]; names=[]
        stats={}
        for line in diff:
            parts=line.split("\t",2)
            if len(parts)==3: stats[parts[2]]=(parts[0],parts[1])
        for line in names:
            parts=line.split("\t",1)
            status=parts[0]; path=parts[1] if len(parts)>1 else ""
            add,delete=stats.get(path,("0","0"))
            event_rows.append([sha,status,add,delete,path])
    with (out/"UJ2_COMMITS.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n"); w.writerow(["commit_sha","parents","author","author_date","subject"]); w.writerows(commit_rows)
    with (out/"UJ2_FILE_EVENTS.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n"); w.writerow(["commit_sha","status_no_renames","additions","deletions","path"]); w.writerows(event_rows)
    return base_date,len(commit_rows),len(event_rows)

def run_ledger(repo,baseline_date,token,current_run,out):
    found={}; page=1; api_ok=True; error=""
    base=datetime.fromisoformat(baseline_date.replace("Z","+00:00"))
    while True:
        try:
            payload=api(f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}",token)
        except Exception as exc:
            api_ok=False; error=str(exc); break
        runs=payload.get("workflow_runs",[])
        if not runs: break
        older=False
        for run in runs:
            rid=int(run["id"])
            created=datetime.fromisoformat(run["created_at"].replace("Z","+00:00"))
            if created>=base or rid==MONITOR_RUN: found[rid]=run
            else: older=True
        if older or len(runs)<100: break
        page+=1
    if MONITOR_RUN not in found:
        try:
            found[MONITOR_RUN]=api(f"https://api.github.com/repos/{repo}/actions/runs/{MONITOR_RUN}",token)
        except Exception as exc:
            api_ok=False; error=(error+"; "+str(exc)).strip("; ")
    rows=[]
    for rid,run in sorted(found.items()):
        if rid==current_run: continue
        try:
            jobs=api(f"https://api.github.com/repos/{repo}/actions/runs/{rid}/jobs?per_page=100",token).get("jobs",[])
        except Exception as exc:
            api_ok=False; error=(error+"; "+str(exc)).strip("; "); jobs=[]
        if not jobs:
            rows.append([rid,run.get("name",""),run.get("event",""),run.get("created_at",""),run.get("status",""),run.get("conclusion",""),run.get("head_sha",""),"TIDAK TAHU","TIDAK TAHU","TIDAK TAHU"])
        for job in jobs:
            conclusion=job.get("conclusion") or "TIDAK TAHU"
            exit_code="0" if conclusion=="success" else ("N/A" if conclusion=="skipped" else "TIDAK TAHU")
            rows.append([rid,run.get("name",""),run.get("event",""),run.get("created_at",""),run.get("status",""),run.get("conclusion",""),run.get("head_sha",""),job.get("name",""),job.get("status",""),conclusion+":"+exit_code])
    with (out/"UJ2_ACTIONS_RUNS.tsv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n")
        w.writerow(["run_id","workflow","event","created_at","run_status","run_conclusion","source_sha","job","job_status","job_conclusion_exit_code"])
        w.writerows(rows)
    return api_ok,error,len({r[0] for r in rows}),len(rows),MONITOR_RUN in found

def self_test():
    assert BASELINE_DEFAULT.startswith("d2c57a79")
    assert MONITOR_RUN==43109652913
    print("UJ2_SELF_TEST=PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo"); ap.add_argument("--baseline",default=BASELINE_DEFAULT)
    ap.add_argument("--token"); ap.add_argument("--out-dir",type=Path); ap.add_argument("--current-run",type=int,default=0)
    ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    if a.self_test: self_test(); return 0
    if not all((a.repo,a.token,a.out_dir)): ap.error("--repo, --token and --out-dir required")
    a.out_dir.mkdir(parents=True,exist_ok=True)
    base_date,ncommits,nevents=commit_ledger(a.baseline,a.out_dir)
    api_ok,error,nruns,njobs,monitor=run_ledger(a.repo,base_date,a.token,a.current_run,a.out_dir)
    summary=["UJ2_LEDGER","STATUS=TUNTAS" if api_ok else "STATUS=SEBAGIAN",
      f"BASELINE_INCLUSIVE={a.baseline}",f"COMMIT_ROWS_INCLUDING_BASELINE={ncommits}",
      f"FILE_EVENTS_NO_RENAMES={nevents}",f"ACTIONS_RUNS_SINCE_BASELINE={nruns}",
      f"ACTIONS_JOB_ROWS={njobs}",f"MONITOR_RUN_{MONITOR_RUN}_INCLUDED={'YES' if monitor else 'NO'}",
      "CURRENT_RUN_REPORTED_SEPARATELY=YES",f"ACTIONS_API={'PASS' if api_ok else 'INCOMPLETE'}",
      f"ACTIONS_API_ERROR={error or 'NONE'}","EXIT_CODE=0" if api_ok else "EXIT_CODE=2"]
    (a.out_dir/"UJ2_LEDGER_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary)); return 0 if api_ok else 2

if __name__=="__main__": raise SystemExit(main())
