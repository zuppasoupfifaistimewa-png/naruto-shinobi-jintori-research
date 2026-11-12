#!/usr/bin/env python3
"""UN2: baseline-inclusive no-renames commit ledger and full Actions census."""
from __future__ import annotations
import argparse,csv,html,json,os,re,subprocess,tempfile,urllib.request
from pathlib import Path

BASELINE="e8e1c04884b97aa500b10b8cbc6cfb25403ad27e"
CUTOFF=43211668588
API_VERSION="2022-11-28"
CF=["commit_sha","parents","author","author_date","subject"]
EF=["commit_sha","event_no_renames","raw_status","additions","deletions","path"]
RF=["run_id","workflow","event","created_at","run_status","run_conclusion","source_sha","branch","html_url"]
JF=["run_id","job_id","workflow","job_name","job_status","job_conclusion","exit_code_from_conclusion","source_sha","html_url"]
SF=["item","value"]
def git(*args):return subprocess.check_output(["git",*args],text=True,stderr=subprocess.STDOUT).strip()
def api(url,token):
    req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+token,"X-GitHub-Api-Version":API_VERSION,"User-Agent":"Naruto-UN2-static-ledger"})
    with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read().decode("utf-8"))
def write(path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n");w.writerow(fields);w.writerows(rows)
def read(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
def commits(out,source):
    git("fetch","origin","main","--quiet")
    if git("rev-parse",source)!=source or git("merge-base",BASELINE,source)!=BASELINE:raise RuntimeError("BASELINE_NOT_ANCESTOR_OR_SOURCE_SHA_INVALID")
    chain=git("rev-list","--reverse","--ancestry-path",BASELINE+".."+source).splitlines()
    shas=[BASELINE]+chain
    cr=[];er=[];counts={"A":0,"M":0,"D":0,"R":0,"OTHER":0}
    for sha in shas:
        meta=git("show","-s","--format=%H%x09%P%x09%an%x09%aI%x09%s",sha).split("\t",4)
        while len(meta)<5:meta.append("")
        cr.append(meta);parent=meta[1].split()[0] if meta[1] else ""
        if not parent:continue
        names=git("diff","--name-status","--no-renames",parent,sha)
        stats={}
        for line in git("diff","--numstat","--no-renames",parent,sha).splitlines():
            p=line.split("\t",2)
            if len(p)==3:stats[p[2]]=(p[0],p[1])
        for line in names.splitlines():
            p=line.split("\t");status=p[0];path=p[-1];code=status[:1]
            counts[code if code in counts else "OTHER"]+=1
            add,delete=stats.get(path,("0","0"));er.append([sha,code,status,add,delete,path])
    write(out/"UN2_COMMITS.tsv",CF,cr);write(out/"UN2_FILE_EVENTS.tsv",EF,er)
    base_date=git("show","-s","--format=%cI",BASELINE)
    return len(shas),len(er),counts,base_date,cr
def all_runs(repo,token,ceiling):
    found={};page=1
    while True:
        data=api(f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}",token);rr=data.get("workflow_runs",[])
        for run in rr:
            rid=int(run.get("id",0))
            if CUTOFF<rid<=ceiling:found[rid]=run
        if not rr or len(rr)<100 or max(int(x.get("id",0)) for x in rr)<=CUTOFF:break
        page+=1
    run_rows=[];job_rows=[]
    for rid,run in sorted(found.items()):
        sha=run.get("head_sha","");con=run.get("conclusion") or "IN_PROGRESS_OR_UNKNOWN"
        run_rows.append([rid,run.get("name",""),run.get("event",""),run.get("created_at",""),run.get("status",""),con,sha,run.get("head_branch",""),run.get("html_url","")])
        jobs=[];jp=1
        while True:
            jdata=api(f"https://api.github.com/repos/{repo}/actions/runs/{rid}/jobs?per_page=100&page={jp}",token);jj=jdata.get("jobs",[]);jobs.extend(jj)
            if not jj or len(jj)<100:break
            jp+=1
        if not jobs:job_rows.append([rid,"TIDAK TAHU",run.get("name",""),"TIDAK TAHU","TIDAK TAHU","TIDAK TAHU","TIDAK TAHU",sha,"TIDAK TAHU"])
        for j in jobs:
            jc=j.get("conclusion") or "IN_PROGRESS_OR_UNKNOWN"
            # Success is exit 0; failure/cancellation codes are not exposed by the Jobs REST schema.
            ec="0" if jc=="success" else ("NOT_APPLICABLE" if jc=="skipped" else "TIDAK TAHU")
            job_rows.append([rid,j.get("id",""),run.get("name",""),j.get("name",""),j.get("status",""),jc,ec,sha,j.get("html_url","")])
    return run_rows,job_rows
def actions_page(repo,token,ceiling,out):
    url=f"https://github.com/{repo}/actions"
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,"Accept":"text/html","User-Agent":"Mozilla/5.0 UN2-html-audit"})
    with urllib.request.urlopen(req,timeout=60) as r:code=r.status;body=r.read().decode("utf-8","replace")
    ids=sorted({int(x) for x in re.findall(r"/actions/runs/(\d+)",body) if int(x)<=ceiling})
    flat=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",body)))
    monitor="naruto-storymode-adaptive-monitor.yml" in body.lower() or "story mode adaptive player monitor" in flat.lower()
    scheduled=monitor and bool(re.search(r"schedule|scheduled",body,re.I))
    write(out/"UN2_ACTIONS_PAGE.txt",["item","value"],[("URL",url),("HTTP_STATUS",code),("VISIBLE_RUN_IDS",";".join(map(str,ids))),("STORY_MODE_MONITOR_VISIBLE","YES" if monitor else "NO"),("SCHEDULE_MARKER_VISIBLE","YES" if scheduled else "NO")])
    return code==200,ids,monitor,scheduled
