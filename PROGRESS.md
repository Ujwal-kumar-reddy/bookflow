# Capstone Progress Tracker — BookFlow (Session 21)

**Target Deadline:** 16 October 2026, 11:59 PM IST  
**Late Penalty:** 5 points per 24 hours  
**Application Domain:** BookFlow — Student Library Book-Lending Tracker  
**Target Architecture:** FastAPI Backend (8000), React/Vite Frontend (3000), PostgreSQL (5432), Docker Compose, GitHub Actions, Trivy, GHCR, Terraform (AWS VPC + EKS ap-south-1), Kubernetes + Helm, Prometheus + Grafana.

---

## 1. Rubric Progress Table (M1 – M10, 100 Points Total)

| Module | Rubric Item | Weight | Files | Test / Command | Target Evidence File | Status | Label |
|---|---|---|---|---|---|---|---|
| **M1** | FastAPI starts, `/health` responds | 2 | `backend/app/main.py` | `curl http://localhost:8000/health` | `evidence/m1-health.txt` | In Progress | IMPLEMENTED |
| **M1** | 4+ REST API endpoints (GET, POST, PUT, DELETE, stats, checkout, return) | 3 | `backend/app/main.py`, `backend/app/schemas.py`, `backend/app/models.py` | Pytest / curl CRUD | `evidence/m1-api-crud.txt` | In Progress | IMPLEMENTED |
| **M1** | PostgreSQL + Alembic migration for books table | 2 | `backend/alembic/versions/*_create_books_table.py` | `alembic upgrade head` | `evidence/m1-alembic-migration.txt` | In Progress | IMPLEMENTED |
| **M1** | React frontend renders and calls BookFlow API | 2 | `frontend/src/*`, `frontend/package.json` | `npm run build`, browser check | `evidence/m1-frontend-build.txt` | In Progress | IMPLEMENTED |
| **M1** | Responsive, usable library UI (KPI cards, filters, loan modal) | 1 | `frontend/src/App.jsx`, `frontend/src/index.css` | Browser inspection at 3000 | `evidence/m1-app-browser.png` | Pending | PENDING |
| **M2** | `pytest` runs without errors | 3 | `backend/tests/*`, `backend/pytest.ini` | `pytest -v` | `evidence/m2-pytest.txt` | In Progress | IMPLEMENTED |
| **M2** | 5+ test cases covering 3+ API endpoints (8+ planned) | 4 | `backend/tests/test_api.py` | `pytest -v` | `evidence/m2-pytest.txt` | In Progress | IMPLEMENTED |
| **M2** | Isolated test database (SQLite temp in-memory / StaticPool, no prod pollution) | 2 | `backend/tests/conftest.py` | `pytest -v` (no test.db leftover) | `evidence/m2-conftest-isolation.txt` | In Progress | IMPLEMENTED |
| **M2** | `pytest.ini` and `conftest.py` properly configured | 1 | `backend/pytest.ini`, `backend/tests/conftest.py` | `pytest --fixtures` | `evidence/m2-pytest-config.txt` | In Progress | IMPLEMENTED |
| **M3** | Public GitHub repository URL linked in submission | 2 | Git repository remote | `git remote -v` | `evidence/m3-repo-url.txt` | Pending Remote confirmation | PENDING |
| **M3** | Meaningful commit messages (10+ commits) | 2 | Git commit history | `git log --oneline` | `evidence/m3-git-history.png`, `evidence/m3-git-log.txt` | In Progress | IMPLEMENTED |
| **M3** | `.gitignore` excludes `.env`, `__pycache__`, `node_modules`, `.venv`, `.tfvars` | 1 | `.gitignore` | `git status --ignored` | `evidence/m3-gitignore.txt` | Completed | LOCALLY VERIFIED |
| **M4** | `backend/Dockerfile` builds successfully | 2 | `backend/Dockerfile` | `docker build -t bookflow-backend:local ./backend` | `evidence/m4-docker-backend-build.txt` | In Progress | IMPLEMENTED |
| **M4** | `frontend/Dockerfile` multi-stage build (Node build + Nginx runtime) | 3 | `frontend/Dockerfile` | `docker build -t bookflow-frontend:local ./frontend` | `evidence/m4-docker-frontend-build.txt` | In Progress | IMPLEMENTED |
| **M4** | Non-root user in both Dockerfiles | 2 | `backend/Dockerfile`, `frontend/Dockerfile` | `docker run --rm --entrypoint id <image>` | `evidence/m4-docker-nonroot.txt` | In Progress | IMPLEMENTED |
| **M4** | `docker compose up --build` starts frontend, backend, postgres | 3 | `docker-compose.yml` | `docker compose up -d --build` | `evidence/m4-docker-compose.txt`, `evidence/m4-browser-localhost-3000.png` | Pending Compose execution | PENDING |
| **M5** | `.github/workflows/ci-cd.yml` present | 1 | `.github/workflows/ci-cd.yml` | Workflow syntax validation | `evidence/m5-workflow-syntax.txt` | In Progress | IMPLEMENTED |
| **M5** | Pipeline triggers on push to `main` | 1 | `.github/workflows/ci-cd.yml` | GitHub Actions event log | `evidence/m5-actions-green-url.txt` | Pending push to main | PENDING |
| **M5** | `pytest` runs as pipeline quality gate | 3 | `.github/workflows/ci-cd.yml` | Actions job `test` | `evidence/m5-actions-test-step.txt` | Pending CI run | PENDING |
| **M5** | Frontend builds in CI pipeline | 2 | `.github/workflows/ci-cd.yml` | Actions job `test` (npm run build) | `evidence/m5-actions-frontend-build.txt` | Pending CI run | PENDING |
| **M5** | Docker images built for backend & frontend | 3 | `.github/workflows/ci-cd.yml` | Actions job `build-scan-push` | `evidence/m5-actions-docker-build.txt` | Pending CI run | PENDING |
| **M5** | Images pushed to GHCR | 3 | `.github/workflows/ci-cd.yml` | Actions job `build-scan-push` | `evidence/m5-ghcr-packages.png` | Pending CI run | PENDING |
| **M5** | Image tags use Git commit SHA (not latest) | 2 | `.github/workflows/ci-cd.yml` | GHCR package tag verification | `evidence/m5-ghcr-sha-tags.txt` | Pending CI run | PENDING |
| **M6** | Trivy scan runs on backend & frontend images | 3 | `.github/workflows/ci-cd.yml` | Actions Trivy step | `evidence/m6-trivy-scan.txt` | Pending CI run | PENDING |
| **M6** | Pipeline fails on HIGH or CRITICAL CVEs (exit-code 1) | 1 | `.github/workflows/ci-cd.yml` | Trivy config inspection | `evidence/m6-trivy-config.txt` | In Progress | IMPLEMENTED |
| **M6** | Written explanation of CVE findings or clean scan | 1 | `evidence/m6-trivy-explanation.md` | Written documentation | `evidence/m6-trivy-explanation.md` | Completed | IMPLEMENTED |
| **M7** | Valid HCL files in `terraform/` | 2 | `terraform/*.tf` | `terraform fmt -check`, `terraform validate` | `evidence/m7-terraform-validate.txt` | In Progress | IMPLEMENTED |
| **M7** | `terraform init` completes without errors | 1 | `terraform/` | `terraform init` | `evidence/m7-terraform-init.txt` | In Progress | IMPLEMENTED |
| **M7** | `terraform plan` produces non-empty error-free plan | 2 | `terraform/` | `terraform plan` | `evidence/m7-terraform-plan.txt` | Blocked on AWS credentials | BLOCKED |
| **M7** | VPC with >=2 public subnets provisioned | 3 | `terraform/main.tf` | AWS Console / CLI query | `evidence/m7-aws-console-vpc-eks.png` | Blocked on user apply approval | BLOCKED |
| **M7** | EKS cluster with managed worker node group provisioned | 4 | `terraform/main.tf` | AWS Console / `kubectl get nodes` | `evidence/m7-aws-console-vpc-eks.png` | Blocked on user apply approval | BLOCKED |
| **M7** | `terraform destroy` tears down resources cleanly | 2 | `terraform/` | `terraform destroy -auto-approve` | `evidence/m7-terraform-destroy.txt` | Blocked on post-deploy | BLOCKED |
| **M7** | `terraform.tfvars.example` present (no secrets) | 1 | `terraform/terraform.tfvars.example` | File check | `evidence/m7-tfvars-example.txt` | In Progress | IMPLEMENTED |
| **M8** | `k8s/namespace.yaml` exists and applies cleanly | 1 | `k8s/namespace.yaml` | `kubectl apply -f k8s/namespace.yaml` | `evidence/m8-namespace.txt` | In Progress | IMPLEMENTED |
| **M8** | Helm chart in `helm/bookflow/` (Chart.yaml, values, templates) | 3 | `helm/bookflow/` | `helm lint ./helm/bookflow` | `evidence/m8-helm-lint.txt` | In Progress | IMPLEMENTED |
| **M8** | `helm upgrade --install` deploys without errors | 3 | `helm/bookflow/` | `helm upgrade --install bookflow ./helm/bookflow` | `evidence/m8-helm-install.txt` | Pending k8s cluster | PENDING |
| **M8** | Backend & Frontend Deployments run >=2 replicas each | 2 | `helm/bookflow/templates/*-deployment.yaml` | `kubectl get deployment -n bookflow` | `evidence/m8-deployment-replicas.txt` | Pending k8s cluster | PENDING |
| **M8** | ClusterIP Services expose backend and frontend | 2 | `helm/bookflow/templates/*-service.yaml` | `kubectl get svc -n bookflow` | `evidence/m8-kubectl-svc.txt` | Pending k8s cluster | PENDING |
| **M8** | Ingress routes `/` -> frontend and `/api` -> backend | 2 | `helm/bookflow/templates/ingress.yaml` | `kubectl get ingress -n bookflow`, curl | `evidence/m8-ingress-browser.png` | Pending k8s cluster | PENDING |
| **M8** | `kubectl get pods -n bookflow` shows all pods Running | 2 | Kubernetes cluster | `kubectl get pods -n bookflow` | `evidence/m8-kubectl-pods.txt` | Pending k8s cluster | PENDING |
| **M9** | `/metrics` endpoint returns Prometheus metrics | 2 | `backend/app/main.py` | `curl http://<backend>:8000/metrics` | `evidence/m9-curl-metrics.txt` | In Progress | IMPLEMENTED |
| **M9** | Prometheus installed and scrapes BookFlow backend | 3 | `monitoring/prometheus-values.yaml` | Prometheus UI Targets screen | `evidence/m9-prometheus-targets.png` | Pending Prometheus deploy | PENDING |
| **M9** | Grafana installed and accessible | 2 | Helm / port-forward | Grafana login screen | `evidence/m9-grafana-login.png` | Pending Grafana deploy | PENDING |
| **M9** | Grafana panel shows live application metrics | 3 | `monitoring/bookflow-dashboard.json` | Grafana dashboard panel | `evidence/m9-grafana-dashboard.png` | Pending Grafana deploy | PENDING |
| **M10** | Comprehensive root `README.md` explaining architecture & operations | 2 | `README.md` | Documentation review | `evidence/m10-readme-verification.txt` | In Progress | IMPLEMENTED |
| **M10** | Live demo script and pipeline simulation | 3 | `evidence/m10-demo-script.md` | Walkthrough validation | `evidence/m10-demo-script.md` | In Progress | IMPLEMENTED |

