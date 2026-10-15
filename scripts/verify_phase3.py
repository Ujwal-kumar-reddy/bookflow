"""
Phase 3 Local Verification Script: BookFlow Capstone
Tests backend endpoints, frontend endpoints, reverse proxy routing, and full CRUD business logic.
"""
import sys
import json
import urllib.request
import urllib.error

def request_json(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"} if data else {}
    req_body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            status_code = resp.status
            try:
                parsed = json.loads(content)
            except Exception:
                parsed = content
            return status_code, parsed
    except urllib.error.HTTPError as e:
        content = e.read().decode("utf-8")
        try:
            parsed = json.loads(content)
        except Exception:
            parsed = content
        return e.code, parsed

def run_tests():
    print("=" * 60)
    print("BOOKFLOW PHASE 3 LOCAL VERIFICATION - API & ENDPOINT TESTING")
    print("=" * 60)
    
    # 1. Direct Backend Health
    print("\n[1] Testing Backend Direct Endpoints (http://localhost:8000)")
    c, r = request_json("http://localhost:8000/health")
    print(f"  GET /health: HTTP {c} -> {r}")
    assert c == 200 and r.get("status") == "UP", f"Expected UP, got {r}"

    c, r = request_json("http://localhost:8000/ready")
    print(f"  GET /ready: HTTP {c} -> {r}")
    assert c == 200 and r.get("status") == "READY", f"Expected READY, got {r}"

    c, r = request_json("http://localhost:8000/")
    print(f"  GET /: HTTP {c} -> {r}")
    assert c == 200 and r.get("service") == "BookFlow API", f"Expected BookFlow API, got {r}"

    c, r = request_json("http://localhost:8000/metrics")
    print(f"  GET /metrics: HTTP {c} (Length: {len(r)} bytes)")
    assert c == 200 and "app_info" in r or "http_requests" in r or "fastapi" in r or "python_info" in r, "Expected Prometheus metrics"

    # 2. Frontend Web Server and Reverse Proxy
    print("\n[2] Testing Frontend Web Server & Proxy (http://localhost:3000)")
    c, r = request_json("http://localhost:3000")
    print(f"  GET / (Frontend SPA): HTTP {c} (HTML length: {len(r)} bytes)")
    assert c == 200 and "<div id=\"root\">" in r, "Expected React root in HTML"

    c, r = request_json("http://localhost:3000/health")
    print(f"  GET /health (Nginx Proxy -> Backend): HTTP {c} -> {r}")
    assert c == 200 and r.get("status") == "UP", f"Expected UP, got {r}"

    # 3. CRUD and Business Logic Testing via Nginx Proxy
    print("\n[3] Testing CRUD Operations via Reverse Proxy (http://localhost:3000/api/books)")
    
    # 3.1 Create Book 1
    book1_data = {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "category": "Data Engineering"
    }
    c, b1 = request_json("http://localhost:3000/api/books", method="POST", data=book1_data)
    print(f"  POST /api/books (Book 1): HTTP {c} -> ID {b1.get('id')}, Title: '{b1.get('title')}', Status: {b1.get('status')}")
    assert c == 201 and b1.get("status") == "AVAILABLE", f"Create Book 1 failed: {b1}"
    book1_id = b1["id"]

    # 3.2 Create Book 2
    book2_data = {
        "title": "The DevOps Handbook",
        "author": "Gene Kim, Jez Humble, Patrick Debois, John Willis",
        "category": "DevOps & Cloud"
    }
    c, b2 = request_json("http://localhost:3000/api/books", method="POST", data=book2_data)
    print(f"  POST /api/books (Book 2): HTTP {c} -> ID {b2.get('id')}, Title: '{b2.get('title')}', Status: {b2.get('status')}")
    assert c == 201 and b2.get("status") == "AVAILABLE", f"Create Book 2 failed: {b2}"
    book2_id = b2["id"]

    # 3.3 Create Book 3
    book3_data = {
        "title": "Site Reliability Engineering",
        "author": "Niall Richard Murphy, Betsy Beyer, Chris Jones, Jennifer Petoff",
        "category": "Site Reliability"
    }
    c, b3 = request_json("http://localhost:3000/api/books", method="POST", data=book3_data)
    print(f"  POST /api/books (Book 3): HTTP {c} -> ID {b3.get('id')}, Title: '{b3.get('title')}', Status: {b3.get('status')}")
    assert c == 201 and b3.get("status") == "AVAILABLE", f"Create Book 3 failed: {b3}"
    book3_id = b3["id"]

    # 3.4 Verify Stats
    c, stats = request_json("http://localhost:3000/api/books/stats")
    print(f"  GET /api/books/stats: HTTP {c} -> {stats}")
    assert stats["total"] >= 3 and stats["available"] >= 3 and stats["borrowed"] == 0, f"Unexpected stats: {stats}"

    # 3.5 Checkout Book 1
    checkout_payload = {
        "borrower_name": "Aarav Sharma (STU-2026-001)",
        "loan_days": 14
    }
    c, b1_borrowed = request_json(f"http://localhost:3000/api/books/{book1_id}/checkout", method="POST", data=checkout_payload)
    print(f"  POST /api/books/{book1_id}/checkout: HTTP {c} -> Status: {b1_borrowed.get('status')}, Borrower: {b1_borrowed.get('borrower_name')}, Due: {b1_borrowed.get('due_date')}")
    assert c == 200 and b1_borrowed.get("status") == "BORROWED", f"Checkout failed: {b1_borrowed}"

    # 3.6 Verify Stats after Checkout
    c, stats = request_json("http://localhost:3000/api/books/stats")
    print(f"  GET /api/books/stats (post-checkout): HTTP {c} -> {stats}")
    assert stats["borrowed"] >= 1, f"Expected at least 1 borrowed book, got: {stats}"

    # 3.7 Duplicate Checkout Error Handling
    c, err = request_json(f"http://localhost:3000/api/books/{book1_id}/checkout", method="POST", data=checkout_payload)
    print(f"  POST /api/books/{book1_id}/checkout (duplicate): HTTP {c} -> Detail: {err.get('detail')}")
    assert c == 400, f"Expected HTTP 400 for duplicate checkout, got {c}"

    # 3.8 Return Book 1
    c, b1_returned = request_json(f"http://localhost:3000/api/books/{book1_id}/return", method="POST")
    print(f"  POST /api/books/{book1_id}/return: HTTP {c} -> Status: {b1_returned.get('status')}, Borrower: {b1_returned.get('borrower_name')}")
    assert c == 200 and b1_returned.get("status") == "AVAILABLE" and b1_returned.get("borrower_name") is None, f"Return failed: {b1_returned}"

    # 3.9 Update Book 2
    update_data = {
        "title": "The DevOps Handbook (Second Edition)",
        "author": "Gene Kim, Jez Humble, Patrick Debois, John Willis"
    }
    c, b2_updated = request_json(f"http://localhost:3000/api/books/{book2_id}", method="PUT", data=update_data)
    print(f"  PUT /api/books/{book2_id}: HTTP {c} -> Updated Title: '{b2_updated.get('title')}'")
    assert c == 200 and b2_updated.get("title") == update_data["title"], f"Update failed: {b2_updated}"

    # 3.10 Delete Book 3
    c, del_resp = request_json(f"http://localhost:3000/api/books/{book3_id}", method="DELETE")
    print(f"  DELETE /api/books/{book3_id}: HTTP {c} -> {del_resp}")
    assert c == 200, f"Delete failed: {del_resp}"

    # 3.11 Final Check of Books List
    c, final_list = request_json("http://localhost:3000/api/books")
    print(f"\n  Final GET /api/books count: {len(final_list)} books")
    for b in final_list:
        print(f"    - [{b['id']}] {b['title']} by {b['author']} ({b['category']}) - {b['status']}")

    print("\n" + "=" * 60)
    print("ALL API AND BUSINESS LOGIC TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