def capture(repo,token,source,ceiling,out):
    out.mkdir(parents=True,exist_ok=True)
    nc,ne,counts,base_date,cr=commits(out,source);runs,jobs=all_runs(repo,token,ceiling)
    write(out/"UN2_ACTIONS_RUNS.tsv",RF,runs);write(out/"UN2_ACTIONS_JOBS.tsv",JF,jobs)
    page_ok,visible,monitor,scheduled=actions_page(repo,token,ceiling,out)
    current=next((r for r in runs if int(r[0])==ceiling),None);current_jobs=[j for j in jobs if int(j[0])==ceiling]
    source_match=bool(current and current[6]==source)
    events={}
    for r in runs:events[r[2]]=events.get(r[2],0)+1
    failed=[r for r in runs if r[5] not in ("success","IN_PROGRESS_OR_UNKNOWN")]
    schedules=[r for r in runs if r[2]=="schedule"]
    summary=[("STATUS","SEBAGIAN"),("EVIDENCE_LEVEL","K4 maximum; static source history and Actions metadata"),("K5_BLOCKER","No repeated runtime launch evidence; repeated API capture is not gameplay/runtime K5"),("BASELINE_INCLUSIVE",BASELINE),("BASELINE_COMMITTER_DATE",base_date),("SOURCE_SHA",source),("HEAD_LEDGER_CAPTURE",git("rev-parse",source)),("SOURCE_SHA_IN_LEDGER","YES" if source in [r[0] for r in cr] else "NO"),("COMMITS_INCLUDING_BASELINE",nc),("FILE_EVENTS_NO_RENAMES",ne),("FILE_EVENT_COUNTS",";".join(f"{k}={v}" for k,v in counts.items())),("ACTIONS_RUN_ID_STRICTLY_GREATER_THAN",CUTOFF),("ACTIONS_RUN_ID_UPPER_BOUND",ceiling),("ACTIONS_RUN_COUNT",len(runs)),("ACTIONS_JOB_COUNT",len(jobs)),("CURRENT_RUN_INCLUDED","YES" if current else "NO"),("CURRENT_RUN_STATUS",current[4] if current else "TIDAK TAHU"),("CURRENT_RUN_CONCLUSION",current[5] if current else "TIDAK TAHU"),("CURRENT_RUN_SOURCE_SHA_MATCH","YES" if source_match else "NO"),("NON_SUCCESS_RUNS_INCLUDING_FAILED_CANCELLED",len(failed)),("SCHEDULE_EVENT_RUNS",len(schedules)),("SCHEDULE_RUN_IDS",";".join(str(r[0]) for r in schedules) or "NONE"),("RUN_EVENT_COUNTS",";".join(f"{k}={v}" for k,v in sorted(events.items()))),("ACTIONS_HTML_HTTP_200","PASS" if page_ok else "NO"),("ACTIONS_HTML_VISIBLE_ID_COUNT",len(visible)),("STORY_MODE_MONITOR_VISIBLE","YES" if monitor else "NO"),("STORY_MODE_SCHEDULE_MARKER_VISIBLE","YES" if scheduled else "NO"),("CURRENT_RUN_JOB_ROWS",len(current_jobs)),("CLOSEOUT_COMMIT_INCLUDED","NO; output publication occurs after this source-SHA capture")]
    write(out/"UN2_SUMMARY.tsv",SF,summary)
    payload={n:(out/n).read_bytes() for n in ("UN2_COMMITS.tsv","UN2_FILE_EVENTS.tsv","UN2_ACTIONS_RUNS.tsv","UN2_ACTIONS_JOBS.tsv")}
    return {"commits":nc,"events":ne,"counts":counts,"runs":runs,"jobs":jobs,"current":current,"source_match":source_match,"page_ok":page_ok and monitor and scheduled,"payload":payload,"summary":summary}
