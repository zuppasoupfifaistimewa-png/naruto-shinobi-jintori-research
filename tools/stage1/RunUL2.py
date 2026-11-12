#!/usr/bin/env python3
"""UL2: inclusive no-renames Git ledger and paginated Actions runs/jobs ledger."""
from __future__ import annotations
import argparse, csv, json, os, subprocess, tempfile, time, urllib.error, urllib.request
from pathlib import Path

BASELINE_DEFAULT="abd084c4157f75f356a3867bbd68e49dbc3850d8"
RUN_ID_MIN=43145985922
COMMIT_FIELDS=["commit_sha","author","author_date","subject","A","M","D","R","OTHER","file_event_count"]
EVENT_FIELDS=["commit_sha","status","path"]
RUN_FIELDS=["run_id","name","workflow_id","event","status","conclusion","head_branch","head_sha","created_at","updated_at","run_attempt","html_url"]
JOB_FIELDS=["run_id","job_id","job_name","status","conclusion","head_sha","started_at","completed_at","steps_summary"]

def git(*args):
    p=subprocess.run(["git",*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    return p.stdout

def write_tsv(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",extrasaction="ignore",lineterminator="\n")
        w.writeheader(); w.writerows(rows)

def request_json(url,token,attempts=5):
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
      "X-GitHub-Api-Version":"2022-11-28","User-Agent":"naruto-ul2-readonly-ledger"})
    for n in range(attempts):
        try:
            with urllib.request.urlopen(req,timeout=45) as r:
                return json.loads(r.read().decode("utf-8")),dict(r.headers.items())
        except urllib.error.HTTPError as e:
            body=e.read().decode("utf-8","replace")
            if e.code in (403,429) and n+1<attempts:
                wait=int(e.headers.get("Retry-After","5")); time.sleep(min(wait,30)); continue
            raise RuntimeError(f"HTTP_{e.code}:{body[:800]}") from e
        except Exception:
            if n+1==attempts: raise
            time.sleep(2*(n+1))
    raise RuntimeError("API_RETRIES_EXHAUSTED")

def paginate(url,token):
    all_items=[]; page=1; expected_total=None
    while True:
        sep="&" if "?" in url else "?"
        data,_=request_json(f"{url}{sep}per_page=100&page={page}",token)
        if page==1 and isinstance(data.get("total_count"),int): expected_total=data["total_count"]
        items=data.get("workflow_runs",data.get("jobs"))
        if not isinstance(items,list): raise RuntimeError("PAGINATED_API_RESPONSE_MISSING_ITEMS")
        all_items.extend(items)
        if len(items)<100:
            if expected_total is not None and len(all_items)!=expected_total:
                raise RuntimeError(f"PAGINATION_COUNT_MISMATCH:EXPECTED={expected_total}:OBSERVED={len(all_items)}")
            break
        page+=1
        if page>100: raise RuntimeError("PAGINATION_SAFETY_LIMIT")
    return all_items

def commit_ledger(baseline,head,out):
    git("cat-file","-e",baseline+"^{commit}")
    if baseline!=head: git("merge-base","--is-ancestor",baseline,head)
    descendants=git("rev-list","--reverse","--ancestry-path",baseline+".."+head).splitlines()
    commits=[baseline]+descendants
    commit_rows=[]; event_rows=[]; totals={"A":0,"M":0,"D":0,"R":0,"OTHER":0}
    for sha in commits:
        meta=git("show","-s","--format=%H%x09%an%x09%aI%x09%s",sha).rstrip("\n").split("\t",3)
        parents=git("rev-list","--parents","-n","1",sha).strip().split()
        if len(parents)==1:
            diff=git("diff-tree","--root","--no-commit-id","--name-status","--no-renames","-r",sha)
        else:
            diff=git("diff","--name-status","--no-renames","-r",parents[1],sha)
        counts={"A":0,"M":0,"D":0,"R":0,"OTHER":0}
        for line in diff.splitlines():
            if not line.strip(): continue
            parts=line.split("\t",1); status=parts[0].strip(); path=parts[1] if len(parts)>1 else "TIDAK TAHU"
            key=status if status in counts else "OTHER"
            counts[key]+=1; totals[key]+=1
            event_rows.append({"commit_sha":sha,"status":status,"path":path})
        commit_rows.append({"commit_sha":meta[0],"author":meta[1],"author_date":meta[2],"subject":meta[3],
          **counts,"file_event_count":sum(counts.values())})
    write_tsv(out/"UL2_COMMITS.tsv",COMMIT_FIELDS,commit_rows)
    write_tsv(out/"UL2_COMMIT_EVENTS.tsv",EVENT_FIELDS,event_rows)
    return len(commits),len(event_rows),totals

def actions_ledger(repo,token,threshold,out):
    base=f"https://api.github.com/repos/{repo}"
    runs=paginate(base+"/actions/runs",token)
    selected=sorted([x for x in runs if int(x.get("id",0))>threshold],key=lambda x:int(x["id"]))
    run_rows=[]; job_rows=[]; schedule=[]
    for r in selected:
        rid=int(r["id"])
        run_rows.append({"run_id":rid,"name":r.get("name","TIDAK TAHU"),"workflow_id":r.get("workflow_id","TIDAK TAHU"),
          "event":r.get("event","TIDAK TAHU"),"status":r.get("status","TIDAK TAHU"),"conclusion":r.get("conclusion") or "TIDAK TAHU",
          "head_branch":r.get("head_branch","TIDAK TAHU"),"head_sha":r.get("head_sha","TIDAK TAHU"),
          "created_at":r.get("created_at","TIDAK TAHU"),"updated_at":r.get("updated_at","TIDAK TAHU"),
          "run_attempt":r.get("run_attempt","TIDAK TAHU"),"html_url":r.get("html_url","TIDAK TAHU")})
        if r.get("event")=="schedule" or "monitor" in str(r.get("name","")).lower(): schedule.append(rid)
        jobs=paginate(base+f"/actions/runs/{rid}/jobs",token)
        for j in jobs:
            steps=j.get("steps") or []
            step_s=";".join(f"{s.get('number','?')}:{s.get('name','?')}={s.get('conclusion') or s.get('status') or 'TIDAK TAHU'}" for s in steps)
            job_rows.append({"run_id":rid,"job_id":j.get("id","TIDAK TAHU"),"job_name":j.get("name","TIDAK TAHU"),
              "status":j.get("status","TIDAK TAHU"),"conclusion":j.get("conclusion") or "TIDAK TAHU","head_sha":r.get("head_sha","TIDAK TAHU"),
              "started_at":j.get("started_at") or "TIDAK TAHU","completed_at":j.get("completed_at") or "TIDAK TAHU",
              "steps_summary":step_s})
    write_tsv(out/"UL2_ACTIONS_RUNS.tsv",RUN_FIELDS,run_rows)
    write_tsv(out/"UL2_ACTIONS_JOBS.tsv",JOB_FIELDS,job_rows)
    return len(run_rows),len(job_rows),len(schedule),schedule,run_rows,job_rows

def sync_main(repo,token):
    base=f"https://api.github.com/repos/{repo}"
    for _ in range(4):
        git("fetch","origin","main")
        fetched=git("rev-parse","refs/remotes/origin/main").strip()
        branch,_=request_json(base+"/git/ref/heads/main",token)
        api_head=branch.get("object",{}).get("sha","TIDAK TAHU")
        if fetched==api_head: return fetched
        time.sleep(1)
    raise RuntimeError(f"MAIN_HEAD_DID_NOT_STABILIZE:FETCHED={fetched}:API={api_head}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo"); ap.add_argument("--baseline",default=BASELINE_DEFAULT)
    ap.add_argument("--threshold",type=int,default=RUN_ID_MIN); ap.add_argument("--token")
    ap.add_argument("--out-dir",type=Path); ap.add_argument("--current-run",type=int,default=0)
    ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
    if a.self_test:
        assert BASELINE_DEFAULT=="abd084c4157f75f356a3867bbd68e49dbc3850d8" and RUN_ID_MIN==43145985922
        original=Path.cwd()
        with tempfile.TemporaryDirectory(prefix="ul2-ledger-selftest-") as td:
            root=Path(td); repo_path=root/"repo"; out=root/"out"; repo_path.mkdir(); out.mkdir()
            os.chdir(repo_path)
            try:
                git("init","-q"); git("config","user.name","UL2 self-test"); git("config","user.email","ul2-selftest@example.invalid")
                (repo_path/"root.txt").write_text("root\n"); git("add","root.txt"); git("commit","-qm","root")
                (repo_path/"base.txt").write_text("base\n"); git("add","base.txt"); git("commit","-qm","baseline")
                baseline=git("rev-parse","HEAD").strip()
                (repo_path/"base.txt").write_text("base modified\n"); git("add","base.txt"); git("commit","-qm","modify")
                (repo_path/"new.txt").write_text("new\n"); git("add","new.txt"); git("commit","-qm","add")
                head=git("rev-parse","HEAD").strip()
                ncommits,nevents,totals=commit_ledger(baseline,head,out)
                assert ncommits==3 and nevents==3 and totals=={"A":2,"M":1,"D":0,"R":0,"OTHER":0},(ncommits,nevents,totals)
            finally:
                os.chdir(original)
        print("UL2_SELF_TEST=PASS baseline-inclusive A/M/D/R no-renames ledger")
        return 0
    if not a.repo or not a.token or not a.out_dir: ap.error("--repo --token --out-dir required")
    a.out_dir.mkdir(parents=True,exist_ok=True)
    checkout_head=git("rev-parse","HEAD").strip(); source=os.getenv("GITHUB_SHA",checkout_head)
    if checkout_head!=source: raise RuntimeError(f"CHECKOUT_SHA_MISMATCH:HEAD={checkout_head}:SOURCE={source}")
    nruns,njobs,nschedule,schedule,run_rows,job_rows=actions_ledger(a.repo,a.token,a.threshold,a.out_dir)
    ledger_head=sync_main(a.repo,a.token)
    if ledger_head!=source and not git("merge-base","--is-ancestor",source,ledger_head):
        raise RuntimeError(f"MAIN_NOT_DESCENDANT_OF_SOURCE:SOURCE={source}:MAIN={ledger_head}")
    ncommits,nevents,totals=commit_ledger(a.baseline,ledger_head,a.out_dir)
    current=next((r for r in run_rows if int(r["run_id"])==a.current_run),None)
    current_jobs=[j for j in job_rows if int(j["run_id"])==a.current_run]
    summary=["UL2 GIT AND ACTIONS LEDGER","STATUS=TUNTAS",f"BASELINE_INCLUSIVE={a.baseline}",
      f"CODE_SOURCE_SHA={source}",f"LEDGER_HEAD_AT_QUERY={ledger_head}",f"COMMITS_INCLUDING_BASELINE={ncommits}",
      f"FILE_EVENTS_NO_RENAMES={nevents}",f"TOTAL_A={totals['A']}",f"TOTAL_M={totals['M']}",
      f"TOTAL_D={totals['D']}",f"TOTAL_R={totals['R']}",f"TOTAL_OTHER={totals['OTHER']}",
      f"ACTIONS_RUN_ID_STRICTLY_GREATER_THAN={a.threshold}",f"ACTIONS_RUN_ROWS={nruns}",f"ACTIONS_JOB_ROWS={njobs}",
      f"SCHEDULED_OR_MONITOR_RUN_ROWS={nschedule}",f"SCHEDULED_OR_MONITOR_RUN_IDS={';'.join(map(str,schedule)) if schedule else 'NONE'}",
      f"CURRENT_RUN_ID={a.current_run}",f"CURRENT_RUN_STATUS={current['status'] if current else 'TIDAK TAHU'}",
      f"CURRENT_RUN_SOURCE_SHA={current['head_sha'] if current else 'TIDAK TAHU'}",f"CURRENT_RUN_JOB_ROWS={len(current_jobs)}",
      f"MAIN_HEAD_AT_LEDGER_QUERY={ledger_head}",
      "FINAL_MAIN_HEAD_AFTER_REPORT_COMMIT=TIDAK TAHU (diverifikasi setelah workflow selesai)",
      "ACTION_API=PAGINATED_ALL_PAGES; JOBS=PAGINATED_ALL_PAGES","NO_RENAMES=YES","EXIT_CODE=0"]
    (a.out_dir/"UL2_SUMMARY.txt").write_text("\n".join(summary)+"\n",encoding="utf-8")
    print("\n".join(summary)); return 0

if __name__=="__main__": raise SystemExit(main())
