import urllib.request
import time
import sys

base_url = "http://localhost:8088"
total = int(sys.argv[1]) if len(sys.argv) > 1 else 100

print(f"Starting BookFlow load generator: {total} requests -> {base_url}")
success = 0
failed = 0

start = time.time()
for i in range(1, total + 1):
    path = "/api/books" if i % 2 == 0 else "/api/books/stats"
    try:
        req = urllib.request.Request(f"{base_url}{path}")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if 200 <= resp.status < 400:
                success += 1
            else:
                failed += 1
    except Exception as e:
        failed += 1
    
    if i % 25 == 0 or i == total:
        print(f"  [{i}/{total}] Success: {success}, Failed: {failed}")

duration = time.time() - start
print(f"Finished in {duration:.2f}s: {success} succeeded, {failed} failed ({(success/duration):.1f} req/s)")
