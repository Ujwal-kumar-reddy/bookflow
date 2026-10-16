"""
Check GitHub Actions Workflow Status and Job Details
"""
import urllib.request
import json

REPO = "Ujwal-kumar-reddy/bookflow"

def check_details():
    url = f"https://api.github.com/repos/{REPO}/actions/runs"
    req = urllib.request.Request(url, headers={"User-Agent": "Python"})
    with urllib.request.urlopen(req) as resp:
        runs = json.loads(resp.read().decode()).get("workflow_runs", [])

    if not runs:
        print("No runs found")
        return

    latest = runs[0]
    run_id = latest["id"]
    print(f"Run {run_id}: status={latest['status']}, conclusion={latest['conclusion']}, html={latest['html_url']}")

    jobs_url = f"https://api.github.com/repos/{REPO}/actions/runs/{run_id}/jobs"
    req_jobs = urllib.request.Request(jobs_url, headers={"User-Agent": "Python"})
    with urllib.request.urlopen(req_jobs) as resp:
        jobs_resp = json.loads(resp.read().decode())
        jobs = jobs_resp.get("jobs", [])
        print(f"Jobs count: {len(jobs)}")
        for j in jobs:
            print(f"\n--- Job: {j.get('name')} | status: {j.get('status')} | conclusion: {j.get('conclusion')} ---")
            for s in j.get("steps", []):
                print(f"  * Step {s.get('number')}: {s.get('name')} | status={s.get('status')} | conclusion={s.get('conclusion')}")

if __name__ == "__main__":
    check_details()
