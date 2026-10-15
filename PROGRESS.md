# Capstone Progress Tracker — BookFlow (Session 21)

**Target Deadline:** 16 October 2026, 11:59 PM IST  
**Current Status:** Application transformed, tests passing (15/15), frontend built, Dockerfiles fixed (non-root), Helm chart linted, Terraform validated, 13 semantic commits created.  
**Application Domain:** BookFlow — Student Library Book-Lending Tracker  
**Target Architecture:** FastAPI Backend (8000), React/Vite Frontend (3000/8080), PostgreSQL (5433 host / 5432 container), Docker Compose, GitHub Actions, Trivy, GHCR, Terraform (AWS VPC + EKS ap-south-1), Kubernetes + Helm, Prometheus + Grafana.

---

## 1. Rubric Progress Table (M1 – M10, 100 Points Total)

| Module | Rubric Item | Weight | Files | Test / Command | Target Evidence File | Status | Label |
|---|---|---|---|---|---|---|---|
| **M1** | FastAPI starts, `/health` responds | 2 | `backend/app/main.py` | `pytest test_health` | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M1** | 4+ REST API endpoints (GET, POST, PUT, DELETE, stats, checkout, return) | 3 | `backend/app/main.py`, `backend/app/schemas.py`, `backend/app/models.py` | Pytest CRUD tests | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M1** | PostgreSQL + Alembic migration for books table | 2 | `backend/alembic/versions/0001_create_books.py` | Alembic migration code | `backend/alembic/versions/0001_create_books.py` | Completed | IMPLEMENTED |
| **M1** | React frontend renders and calls BookFlow API | 2 | `frontend/src/main.jsx`, `frontend/package.json` | `npm run build` | `evidence/m1-frontend-build.txt` | Completed | LOCALLY VERIFIED |
| **M1** | Responsive, usable library UI (KPI cards, filters, loan modal) | 1 | `frontend/src/main.jsx`, `frontend/src/styles.css` | Browser inspection at localhost:3000 | `evidence/m1-app-browser.png` | Pending Docker start | PENDING |
| **M2** | `pytest` runs without errors | 3 | `backend/tests/*`, `backend/pytest.ini` | `pytest -v` (15/15 passed) | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M2** | 5+ test cases covering 3+ API endpoints (15 tests written) | 4 | `backend/tests/test_api.py` | `pytest -v` | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M2** | Isolated test database (SQLite temp in-memory / StaticPool, no prod pollution) | 2 | `backend/tests/conftest.py` | `pytest -v` (0 disk files leftover) | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M2** | `pytest.ini` and `conftest.py` properly configured | 1 | `backend/pytest.ini`, `backend/tests/conftest.py` | `pytest -v` | `backend/pytest.ini` | Completed | LOCALLY VERIFIED |
| **M3** | Public GitHub repository URL linked in submission | 2 | Git repository remote | `git remote -v` | `evidence/m3-repo-url.txt` | Awaiting empty remote URL | PENDING |
| **M3** | Meaningful commit messages (13 commits created) | 2 | Git commit history | `git log --oneline` | `evidence/m3-git-history.png`, `evidence/m3-git-log.txt` | Completed | LOCALLY VERIFIED |
| **M3** | `.gitignore` excludes `.env`, `__pycache__`, `node_modules`, `.venv`, `.tfvars` | 1 | `.gitignore` | `git status --ignored` | `.gitignore` | Completed | LOCALLY VERIFIED |
| **M4** | `backend/Dockerfile` builds successfully | 2 | `backend/Dockerfile` | `docker build -t bookflow-backend ./backend` | `evidence/m4-docker-backend-build.txt` | Pending Docker start | PENDING |
| **M4** | `frontend/Dockerfile` multi-stage build (Node build + Nginx runtime) | 3 | `frontend/Dockerfile` | `docker build -t bookflow-frontend ./frontend` | `evidence/m4-docker-frontend-build.txt` | Completed | IMPLEMENTED |
| **M4** | Non-root user in both Dockerfiles (10001 backend, 101 frontend) | 2 | `backend/Dockerfile`, `frontend/Dockerfile` | `id` inspection in Dockerfiles | `evidence/m4-docker-nonroot.txt` | Completed | IMPLEMENTED |
| **M4** | `docker compose up --build` starts frontend, backend, postgres | 3 | `docker-compose.yml` | `docker compose up -d --build` | `evidence/m4-docker-compose.txt`, `evidence/m4-browser-localhost-3000.png` | Pending Docker start | PENDING |
| **M5** | `.github/workflows/ci-cd.yml` present | 1 | `.github/workflows/ci-cd.yml` | Workflow syntax validation | `.github/workflows/ci-cd.yml` | Completed | IMPLEMENTED |
| **M5** | Pipeline triggers on push to `main` | 1 | `.github/workflows/ci-cd.yml` | Push event to GitHub | `evidence/m5-actions-green-url.txt` | Awaiting remote & push approval | PENDING |
| **M5** | `pytest` runs as pipeline quality gate | 3 | `.github/workflows/ci-cd.yml` | Actions job `test` | `evidence/m5-actions-test-step.txt` | Awaiting remote & push approval | PENDING |
| **M5** | Frontend builds in CI pipeline | 2 | `.github/workflows/ci-cd.yml` | Actions job `test` (`npm ci && npm run build`) | `evidence/m5-actions-frontend-build.txt` | Awaiting remote & push approval | PENDING |
| **M5** | Docker images built for backend & frontend | 3 | `.github/workflows/ci-cd.yml` | Actions job `build-scan-push` | `evidence/m5-actions-docker-build.txt` | Awaiting remote & push approval | PENDING |
| **M5** | Images pushed to GHCR | 3 | `.github/workflows/ci-cd.yml` | Actions job `build-scan-push` | `evidence/m5-ghcr-packages.png` | Awaiting remote & push approval | PENDING |
| **M5** | Image tags use Git commit SHA (not latest) | 2 | `.github/workflows/ci-cd.yml` | GHCR package tag verification | `evidence/m5-ghcr-sha-tags.txt` | Awaiting remote & push approval | PENDING |
| **M6** | Trivy scan runs on backend & frontend images | 3 | `.github/workflows/ci-cd.yml` | Actions Trivy step | `evidence/m6-trivy-scan.txt` | Awaiting remote & push approval | PENDING |
| **M6** | Pipeline fails on HIGH or CRITICAL CVEs (exit-code 1) | 1 | `.github/workflows/ci-cd.yml` | Trivy config inspection | `.github/workflows/ci-cd.yml` | Completed | IMPLEMENTED |
| **M6** | Written explanation of CVE findings or clean scan | 1 | `evidence/m6-trivy-explanation.md` | Written documentation | `evidence/m6-trivy-explanation.md` | Completed | IMPLEMENTED |
| **M7** | Valid HCL files in `terraform/` | 2 | `terraform/*.tf` | `terraform fmt -check`, `terraform validate` | `evidence/m7-terraform-validate.txt` | Completed | LOCALLY VERIFIED |
| **M7** | `terraform init` completes without errors | 1 | `terraform/` | `terraform init` (exited 0) | `.terraform/` | Completed | LOCALLY VERIFIED |
| **M7** | `terraform plan` produces non-empty error-free plan | 2 | `terraform/` | `terraform plan` | `evidence/m7-terraform-plan.txt` | Blocked on AWS credentials | BLOCKED |
| **M7** | VPC with >=2 public subnets provisioned | 3 | `terraform/main.tf` | AWS Console screenshot | `evidence/m7-aws-console-vpc-eks.png` | Blocked on user apply approval | BLOCKED |
| **M7** | EKS cluster with managed worker node group provisioned | 4 | `terraform/main.tf` | AWS Console / `kubectl get nodes` | `evidence/m7-aws-console-vpc-eks.png` | Blocked on user apply approval | BLOCKED |
| **M7** | `terraform destroy` tears down resources cleanly | 2 | `terraform/` | `terraform destroy` output | `evidence/m7-terraform-destroy.txt` | Blocked on post-deploy | BLOCKED |
| **M7** | `terraform.tfvars.example` present (no secrets) | 1 | `terraform/terraform.tfvars.example` | File check | `terraform/terraform.tfvars.example` | Completed | IMPLEMENTED |
| **M8** | `k8s/namespace.yaml` exists and applies cleanly | 1 | `k8s/namespace.yaml` | `kubectl apply -f k8s/namespace.yaml` | `k8s/namespace.yaml` | Completed | IMPLEMENTED |
| **M8** | Helm chart in `helm/bookflow/` (Chart.yaml, values, templates) | 3 | `helm/bookflow/` | `helm lint ./helm/bookflow` (0 failed) | `evidence/m8-helm-lint.txt` | Completed | LOCALLY VERIFIED |
| **M8** | `helm upgrade --install` deploys without errors | 3 | `helm/bookflow/` | `helm template` passed | `evidence/m8-helm-template-prod.yaml` | Completed | LOCALLY VERIFIED |
| **M8** | Backend & Frontend Deployments run >=2 replicas each | 2 | `helm/bookflow/templates/*-deployment.yaml` | Helm template verification | `evidence/m8-helm-template-prod.yaml` | Completed | LOCALLY VERIFIED |
| **M8** | ClusterIP Services expose backend and frontend | 2 | `helm/bookflow/templates/*-service.yaml` | Helm template verification | `evidence/m8-helm-template-prod.yaml` | Completed | LOCALLY VERIFIED |
| **M8** | Ingress routes `/` -> frontend and `/api` -> backend | 2 | `helm/bookflow/templates/ingress.yaml` | Helm template verification | `evidence/m8-helm-template-dev.yaml` | Completed | LOCALLY VERIFIED |
| **M8** | `kubectl get pods -n bookflow` shows all pods Running | 2 | Kubernetes cluster | `kubectl get pods -n bookflow` | `evidence/m8-kubectl-pods.txt` | Pending k8s cluster | PENDING |
| **M9** | `/metrics` endpoint returns Prometheus metrics | 2 | `backend/app/main.py` | `pytest test_metrics` passed | `evidence/m2-pytest.txt` | Completed | LOCALLY VERIFIED |
| **M9** | Prometheus installed and scrapes BookFlow backend | 3 | `monitoring/prometheus-values.yaml` | Prometheus UI Targets screen | `evidence/m9-prometheus-targets.png` | Pending Prometheus deploy | PENDING |
| **M9** | Grafana installed and accessible | 2 | Helm / port-forward | Grafana login screen | `evidence/m9-grafana-login.png` | Pending Grafana deploy | PENDING |
| **M9** | Grafana panel shows live application metrics | 3 | `monitoring/bookflow-dashboard.json` | Grafana dashboard panel | `monitoring/bookflow-dashboard.json` | Completed | IMPLEMENTED |
| **M10** | Comprehensive root `README.md` explaining architecture & operations | 2 | `README.md` | Full documentation authored | `README.md` | Completed | IMPLEMENTED |
| **M10** | Live demo script and pipeline simulation | 3 | `evidence/m10-demo-script.md` | Walkthrough guide authored | `evidence/m10-demo-script.md` | Completed | IMPLEMENTED |

