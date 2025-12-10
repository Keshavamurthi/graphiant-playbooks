# Variables for InterConnect configuration in google
variable "project_id" {
    description = "GCP Project ID"
    type        = string
    default     = null
}

variable "region" {
    description = "Google region to deploy infrastructure"
    type        = string
    default     = null
}

variable "use_existing_vpc" {
  description = "Whether to use an existing VPC (true) or create a new one (false)"
  type        = bool
  default     = true
}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
  default     = null
}

variable "use_existing_vm" {
  description = "Whether to use an existing VM (true) or create a new one (false)"
  type        = bool
  default     = true
}

variable "vm_name" {
  type    = string
  default = "demo-vm"
}

variable "machine_type" {
  type    = string
  default = "e2-medium"
}

variable "image" {
  type    = string
  default = "debian-cloud/debian-12"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "use_existing_subnet" {
  description = "Whether to use an existing subnet (true) or create a new one (false)"
  type        = bool
  default     = true
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "subnet_name" {
  description = "Name of the subnet (used for both creating new or referencing existing subnet)"
  type        = string
  default     = null
}

variable "router_name" {
  description = "Name of the Cloud Router"
  type        = string
  default     = "graphiant-cloud-router"
}

variable "router_asn" {
  description = "BGP ASN for the Cloud Router"
  type        = number
  default     = 16550
}

# -----------------------
#    InterConnect Configuration
# -----------------------

variable "vlan_a_name" {
  description = "Name for VLAN Attachment A"
  type        = string
  default     = "graphiant-vlan-attachment-a"
}

variable "vlan_b_name" {
  description = "Name for VLAN Attachment B"
  type        = string
  default     = "graphiant-vlan-attachment-b"
}

variable "vlan_a_tag" {
  description = "802.1q VLAN tag for VLAN Attachment A"
  type        = number
  default     = null
}

variable "vlan_b_tag" {
  description = "802.1q VLAN tag for VLAN Attachment B"
  type        = number
  default     = null
}

variable "mtu" {
  description = "Maximum Transmission Unit (MTU) in bytes. Valid values: 1440 or 1500"
  type        = number
  default     = 1440
}
