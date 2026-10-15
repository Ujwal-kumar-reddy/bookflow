#!/usr/bin/env bash
# BookFlow Load Generator & Traffic Simulator
set -euo pipefail

BASE_URL="${BASE_URL:-http://bookflow.local}"
REQUEST_COUNT="${1:-250}"

echo "=========================================================="
echo " Starting BookFlow Traffic & CPU Load Generator"
echo " Target Base URL : ${BASE_URL}"
echo " Total Requests  : ${REQUEST_COUNT}"
echo "=========================================================="

# Check target reachability
echo "[1/3] Testing endpoint connectivity..."
if ! curl -sf "${BASE_URL}/health" >/dev/null 2>&1 && ! curl -sf "http://localhost:8000/health" >/dev/null 2>&1; then
  echo "WARN: Health endpoint not responding on ${BASE_URL}/health. Continuing anyway..."
fi

echo "[2/3] Generating read and computation traffic against /api/books and /api/books/stats..."
SUCCESS=0
FAILED=0

for i in $(seq 1 "${REQUEST_COUNT}"); do
  # Alternate between catalogue listing and stats calculation to trigger DB queries and metrics
  if [ $((i % 2)) -eq 0 ]; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/api/books" || echo "000")
  else
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/api/books/stats" || echo "000")
  fi

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 400 ]; then
    SUCCESS=$((SUCCESS + 1))
  else
    FAILED=$((FAILED + 1))
  fi

  if [ $((i % 50)) -eq 0 ]; then
    echo "  Processed ${i}/${REQUEST_COUNT} requests (Success: ${SUCCESS}, Failed: ${FAILED})..."
  fi
done

echo "[3/3] Load test execution finished."
echo "Summary: ${SUCCESS} successful requests, ${FAILED} failed requests."
echo "Check Prometheus / Grafana http_requests_total metrics and HPA cpu utilization."
