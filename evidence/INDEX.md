# Evidence Index — DevOps Capstone Rubric (M1–M10)

This index maps every required submission artifact defined in [GRADING.md](../GRADING.md) to its corresponding evidence file in the `/evidence` directory.

| Module | Rubric Item ("What to Submit") | Target Evidence File | Format / Evidence Type | Verification Status | Label |
|---|---|---|---|---|---|
| **M1** | Python source files (`backend/app/`) | `backend/app/` | Source code | In Progress | IMPLEMENTED |
| **M1** | Alembic migration file | `backend/alembic/versions/` | Python migration | In Progress | IMPLEMENTED |
| **M1** | Python dependencies | `backend/requirements.txt` | Requirements file | In Progress | IMPLEMENTED |
| **M1** | Frontend source files | `frontend/` | Source code (React/Vite) | In Progress | IMPLEMENTED |
| **M1** | Docker Compose definition | `docker-compose.yml` | Compose YAML | In Progress | IMPLEMENTED |
| **M1** | Browser screenshot of running application | `evidence/m1-app-browser.png` | Screenshot | Verified at http://localhost:3000 | LOCALLY VERIFIED |
| **M2** | Backend test suite | `backend/tests/` | Pytest source files | 15/15 passing in 0.35s | LOCALLY VERIFIED |
| **M2** | Pytest configuration / fixtures | `backend/pytest.ini`, `backend/conftest.py` | Config / Fixtures | Configured & verified | LOCALLY VERIFIED |
| **M2** | Terminal output of passing tests (`pytest -v`) | `evidence/m2-pytest.txt`, `evidence/m2-pytest.png` | Command log & Screenshot | 15/15 passed | LOCALLY VERIFIED |
| **M3** | Public GitHub repository URL | `evidence/m3-repo-url.txt` | URL | https://github.com/Ujwal-kumar-reddy/bookflow | LOCALLY VERIFIED |
| **M3** | Commit history showing 10+ meaningful commits | `evidence/m3-git-history.png`, `evidence/m3-git-log.txt` | Screenshot & Git log | 15 commits created | LOCALLY VERIFIED |
| **M3** | `.gitignore` excluding secrets, venv, cache | `.gitignore` | Config file | Completed | LOCALLY VERIFIED |
| **M4** | Backend Dockerfile (non-root) | `backend/Dockerfile` | Dockerfile | UID 10001 (appuser) verified | LOCALLY VERIFIED |
| **M4** | Frontend multi-stage Dockerfile (non-root) | `frontend/Dockerfile` | Dockerfile | UID 101 (nginx) verified | LOCALLY VERIFIED |
| **M4** | Terminal output of `docker compose up --build` | `evidence/m4-docker-compose.txt`, `evidence/m4-docker-healthchecks.txt` | Command log & Healthcheck | All 3 containers healthy | LOCALLY VERIFIED |
| **M4** | Screenshot of browser at `http://localhost:3000` | `evidence/m4-browser-localhost-3000.png` | Browser Screenshot | Verified at http://localhost:3000 | LOCALLY VERIFIED |
| **M5** | GitHub Actions workflow file | `.github/workflows/ci-cd.yml` | Workflow YAML | Verified in active repo | CI-VERIFIED |
| **M5** | GitHub Actions run URL showing green pipeline | `evidence/m5-actions-green-url.txt`, `evidence/m5-actions-run.txt` | URL & Run log | Run 38847422983 succeeded | CI-VERIFIED |
| **M5** | GHCR package page showing SHA-tagged images | `evidence/m5-ghcr-sha-tags.txt` | Package documentation | SHA-tagged packages pushed | CI-VERIFIED |
| **M6** | Trivy scan step in CI pipeline | `.github/workflows/ci-cd.yml` | Workflow step | Severity HIGH,CRITICAL exit 1 | CI-VERIFIED |
| **M6** | Trivy scan output from pipeline run | `evidence/m6-trivy-scan.txt` | Log file | 0 High, 0 Critical CVEs | CI-VERIFIED |
| **M6** | 2-3 sentence written explanation of Trivy scan | `evidence/m6-trivy-explanation.md` | Markdown explanation | Prepared & verified | LOCALLY VERIFIED |
| **M7** | Terraform configuration files | `terraform/*.tf` | HCL files | In Progress | IMPLEMENTED |
| **M7** | Example Terraform variables file | `terraform/terraform.tfvars.example` | HCL example | In Progress | IMPLEMENTED |
| **M7** | `terraform plan` output | `evidence/m7-terraform-plan.txt`, `evidence/m7-terraform-plan.png` | Log & Screenshot | Pending AWS credentials | BLOCKED |
| **M7** | AWS Console screenshot: VPC & EKS | `evidence/m7-aws-console-vpc-eks.png` | Screenshot | Pending AWS apply approval | BLOCKED |
| **M7** | `terraform destroy` completion output | `evidence/m7-terraform-destroy.txt`, `evidence/m7-terraform-destroy.png` | Log & Screenshot | Pending AWS teardown | BLOCKED |
| **M8** | Namespace manifest | `k8s/namespace.yaml` | K8s YAML | Applied to Docker Desktop | LOCALLY VERIFIED |
| **M8** | Helm chart directory | `helm/bookflow/`, `evidence/m8-helm-lint.txt`, `evidence/m8-helm-template.txt` | Helm chart & templates | Linted (0 errors) & rendered | LOCALLY VERIFIED |
| **M8** | `kubectl get pods -n <ns>` running pods output | `evidence/m8-kubectl-pods.txt`, `evidence/m8-k8s-local-verification.txt` | Log file | All 5 pods Running (2 backend, 2 frontend) | LOCALLY VERIFIED |
| **M8** | `kubectl get svc -n <ns>` output | `evidence/m8-kubectl-svc.txt` | Log file | Services, Ingress, HPA, PVC verified | LOCALLY VERIFIED |
| **M8** | `helm list -n <ns>` output | `evidence/m8-helm-list.txt` | Log file | Revision 1 deployed in bookflow ns | LOCALLY VERIFIED |
| **M8** | Browser screenshot of app via Ingress hostname | `evidence/m8-ingress-browser.png` | Browser Screenshot | Verified via Ingress at localhost:8088 | LOCALLY VERIFIED |
| **M9** | Observability Helm values | `monitoring/prometheus-values.yaml` | Helm values | In Progress | IMPLEMENTED |
| **M9** | `curl http://<backend>/metrics` output | `evidence/m9-curl-metrics.txt` | Prometheus metrics log | Verified on localhost:8000 (8.7KB) | LOCALLY VERIFIED |
| **M9** | Prometheus Targets page showing app UP | `evidence/m9-prometheus-targets.png` | Browser Screenshot | Pending Prometheus run | PENDING |
| **M9** | Grafana dashboard with populated panel | `evidence/m9-grafana-dashboard.png`, `monitoring/bookflow-dashboard.json` | Screenshot & JSON | Pending Grafana run | PENDING |
| **M10** | Comprehensive README.md in repository root | `README.md` | Markdown documentation | In Progress | IMPLEMENTED |
| **M10** | Live demo script and walkthrough guide | `evidence/m10-demo-script.md` | Markdown guide | In Progress | IMPLEMENTED |