---

## 2. Audit Targets Verification Status

| Audit Target | Description | Verified Status | Resolution Plan |
|---|---|---|---|
| 1. Pytest failure & lack of conftest | Only 3 tests; `test_create_task_validation` fails; relative `test.db` pollution; no `conftest.py`. | **CONFIRMED** | Add `backend/tests/conftest.py` with in-memory SQLite / StaticPool, rewrite tests to 8+ test cases covering CRUD, validation, 404, checkout, return, health, ready, metrics. |
| 2. Terraform invalid HCL | `main.tf` and `versions.tf` are single-line blocks ("Invalid single-argument block definition"). | **CONFIRMED** | Rewrite HCL into clean multi-line blocks with proper formatting (`terraform fmt`). |
| 3. Frontend unpinned dependencies | `package.json` uses `"latest"` for all deps, no lockfile. | **CONFIRMED** | Pin dependencies (Vite 5+, React 18+, @vitejs/plugin-react) and commit `package-lock.json`. |
| 4. Frontend root container | `frontend/Dockerfile` runs Nginx as root on port 80. | **CONFIRMED** | Use non-root Nginx (`nginxinc/nginx-unprivileged:alpine` or non-root user on port 8080) with writable pid/temp paths; update Compose and Helm port mappings. Document as an adaptation. |
| 5. Ingress port mismatch | Ingress routes to `taskboard-backend:8080`, but backend service is port 8000. | **CONFIRMED** | Fix Ingress service name and port (`bookflow-backend:8000` / `/api` and `bookflow-frontend:8080` / `/`). |
| 6. Nginx proxy upstream name | `nginx.conf` proxies to `http://backend:8000`, but Helm has no Service named `backend`. | **CONFIRMED** | Add Service alias or configure Ingress routing so frontend static files do not fail upstream resolution. |
| 7. Deployment imagePullSecrets & latest tag | Backend Deployment lacks `imagePullSecrets`; `values.yaml` has placeholder `YOUR_ORG` and `latest`. | **CONFIRMED** | Add `imagePullSecrets`, parameterized image tags, and `imagePullPolicy: IfNotPresent` for local builds. |
| 8. `values-dev.yaml` replicaCount = 1 & no HPA | Dev values set replicaCount 1 and disable HPA, violating rubric. | **CONFIRMED** | Update `values-dev.yaml` to retain 2+ replicas and enable HPA for rubric compliance. |
| 9. Plaintext DB password & root PVC mount | Postgres password in plaintext; PVC mounted at `/var/lib/postgresql/data` root without PGDATA subfolder. | **CONFIRMED** | Use Kubernetes Secret `secretKeyRef` in backend deployment; set `PGDATA=/var/lib/postgresql/data/pgdata` to avoid lost+found mount collision. |
| 10. CI uppercase repo owner & deploy crash | `${{ github.repository_owner }}` not lowercased; Trivy `ignore-unfixed: true`; deploy job fails on missing kubeconfig. | **CONFIRMED** | Lowercase image repository path in workflow; add condition `if: vars.DEPLOY_ENABLED == 'true' && secrets.KUBE_CONFIG_DATA != ''` so CI runs green without cluster; justify Trivy flag. |
| 11. CI EKS auth mechanism | Runner lacks AWS CLI credentials to run `aws eks get-token`. | **CONFIRMED** | Propose Option A (OIDC IAM role) and Option B (K8s ServiceAccount token kubeconfig) for user decision. |
| 12. Unclean `.gitignore` & repository bloat | Missing `.venv`, `__pycache__`, `*.pyc`, `test.db`, `terraform.tfvars`, `.DS_Store`. 7 `.pyc` and `.DS_Store` present. | **CONFIRMED** | Removed pyc and DS_Store files; updated `.gitignore` with all required patterns. |
| 13. Docker Compose startup race | No healthcheck on Postgres; Alembic can crash before DB is ready. | **CONFIRMED** | Add Postgres `pg_isready` healthcheck and `depends_on: postgres: condition: service_healthy`. |
| 14. Dual schema creation race | `main.py` runs `Base.metadata.create_all` AND Dockerfile CMD runs `alembic upgrade head`. | **CONFIRMED** | Remove `create_all` from production startup; let Alembic be the sole schema source; use `create_all` only in pytest fixtures. |
| 15. Terraform gaps for EKS | Missing `terraform.tfvars.example`, no EBS CSI driver, hardcoded AZs, missing ELB subnet tags, no kubeconfig output. | **CONFIRMED** | Add variables, `terraform.tfvars.example`, public subnet tags (`kubernetes.io/role/elb = 1`), EBS CSI IRSA/add-on, dynamic AZs, and kubeconfig command output. |
| 16. Load test broken endpoint | `scripts/load-test.sh` calls `/api/health` which is 404. | **CONFIRMED** | Point load test to `/api/books` or `/api/books/stats` to generate real traffic and CPU metrics. |
| 17. Monitoring gaps | Only `prometheus-values.yaml` exists; no dashboard, no install docs. | **CONFIRMED** | Document exact `kube-prometheus-stack` helm commands, configure ServiceMonitor for BookFlow backend, export dashboard JSON. |
| 18. Vite proxy port mismatch | `vite.config.js` proxies to 8080 while backend runs on 8000. | **CONFIRMED** | Update Vite server proxy to `http://localhost:8000`. |

