# Variables For DirectConnect circuit configuration on AWS
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "graphiant-direct-connect"
}

variable "aws_region" {
  description = "AWS region to deploy the infrastructure"
  type        = string
  default     = "us-east-2"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "use_existing_vpc" {
  description = "Whether to create a VPC"
  type        = bool
  default     = true
}

variable "cidr_block" {
  description = "IP address range for a network in AWS"
  type        = string
  default     = "10.0.0.0/16"
}

variable "tenancy" {
  description = "VPC instance tenancy (default | dedicated)"
  type        = string
  default     = "default"
}

variable "existing_vpc_name" {
  description = "Name of an already existing VPC"
  type        = string
  default     = null
}

variable "use_existing_subnet" {
  description = "Whether to create a Private Subnet"
  type        = bool
  default     = true
}

variable "private_subnet_cidr" {
  description = "IP address range for a network in AWS"
  type        = string
  default     = "10.0.1.0/24"
}

variable "aws_az" {
  description = "Availability Zone for the Private Subnet"
  type        = string
  default     = "us-east-2a"
}

variable "existing_subnet_name" {
  description = "Name of an already existing Subnet"
  type        = string
  default     = null
}

variable "use_existing_route_table" {
  description = "Whether to create new route table"
  type        = bool
  default     = true
}

variable "existing_route_table_name" {
  description = "Name of an already existing route table"
  type        = string
  default     = null
}

variable "deploy_vm" {
  type        = bool
  default     = true
  description = "Set to true to deploy the VM, false to skip."
}

variable "ami" {
  type    = string
  default = "ami-0f9fc25dd2506cf6d" # Amazon Linux 2023, us-east-1
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "key_name" {
  type = string
}

variable "ssh_allowed_cidr" {
  type    = string
  default = "your-management-ip/32" # Replace with your management IP or VPN CIDR
}

variable "deploy_connect_endpoint" {
  type    = bool
  default = true
}

variable "tgw_description" {
  description = "Description for transit gateway"
  type        = string
  default     = "Graphiant Core Connection"
}

variable "tgw_asn_number" {
  description = "Amazon side ASN number"
  type        = number
  default     = 64512
}

variable "dx_gateway_name" {
  description = "Direct Connect Gateway Name"
  type        = string
  default     = "dry_run_dxgw"
}

variable "dx_gateway_asn" {
  description = "amazon side ASN Number"
  type        = number
  default     = 64513
}

variable "dxgw_allowed_prefixes" {
  description = "Restricted Prefix allowed from VPC"
  type        = list(string)
  default     = ["10.0.0.0/16", "192.168.1.0/24"]
}

variable "dx_connection_id" {
  description = "Direct Connect connection ID (e.g., dxcon-xxxxx)"
  type        = string
  default     = null
}

variable "dx_connection_vlan" {
  description = "VLAN ID for the Transit Virtual Interface"
  type        = number
  default     = null
}

variable "dx_vif_name" {
  description = "Name for the Direct Connect private virtual interface"
  type        = string
  default     = "dry_run-dx_vif"
}

variable "customer_bgp_asn" {
  description = "Your BGP ASN for peering"
  type        = number
  default     = 30656
}

variable "transit_vif_mtu" {
  description = "MTU value for the Virtual interface. Valid values: 1500 or 8500 (jumbo frames)"
  type        = number
  default     = 8500
}

variable "skip_manual_steps" {
  description = "Set to true to skip resources that require manual Direct Connect connection acceptance. Use false for pre-manual step, true for post-manual step."
  type        = bool
  default     = false
}
