output "cluster_name" {
  value       = module.eks.cluster_name
  description = "Name of the provisioned Amazon EKS cluster"
}

output "cluster_endpoint" {
  value       = module.eks.cluster_endpoint
  description = "Kubernetes API server endpoint URL"
}

output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "ID of the provisioned AWS VPC"
}

output "aws_region" {
  value       = var.aws_region
  description = "AWS region where resources are deployed"
}

output "configure_kubectl" {
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
  description = "Command to configure local kubectl to authenticate with the EKS cluster"
}
