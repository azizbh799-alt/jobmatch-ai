# Terraform production starter

This directory is intentionally a starter architecture rather than a fake complete AWS deployment.

Recommended production components:

- VPC with public/private subnets
- EKS
- ECR
- RDS PostgreSQL with pgvector-compatible setup
- ElastiCache Redis
- S3 for CV objects
- Secrets Manager
- IAM roles for service accounts
- ALB/Ingress + ACM TLS
- CloudWatch

Keep Terraform state in an encrypted remote backend and never commit secrets or tfstate.
