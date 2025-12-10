# Terraform configuration for InterConnect in google
terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
            version = ">= 5.0.0"
        }
    }

    required_version = ">= 1.3.0"
}

# Configure Google Provider
provider "google" {
    project = var.project_id
    region  = var.region
    zone    = var.zone
}

locals {
    vpc_id = var.use_existing_vpc ? data.google_compute_network.existing_vpc[0].id : google_compute_network.vpc[0].id
    vpc_self_link = var.use_existing_vpc ? data.google_compute_network.existing_vpc[0].self_link : google_compute_network.vpc[0].self_link
    subnet_self_link = var.use_existing_subnet ? data.google_compute_subnetwork.existing_subnet[0].self_link : google_compute_subnetwork.subnet[0].self_link
}

# Create VPC
resource "google_compute_network" "vpc" {
    count                   = var.use_existing_vpc ? 0 : 1
    name                    = var.vpc_name
    auto_create_subnetworks = false
    routing_mode            = "GLOBAL"
}

# get existing VPC by VPC Name
data "google_compute_network" "existing_vpc" {
    count = var.use_existing_vpc ? 1 : 0
    name  = var.vpc_name
}

# Create subnet
resource "google_compute_subnetwork" "subnet" {
    count         = var.use_existing_subnet ? 0 : 1
    name          = var.subnet_name
    region        = var.region
    network       = local.vpc_id
    ip_cidr_range = var.subnet_cidr
}

# Get existing subnet by Name
data "google_compute_subnetwork" "existing_subnet" {
    count  = var.use_existing_subnet ? 1 : 0
    name   = var.subnet_name
    region = var.region
}

# Create VM instance
resource "google_compute_instance" "vm" {
    count        = var.use_existing_vm ? 0 : 1
    name         = var.vm_name
    machine_type = var.machine_type
    zone         = var.zone

    boot_disk {
        initialize_params {
        image = var.image
        }
    }

    network_interface {
        subnetwork = local.subnet_self_link

        # Enable external IP only if needed
        access_config {}
    }
}

# Create Cloud Router
resource "google_compute_router" "cloud_router" {
  name    = var.router_name
  region  = var.region
  network = local.vpc_self_link

  bgp {
    asn = var.router_asn
  }

  description = "Terraform-created Cloud Router attached to custom VPC"
}

# Create VLAN Attachment
# VLAN Attachment A
resource "google_compute_interconnect_attachment" "vlan_a" {
  name          = var.vlan_a_name
  region        = var.region
  type          = "PARTNER"
  admin_enabled = true
  router        = google_compute_router.cloud_router.id
  stack_type    = "IPV4_ONLY"
  mtu           = var.mtu
}

# VLAN Attachment B
resource "google_compute_interconnect_attachment" "vlan_b" {
  name          = var.vlan_b_name
  region        = var.region
  type          = "PARTNER"
  admin_enabled = true
  router        = google_compute_router.cloud_router.id
  stack_type    = "IPV4_ONLY"
  mtu           = var.mtu
}