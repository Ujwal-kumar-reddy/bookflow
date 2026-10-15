# BookFlow — Student Library Book-Lending Tracker

[![BookFlow CI/CD](https://github.com/placeholder/bookflow/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/placeholder/bookflow/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.31-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-1.10+-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)](https://react.dev/)

**BookFlow** is a modern, cloud-native student library book circulation and loan management system built as the final capstone for Session 21 DevOps Engineering. It demonstrates a complete production-grade delivery lifecycle: from local containerized development and automated testing, through DevSecOps pipelines and Infrastructure as Code, to monitored multi-replica Kubernetes orchestration on AWS EKS.

---

## 1. Architecture Overview

```text
[ Developer Laptop ]
        │
        ▼
   [ Git / GitHub ] (main branch push)
        │
        ▼
[ GitHub Actions CI/CD ]
   ├─ 1. Quality Gate: Pytest test suite (15 tests) + Frontend production build
   ├─ 2. Containerization: Docker build backend & frontend
   ├─ 3. DevSecOps: Trivy security scan (HIGH/CRITICAL, exit-code 1)
   └─ 4. Registry: Publish to GHCR tagged with Git commit SHA
        │
        ▼
 [ Terraform IaC (ap-south-1) ]
   ├─ AWS VPC (2 public subnets with ELB tags, 2 private subnets, NAT Gateway)
   ├─ Amazon EKS Cluster (Managed Node Group: 2x t3.medium)
   └─ AWS EBS CSI Driver Add-on (for dynamic PVC storage)
        │
        ▼
 [ Kubernetes Orchestration via Helm ]
   ├─ Ingress Controller (nginx): / -> Frontend (8080), /api -> Backend (8000)
   ├─ Frontend: 2 Replicas (Nginx unprivileged, non-root UID 101)
   ├─ Backend: 2 Replicas (FastAPI Python 3.12, non-root UID 10001)
   ├─ Horizontal Pod Autoscaler (HPA): 2–6 replicas scaling at 60% CPU
   └─ PostgreSQL Database: 1 Replica with 5Gi Persistent Volume Claim (PGDATA subpath)
        │
        ▼
 [ Observability Stack (kube-prometheus-stack) ]
   ├─ Prometheus Operator + ServiceMonitor scraping backend /metrics
   └─ Grafana Dashboard: Live request rate, p95 latency, error rate, CPU metrics
```

---

## 2. Application Features & API Endpoints

### Domain Capabilities
- **Book Catalogue Management:** Full CRUD operations on library books with title, author, and genre/category.
- **Student Lending & Circulation Rules:**
  - One-click checkout with borrower identification and custom loan duration (7, 14, 21, or 30 days).
  - Business rule enforcement: Cannot check out an already borrowed book.
  - One-click book returns restoring shelf availability.
- **Live Circulation Analytics:** Real-time KPI counters for Total Books, Available on Shelves, Active Loans, and Overdue Loans.
- **Search & Filtering:** Real-time search across titles, authors, and student borrowers with category and status filters.

### REST API Reference (FastAPI Backend on Port 8000)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API service metadata, version, and documentation link |
| `GET` | `/health` | Lightweight liveness probe returning `{"status": "UP"}` |
| `GET` | `/ready` | Deep readiness probe verifying database query connectivity (`{"status": "READY"}`) |
| `GET` | `/metrics` | Prometheus-formatted metrics exposed by `prometheus-fastapi-instrumentator` |
| `GET` | `/docs` | Interactive Swagger UI API documentation |
| `GET` | `/api/books` | List books with optional `status`, `category`, and `search` query parameters |
| `POST` | `/api/books` | Add a new book to the catalogue (Status: 201 Created) |
| `GET` | `/api/books/{id}` | Retrieve details for a specific book by ID |
| `PUT` | `/api/books/{id}` | Update book details (title, author, category) |
| `DELETE`| `/api/books/{id}` | Remove a book from the catalogue |
| `GET` | `/api/books/stats` | Aggregated metrics: `total`, `available`, `borrowed`, and `overdue` counts |
| `POST` | `/api/books/{id}/checkout` | Loan out a book to a student with duration in days |
| `POST` | `/api/books/{id}/return` | Return a borrowed book back to library inventory |

---

## 3. Local Development & Docker Compose

### Prerequisites
- Python 3.12+
- Node.js 22+ & npm
- Docker Desktop with Compose

### Fast Start with Docker Compose
To launch the entire stack (PostgreSQL, FastAPI backend, and React frontend) with a single command:

```bash
docker compose up -d --build
```

Access the services:
- **Frontend Application:** [http://localhost:3000](http://localhost:3000)
- **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Backend Health Check:** [http://localhost:8000/health](http://localhost:8000/health)
- **Prometheus Metrics:** [http://localhost:8000/metrics](http://localhost:8000/metrics)

To shut down the stack:
```bash
docker compose down
```

### Running Backend Directly (Standalone)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://bookflow:bookflow@localhost:5433/bookflow"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Running Frontend Directly (Vite Dev Server)
```bash
cd frontend
npm ci
npm run dev
```

---

## 4. Testing & Quality Gate (Module 2)

The backend features an isolated, deterministic test suite utilizing `pytest` with an in-memory SQLite database (`sqlite:///:memory:`) and `StaticPool`. 

- **Safety Guard:** Built-in safeguards abort test execution if accidentally targeted against any non-test database URL.
- **Zero Pollution:** Tables are created and dropped on each test fixture, leaving no leftover database files or state behind.
- **Coverage:** 15 test cases covering full CRUD, validation errors (422), not found (404), checkout rules, return rules, stats calculations, `/health`, `/ready`, and `/metrics`.

Run the test suite:
```bash
cd backend
pytest -v
```

---

## 5. DevSecOps: Trivy Container Security Scanning (Module 6)

In accordance with modern DevSecOps standards, every container image built in the pipeline is scanned by **Trivy** prior to publication to GitHub Container Registry.

- **Scan Configuration:** Gated on `HIGH,CRITICAL` severity with `exit-code: '1'`.
- **Policy Enforcement:** If any unpatched high or critical CVE is present in Debian base layers, Python wheels, Alpine base layers, or NPM packages, the pipeline immediately halts and blocks deployment.
- **Justification for `ignore-unfixed: true`:** By focusing exclusively on CVEs that possess an available vendor security fix, engineering teams avoid false-positive build failures caused by unactionable upstream disclosures, while strictly enforcing zero tolerance on patchable vulnerabilities.

---

## 6. Infrastructure as Code: Terraform (Module 7)

Terraform provisions the underlying AWS network and managed Kubernetes infrastructure in region `ap-south-1` (Mumbai).

### Provisioned Resources
- **Amazon VPC:** CIDR `10.20.0.0/16`, across 2 Availability Zones.
- **Subnets:** 2 public subnets (`10.20.101.0/24`, `10.20.102.0/24`) tagged with `kubernetes.io/role/elb = 1`, and 2 private subnets (`10.20.1.0/24`, `10.20.2.0/24`).
- **NAT Gateway:** 1 Single NAT Gateway for outbound egress from private worker nodes.
- **Amazon EKS Cluster:** Managed Kubernetes cluster (v1.31) with public endpoint access enabled.
- **Managed Node Group:** 2x `t3.medium` worker nodes (scalable from 2 to 4 nodes).
- **EBS CSI Driver:** Configured as an EKS add-on with IAM permissions to support persistent volumes.

### Terraform Commands
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
# Apply only after explicit interactive confirmation:
terraform apply
# Update local kubectl context:
aws eks update-kubeconfig --region ap-south-1 --name bookflow-eks
# Clean teardown:
terraform destroy
```

---

## 7. Kubernetes & Helm Deployment (Module 8)

The application is packaged and deployed as a unified Helm chart located in `helm/bookflow`.

### Deployment Steps
```bash
# 1. Apply dedicated namespace
kubectl apply -f k8s/namespace.yaml

# 2. Deploy BookFlow via Helm
helm upgrade --install bookflow ./helm/bookflow \
  --namespace bookflow \
  --create-namespace \
  -f ./helm/bookflow/values-dev.yaml

# 3. Verify deployment health
kubectl get pods -n bookflow -o wide
kubectl get svc -n bookflow
kubectl get ingress -n bookflow
kubectl get hpa -n bookflow
```

---

## 8. Observability: Prometheus & Grafana (Module 9)

### 1. Install Prometheus Stack
Install `kube-prometheus-stack` into a dedicated `monitoring` namespace **before** the application chart, ensuring the `ServiceMonitor` CRD is registered:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f ./monitoring/prometheus-values.yaml
```

### 2. Access Dashboards
```bash
# Access Prometheus Targets
kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
# Open http://localhost:9090/targets and verify bookflow-backend target is UP

# Access Grafana
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3001:80
# Open http://localhost:3001 and import ./monitoring/bookflow-dashboard.json
```

### 3. Generate Load
Generate automated traffic against BookFlow to visualize live metrics and observe HPA scaling:
```bash
./scripts/load-test.sh 500
```

---

## 9. Troubleshooting Lab Exercises

The `troubleshooting/` directory contains manifests designed to practice diagnosing common Kubernetes failure modes:

### Scenario 1: Broken Image (`ImagePullBackOff`)
```bash
kubectl apply -f troubleshooting/broken-image.yaml
kubectl get pods -n bookflow
kubectl describe pod -n bookflow -l app=broken-image
# Root Cause: Image tag 'does-not-exist' cannot be pulled.
# Fix & Cleanup:
kubectl delete -f troubleshooting/broken-image.yaml
```

### Scenario 2: Broken Service (Label Mismatch / Empty Endpoints)
```bash
kubectl apply -f troubleshooting/broken-service.yaml
kubectl get svc -n bookflow bookflow-broken-service
kubectl get endpoints -n bookflow bookflow-broken-service
# Root Cause: Service selector 'app: label-that-does-not-exist' matches 0 pods.
# Fix & Cleanup:
kubectl delete -f troubleshooting/broken-service.yaml
```

---

## 10. Architectural Adaptations from Starter Code

Every deviation from the original starter repository has been deliberately engineered, verified, and documented below:

| Component | Starter Issue / Limitation | BookFlow Adaptation & Engineering Justification |
|---|---|---|
| **Application Domain** | Generic TaskBoard clone (0 pts for originality) | Replaced with **BookFlow**: an original student library lending tracker with Book data model, checkout/return business rules, loan duration logic, and custom KPI cards. |
| **Frontend Security** | Ran as `root` on port 80 in `nginx:1.27-alpine` | Switched to `nginxinc/nginx-unprivileged:1.27-alpine` listening on port 8080 as non-root user `UID 101`. Writable temp and PID paths configured. Compose and Helm updated to 8080. |
| **Database Security** | Plaintext database password in Helm values | Migrated backend database credentials in Helm to reference the `bookflow-postgres` Kubernetes Secret via `secretKeyRef`. |
| **PVC Data Integrity** | Postgres data mounted directly at `/var/lib/postgresql/data` | Set `PGDATA=/var/lib/postgresql/data/pgdata` to avoid filesystem collisions with `lost+found` directory on fresh persistent volume mounts. |
| **Dual Schema Race** | Backend ran `Base.metadata.create_all` AND `alembic upgrade head` | Removed `create_all` from production startup; Alembic is now the single authoritative schema source. Tests use `conftest.py` with in-memory SQLite. |
| **Pytest Suite** | 3 tests; 1 test failed with "no such table"; relative `test.db` pollution | Added `conftest.py` with in-memory SQLite (`StaticPool`), dependency overrides, safety guards, and 15 comprehensive tests covering all endpoints. |
| **Terraform HCL** | Invalid single-line HCL blocks failing `terraform validate` | Formatted into clean multi-line HCL blocks; added variables, dynamic AZs, EBS CSI add-on, public subnet ELB tags, and `configure_kubectl` output. |
| **CI Workflow Reliability** | Failed on uppercase GitHub usernames and empty kubeconfigs | Implemented bash lowercasing for GHCR image paths; added `if: vars.DEPLOY_ENABLED == 'true'` guard so CI runs green without an active cluster. |
| **Frontend Package Quality** | Unpinned `"latest"` dependencies with no lockfile | Pinned stable versions for React 18 and Vite 5; generated clean `package-lock.json` with 0 npm audit vulnerabilities. |
| **Nginx Upstream Resolution**| `nginx.conf` proxied to `backend:8000`, causing Nginx DNS crash in K8s | Added a Service alias named `backend` in the Helm chart matching the Nginx upstream name. |
| **Dev Replicas & HPA** | `values-dev.yaml` set 1 replica and disabled HPA | Updated `values-dev.yaml` to configure 2 replicas and enable HPA to satisfy the 2+ replica rubric requirement. |
| **Load Test Target** | `scripts/load-test.sh` queried non-existent `/api/health` | Rewrote script to target routed `/api/books` and `/api/books/stats` endpoints, generating genuine DB and CPU load. |
