# Variables for AWS Direct Connect configuration

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "aws-direct-connect-demo"
}

variable "aws_region" {
  description = "AWS region to deploy the infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# VPC Configuration
variable "vpc_cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "availability_zone" {
  description = "Availability zone for subnets"
  type        = string
  default     = "us-east-1a"
}

# Direct Connect Configuration
variable "enable_direct_connect" {
  description = "Whether to create Direct Connect resources"
  type        = bool
  default     = true
}

variable "dx_bandwidth" {
  description = "Direct Connect connection bandwidth (1Gbps, 10Gbps)"
  type        = string
  default     = "1Gbps"
}

variable "dx_location" {
  description = "Direct Connect location"
  type        = string
  default     = "EqDC2"  # Equinix DC2 in Ashburn, VA
}

variable "dx_gateway_asn" {
  description = "ASN for Direct Connect Gateway"
  type        = number
  default     = 64512
}

# BGP Configuration
variable "customer_asn" {
  description = "Customer ASN for BGP peering"
  type        = number
  default     = 65000
}

variable "customer_ip" {
  description = "Customer IP address for BGP peering"
  type        = string
  default     = "169.254.1.1/30"
}

variable "aws_ip" {
  description = "AWS IP address for BGP peering"
  type        = string
  default     = "169.254.1.2/30"
}

# Tags
variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default = {
    Project     = "DirectConnect"
    ManagedBy   = "Terraform"
  }
}
