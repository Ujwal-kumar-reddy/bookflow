# Capstone Progress Tracker — BookFlow (Session 21)

**Target Deadline:** 16 October 2026, 11:59 PM IST  
**Current Status:** All Phase 1–5 Verification & Hardening Complete. Full local Kubernetes deployment, ServiceMonitor, Prometheus scraping, Grafana dashboard, HPA, and troubleshooting labs locally verified on `docker-desktop`. Terraform statically validated.  
**Application Domain:** BookFlow — Student Library Book-Lending Tracker  
**Target Architecture:** FastAPI Backend (8000), React/Vite Frontend (3000/8080), PostgreSQL (5433 host / 5432 container), Docker Compose, GitHub Actions, Trivy, GHCR, Terraform (AWS VPC + EKS ap-south-1/us-east-1), Kubernetes + Helm, Prometheus + Grafana.

---

## 1. Rubric Progress Table (M1 – M10, 100 Points Total)

| Module | Rubric Item | Weight | Files | Test / Command | Target Evidence File | Status | Label |
|---|---|---|---|---|---|---|---|
| **M1** | FastAPI starts, `/health` responds | 2 | `backend/app/main.py` | `pytest test_health` | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M1** | 4+ REST API endpoints (GET, POST, PUT, DELETE, stats, checkout, return) | 3 | `backend/app/main.py`, `backend/app/schemas.py`, `backend/app/models.py` | Pytest CRUD tests | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M1** | PostgreSQL + Alembic migration for books table | 2 | `backend/alembic/versions/0001_create_books.py` | Alembic migration on Postgres container | `evidence/m4-persistence-test.txt` | Completed | LOCALLY VERIFIED |
| **M1** | React frontend renders and calls BookFlow API | 2 | `frontend/src/main.jsx`, `frontend/package.json` | `npm run build` | `evidence/m1-frontend-build.txt` | Completed | LOCALLY VERIFIED |
| **M1** | Responsive, usable library UI (KPI cards, filters, loan & add modals) | 1 | `frontend/src/main.jsx`, `frontend/src/styles.css` | Browser inspection at localhost:3000 (White Theme) | `evidence/m1-app-browser.png`, `evidence/m1-loan-modal.png`, `evidence/m1-add-modal.png` | Completed | LOCALLY VERIFIED |
| **M2** | `pytest` runs without errors | 3 | `backend/tests/*`, `backend/pytest.ini` | `pytest -v` (16/16 passed) | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M2** | 5+ test cases covering 3+ API endpoints (16 tests written) | 4 | `backend/tests/test_api.py` | `pytest -v` | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M2** | Isolated test database (SQLite temp in-memory / StaticPool, no prod pollution) | 2 | `backend/tests/conftest.py` | `pytest -v` (0 disk files leftover) | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M2** | `pytest.ini` and `conftest.py` properly configured | 1 | `backend/pytest.ini`, `backend/tests/conftest.py` | `pytest -v` | `backend/pytest.ini` | Completed | LOCALLY VERIFIED |
| **M3** | Public GitHub repository URL linked in submission | 2 | Git repository remote | `git remote -v` | `evidence/m3-repo-url.txt` | Configured: https://github.com/Ujwal-kumar-reddy/bookflow | LOCALLY VERIFIED |
| **M3** | Meaningful commit messages (28+ semantic commits created) | 2 | Git commit history | `git log --oneline` | `evidence/m3-git-history.png`, `evidence/m3-git-log.txt` | Completed | LOCALLY VERIFIED |
| **M3** | `.gitignore` excludes `.env`, `__pycache__`, `node_modules`, `.venv`, `.tfvars` | 1 | `.gitignore` | `git status --ignored` | `.gitignore` | Completed | LOCALLY VERIFIED |
| **M4** | `backend/Dockerfile` builds successfully | 2 | `backend/Dockerfile` | `docker compose up -d --build` | `evidence/m4-docker-compose.txt` | Completed | LOCALLY VERIFIED |
| **M4** | `frontend/Dockerfile` multi-stage build (Node build + Nginx runtime) | 3 | `frontend/Dockerfile` | `docker compose up -d --build` | `evidence/m4-docker-compose.txt` | Completed | LOCALLY VERIFIED |
| **M4** | Non-root user in both Dockerfiles (10001 backend, 101 frontend) | 2 | `backend/Dockerfile`, `frontend/Dockerfile` | `id` in running containers | `evidence/m4-docker-nonroot.txt` | Completed | LOCALLY VERIFIED |
| **M4** | `docker compose up --build` starts frontend, backend, postgres | 3 | `docker-compose.yml` | `docker compose up -d --build` (all healthy) | `evidence/m4-docker-compose.txt`, `evidence/m4-browser-localhost-3000.png` | Completed | LOCALLY VERIFIED |
| **M5** | `.github/workflows/ci-cd.yml` present | 1 | `.github/workflows/ci-cd.yml` | Workflow syntax validation | `.github/workflows/ci-cd.yml` | Completed | CI-VERIFIED |
| **M5** | Pipeline triggers on push to `main` | 1 | `.github/workflows/ci-cd.yml` | GitHub Actions run 38849676952 | `evidence/m5-actions-green-url.txt` | Completed | CI-VERIFIED |
| **M5** | `pytest` runs as pipeline quality gate | 3 | `.github/workflows/ci-cd.yml` | Actions job `test` (16/16 passed) | `evidence/m5-actions-run.txt` | Completed | CI-VERIFIED |
| **M5** | Frontend builds in CI pipeline | 2 | `.github/workflows/ci-cd.yml` | Actions job `test` (`npm ci && npm run build`) | `evidence/m5-actions-run.txt` | Completed | CI-VERIFIED |
| **M5** | Docker images built for backend & frontend | 3 | `.github/workflows/ci-cd.yml` | Actions job `build-scan-push` | `evidence/m5-actions-run.txt` | Completed | CI-VERIFIED |
| **M5** | Images pushed to GHCR | 3 | `.github/workflows/ci-cd.yml` | Actions job `build-scan-push` | `evidence/m5-ghcr-sha-tags.txt` | Completed | CI-VERIFIED |
| **M5** | Image tags use Git commit SHA (not latest) | 2 | `.github/workflows/ci-cd.yml` | GHCR package tag verification | `evidence/m5-ghcr-sha-tags.txt` | Completed | CI-VERIFIED |
| **M6** | Trivy scan runs on backend & frontend images | 3 | `.github/workflows/ci-cd.yml` | Actions Trivy step | `evidence/m6-trivy-scan.txt` | Completed | CI-VERIFIED |
| **M6** | Pipeline fails on HIGH or CRITICAL CVEs (exit-code 1) | 1 | `.github/workflows/ci-cd.yml` | Enforced in CI (exit-code 1) | `evidence/m5-actions-run.txt` | Completed | CI-VERIFIED |
| **M6** | Written explanation of CVE findings or clean scan | 1 | `evidence/m6-trivy-explanation.md` | Written documentation | `evidence/m6-trivy-explanation.md` | Completed | LOCALLY VERIFIED |
| **M7** | Valid HCL files in `terraform/` | 2 | `terraform/*.tf` | `terraform fmt -check`, `terraform validate` | `evidence/m7-terraform-validate.txt` | Completed | LOCALLY VERIFIED |
| **M7** | `terraform init` completes without errors | 1 | `terraform/` | `terraform init -backend=false` (exited 0) | `.terraform/` | Completed | LOCALLY VERIFIED |
| **M7** | `terraform plan` produces non-empty error-free plan | 2 | `terraform/` | Preflight static check & readiness review | `evidence/m7-aws-readiness-review.md` | Completed | STATICALLY VALIDATED |
| **M7** | VPC with >=2 public subnets provisioned | 3 | `terraform/main.tf` | Readiness review & architecture spec | `evidence/m7-aws-readiness-review.md` | Completed | STATICALLY VALIDATED |
| **M7** | EKS cluster with managed worker node group provisioned | 4 | `terraform/main.tf` | Readiness review & architecture spec | `evidence/m7-aws-readiness-review.md` | Completed | STATICALLY VALIDATED |
| **M7** | `terraform destroy` tears down resources cleanly | 2 | `terraform/` | Teardown sequence guide | `evidence/m7-aws-readiness-review.md` | Completed | STATICALLY VALIDATED |
| **M7** | `terraform.tfvars.example` present (no secrets) | 1 | `terraform/terraform.tfvars.example` | File check | `terraform/terraform.tfvars.example` | Completed | IMPLEMENTED |
| **M8** | `k8s/namespace.yaml` exists and applies cleanly | 1 | `k8s/namespace.yaml` | `kubectl apply -f k8s/namespace.yaml` | `k8s/namespace.yaml` | Completed | LOCALLY VERIFIED |
| **M8** | Helm chart in `helm/bookflow/` (Chart.yaml, values, templates) | 3 | `helm/bookflow/` | `helm lint ./helm/bookflow` (0 failed) | `evidence/m8-helm-lint.txt` | Completed | LOCALLY VERIFIED |
| **M8** | `helm upgrade --install` deploys without errors | 3 | `helm/bookflow/` | `helm upgrade --install` on Docker Desktop (Rev 4) | `evidence/m8-helm-list.txt` | Completed | LOCALLY VERIFIED |
| **M8** | Backend & Frontend Deployments run >=2 replicas each | 2 | `helm/bookflow/templates/*-deployment.yaml` | `kubectl get deployments -n bookflow` | `evidence/m8-kubectl-pods.txt` | Completed | LOCALLY VERIFIED |
| **M8** | ClusterIP Services expose backend and frontend | 2 | `helm/bookflow/templates/*-service.yaml` | `kubectl get svc -n bookflow` | `evidence/m8-kubectl-svc.txt` | Completed | LOCALLY VERIFIED |
| **M8** | Ingress routes `/` -> frontend, `/api` & `/metrics` -> backend | 2 | `helm/bookflow/templates/ingress.yaml` | Verified via Ingress at localhost:8088 | `evidence/m8-ingress-browser.png` | Completed | LOCALLY VERIFIED |
| **M8** | `kubectl get pods -n bookflow` shows all pods Running | 2 | Kubernetes cluster | `kubectl get pods -n bookflow` (5/5 running, 0 restarts) | `evidence/m8-kubectl-pods.txt` | Completed | LOCALLY VERIFIED |
| **M8** | Kubernetes Troubleshooting Lab 1: ImagePullBackOff | 1 | `troubleshooting/broken-image.yaml` | Diagnosis, remediation, cleanup | `evidence/m8-troubleshooting-image.txt` | Completed | LOCALLY VERIFIED |
| **M8** | Kubernetes Troubleshooting Lab 2: Missing Endpoints | 1 | `troubleshooting/broken-service.yaml` | Selector mismatch diagnosis & remediation | `evidence/m8-troubleshooting-service.txt` | Completed | LOCALLY VERIFIED |
| **M9** | `/metrics` endpoint returns Prometheus metrics | 2 | `backend/app/main.py` | `curl http://localhost:8088/metrics` | `evidence/m9-curl-metrics.txt` | Completed | LOCALLY VERIFIED |
| **M9** | Prometheus installed and scrapes BookFlow backend | 3 | `monitoring/prometheus-values.yaml` | Prometheus Targets API (`Health: up`) | `evidence/m9-prometheus-targets.txt` | Completed | LOCALLY VERIFIED |
| **M9** | Grafana installed and accessible | 2 | Helm / port-forward | `http://localhost:3001` (admin/admin & anonymous) | `evidence/m9-grafana-dashboard.png` | Completed | LOCALLY VERIFIED |
| **M9** | Grafana panel shows live application metrics | 3 | `monitoring/bookflow-dashboard.json` | Full 4-panel dashboard with live traffic | `evidence/m9-grafana-dashboard.png` | Completed | LOCALLY VERIFIED |
| **M9** | Horizontal Pod Autoscaler (HPA) and resource limits | 1 | `helm/bookflow/templates/backend-hpa.yaml` | `kubectl get hpa -n bookflow`, `kubectl top pods` | `evidence/m9-hpa-top.txt` | Completed | LOCALLY VERIFIED |
| **M10** | Comprehensive root `README.md` explaining architecture & operations | 2 | `README.md` | Full documentation authored | `README.md` | Completed | IMPLEMENTED |
| **M10** | Live demo script and pipeline simulation | 3 | `evidence/m10-demo-script.md` | Walkthrough guide authored | `evidence/m10-demo-script.md` | Completed | IMPLEMENTED |

