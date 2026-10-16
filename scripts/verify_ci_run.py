"""
Detailed CI Run and Job Verification for BookFlow
"""
import urllib.request
import json

REPO = "Ujwal-kumar-reddy/bookflow"

def print_run_details():
    url = f"https://api.github.com/repos/{REPO}/actions/runs"
    req = urllib.request.Request(url, headers={"User-Agent": "Python", "Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req) as resp:
        runs = json.loads(resp.read().decode()).get("workflow_runs", [])

    if not runs:
        print("No runs found.")
        return

    latest = runs[0]
    run_id = latest["id"]
    print("=" * 65)
    print("BOOKFLOW CI/CD PIPELINE EXECUTION VERIFICATION")
    print("=" * 65)
    print(f"Run ID: {run_id}")
    print(f"Workflow: {latest.get('name')}")
    print(f"Commit SHA: {latest.get('head_sha')}")
    print(f"Commit Message: {latest.get('head_commit', {}).get('message')}")
    print(f"Overall Status: {latest.get('status')}")
    print(f"Overall Conclusion: {latest.get('conclusion')}")
    print(f"HTML URL: {latest.get('html_url')}")
    print("-" * 65)

    jobs_url = f"https://api.github.com/repos/{REPO}/actions/runs/{run_id}/jobs"
    req_jobs = urllib.request.Request(jobs_url, headers={"User-Agent": "Python", "Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req_jobs) as resp:
        jobs = json.loads(resp.read().decode()).get("jobs", [])

    for j in jobs:
        print(f"\n[Job] {j.get('name')} -> Status: {j.get('status')}, Conclusion: {j.get('conclusion')}")
        print(f"Started: {j.get('started_at')} | Completed: {j.get('completed_at')}")
        for s in j.get("steps", []):
            duration = ""
            print(f"   - Step {s.get('number'):2d}: {s.get('name'):<45} | {s.get('status')} | {s.get('conclusion')}")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    print_run_details()
