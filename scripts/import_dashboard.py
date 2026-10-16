import urllib.request
import json
import base64

with open('monitoring/bookflow-dashboard.json', 'r', encoding='utf-8') as f:
    dashboard_data = json.load(f)

# Grafana API expects a wrapper payload: {"dashboard": <dashboard_data>, "overwrite": True}
# Clear id and set overwrite True
dashboard_data["id"] = None
payload = {
    "dashboard": dashboard_data,
    "overwrite": True
}

req = urllib.request.Request(
    "http://localhost:3001/api/dashboards/db",
    data=json.dumps(payload).encode('utf-8'),
    headers={
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(b"admin:admin").decode('ascii')
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print("Dashboard uploaded successfully!")
        print(f"UID: {result.get('uid')}")
        print(f"URL: {result.get('url')}")
        print(f"Status: {result.get('status')}")
except Exception as e:
    print(f"Failed to upload dashboard: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
