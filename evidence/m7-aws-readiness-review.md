# BookFlow - AWS & Terraform Architecture & Readiness Review

## 1. Executive Summary & Status

| Attribute | Value / Status |
|---|---|
| **Module** | M7 - Infrastructure as Code & AWS Deployment Readiness |
| **Status** | **STATICALLY VALIDATED (DEPLOYMENT BLOCKED BY AWS)** |
| **Cluster State** | Verified Locally on `docker-desktop` (Kubernetes 1.31) |
| **AWS Authentication** | Not configured (`aws sts get-caller-identity` returns no credentials) |
| **Cloud Cost Incurred** | **$0.00** (Zero resources provisioned, zero drift, zero dangling assets) |
| **Terraform Format** | Clean (`terraform fmt -check` passed with 0 diff) |
| **Terraform Validation** | **Success! The configuration is valid.** (`terraform validate` exit code 0) |

> [!IMPORTANT]
> Per non-negotiable mission constraints, no AWS cloud resources have been created, modified, or destroyed. All infrastructure manifests are fully authored, syntax-checked, and statically validated. The complete application stack has been thoroughly verified locally on Docker Desktop Kubernetes.

---

## 2. Tooling Preflight & Validation Results

- **Terraform Binary:** Terraform CLI with HashiCorp AWS Provider `v5.100.0`, Time `v0.14.2`, TLS `v4.4.1`, CloudInit `v2.4.1`.
- **AWS CLI:** Installed and present in PATH.
- **Identity Check:**
  ```text
  $ aws sts get-caller-identity
  Unable to locate credentials. You can configure credentials by running "aws configure".
  ```
- **Validation Command:**
  ```text
  $ cd terraform
  $ terraform init -backend=false
  $ terraform validate
  Success! The configuration is valid.
  ```

---

## 3. Production Cloud Architecture Specification

### 3.1 Network Topology (VPC Module `v5.8.1`)
- **CIDR Block:** `10.20.0.0/16` providing 65,536 private IP addresses.
- **Availability Zones:** 2 AZs in target region (e.g., `us-east-1a`, `us-east-1b`).
- **Subnet Layout:**
  - **Public Subnets:** `10.20.101.0/24`, `10.20.102.0/24` with tag `kubernetes.io/role/elb = 1`.
  - **Private Subnets:** `10.20.1.0/24`, `10.20.2.0/24` with tag `kubernetes.io/role/internal-elb = 1`.
- **NAT Gateway:** 1x Single NAT Gateway (`single_nat_gateway = true`) placed in public subnet to minimize idle cost while providing outbound internet access for private node pulling images.
- **Internet Gateway:** Attached to VPC for public ingress traffic.

### 3.2 Elastic Kubernetes Service (EKS Module `v20.37.1`)
- **Kubernetes Version:** `1.31`
- **Control Plane Endpoint:** Public endpoint enabled (`cluster_endpoint_public_access = true`).
- **Cluster Creator Admin Permissions:** Enabled (`enable_cluster_creator_admin_permissions = true`).
- **Managed Node Group (`main`):**
  - **Instance Type:** `t3.medium` (2 vCPU, 4 GiB Memory, burstable).
  - **Capacity:** Min 2, Max 4, Desired 2 replicas.
  - **Subnets:** Distributed across private subnets for security isolation.
- **Cluster Addons:**
  - `coredns`
  - `kube-proxy`
  - `vpc-cni`
  - `aws-ebs-csi-driver` (most_recent = true)

### 3.3 Storage & Persistence
- **EBS CSI Driver:** Configured with IAM policy `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy` attached to managed node group IAM role.
- **Volume Type:** AWS GP3 dynamic volume provisioning for PostgreSQL database (`10Gi` persistent volume claim with `ReadWriteOnce` access mode).

---

## 4. Itemized Cost Breakdown & Idle Expense Warning

*Source: Official AWS Pricing Documentation (US East N. Virginia, us-east-1)*

| Resource | Pricing Model | Hourly Rate | Estimated Monthly Cost (730h) | Charges Incurred When Idle? |
|---|---|---|---|---|
| **EKS Control Plane** | $0.10 / cluster / hour | $0.1000 | **$73.00** | **YES** (flat hourly fee regardless of workload) |
| **EC2 Managed Nodes (2x `t3.medium`)** | $0.0416 / instance / hour | $0.0832 | **$60.74** | **YES** (unless instances are stopped) |
| **NAT Gateway** | $0.045 / gateway / hour | $0.0450 | **$32.85** | **YES** (continuous hourly fee + data fees) |
| **EBS Storage (50 GB gp3)** | $0.08 / GB / month | ~$0.0055 | **$4.00** | **YES** (storage charged until volume deleted) |
| **Application Load Balancer** | $0.0225 / ALB / hour | $0.0225 | **$16.43** | **YES** (charged continuously while provisioned) |
| **Total Estimated Baseline** | — | **~$0.2562/hr** | **~$187.02 / month (~$6.23 / day)** | — |

> [!WARNING]
> **Idle Cost Alert:** The NAT Gateway ($32.85/mo) and EKS Control Plane ($73.00/mo) charge continuously on an hourly basis even if zero application traffic is served. Always execute `terraform destroy` when not actively testing.

---

## 5. Amazon EKS 1.31 Lifecycle: Standard vs. Extended Support

*Source: Amazon EKS Version Lifecycle Documentation*

- **Standard Support Window:**
  - Amazon EKS provides standard support for approximately **14 months** after the upstream Kubernetes version is released on EKS.
  - During standard support, the standard control plane rate of **$0.10 per cluster per hour** applies.
- **Extended Support Phase:**
  - After the 14-month standard support period ends, clusters automatically enter Extended Support for an additional 12 months.
  - In extended support, AWS charges an additional **$0.50 per cluster per hour**, totaling **$0.60 per hour ($438.00/month)**.
- **Recommendation:**
  - Upgrade the cluster to Kubernetes 1.32+ prior to the conclusion of the 14-month window to prevent a 600% control plane cost increase.

---

## 6. Future Deployment & Teardown Execution Guide

When AWS credentials become available and provisioning is authorized, execute this exact sequence:

### Step 1: Authentication & Preflight
```bash
aws configure
aws sts get-caller-identity
```

### Step 2: Infrastructure Provisioning
```bash
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

### Step 3: Kubernetes Configuration & Helm Deployment
```bash
aws eks update-kubeconfig --region us-east-1 --name bookflow-eks
kubectl get nodes -o wide

# Deploy BookFlow with production values
helm upgrade --install bookflow ./helm/bookflow \
  --namespace bookflow --create-namespace \
  -f ./helm/bookflow/values.yaml \
  -f ./helm/bookflow/values-prod.yaml
```

### Step 4: Complete Teardown & Cost Elimination
```bash
# First uninstall Helm release to release Load Balancers and PVCs
helm uninstall bookflow -n bookflow
kubectl delete pvc --all -n bookflow

# Destroy cloud infrastructure
cd terraform
terraform destroy -auto-approve
```
