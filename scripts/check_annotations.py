"""
Check check-runs error annotations
"""
import urllib.request
import json

REPO = "Ujwal-kumar-reddy/bookflow"

def check_check_runs():
    url = f"https://api.github.com/repos/{REPO}/commits/02d4ae6/check-runs"
    req = urllib.request.Request(url, headers={"User-Agent": "Python", "Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Check runs count: {data.get('total_count')}")
            for cr in data.get("check_runs", []):
                print(f"\nName: {cr.get('name')}")
                print(f"Status: {cr.get('status')}")
                print(f"Conclusion: {cr.get('conclusion')}")
                out = cr.get("output", {})
                print(f"Title: {out.get('title')}")
                print(f"Summary: {out.get('summary')}")
                print(f"Text: {out.get('text')}")
                print(f"Annotations URL: {out.get('annotations_url')}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_check_runs()
