# Evidence Index — DevOps Capstone Rubric (M1–M10)

This index maps every required submission artifact defined in [GRADING.md](../GRADING.md) to its corresponding evidence file in the `/evidence` directory.

| Module | Rubric Item ("What to Submit") | Target Evidence File | Format / Evidence Type | Verification Status | Label |
|---|---|---|---|---|---|
| **M1** | Python source files (`backend/app/`) | `backend/app/` | Source code | Completed | LOCALLY VERIFIED |
| **M1** | Alembic migration file | `backend/alembic/versions/0001_create_books.py` | Python migration | Completed | LOCALLY VERIFIED |
| **M1** | Python dependencies | `backend/requirements.txt` | Requirements file | Pinned exact versions | LOCALLY VERIFIED |
| **M1** | Frontend source files | `frontend/` | Source code (React/Vite) | Clean build (2.96s) | LOCALLY VERIFIED |
| **M1** | Docker Compose definition | `docker-compose.yml` | Compose YAML | Completed | LOCALLY VERIFIED |
| **M1** | Browser screenshot of running application | `evidence/m1-app-browser.png` | Screenshot | Verified at http://localhost:3000 (White Theme) | LOCALLY VERIFIED |
| **M1** | Browser screenshot of student loan modal workflow | `evidence/m1-loan-modal.png` | Screenshot | Loan modal verified at localhost:3000 | LOCALLY VERIFIED |
| **M1** | Browser screenshot of add book modal workflow | `evidence/m1-add-modal.png` | Screenshot | Add book modal verified at localhost:3000 | LOCALLY VERIFIED |
| **M1** | REST API CRUD terminal execution | `evidence/m1-api-crud.txt` | Command log | 4+ endpoints tested | LOCALLY VERIFIED |
| **M1** | Frontend production build output | `evidence/m1-frontend-build.txt` | Command log | Vite build passed | LOCALLY VERIFIED |
| **M2** | Backend test suite | `backend/tests/test_api.py` | Pytest source files | 16/16 passing in 0.40s | LOCALLY VERIFIED |
| **M2** | Pytest configuration / fixtures | `backend/pytest.ini`, `backend/conftest.py` | Config / Fixtures | Configured & verified | LOCALLY VERIFIED |
| **M2** | Terminal output of passing tests (`pytest -v`) | `evidence/m2-pytest.txt` | Command log | 16/16 passed | LOCALLY VERIFIED |
| **M3** | Public GitHub repository URL | `evidence/m3-repo-url.txt` | URL | https://github.com/Ujwal-kumar-reddy/bookflow | LOCALLY VERIFIED |
| **M3** | Commit history showing 10+ meaningful commits | `evidence/m3-git-log.txt` | Git log | 28+ semantic commits | LOCALLY VERIFIED |
| **M3** | `.gitignore` excluding secrets, venv, cache | `.gitignore` | Config file | Completed | LOCALLY VERIFIED |
| **M4** | Backend Dockerfile (non-root) | `backend/Dockerfile` | Dockerfile | UID 10001 (appuser) verified | LOCALLY VERIFIED |
| **M4** | Frontend multi-stage Dockerfile (non-root) | `frontend/Dockerfile` | Dockerfile | UID 101 (nginx) verified | LOCALLY VERIFIED |
| **M4** | Runtime non-root UID verification | `evidence/m4-docker-nonroot.txt` | Command log | UID 10001 / 101 verified | LOCALLY VERIFIED |
| **M4** | Terminal output of `docker compose up --build` | `evidence/m4-docker-compose.txt`, `evidence/m4-docker-healthchecks.txt` | Command log & Healthcheck | All 3 containers healthy | LOCALLY VERIFIED |
| **M4** | Screenshot of browser at `http://localhost:3000` | `evidence/m4-browser-localhost-3000.png` | Browser Screenshot | Verified at http://localhost:3000 | LOCALLY VERIFIED |
| **M4** | Database persistence verification across restarts | `evidence/m4-persistence-test.txt` | Command log | Data persists across down/up | LOCALLY VERIFIED |
| **M5** | GitHub Actions workflow file | `.github/workflows/ci-cd.yml` | Workflow YAML | Verified in active repo | CI-VERIFIED |
| **M5** | GitHub Actions run URL showing green pipeline | `evidence/m5-actions-green-url.txt`, `evidence/m5-actions-run.txt` | URL & Run log | Run 38849676952 succeeded | CI-VERIFIED |
| **M5** | GHCR package page showing SHA-tagged images | `evidence/m5-ghcr-sha-tags.txt` | Package documentation | SHA-tagged packages pushed | CI-VERIFIED |
| **M6** | Trivy scan step in CI pipeline | `.github/workflows/ci-cd.yml` | Workflow step | Severity HIGH,CRITICAL exit 1 | CI-VERIFIED |
| **M6** | Trivy scan output from pipeline run | `evidence/m6-trivy-scan.txt` | Log file | 0 High, 0 Critical CVEs | CI-VERIFIED |
| **M6** | Written explanation of Trivy scan & flag usage | `evidence/m6-trivy-explanation.md` | Markdown explanation | Prepared & verified | LOCALLY VERIFIED |
| **M7** | Terraform configuration files | `terraform/*.tf`, `evidence/m7-terraform-validate.txt` | HCL files & validation log | Validated (`terraform validate` success) | LOCALLY VERIFIED |
| **M7** | Example Terraform variables file | `terraform/terraform.tfvars.example` | HCL example | Fully authored | IMPLEMENTED |
| **M7** | AWS Readiness Review & Architecture Specification | `evidence/m7-aws-readiness-review.md` | Markdown Review | VPC, EKS 1.31, Costs, Lifecycle | STATICALLY VALIDATED (DEPLOYMENT BLOCKED BY AWS) |
| **M8** | Namespace manifest | `k8s/namespace.yaml` | K8s YAML | Applied to Docker Desktop | LOCALLY VERIFIED |
| **M8** | Helm chart directory | `helm/bookflow/`, `evidence/m8-helm-lint.txt`, `evidence/m8-helm-template.txt` | Helm chart & templates | Linted (0 errors) & rendered | LOCALLY VERIFIED |
| **M8** | `kubectl get pods -n <ns>` running pods output | `evidence/m8-kubectl-pods.txt`, `evidence/m8-k8s-local-verification.txt` | Log file | All 5 pods Running (2 backend, 2 frontend, 1 postgres) | LOCALLY VERIFIED |
| **M8** | `kubectl get svc -n <ns>` output | `evidence/m8-kubectl-svc.txt` | Log file | Services, Ingress, HPA, PVC verified | LOCALLY VERIFIED |
| **M8** | `helm list -n <ns>` output | `evidence/m8-helm-list.txt` | Log file | Revision 4 deployed in bookflow ns | LOCALLY VERIFIED |
| **M8** | Browser screenshot of app via Ingress hostname | `evidence/m8-ingress-browser.png` | Browser Screenshot | Verified via Ingress at localhost:8088 | LOCALLY VERIFIED |
| **M8** | Kubernetes Troubleshooting Lab 1: ImagePullBackOff | `evidence/m8-troubleshooting-image.txt` | Troubleshooting Log | Diagnosis, remediation, cleanup | LOCALLY VERIFIED |
| **M8** | Kubernetes Troubleshooting Lab 2: Missing Endpoints | `evidence/m8-troubleshooting-service.txt` | Troubleshooting Log | Missing endpoints & selector fix | LOCALLY VERIFIED |
| **M9** | Observability Helm values | `monitoring/prometheus-values.yaml` | Helm values | Deployed to monitoring ns | LOCALLY VERIFIED |
| **M9** | `curl http://<backend>/metrics` output | `evidence/m9-curl-metrics.txt` | Prometheus metrics log | Verified via Ingress at localhost:8088 | LOCALLY VERIFIED |
| **M9** | Prometheus active targets verification | `evidence/m9-prometheus-targets.txt` | Command log | BookFlow targets Health: UP | LOCALLY VERIFIED |
| **M9** | Horizontal Pod Autoscaler & Top Pods output | `evidence/m9-hpa-top.txt` | Command log | HPA (cpu: 5%/60%) & top pods | LOCALLY VERIFIED |
| **M9** | Grafana dashboard with populated panels | `evidence/m9-grafana-dashboard.png`, `monitoring/bookflow-dashboard.json` | Live Screenshot & JSON | All 4 panels rendering live data | LOCALLY VERIFIED |
| **M10** | Comprehensive README.md in repository root | `README.md` | Markdown documentation | Fully authored & synchronized | IMPLEMENTED |
| **M10** | Live demo script and walkthrough guide | `evidence/m10-demo-script.md` | Markdown guide | Step-by-step evaluator script | IMPLEMENTED |
