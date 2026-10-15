variable "aws_region" {
  type        = string
  default     = "ap-south-1"
  description = "AWS deployment region (default: ap-south-1 Mumbai)"
}

variable "cluster_name" {
  type        = string
  default     = "bookflow-eks"
  description = "Name of the Amazon EKS cluster"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment environment name (dev/staging/prod)"
}

variable "cluster_version" {
  type        = string
  default     = "1.31"
  description = "Kubernetes control plane version for Amazon EKS"
}

variable "node_instance_types" {
  type        = list(string)
  default     = ["t3.medium"]
  description = "Instance types for EKS managed worker nodes"
}