def self_test():
    assert len(BASELINE)==40 and CUTOFF==43211668588
    print("UN2_SELF_TEST=PASS inclusive baseline and strict Actions cutoff")
def main():
    p=argparse.ArgumentParser();p.add_argument("--repo");p.add_argument("--token");p.add_argument("--out-dir",type=Path);p.add_argument("--self-test",action="store_true");a=p.parse_args()
    if a.self_test:self_test();return 0
    if not a.repo or not a.token or not a.out_dir:p.error("--repo --token --out-dir required")
    source=os.getenv("GITHUB_SHA","");ceiling=int(os.getenv("GITHUB_RUN_ID","0"))
    if not source or git("rev-parse","HEAD")!=source:raise SystemExit("UN2_SOURCE_SHA_MISMATCH")
    if ceiling<=CUTOFF:raise SystemExit("UN2_CURRENT_RUN_NOT_ABOVE_CUTOFF")
    first=capture(a.repo,a.token,source,ceiling,a.out_dir)
    with tempfile.TemporaryDirectory(prefix="un2-repeat-") as td:second=capture(a.repo,a.token,source,ceiling,Path(td))
    same=all(first["payload"][k]==second["payload"][k] for k in first["payload"])
    meta=first["commits"]==second["commits"] and first["events"]==second["events"] and first["counts"]==second["counts"] and [r[0:7] for r in first["runs"]]==[r[0:7] for r in second["runs"]] and [j[0:7] for j in first["jobs"]]==[j[0:7] for j in second["jobs"]]
    comparison=[("REPEAT_CAPTURE_STATIC_FILES_IDENTICAL","YES" if same else "NO"),("REPEAT_CAPTURE_METADATA_IDENTICAL","YES" if meta else "NO"),("SOURCE_SHA_IS_FINAL_CODE_SHA","YES" if first["source_match"] else "NO"),("K_LEVEL","K4 maximum; static ledger only"),("K5","NOT_MET: no runtime launch repetitions"),("CLOSEOUT_COMMIT_INCLUDED","NO")]
    write(a.out_dir/"UN2_REPEAT_COMPARISON.tsv",SF,comparison)
    ok=same and meta and first["source_match"] and first["current"] is not None and first["page_ok"]
    print(f"UN2_SEBAGIAN_K4 commits={first['commits']} events={first['events']} runs={len(first['runs'])} jobs={len(first['jobs'])} repeat={same and meta}")
    return 2 if ok else 1
if __name__=="__main__":raise SystemExit(main())
