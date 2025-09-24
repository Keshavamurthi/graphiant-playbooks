# AWS Direct Connect Configuration
# Copy this file to terraform.tfvars and modify the values as needed

# AWS Configuration
aws_region = "us-east-1"

# Environment Configuration
environment   = "dev"
project_name  = "aws-direct-connect-demo"

# VPC Configuration
vpc_cidr_block        = "10.0.0.0/16"
public_subnet_cidr    = "10.0.1.0/24"
private_subnet_cidr   = "10.0.2.0/24"
availability_zone     = "us-east-1a"

# Direct Connect Configuration
enable_direct_connect = true
dx_bandwidth          = "1Gbps"
dx_location           = "EqDC2"  # Equinix DC2 in Ashburn, VA
dx_gateway_asn        = 64512

# BGP Configuration
customer_asn = 65000
customer_ip  = "169.254.1.1/30"
aws_ip       = "169.254.1.2/30"

# Tags
tags = {
  Project     = "DirectConnect"
  ManagedBy   = "Terraform"
  Environment = "dev"
}
