# gcp InterConnect Configuration
# Copy this file to terraform.tfvars and modify the values as needed

# -----------------------
#    gcp Project Configuration
# -----------------------
project_id = "qa-playbooks-automation"
region     = "us-central1"
zone       = "us-central1-a"

# -----------------------
#    VPC Configuration
# -----------------------

# To deploy new VPC
use_existing_vpc = true
vpc_name         = "graphiant-dry-run-vpc"

# -----------------------
#    Subnet Configuration
# -----------------------

# To create new Subnet
use_existing_subnet = true
subnet_name         = "graphiant-dry-run-subnet"
# subnet_cidr         = "10.0.1.0/24"

# -----------------------
#    VM Instance Configuration
# -----------------------

# To create new VM
use_existing_vm = true
# vm_name         = "graphiant-dry-run-test-vm"
# machine_type    = "e2-medium"
# image           = "debian-cloud/debian-12"

# -----------------------
#    Cloud Router Configuration
# -----------------------

router_name = "graphiant-dry-run-cloud-router"
router_asn  = 16550

# -----------------------
#    InterConnect Configuration
# -----------------------

# VLAN Attachment A
vlan_a_name = "graphiant-dry-run-vlan-attachment-a"

# VLAN Attachment B
vlan_b_name = "graphiant-dry-run-vlan-attachment-b"

# MTU Configuration
mtu = 1440  # Valid values: 1440 or 1500