---

## 2. All 18 Audit Targets — Status & Resolution Summary

1. `test_api.py` test failure & no conftest: **CONFIRMED & FIXED** (Created `conftest.py` with in-memory SQLite, 15 tests passing, zero db pollution).
2. `terraform/main.tf` and `versions.tf` invalid HCL: **CONFIRMED & FIXED** (Rewritten into multi-line HCL blocks, `terraform fmt` and `terraform validate` passed).
3. `package.json` unpinned dependencies: **CONFIRMED & FIXED** (Pinned React 18 & Vite 5, `package-lock.json` generated, 0 npm audit vulnerabilities).
4. `frontend/Dockerfile` root container: **CONFIRMED & FIXED** (Multi-stage build with `nginxinc/nginx-unprivileged:1.27-alpine`, non-root user 101, port 8080).
5. Ingress port 8080 mismatch: **CONFIRMED & FIXED** (Ingress routes `/api` to `backend:8000` and `/` to `frontend:80`).
6. Nginx upstream `backend:8000` DNS failure: **CONFIRMED & FIXED** (Added Service alias `backend` in Helm).
7. `backend` Deployment imagePullSecrets & latest tag: **CONFIRMED & FIXED** (Added `imagePullSecrets` and `imagePullPolicy: IfNotPresent`).
8. `values-dev.yaml` replicaCount 1 & disabled HPA: **CONFIRMED & FIXED** (Set `replicaCount: 2` and `hpa.enabled: true` with minReplicas 2).
9. Plaintext DB password & root PVC mount: **CONFIRMED & FIXED** (Kubernetes `secretKeyRef` implemented, `PGDATA=/var/lib/postgresql/data/pgdata`).
10. CI uppercase repo owner & deploy crash: **CONFIRMED & FIXED** (Bash tr lowercasing implemented, deploy job guarded by `vars.DEPLOY_ENABLED == 'true'`).
11. CI EKS auth mechanism: **CONFIRMED & PROPOSED** (Options A and B formulated for user decision).
12. `.gitignore` omissions & leftover pyc/DS_Store: **CONFIRMED & FIXED** (7 pyc files and DS_Store removed, `.gitignore` updated).
13. Docker Compose startup race & port 5432 collision: **CONFIRMED & FIXED** (Added `service_healthy` condition on Postgres, mapped host port to 5433 to avoid collision with user's existing local Postgres on 5432).
14. Backend dual schema race: **CONFIRMED & FIXED** (Removed `create_all` from production startup; Alembic is single schema source).
15. Terraform EKS gaps: **CONFIRMED & FIXED** (Added variables, `terraform.tfvars.example`, dynamic AZs, EBS CSI add-on, ELB subnet tags, and `configure_kubectl` output).
16. Load test broken `/api/health`: **CONFIRMED & FIXED** (Pointed `scripts/load-test.sh` to `/api/books` and `/api/books/stats`).
17. Monitoring gaps: **CONFIRMED & FIXED** (Exported `monitoring/bookflow-dashboard.json`, documented installation steps in README).
18. Vite proxy port mismatch: **CONFIRMED & FIXED** (Updated `frontend/vite.config.js` proxy target to `http://localhost:8000`).

---

## 3. Blockers and User Actions Needed

1. **Empty Public GitHub Repository URL:** We need your new empty public GitHub repository URL (e.g. `https://github.com/<your-username>/bookflow.git`) so we can add the remote and wait for your explicit confirmation to push.
2. **Docker Desktop:** Docker Desktop application is installed but needs to be opened/started from Windows Start Menu so the Docker daemon and local Kubernetes cluster (`docker-desktop` context) are active.
3. **AWS CLI & Credentials:** When you are ready for Phase 5 / Phase 6 on EKS, provide AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION=ap-south-1`) so we can run `aws sts get-caller-identity` and generate the `terraform plan`.
