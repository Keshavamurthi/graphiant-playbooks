# -----------------------
#    VPC Configuration
# -----------------------

# Output the VPC ID
output "vpc_id" {
  description = "The ID of the VPC in use"
  value       = local.vpc_id
}

# Output the VPC Name
output "vpc_name" {
  description = "The name of the VPC"
  value       = var.vpc_name
}

# -----------------------
#    Subnet Configuration
# -----------------------

# Output the Subnet Self Link
output "subnet_self_link" {
  description = "Self link of the subnet (created or existing)"
  value       = local.subnet_self_link
}

# Output the Subnet Name
output "subnet_name" {
  description = "Name of the subnet"
  value       = var.subnet_name
}

# -----------------------
#    VM Instance
# -----------------------

output "vm_instance_id" {
  description = "ID of the VM instance"
  value       = var.use_existing_vm ? null : google_compute_instance.vm[0].id
}

output "vm_instance_name" {
  description = "Name of the VM instance"
  value       = var.use_existing_vm ? null : google_compute_instance.vm[0].name
}

output "vm_private_ip" {
  description = "Private IP address of the VM instance"
  value       = var.use_existing_vm ? null : google_compute_instance.vm[0].network_interface[0].network_ip
}

output "vm_public_ip" {
  description = "Public IP address of the VM instance"
  value       = var.use_existing_vm ? null : try(google_compute_instance.vm[0].network_interface[0].access_config[0].nat_ip, null)
}

# -----------------------
#    Cloud Router
# -----------------------

output "cloud_router_id" {
  description = "ID of the Cloud Router"
  value       = google_compute_router.cloud_router.id
}

output "cloud_router_name" {
  description = "Name of the Cloud Router"
  value       = google_compute_router.cloud_router.name
}

output "cloud_router_asn" {
  description = "BGP ASN of the Cloud Router"
  value       = google_compute_router.cloud_router.bgp[0].asn
}

# -----------------------
#    VLAN Attachments
# -----------------------

output "vlan_attachment_a_id" {
  description = "ID of VLAN Attachment A"
  value       = google_compute_interconnect_attachment.vlan_a.id
}

output "vlan_attachment_a_name" {
  description = "Name of VLAN Attachment A"
  value       = google_compute_interconnect_attachment.vlan_a.name
}

output "vlan_attachment_a_self_link" {
  description = "Self link of VLAN Attachment A"
  value       = google_compute_interconnect_attachment.vlan_a.self_link
}

output "vlan_attachment_a_cloud_router_ip_address" {
  description = "Cloud Router IP address for VLAN Attachment A"
  value       = google_compute_interconnect_attachment.vlan_a.cloud_router_ip_address
}

output "vlan_attachment_a_customer_router_ip_address" {
  description = "Customer Router IP address for VLAN Attachment A"
  value       = google_compute_interconnect_attachment.vlan_a.customer_router_ip_address
}

output "vlan_attachment_a_pairing_key" {
  description = "Pairing key for VLAN Attachment A (for partner interconnect)"
  value       = google_compute_interconnect_attachment.vlan_a.pairing_key
  sensitive   = true
}

output "vlan_attachment_b_id" {
  description = "ID of VLAN Attachment B"
  value       = google_compute_interconnect_attachment.vlan_b.id
}

output "vlan_attachment_b_name" {
  description = "Name of VLAN Attachment B"
  value       = google_compute_interconnect_attachment.vlan_b.name
}

output "vlan_attachment_b_self_link" {
  description = "Self link of VLAN Attachment B"
  value       = google_compute_interconnect_attachment.vlan_b.self_link
}

output "vlan_attachment_b_cloud_router_ip_address" {
  description = "Cloud Router IP address for VLAN Attachment B"
  value       = google_compute_interconnect_attachment.vlan_b.cloud_router_ip_address
}

output "vlan_attachment_b_customer_router_ip_address" {
  description = "Customer Router IP address for VLAN Attachment B"
  value       = google_compute_interconnect_attachment.vlan_b.customer_router_ip_address
}

output "vlan_attachment_b_pairing_key" {
  description = "Pairing key for VLAN Attachment B (for partner interconnect)"
  value       = google_compute_interconnect_attachment.vlan_b.pairing_key
  sensitive   = true
}
