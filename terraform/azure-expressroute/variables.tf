# Variables for ExpressRoute circuit configuration on Azure
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "graphiant-express-route"
}

variable "azure_region" {
  description = "Azure region to deploy the infrastructure"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vnet_address_space" {
  description = "Address space for Virtual Network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_prefix" {
  description = "Address prefix for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

# ExpressRoute Circuit Configuration Variables
variable "enable_expressroute" {
  description = "Whether to create an ExpressRoute circuit"
  type        = bool
  default     = true
}

variable "expressroute_sku" {
  description = "ExpressRoute circuit SKU (Standard, Premium)"
  type        = string
  default     = "Standard"
}

variable "expressroute_family" {
  description = "ExpressRoute circuit family (MeteredData, UnlimitedData)"
  type        = string
  default     = "MeteredData"
}

variable "expressroute_bandwidth" {
  description = "ExpressRoute circuit bandwidth in Mbps (50, 100, 200, 500, 1000, 2000, 5000, 10000)"
  type        = number
  default     = 50
}

variable "expressroute_peering_location" {
  description = "ExpressRoute peering location"
  type        = string
  default     = "Washington DC"
}

variable "expressroute_service_provider" {
  description = "ExpressRoute service provider name"
  type        = string
  default     = "PacketFabric"
}

variable "expressroute_allow_classic_operations" {
  description = "Allow classic operations on ExpressRoute circuit"
  type        = bool
  default     = false
}

variable "expressroute_secondary_peering_location" {
  description = "Secondary ExpressRoute peering location for redundancy"
  type        = string
  default     = ""
}

variable "expressroute_secondary_bandwidth" {
  description = "Secondary ExpressRoute circuit bandwidth in Mbps"
  type        = number
  default     = 50
}

variable "expressroute_secondary_service_provider" {
  description = "Secondary ExpressRoute service provider name"
  type        = string
  default     = "PacketFabric"
}

variable "expressroute_gateway_sku" {
  description = "ExpressRoute Gateway SKU (Standard, HighPerformance, UltraPerformance)"
  type        = string
  default     = "Standard"
}

variable "expressroute_gateway_scale_units" {
  description = "Number of scale units for ExpressRoute Gateway"
  type        = number
  default     = 1
}

# ExpressRoute Peering Configuration Variables
variable "expressroute_shared_key" {
  description = "Shared key for ExpressRoute circuit peering"
  type        = string
  default     = ""
  sensitive   = true
}

variable "expressroute_peer_asn" {
  description = "ASN for ExpressRoute circuit peering"
  type        = number
  default     = 100
}

variable "expressroute_primary_peer_address_prefix" {
  description = "Primary peer address prefix for ExpressRoute peering"
  type        = string
  default     = "192.168.1.0/30"
}

variable "expressroute_secondary_peer_address_prefix" {
  description = "Secondary peer address prefix for ExpressRoute peering"
  type        = string
  default     = "192.168.2.0/30"
}

variable "expressroute_vlan_id" {
  description = "VLAN ID for ExpressRoute circuit peering"
  type        = number
  default     = 100
}

variable "expressroute_advertised_public_prefixes" {
  description = "Advertised public prefixes for ExpressRoute peering"
  type        = list(string)
  default     = ["168.62.0.0/16"]
}

variable "create_expressroute_connection" {
  description = "Whether to create the ExpressRoute connection (set to true after service provider provisions the circuit)"
  type        = bool
  default     = false
}

variable "route_table_disable_bgp_propagation" {
  description = "Whether to disable BGP route propagation on the route table"
  type        = bool
  default     = false
}

variable "route_table_default_route" {
  description = "Default route destination (e.g., 0.0.0.0/0 for all traffic, or specific subnet)"
  type        = string
  default     = "0.0.0.0/0"
}
