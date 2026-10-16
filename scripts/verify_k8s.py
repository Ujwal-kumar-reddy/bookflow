"""
Local Kubernetes (Docker Desktop) Verification Script for BookFlow
Tests deployments, replica counts, services, ingress routing, CRUD API, probes, and PVC persistence.
"""
import subprocess
import urllib.request
import urllib.error
import json
import time
import sys

BASE_URL = "http://localhost:8088"

def req_json(url, method="GET", data=None, headers=None):
    h = {"Content-Type": "application/json"} if data else {}
    if headers:
        h.update(headers)
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            try:
                parsed = json.loads(content)
            except Exception:
                parsed = content
            return resp.status, parsed
    except urllib.error.HTTPError as e:
        content = e.read().decode("utf-8")
        try:
            parsed = json.loads(content)
        except Exception:
            parsed = content
        return e.code, parsed

def run_k8s_verification():
    print("=" * 65)
    print("BOOKFLOW LOCAL KUBERNETES VERIFICATION (DOCKER DESKTOP)")
    print("=" * 65)

    # 1. Inspect Pods and Replicas
    print("\n[1] Checking Pods and Replica Counts in 'bookflow' namespace...")
    res = subprocess.run(["kubectl", "get", "pods", "-n", "bookflow", "-o", "wide"], capture_output=True, text=True)
    print(res.stdout.strip())
    assert res.returncode == 0, f"kubectl get pods failed: {res.stderr}"

    # Verify replica counts via Deployment status
    res = subprocess.run(["kubectl", "get", "deployments", "-n", "bookflow", "-o", "json"], capture_output=True, text=True)
    deps = json.loads(res.stdout).get("items", [])
    for d in deps:
        name = d["metadata"]["name"]
        ready = d["status"].get("readyReplicas", 0)
        desired = d["spec"]["replicas"]
        print(f"  - Deployment '{name}': {ready}/{desired} replicas ready")
        assert ready == desired and ready >= 1, f"Deployment {name} not fully ready ({ready}/{desired})"

    # 2. Inspect Services and Ingress
    print("\n[2] Checking Services and Ingress...")
    res = subprocess.run(["kubectl", "get", "svc,ingress,hpa,pvc", "-n", "bookflow"], capture_output=True, text=True)
    print(res.stdout.strip())

    # 3. Test Ingress Routing and Probes
    print("\n[3] Testing Ingress Routing via http://localhost:8088...")
    c, html = req_json(f"{BASE_URL}/")
    print(f"  GET / (Frontend React SPA): HTTP {c} -> Contains '<div id=\"root\">': {'<div id=\"root\">' in html}")
    assert c == 200 and '<div id="root">' in html, "Frontend root not found in Ingress response"

    c, h = req_json(f"{BASE_URL}/health")
    print(f"  GET /health (Liveness via Frontend Proxy): HTTP {c} -> {h}")
    assert c == 200 and h.get("status") == "UP", f"Expected UP, got {h}"

    # 4. CRUD and Lending Operations via Ingress
    print("\n[4] Executing CRUD & Lending Operations via Ingress (/api/books)...")
    
    b1_data = {"title": "Kubernetes in Action", "author": "Marko Luksa", "category": "DevOps & Cloud"}
    c, b1 = req_json(f"{BASE_URL}/api/books", method="POST", data=b1_data)
    print(f"  POST /api/books (Book 1): HTTP {c} -> ID {b1.get('id')}: '{b1.get('title')}'")
    assert c == 201, f"Failed creating Book 1: {b1}"
    book1_id = b1["id"]

    b2_data = {"title": "Site Reliability Engineering", "author": "Betsy Beyer et al.", "category": "Site Reliability"}
    c, b2 = req_json(f"{BASE_URL}/api/books", method="POST", data=b2_data)
    print(f"  POST /api/books (Book 2): HTTP {c} -> ID {b2.get('id')}: '{b2.get('title')}'")
    assert c == 201, f"Failed creating Book 2: {b2}"
    book2_id = b2["id"]

    b3_data = {"title": "Database Internals", "author": "Alex Petrov", "category": "Data Engineering"}
    c, b3 = req_json(f"{BASE_URL}/api/books", method="POST", data=b3_data)
    print(f"  POST /api/books (Book 3): HTTP {c} -> ID {b3.get('id')}: '{b3.get('title')}'")
    assert c == 201, f"Failed creating Book 3: {b3}"
    book3_id = b3["id"]

    # Checkout Book 1
    c, b1_borrowed = req_json(f"{BASE_URL}/api/books/{book1_id}/checkout", method="POST", data={"borrower_name": "Priya Patel (STU-2026-002)", "loan_days": 21})
    print(f"  POST /api/books/{book1_id}/checkout: HTTP {c} -> Status: {b1_borrowed.get('status')}, Borrower: {b1_borrowed.get('borrower_name')}")
    assert c == 200 and b1_borrowed.get("status") == "BORROWED"

    # Verify Stats
    c, stats = req_json(f"{BASE_URL}/api/books/stats")
    print(f"  GET /api/books/stats: HTTP {c} -> Total={stats.get('total')}, Available={stats.get('available')}, Borrowed={stats.get('borrowed')}")
    assert stats["total"] >= 3 and stats["borrowed"] >= 1

    # 5. Verify PostgreSQL Data Persistence Across Pod Restarts
    print("\n[5] Testing PostgreSQL Data Persistence Across Pod Deletion...")
    res = subprocess.run(["kubectl", "get", "pods", "-n", "bookflow", "-l", "app=bookflow-postgres", "-o", "jsonpath={.items[0].metadata.name}"], capture_output=True, text=True)
    old_pg_pod = res.stdout.strip()
    print(f"  Deleting active PostgreSQL pod '{old_pg_pod}'...")
    subprocess.run(["kubectl", "delete", "pod", "-n", "bookflow", old_pg_pod], check=True, capture_output=True)

    print("  Waiting for PostgreSQL pod to be recreated and become Ready...")
    for _ in range(30):
        time.sleep(2)
        res = subprocess.run(["kubectl", "get", "pods", "-n", "bookflow", "-l", "app=bookflow-postgres", "-o", "jsonpath={.items[0].status.phase}"], capture_output=True, text=True)
        if res.stdout.strip() == "Running":
            time.sleep(3)
            break

    c, post_restart_books = req_json(f"{BASE_URL}/api/books")
    print(f"  GET /api/books (post-postgres-deletion): HTTP {c} -> Found {len(post_restart_books)} books")
    assert c == 200 and len(post_restart_books) >= 3, "Books lost after PostgreSQL pod deletion!"
    book_ids = [b["id"] for b in post_restart_books]
    assert book1_id in book_ids and book2_id in book_ids, "Original book IDs missing after restart!"
    print(f"  -> PASSED: All books persisted on PVC across PostgreSQL pod deletion!")

    print("\n" + "=" * 65)
    print("LOCAL KUBERNETES VERIFICATION PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_k8s_verification()
