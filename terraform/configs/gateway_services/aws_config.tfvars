# AWS Direct Connect Configuration
# Copy this file to terraform.tfvars and modify the values as needed

# -----------------------
#    Project Configuration
# -----------------------
project_name = "your-project"
aws_region   = "us-east-1"
environment  = "prod"

# ------------------------------
#   Deployment Control
# ------------------------------
# STEP 1 (Pre-Manual): Set skip_manual_steps = false (or omit, false is default)
#   - Creates: VPC, Subnet, Route Table, Transit Gateway, DirectConnect Gateway
#   - Then: Manually accept Direct Connect connection in AWS Console
#
# STEP 2 (Post-Manual): Set skip_manual_steps = true
#   - Creates: DX Gateway Association, Transit Virtual Interface
#   - Requires: Direct Connect connection to be in "available" or "pending" state

skip_manual_steps = false  # Set to true after accepting the Direct Connect connection

# -----------------------
#    VPC Configuration
# -----------------------

# To deploy new VPC 
use_existing_vpc = false
cidr_block      = "10.0.0.0/16"
tenancy         = "default"

# Use Existing VPC
# use_existing_vpc      = true
# existing_vpc_name = "your-existing-vpc-name"

# -----------------------
#    Private Subnet
# -----------------------

# To create new Private Subnet
use_existing_subnet   = false
private_subnet_cidr = "10.0.1.0/24"
aws_az          = "us-east-1a"

# Use Existing Subnet
# use_existing_subnet = true
# existing_subnet_name = "your-existing-subnet-name"

# -----------------------
#    Route Table
# -----------------------

# To create new Route Table
use_existing_route_table   = false

# Use Existing Route Table
# use_existing_route_table = true
# existing_route_table_name = "your-existing-route-table-name"

# --------------------------------
#    VM Instance (Optional)
# --------------------------------
deploy_vm       = false  # Set to true to deploy a test VM
# ami             = "ami-0f9fc25dd2506cf6d"   # Amazon Linux 2023 (us-east-1) - update for your region
# instance_type   = "t3.micro"
# key_name        = "your-ssh-key-name"
# ssh_allowed_cidr = "0.0.0.0/0"

# -----------------------
#    Transit Gateway
# -----------------------

tgw_description     = "Graphiant Core Connection"
tgw_asn_number      = 64512  # Amazon side ASN (must be different from DirectConnect Gateway ASN)

# ------------------------------
#    DirectConnect Gateway
# ------------------------------

dx_gateway_name     = "graphiant-dx-gateway"
dx_gateway_asn      = 64513  # Amazon side ASN (must be different from Transit Gateway ASN)

dxgw_allowed_prefixes = ["10.0.0.0/16"]  # Prefixes to advertise from AWS to Graphiant

# ------------------------------
#    DirectConnect Connection
# ------------------------------
# This connection ID is provided by Graphiant after you request the Gateway Service

dx_connection_id = "dx-xxxxx"  # From Graphiant
dx_connection_vlan = 100       # VLAN ID from the Direct Connect connection

# ------------------------------
#   Transit Virtual Interfaces
# ------------------------------

dx_vif_name = "graphiant-transit-vif"
customer_bgp_asn = 30656  # Graphiant's ASN
transit_vif_mtu = 8500    # Valid values: 1500 or 8500 (jumbo frames)