---

## 3. Blockers and Credentials Needed

1. **GitHub Repository:** Waiting for user to provide the URL of an empty public GitHub repository before adding a git remote.
2. **AWS CLI & Credentials:** AWS CLI is not yet installed on Windows host, and no AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, or SSO) have been configured. Required for Phase 5 (`aws sts get-caller-identity`, `terraform plan`, `terraform apply`).
3. **Docker Desktop Daemon:** Docker Desktop service is installed but currently stopped. Need user to start Docker Desktop so local Docker daemon and local Kubernetes cluster (`docker-desktop` context) are active.

---

## 4. Itemised AWS Cost Estimate & Window Management

| AWS Component | Specifications | Price per Unit | Estimated Cost / Hour | 2-Hour Evidence Window Cost |
|---|---|---|---|---|
| **EKS Control Plane** | 1 EKS Cluster | $0.10 / hour | $0.100 | $0.20 |
| **EKS Worker Nodes** | 2 x `t3.medium` EC2 instances (2 vCPU, 4 GiB) | ~$0.0416 / instance-hour (ap-south-1) | $0.083 | $0.17 |
| **AWS VPC NAT Gateway** | 1 NAT Gateway | $0.045 / hour + $0.045 / GB data | $0.045 | $0.09 |
| **EBS Storage** | 20 GB gp3 per node (40 GB) + 5 GB Postgres PVC | ~$0.08 / GB-month (~$0.00011 / GB-hr) | $0.005 | $0.01 |
| **AWS Network / Ingress Load Balancer** | 1 NLB / ALB | $0.0225 / hour | $0.023 | $0.05 |
| **Total Estimated Run Cost** | | | **~$0.26 / hour** | **~$0.52 total** |

*Sources: AWS Official Pricing (EKS: aws.amazon.com/eks/pricing, EC2 t3.medium ap-south-1: aws.amazon.com/ec2/pricing/on-demand, VPC NAT Gateway: aws.amazon.com/vpc/pricing).*  
*Safety Rule:* We will execute `terraform apply` ONLY after explicit user confirmation, capture all required screenshots and logs within a strictly managed ~1 to 2 hour window, and immediately execute `terraform destroy` followed by an audit of remaining resources (NAT Gateways, Elastic IPs, Load Balancers, EBS volumes).

---

## 5. Irreversible Operations Policy
- **NEVER** run `terraform apply` or `terraform destroy` without explicit interactive confirmation.
- **NEVER** push to GitHub or modify remotes without explicit approval.
- **NEVER** run `docker system prune -a` or global `kubectl delete` commands.
- **NEVER** commit `.env`, AWS credentials, kubeconfig, or `*.tfstate` files.
