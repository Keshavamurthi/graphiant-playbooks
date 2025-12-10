# -----------------------
#    VPC Configuration
# -----------------------

# Output the VPC ID
output "vpc_id" {
  description = "The ID of the VPC in use"
  value       = var.use_existing_vpc ? data.aws_vpc.existing[0].id : aws_vpc.main[0].id
}

# Output the VPC Name
output "vpc_name" {
  description = "The Name tag of the VPC"
  value       = var.use_existing_vpc ? data.aws_vpc.existing[0].tags["Name"] : aws_vpc.main[0].tags["Name"]
}

# Output the VPC CIDR block
output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = var.use_existing_vpc ? data.aws_vpc.existing[0].cidr_block : aws_vpc.main[0].cidr_block
}

# -----------------------
#    Private Subnet
# -----------------------

# Output the Subnet IDs
output "subnet_ids" {
  description = "List of private subnet IDs (created or existing)"
  value       = var.use_existing_subnet ? [data.aws_subnet.existing[0].id] : [aws_subnet.private_subnet[0].id]
}

# Output the Subnet Names
output "subnet_name" {
  description = "Name tag of the subnet"
  value       = var.use_existing_subnet ? data.aws_subnet.existing[0].tags["Name"] : aws_subnet.private_subnet[0].tags["Name"]
}

# -----------------------
#    Route Table
# -----------------------

# Output the Route Table ID
output "private_route_table_id" {
  description = "ID of the private route table (created or existing)"
  value       = var.use_existing_route_table ? data.aws_route_table.existing_private[0].id : aws_route_table.private[0].id
}

# Output the Route Table Name
output "private_route_table_name" {
  description = "Name tag of the private route table"
  value       = var.use_existing_route_table ? data.aws_route_table.existing_private[0].tags["Name"] : aws_route_table.private[0].tags["Name"]
}

# -----------------------
#    Transit Gateway
# -----------------------

# Output the Transit Gateway ID
output "transit_gateway_id" {
  description = "ID of the AWS Transit Gateway"
  value       = aws_ec2_transit_gateway.tgw.id
}

# Output the transit Gateway Name
output "transit_gateway_name" {
  description = "Name tag of the AWS Transit Gateway"
  value       = aws_ec2_transit_gateway.tgw.tags["Name"]
}

# --------------------------------
#    DirectConnect Gateway
# --------------------------------

# Output the DirectConnect Gateway ID
output "dxgw_id" {
  description = "ID of the Direct Connect Gateway"
  value       = aws_dx_gateway.dxgw.id
}

# Output the DirectConnect Gateway Name
output "dxgw_name" {
  description = "Name of the Direct Connect Gateway (resource attribute)"
  value       = aws_dx_gateway.dxgw.name
}

# Output the DirectConnect Gateway Association ID
output "dxgw_tgw_association_id" {
  description = "ID of the association between Direct Connect Gateway and Transit Gateway"
  value       = var.skip_manual_steps ? aws_dx_gateway_association.tgw_dxgw_association[0].id : "Run Step 2 with skip_manual_steps = true"
}

# --------------------------------
#    Transit Virtual Interface
# --------------------------------

# Amazon side ASN
output "amazon_side_asn" {
  description = "Amazon side ASN for BGP peering"
  value       = var.skip_manual_steps ? aws_dx_transit_virtual_interface.transit_vif[0].amazon_side_asn : "Run Step 2 with skip_manual_steps = true"
}

# BGP Authentication Key
output "bgp_authentication_key" {
  description = "BGP authentication key for the virtual interface"
  value       = var.skip_manual_steps ? aws_dx_transit_virtual_interface.transit_vif[0].bgp_auth_key : "Run Step 2 with skip_manual_steps = true"
}

# Your router peer IP (Customer side)
output "customer_router_peer_ip" {
  description = "Customer router peer IP address"
  value       = var.skip_manual_steps ? aws_dx_transit_virtual_interface.transit_vif[0].customer_address : "Run Step 2 with skip_manual_steps = true"
}

# Amazon router peer IP
output "amazon_router_peer_ip" {
  description = "Amazon router peer IP address"
  value       = var.skip_manual_steps ? aws_dx_transit_virtual_interface.transit_vif[0].amazon_address : "Run Step 2 with skip_manual_steps = true"
}

# --------------------------------
#    VM Instance
# --------------------------------

output "VM-instance_id" {
  value = var.deploy_vm ? aws_instance.vm[0].id : null
}

output "VM-private_ip" {
  value = var.deploy_vm ? aws_instance.vm[0].private_ip : null
}
