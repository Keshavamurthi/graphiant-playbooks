# Outputs for AWS Direct Connect configuration

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "private_subnet_id" {
  description = "ID of the private subnet"
  value       = aws_subnet.private.id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

# Direct Connect Outputs
output "direct_connect_connection_id" {
  description = "ID of the Direct Connect connection"
  value       = var.enable_direct_connect ? aws_dx_connection.main[0].id : "Direct Connect not enabled"
}

output "direct_connect_connection_name" {
  description = "Name of the Direct Connect connection"
  value       = var.enable_direct_connect ? aws_dx_connection.main[0].name : "Direct Connect not enabled"
}

output "direct_connect_connection_bandwidth" {
  description = "Bandwidth of the Direct Connect connection"
  value       = var.enable_direct_connect ? aws_dx_connection.main[0].bandwidth : "Direct Connect not enabled"
}

output "direct_connect_connection_location" {
  description = "Location of the Direct Connect connection"
  value       = var.enable_direct_connect ? aws_dx_connection.main[0].location : "Direct Connect not enabled"
}

output "direct_connect_connection_arn" {
  description = "ARN of the Direct Connect connection"
  value       = var.enable_direct_connect ? aws_dx_connection.main[0].arn : "Direct Connect not enabled"
}

output "direct_connect_gateway_id" {
  description = "ID of the Direct Connect Gateway"
  value       = var.enable_direct_connect ? aws_dx_gateway.main[0].id : "Direct Connect not enabled"
}

output "direct_connect_gateway_name" {
  description = "Name of the Direct Connect Gateway"
  value       = var.enable_direct_connect ? aws_dx_gateway.main[0].name : "Direct Connect not enabled"
}

output "direct_connect_gateway_asn" {
  description = "ASN of the Direct Connect Gateway"
  value       = var.enable_direct_connect ? aws_dx_gateway.main[0].amazon_side_asn : "Direct Connect not enabled"
}

output "vpn_gateway_id" {
  description = "ID of the VPN Gateway"
  value       = var.enable_direct_connect ? aws_vpn_gateway.main[0].id : "Direct Connect not enabled"
}

output "nat_gateway_id" {
  description = "ID of the NAT Gateway"
  value       = var.enable_direct_connect ? aws_nat_gateway.main[0].id : "Direct Connect not enabled"
}

output "nat_gateway_public_ip" {
  description = "Public IP of the NAT Gateway"
  value       = var.enable_direct_connect ? aws_eip.nat[0].public_ip : "Direct Connect not enabled"
}

output "security_group_id" {
  description = "ID of the Direct Connect security group"
  value       = var.enable_direct_connect ? aws_security_group.dx[0].id : "Direct Connect not enabled"
}

# Deployment Status
output "deployment_status" {
  description = "Current deployment status and next steps"
  value = var.enable_direct_connect ? "✅ AWS Direct Connect infrastructure is ready! Contact your Direct Connect partner to provision the physical connection." : "Direct Connect not enabled"
}

output "next_steps" {
  description = "Next steps for Direct Connect setup"
  value = var.enable_direct_connect ? "1. Contact your Direct Connect partner (Equinix, etc.) to provision the physical connection\n2. Once provisioned, create a Direct Connect Virtual Interface\n3. Configure BGP peering with AWS" : "N/A"
}

output "connection_details" {
  description = "Connection details for Direct Connect partner"
  value = var.enable_direct_connect ? {
    connection_id = aws_dx_connection.main[0].id
    location      = aws_dx_connection.main[0].location
    bandwidth     = aws_dx_connection.main[0].bandwidth
    owner_account = aws_dx_connection.main[0].owner_account_id
  } : "Direct Connect not enabled"
}
