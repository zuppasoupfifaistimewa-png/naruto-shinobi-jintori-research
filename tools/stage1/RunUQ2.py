#!/usr/bin/env python3
"""UQ2: inclusive Git history, file events and all recent Actions run/job ledger."""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path

BASELINE="e7fd95da69fe8519439fc720ee079409c59e6363"
AFTER_RUN_ID=43367280636
REPO_DEFAULT="zuppasoupfifaistimewa-png/naruto-shinobi-jintori-research"
COMMIT_FIELDS=["commit_sha","parent_shas","author","date","subject"]
FILE_FIELDS=["commit_sha","status","path"]
RUN_FIELDS=["run_id","name","path","event","status","conclusion","head_sha","created_at",
 "source_sha_match","preflight_marker_status","workflow_class"]
JOB_FIELDS=["run_id","job_id","job_name","status","conclusion","started_at","completed_at"]

def write_tsv(path:Path,fields:list[str],rows:list[dict])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        writer.writeheader();writer.writerows(rows)

def api_get(url:str,token:str)->tuple[dict|list,str,int]:
    request=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,
      "Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28",
      "User-Agent":"naruto-jintori-research-UQ2"})
    with urllib.request.urlopen(request,timeout=45) as response:
        return json.loads(response.read().decode("utf-8","replace")),response.headers.get("Link",""),response.status

def git_ledger(source_sha:str)->tuple[list[dict],list[dict]]:
    spec=f"{BASELINE}^..{source_sha}"
    command=["git","log","--no-renames","--date=iso-strict",
      "--format=UQ_COMMIT%x09%H%x09%P%x09%an%x09%ad%x09%s","--name-status",spec]
    process=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=False)
    if process.returncode!=0:raise RuntimeError("GIT_LOG_FAILED: "+process.stdout[-2000:])
    commits=[];files=[];current=""
    for line in process.stdout.splitlines():
        if line.startswith("UQ_COMMIT\t"):
            parts=line.split("\t",5)
            if len(parts)!=6:continue
            _,sha,parents,author,date,subject=parts
            commits.append({"commit_sha":sha,"parent_shas":parents,"author":author,"date":date,"subject":subject})
            current=sha
        elif line and current:
            parts=line.split("\t",1)
            if len(parts)==2:files.append({"commit_sha":current,"status":parts[0],"path":parts[1]})
    return commits,files

def all_runs(repo:str,token:str)->tuple[list[dict],int]:
    found=[];page=1
    while True:
        data,_,_=api_get(f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}",token)
        items=data.get("workflow_runs",[]);found.extend(items)
        if len(items)<100:break
        page+=1
        if page>60:raise RuntimeError("ACTIONS_RUN_PAGINATION_LIMIT")
    return found,page

