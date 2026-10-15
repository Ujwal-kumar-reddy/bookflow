# BookFlow — Terraform Infrastructure as Code

This directory provisions the AWS Virtual Private Cloud (VPC) and Amazon Elastic Kubernetes Service (EKS) cluster for the BookFlow cloud-native deployment.

## Architecture Provisioned
- **AWS VPC:** 2 Public Subnets (with `kubernetes.io/role/elb` tags) and 2 Private Subnets in `ap-south-1`.
- **EKS Cluster:** Managed Kubernetes Control Plane (`v1.31`).
- **Managed Node Group:** 2x `t3.medium` worker nodes with autoscaling (2–4 nodes).
- **EBS CSI Driver:** Dynamic storage driver for Kubernetes PersistentVolumeClaims.

> **Cost Safety Notice:** An EKS control plane and NAT Gateway incur per-hour AWS charges (~$0.26/hr total). Always tear down infrastructure with `terraform destroy` immediately after capturing evaluation evidence.

## Deployment Workflow
```bash
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -recursive
terraform validate
terraform plan
# Apply with explicit approval:
terraform apply
# Configure kubectl:
aws eks update-kubeconfig --region ap-south-1 --name bookflow-eks
# Teardown after verification:
terraform destroy
```
