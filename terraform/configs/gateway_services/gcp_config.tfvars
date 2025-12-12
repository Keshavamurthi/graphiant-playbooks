# GCP InterConnect Configuration
# Copy this file to terraform.tfvars and modify the values as needed

# -----------------------
#    GCP Project Configuration
# -----------------------
project_id = "your-project-id"
region     = "us-central1"
zone       = "us-central1-a"

# -----------------------
#    VPC Configuration
# -----------------------

# Set to true to use an existing VPC, false to create a new one
use_existing_vpc = true
vpc_name         = "your-vpc-name"  # Name of existing VPC or name for new VPC

# -----------------------
#    Subnet Configuration
# -----------------------

# Set to true to use an existing subnet, false to create a new one
use_existing_subnet = true
subnet_name         = "your-subnet-name"  # Name of existing subnet or name for new subnet
# subnet_cidr         = "10.0.1.0/24"  # Required only when creating new subnet (use_existing_subnet = false)

# -----------------------
#    VM Instance Configuration
# -----------------------

# Set to true to skip VM creation, false to create a new VM (optional)
use_existing_vm = true
# vm_name         = "graphiant-test-vm"  # Required only when creating new VM
# machine_type    = "e2-medium"          # Required only when creating new VM
# image           = "debian-cloud/debian-12"  # Required only when creating new VM

# -----------------------
#    Cloud Router Configuration
# -----------------------

router_name = "graphiant-cloud-router"
router_asn  = 16550

# -----------------------
#    InterConnect Configuration
# -----------------------

# VLAN Attachment A
vlan_a_name = "graphiant-vlan-attachment-a"

# VLAN Attachment B
vlan_b_name = "graphiant-vlan-attachment-b"

# MTU Configuration
mtu = 1440  # Valid values: 1440 or 1500