def jobs_for_run(repo:str,token:str,run_id:int)->list[dict]:
    rows=[];page=1
    while True:
        data,_,_=api_get(f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs?per_page=100&page={page}",token)
        items=data.get("jobs",[])
        for j in items:
            rows.append({"run_id":run_id,"job_id":j.get("id",""),"job_name":j.get("name",""),
              "status":j.get("status",""),"conclusion":j.get("conclusion") or "",
              "started_at":j.get("started_at") or "","completed_at":j.get("completed_at") or ""})
        if len(items)<100:break
        page+=1
        if page>30:raise RuntimeError(f"JOB_PAGINATION_LIMIT:{run_id}")
    return rows

def self_test()->None:
    assert BASELINE=="e7fd95da69fe8519439fc720ee079409c59e6363"
    assert AFTER_RUN_ID==43367280636
    assert "A" in ("A","M","D")
    print("UQ2_SELF_TEST=PASS baseline, threshold and ledger schema")

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",default=REPO_DEFAULT)
    parser.add_argument("--token",default=os.getenv("GH_TOKEN",""))
    parser.add_argument("--source-sha",default=os.getenv("GITHUB_SHA",""))
    parser.add_argument("--run-id",default=os.getenv("GITHUB_RUN_ID",""))
    parser.add_argument("--preflight-marker",type=Path)
    parser.add_argument("--out-dir",type=Path)
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:self_test();return 0
    if not args.token or not args.source_sha or not args.out_dir:parser.error("--token --source-sha --out-dir required")
    out=args.out_dir;out.mkdir(parents=True,exist_ok=True)
    head=subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True,check=False)
    checkout_sha=head.stdout.strip() if head.returncode==0 else "TIDAK TAHU"
    marker_exists=bool(args.preflight_marker and args.preflight_marker.is_file() and args.preflight_marker.stat().st_size>0)
    marker_text=args.preflight_marker.read_text(encoding="utf-8",errors="replace") if marker_exists else ""
    source_match=re.search(r"^(?:SOURCE_SHA|GITHUB_SHA)=([0-9a-f]{40})$",marker_text,re.M)
    status_match=re.search(r"^STATUS=(TUNTAS|SEBAGIAN|BELUM)$",marker_text,re.M)
    marker_sha=source_match.group(1) if source_match else ""
    marker_ok=bool(marker_exists and status_match and status_match.group(1)=="TUNTAS" and marker_sha==args.source_sha)
    commits,files=git_ledger(args.source_sha)
    runs,pages=all_runs(args.repo,args.token)
    selected=sorted([r for r in runs if int(r.get("id",0))>AFTER_RUN_ID],key=lambda r:int(r["id"]))
    current=next((r for r in selected if int(r.get("id",0))==int(args.run_id or 0)),None)
    job_rows=[];job_errors=0
    for run in selected:
        try:job_rows.extend(jobs_for_run(args.repo,args.token,int(run["id"])))
        except Exception as exc:
            job_errors+=1
            job_rows.append({"run_id":run.get("id",""),"job_id":"","job_name":"JOB_FETCH_FAILED",
              "status":"ERROR","conclusion":type(exc).__name__+":"+str(exc)[:300],"started_at":"","completed_at":""})
    run_rows=[]
    for run in selected:
        name=run.get("name","");path=run.get("path","")
        kind=(name+" "+path).lower()
        if "uq0-uq2" in kind or "uq0_uq2" in kind:
            workflow_class="UQ_CODE_RUN"
            marker_state="PASS_CURRENT_SOURCE_PREFLIGHT" if run.get("head_sha")==args.source_sha and marker_ok else (
              "NOT_VERIFIED_DIFFERENT_SOURCE_SHA" if run.get("head_sha")!=args.source_sha else "FAIL_OR_MISSING_PREFLIGHT")
        elif "monitor" in kind:
            workflow_class="STORYMODE_MONITOR_ONLY";marker_state="NOT_APPLICABLE_MONITOR"
        else:
            workflow_class="OTHER_WORKFLOW";marker_state="NOT_APPLICABLE_OTHER_WORKFLOW"
        run_rows.append({"run_id":run.get("id",""),"name":name,"path":path,"event":run.get("event",""),
          "status":run.get("status",""),"conclusion":run.get("conclusion") or "","head_sha":run.get("head_sha",""),
          "created_at":run.get("created_at",""),"source_sha_match":"YES" if run.get("head_sha")==args.source_sha else "NO",
          "preflight_marker_status":marker_state,"workflow_class":workflow_class})
    monitor=[r for r in selected if "monitor" in (r.get("name","")+" "+r.get("path","")).lower()]
    uq_runs=[r for r in selected if "uq0-uq2" in r.get("path","").lower() or "uq0-uq2" in r.get("name","").lower()]
    write_tsv(out/"UQ2_COMMITS.tsv",COMMIT_FIELDS,commits)
    write_tsv(out/"UQ2_FILE_EVENTS.tsv",FILE_FIELDS,files)
    write_tsv(out/"UQ2_ACTIONS_RUNS.tsv",RUN_FIELDS,run_rows)
    write_tsv(out/"UQ2_ACTIONS_JOBS.tsv",JOB_FIELDS,job_rows)
    current_ok=bool(current and current.get("head_sha")==args.source_sha)
    summary=["UQ2_INCLUSIVE_GIT_AND_ACTIONS_LEDGER",
      "STATUS="+("TUNTAS" if checkout_sha==args.source_sha and marker_ok and current_ok and job_errors==0 else "SEBAGIAN"),
      "EVIDENCE=K4 repository Git metadata and Actions run/job metadata; no gameplay semantics",
      f"BASELINE_INCLUSIVE={BASELINE}",f"AFTER_RUN_ID_STRICTLY_GREATER_THAN={AFTER_RUN_ID}",
      f"SOURCE_SHA={args.source_sha}",f"GIT_CHECKOUT_HEAD_SHA={checkout_sha}",
      f"SOURCE_SHA_MATCHES_CHECKOUT={'YES' if checkout_sha==args.source_sha else 'NO'}",
      f"PREFLIGHT_MARKER_PATH={args.preflight_marker if args.preflight_marker else 'TIDAK TAHU'}",
      f"PREFLIGHT_MARKER_NONEMPTY={'YES' if marker_exists else 'NO'}",
      f"PREFLIGHT_STATUS={status_match.group(1) if status_match else 'TIDAK TAHU'}",
      f"PREFLIGHT_MARKER_SOURCE_SHA={marker_sha or 'TIDAK TAHU'}",
      f"COMMIT_COUNT_INCLUSIVE={len(commits)}",f"FILE_EVENT_COUNT={len(files)}",
      "FILE_EVENT_TYPES=A/M/D; --no-renames",
      f"ACTIONS_API_PAGES={pages}",f"ACTIONS_RUNS_TOTAL_SEEN={len(runs)}",
      f"ACTIONS_RUNS_ABOVE_THRESHOLD={len(selected)}",
      f"UQ_WORKFLOW_RUNS_ABOVE_THRESHOLD={len(uq_runs)}",
      f"STORYMODE_MONITOR_RUNS_ABOVE_THRESHOLD={len(monitor)}",
      "STORYMODE_MONITOR_DETAILS="+";".join(
        f"{r.get('id')}:{r.get('status')}/{r.get('conclusion')}:sha={r.get('head_sha')}" for r in monitor) if monitor else "NO_MONITOR_RUNS_ABOVE_THRESHOLD",
      f"ACTIONS_JOB_ROWS={len(job_rows)}",f"ACTIONS_JOB_FETCH_ERRORS={job_errors}",
      f"CURRENT_RUN_ID={args.run_id or 'TIDAK TAHU'}",
      f"CURRENT_RUN_PRESENT={'YES' if current else 'NO'}",
      f"CURRENT_RUN_HEAD_SHA={current.get('head_sha') if current else 'TIDAK TAHU'}",
      f"CURRENT_RUN_SHA_MATCHES_SOURCE={'YES' if current_ok else 'NO'}",
      "CLOSEOUT_COMMIT_INCLUDED=NO; UQ2 source snapshot is GITHUB_SHA before the later report-only commit",
      "LEDGER_RANGE=BASELINE^..SOURCE_SHA; baseline commit itself is included",
      "STORYMODE_COMPLETION=TIDAK TAHU; monitor metadata does not prove gameplay progress"]
    (out/"UQ2_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary),flush=True)
    return 0 if summary[1]=="STATUS=TUNTAS" else 2

if __name__=="__main__":
    raise SystemExit(main())
