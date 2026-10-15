# BookFlow — Capstone Live Demonstration Script (Module 10)

This script outlines the exact live demonstration flow for the final capstone evaluation session. Follow these sequential steps to demonstrate every layer of the DevOps architecture.

---

## 1. Application Layer (M1) — BookFlow Demonstration
1. Open the web browser to `http://localhost:3000` (Local Compose) or `http://bookflow.local` (Kubernetes Ingress).
2. Point out the original domain: **BookFlow — Student Library Lending Tracker**.
3. Point out the live KPI summary cards:
   - **Total Books**, **Available on Shelves**, **Active Loans**, and **Overdue Loans**.
4. Click **"+ Add New Book"**:
   - Title: `Designing Data-Intensive Applications`
   - Author: `Martin Kleppmann`
   - Category: `Computer Science`
   - Click **"Add to Catalogue"**; show the book appear dynamically in the table with status `Available`.
5. Demonstrate Circulation Business Rules:
   - Click **"Loan Out"** on the newly created book.
   - Enter student borrower name: `Aarav Sharma (Roll #2024-CS-042)`.
   - Select loan duration: `14 Days (Standard Loan)`.
   - Click **"Confirm Loan"**; show the status turn to `Borrowed` with calculated due date.
   - Attempt to borrow again or show that the UI only exposes **"Return"**.
   - Click **"Return"**; show the book instantly restored to `Available`.

---

## 2. Backend & REST API Verification (M1, M2, M9)
1. Open FastAPI Swagger UI at `http://localhost:8000/docs` (or `/docs` on Ingress).
2. Execute `GET /health` -> returns `{"status": "UP"}`.
3. Execute `GET /ready` -> performs active database query check and returns `{"status": "READY"}`.
4. Execute `GET /metrics` -> show raw Prometheus metrics instrumented by `prometheus-fastapi-instrumentator`.
5. Run Pytest in the terminal:
   ```bash
   pytest -v
   ```
   Show all 15 tests passing across CRUD, validation errors, loan rules, health, and metrics.

---

## 3. Git Version Control & Commit Traceability (M3)
1. In the terminal, run:
   ```bash
   git log --oneline -n 12
   ```
2. Demonstrate that all commits follow conventional semantic format with meaningful explanations (`feat(backend): ...`, `test(backend): ...`, `ci(pipeline): ...`, `feat(helm): ...`).

---

## 4. Automated CI/CD Pipeline & DevSecOps (M5, M6)
1. Open GitHub repository in the browser: `Actions` tab.
2. Show the latest green pipeline run triggered on push to `main`:
   - Stage 1: `test` — Pytest quality gate passes, Frontend builds.
   - Stage 2: `build-scan-push`:
     - Builds Docker images for backend and frontend.
     - Runs **Trivy** container scan for HIGH and CRITICAL vulnerabilities with exit code 1.
     - Pushes images to GHCR tagged with full Git commit SHA.
3. Open GitHub Container Registry (GHCR) package page:
   - Show `bookflow-backend` and `bookflow-frontend` images tagged with the exact Git commit SHA.

---

## 5. Infrastructure as Code — Terraform (M7)
1. In `terraform/`, show the clean multi-line HCL configuration:
   - VPC with 2 public subnets and 2 private subnets (`10.20.0.0/16`).
   - Dynamic Availability Zones via data source.
   - Public subnet ELB tags (`kubernetes.io/role/elb = 1`).
   - Amazon EKS cluster with managed node group (`t3.medium`).
   - AWS EBS CSI driver add-on for dynamic volume provisioning.
2. Demonstrate validation:
   ```bash
   terraform validate
   ```

---

## 6. Kubernetes & Helm Deployment (M8)
1. Show cluster context:
   ```bash
   kubectl config current-context
   ```
2. Inspect deployed namespace and pods:
   ```bash
   kubectl get pods -n bookflow -o wide
   ```
   Show all pods in `Running` state:
   - 2 replicas of `bookflow-backend`
   - 2 replicas of `bookflow-frontend`
   - 1 replica of `bookflow-postgres`
3. Inspect Services and Ingress:
   ```bash
   kubectl get svc -n bookflow
   kubectl get ingress -n bookflow
   ```
   Show that `/` routes to frontend port 80 and `/api` routes to backend port 8000.
4. Inspect Horizontal Pod Autoscaler (HPA):
   ```bash
   kubectl get hpa -n bookflow
   ```

---

## 7. Observability — Prometheus & Grafana (M9)
1. Show Prometheus targets:
   ```bash
   kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
   ```
   Open `http://localhost:9090/targets` and show `bookflow-backend` ServiceMonitor target in state **UP**.
2. Show Grafana Dashboard:
   ```bash
   kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3001:80
   ```
   Open `http://localhost:3001`, navigate to **"BookFlow - Application Performance & Observability"**:
   - Show HTTP Request Rate panel responding in real-time.
   - Show Request Latency (p95) and Error Rate panels.
3. Run traffic load generator:
   ```bash
   ./scripts/load-test.sh 200
   ```
   Show the live metrics spike in Grafana during traffic generation.

---

## 8. Failure Simulation & Live Troubleshooting Lab
1. **Broken Image Simulation:**
   ```bash
   kubectl apply -f troubleshooting/broken-image.yaml
   kubectl get pods -n bookflow
   ```
   - Observe `ImagePullBackOff`.
   - Run `kubectl describe pod -n bookflow -l app=broken-image` and identify invalid image tag.
   - Cleanup: `kubectl delete -f troubleshooting/broken-image.yaml`.
2. **Broken Service Simulation:**
   ```bash
   kubectl apply -f troubleshooting/broken-service.yaml
   kubectl get svc bookflow-broken-service -n bookflow
   kubectl get endpoints bookflow-broken-service -n bookflow
   ```
   - Observe `<none>` endpoints due to label selector mismatch.
   - Cleanup: `kubectl delete -f troubleshooting/broken-service.yaml`.
   - Show that standard `bookflow-backend` endpoints remain completely healthy.
