# AWS Configuration

project_name    = "direct-connect_dry_run"
aws_region      = "us-east-1"
environment     = "prod"

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

skip_manual_steps = true  # Set to true after accepting the Direct Connect connection

# -----------------------
#    VPC Configuration
# -----------------------

# To deploy new VPC 
use_existing_vpc      = false
cidr_block      = "10.0.0.0/16"
tenancy         = "default"

# Use Existing VPC
# use_existing_vpc      = true
# existing_vpc_name = "direct-connect_dry_run-vpc"

# -----------------------
#    Private Subnet
# -----------------------

# To create new Private Subnet
use_existing_subnet   = false
private_subnet_cidr = "10.0.1.0/24"
aws_az          = "us-east-1a"

# Use Existing Subnet
# use_existing_subnet = true
# existing_subnet_name = "direct-connect_dry_run-private-subnet"

# -----------------------
#    Route Table
# -----------------------

# To create new Route Table
use_existing_route_table   = false

# Use Existing Route Table
# use_existing_route_table = true
#  existing_route_table_name = "direct-connect_dry_run-private-rt"

# --------------------------------
#    VM Instance
# --------------------------------
deploy_vm       = true
ami             = "ami-0f9fc25dd2506cf6d"   # Amazon Linux 2023 (us-east-1)
instance_type   = "t3.micro"
key_name        = "nermin-key"
ssh_allowed_cidr = "0.0.0.0/0"

# -----------------------
#    Transit Gateway
# -----------------------

tgw_description     = "Graphiant Core Connection"
tgw_asn_number      = 64512

# ------------------------------
#    DirectConnect Gateway
# ------------------------------

dx_gateway_name     = "dry_run_dxgw"
dx_gateway_asn      = 64513

dxgw_allowed_prefixes = ["10.0.0.0/16"]

# ------------------------------
#    DirectConnect Connection
# ------------------------------

dx_connection_id = "dxcon-fgkk8cr8"
dx_connection_vlan = 2399

# ------------------------------
#   Transit Virtual Interfaces
# ------------------------------

dx_vif_name = "dry_run-trasit-vif"
customer_bgp_asn = 30656
transit_vif_mtu = 8500  # Valid values: 1500 or 8500 (jumbo frames)