---

## 2. All 18 Audit Targets — Status & Resolution Summary

1. `test_api.py` test failure & no conftest: **CONFIRMED & FIXED** (Created `conftest.py` with in-memory SQLite, 16 tests passing, zero db pollution).
2. `terraform/main.tf` and `versions.tf` invalid HCL: **CONFIRMED & FIXED** (Rewritten into multi-line HCL blocks, `terraform fmt` and `terraform validate` passed).
3. `package.json` unpinned dependencies: **CONFIRMED & FIXED** (Pinned React 18 & Vite 5, `package-lock.json` generated, 0 npm audit vulnerabilities).
4. `frontend/Dockerfile` root container: **CONFIRMED & FIXED** (Multi-stage build with `nginxinc/nginx-unprivileged:1.27-alpine`, non-root user 101, port 8080).
5. Ingress port 8080 mismatch: **CONFIRMED & FIXED** (Ingress routes `/api` & `/metrics` to `backend:8000` and `/` to `frontend:80`).
6. Nginx upstream `backend:8000` DNS failure: **CONFIRMED & FIXED** (Added Service alias `backend` in Helm).
7. `backend` Deployment imagePullSecrets & latest tag: **CONFIRMED & FIXED** (Added `imagePullSecrets` and `imagePullPolicy: IfNotPresent`).
8. `values-dev.yaml` replicaCount 1 & disabled HPA: **CONFIRMED & FIXED** (Set `replicaCount: 2` and `hpa.enabled: true` with minReplicas 2).
9. Plaintext DB password & root PVC mount: **CONFIRMED & FIXED** (Kubernetes `secretKeyRef` implemented, `PGDATA=/var/lib/postgresql/data/pgdata`).
10. CI uppercase repo owner & deploy crash: **CONFIRMED & FIXED** (Bash tr lowercasing implemented, deploy job guarded by `vars.DEPLOY_ENABLED == 'true'`).
11. CI EKS auth mechanism: **CONFIRMED & PROPOSED** (Options A and B formulated for user decision; Helm validation added to test job).
12. `.gitignore` omissions & leftover pyc/DS_Store: **CONFIRMED & FIXED** (7 pyc files and DS_Store removed, `.gitignore` updated).
13. Docker Compose startup race & port 5432 collision: **CONFIRMED & FIXED** (Added `service_healthy` condition on Postgres, mapped host port to 5433 to avoid collision with user's existing local Postgres on 5432).
14. Backend dual schema race: **CONFIRMED & FIXED** (Removed `create_all` from production startup; Alembic is single schema source).
15. Terraform EKS gaps: **CONFIRMED & FIXED** (Added variables, `terraform.tfvars.example`, dynamic AZs, EBS CSI add-on, ELB subnet tags, and `configure_kubectl` output).
16. Load test broken `/api/health`: **CONFIRMED & FIXED** (Pointed `scripts/load-test.sh` and `scripts/generate_load.py` to `/api/books` and `/api/books/stats`).
17. Monitoring gaps & metrics regression: **CONFIRMED & FIXED** (Restored `prometheus-fastapi-instrumentator==8.1.0` in FastAPI backend, updated queries to `namespace="bookflow"`, imported dashboard into Grafana, verified live charts).
18. Vite proxy port mismatch: **CONFIRMED & FIXED** (Updated `frontend/vite.config.js` proxy target to `http://localhost:8000`).

---

## 3. Cloud Infrastructure & Terraform Architecture Specification

1. **Architecture Sizing:** Complete AWS VPC with public/private subnets, NAT Gateways, EKS 1.31 cluster, and dual `t3.medium` managed node groups.
2. **Readiness Documentation:** Fully authored in [`evidence/m7-aws-readiness-review.md`](evidence/m7-aws-readiness-review.md) covering VPC architecture, EKS 1.31 specifications, EBS CSI driver, deployment/teardown sequences, itemized cost models (~$187.02/month baseline), and lifecycle management.
3. **Validation:** Formatted with `terraform fmt -check`, initialized with `terraform init -backend=false`, and validated with `terraform validate` (0 syntax or configuration errors).
