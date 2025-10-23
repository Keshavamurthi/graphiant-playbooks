# Example terraform.tfvars file for Azure
# Copy this file to terraform.tfvars and modify the values as needed

# Azure Configuration
azure_region = "East US"

# Environment Configuration
environment   = "dev"
project_name  = "express-route_dry_run"

# Network Configuration
vnet_address_space    = "10.0.0.0/16"
public_subnet_prefix  = "10.0.1.0/24"

# ExpressRoute Configuration
enable_expressroute = true
expressroute_sku = "Standard"
expressroute_family = "MeteredData"
expressroute_bandwidth = 50
expressroute_peering_location = "Washington DC"
expressroute_service_provider = "PacketFabric"
expressroute_allow_classic_operations = false

expressroute_gateway_sku = "Standard"
expressroute_gateway_scale_units = 1

# Secondary ExpressRoute (for redundancy)
expressroute_secondary_peering_location = ""
expressroute_secondary_bandwidth = 50
expressroute_secondary_service_provider = "PacketFabric"

# ExpressRoute Peering Configuration
expressroute_shared_key = ""
expressroute_peer_asn = 30656
expressroute_primary_peer_address_prefix = "169.254.50.0/30"
expressroute_secondary_peer_address_prefix = "169.254.60.0/30"
expressroute_vlan_id = 11
expressroute_advertised_public_prefixes = ["168.62.0.0/16"]

# ExpressRoute Connection (set to true after service provider provisions the circuit)
create_expressroute_connection = true

# Route Table Configuration
route_table_disable_bgp_propagation = false
route_table_default_route = "0.0.0.0/0"

# VM Configuration for E2E Testing
deploy_test_vm = true
vm_size = "Standard_B1s"
vm_admin_username = "azureuser"
vm_ssh_public_key = ""  # Replace with your SSH public key
vm_subnet_prefix = "10.0.3.0/24"
