"""
PostgreSQL Volume Persistence Test for BookFlow Capstone
Verifies data persists across:
1. docker compose restart
2. docker compose down && docker compose up -d
"""
import subprocess
import time
import urllib.request
import json
import sys

def get_books_and_stats():
    with urllib.request.urlopen("http://localhost:3000/api/books/stats", timeout=10) as r:
        stats = json.loads(r.read().decode())
    with urllib.request.urlopen("http://localhost:3000/api/books", timeout=10) as r:
        books = json.loads(r.read().decode())
    return stats, books

def wait_for_healthy(timeout=60):
    start = time.time()
    print("Waiting for services to become healthy...")
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen("http://localhost:3000/health", timeout=3) as r:
                if r.status == 200:
                    time.sleep(2)
                    return True
        except Exception:
            pass
        time.sleep(2)
    return False

def main():
    print("=" * 65)
    print("POSTGRESQL DATA PERSISTENCE VERIFICATION ACROSS CONTAINER RESTARTS")
    print("=" * 65)

    # 1. Capture Initial State
    print("\n[Step 1] Capturing baseline state before restart...")
    stats_initial, books_initial = get_books_and_stats()
    print(f"  Baseline Stats: Total={stats_initial['total']}, Available={stats_initial['available']}, Borrowed={stats_initial['borrowed']}")
    print(f"  Baseline Book IDs: {[b['id'] for b in books_initial]}")
    for b in books_initial:
        print(f"    - ID {b['id']}: '{b['title']}' | Status: {b['status']} | Borrower: {b.get('borrower_name')}")

    # 2. Test docker compose restart
    print("\n[Step 2] Executing 'docker compose restart'...")
    res = subprocess.run(["docker", "compose", "restart"], capture_output=True, text=True)
    print("  " + res.stdout.strip().replace("\n", "\n  "))
    assert res.returncode == 0, f"docker compose restart failed: {res.stderr}"

    assert wait_for_healthy(), "Services did not recover after restart"
    stats_after_restart, books_after_restart = get_books_and_stats()
    print(f"  Post-Restart Stats: Total={stats_after_restart['total']}, Available={stats_after_restart['available']}, Borrowed={stats_after_restart['borrowed']}")
    assert stats_after_restart == stats_initial, "Stats mismatch after restart!"
    assert [b["id"] for b in books_after_restart] == [b["id"] for b in books_initial], "Book IDs mismatch after restart!"
    print("  -> PASSED: All records intact after 'docker compose restart'.")

    # 3. Test docker compose down and docker compose up -d (container destruction & recreation)
    print("\n[Step 3] Executing 'docker compose down' (containers removed, volume preserved)...")
    res = subprocess.run(["docker", "compose", "down"], capture_output=True, text=True)
    print("  " + res.stdout.strip().replace("\n", "\n  "))
    assert res.returncode == 0, f"docker compose down failed: {res.stderr}"

    print("\n[Step 4] Executing 'docker compose up -d' (recreating containers from image)...")
    res = subprocess.run(["docker", "compose", "up", "-d"], capture_output=True, text=True)
    print("  " + res.stdout.strip().replace("\n", "\n  "))
    assert res.returncode == 0, f"docker compose up -d failed: {res.stderr}"

    assert wait_for_healthy(), "Services did not recover after recreate"
    stats_after_down, books_after_down = get_books_and_stats()
    print(f"  Post-Recreation Stats: Total={stats_after_down['total']}, Available={stats_after_down['available']}, Borrowed={stats_after_down['borrowed']}")
    assert stats_after_down == stats_initial, "Stats mismatch after recreate!"
    assert [b["id"] for b in books_after_down] == [b["id"] for b in books_initial], "Book IDs mismatch after recreate!"
    print("  -> PASSED: All records intact after container destruction and recreation!")

    # 4. Verify directly in PostgreSQL using psql
    print("\n[Step 5] Direct verification inside PostgreSQL via psql CLI...")
    psql_cmd = ["docker", "compose", "exec", "-T", "postgres", "psql", "-U", "bookflow", "-d", "bookflow", "-c", "SELECT id, title, status, borrower_name, due_date FROM books ORDER BY id ASC;"]
    res = subprocess.run(psql_cmd, capture_output=True, text=True)
    print("  " + res.stdout.strip().replace("\n", "\n  "))
    assert res.returncode == 0, f"psql query failed: {res.stderr}"

    print("\n" + "=" * 65)
    print("VERIFICATION COMPLETE: POSTGRESQL DATA FULLY PERSISTENT!")
    print("=" * 65)

if __name__ == "__main__":
    main()
