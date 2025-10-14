# Terraform Infrastructure as Code

Graphiant Playbooks includes production-ready Terraform modules for deploying cloud networking infrastructure that seamlessly integrates with Graphiant Edge devices.

## 🎯 What Terraform Creates

### Azure ExpressRoute Infrastructure
- **Resource Group**: Container for all Azure resources
- **Virtual Network**: Network infrastructure with subnets
- **ExpressRoute Circuit**: Primary and secondary circuits for redundancy
- **ExpressRoute Gateway**: Gateway for connecting to ExpressRoute
- **Virtual Hub**: Central networking hub (optional)
- **BGP Peering**: Border Gateway Protocol configuration
- **ExpressRoute Connection**: Connection between Gateway and Circuit

## 📁 Terraform Directory Structure

```
terraform/
├── azure-expressroute/           # Azure ExpressRoute modules
│   ├── main.tf                   # Main Terraform configuration
│   ├── variables.tf              # Variable definitions
│   ├── outputs.tf                # Output values
│   └── README.md                 # Azure-specific documentation

configs/terraform/
├── azure_config.tfvars           # Azure variable configuration
```

## 🔧 Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Terraform CLI** | >= 1.1.0 | Infrastructure provisioning |
| **Azure CLI** | Latest | Azure authentication and management |
| **Cloud Account** | Active | Azure subscription |
| **Permissions** | Required | Resource creation and management rights |

## Quick Start with Terraform

### Azure ExpressRoute Setup

#### 1. Authenticate with Azure
```bash
az login
az account set --subscription "your-subscription-id"
```

#### 2. Configure Variables
```bash
# Edit the configuration file
nano configs/terraform/azure_config.tfvars

# Or copy and modify if needed
cp configs/terraform/azure_config.tfvars configs/terraform/my-azure-config.tfvars
```

#### 3. Deploy Infrastructure
```bash
cd terraform/azure-expressroute

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Create and review plan
terraform plan -var-file="../../configs/terraform/azure_config.tfvars" -out=tfplan

# Apply the configuration
terraform apply tfplan
```

## What Terraform Creates

### Azure ExpressRoute Infrastructure
The Azure Terraform configuration deploys:

- **Resource Group** - Container for all resources
- **Virtual Network** - Network infrastructure with subnets
- **ExpressRoute Circuit** - Primary and secondary circuits for redundancy
- **ExpressRoute Gateway** - Gateway for connecting to ExpressRoute
- **Virtual Hub** - Central networking hub (if enabled)
- **BGP Peering** - Border Gateway Protocol configuration
- **ExpressRoute Connection** - Connection between Gateway and Circuit (conditional)

**Note**: The ExpressRoute Connection is only created after the service provider provisions the physical circuit. This prevents deployment failures while waiting for service provider provisioning.

## Integration with Graphiant Playbooks

After deploying the ExpressRoute infrastructure with Terraform, you can use the outputs to configure BGP peering with your Graphiant edge devices:

```python
from libs.edge import Edge

# Initialize Graphiant Edge
edge = Edge(base_url='https://api.graphiant.com', username='user', password='pass')

# Get Terraform outputs for circuit information
# Use these values in your BGP peering configuration
edge.configure_bgp_peers("your_bgp_config.yaml")
```

## Terraform Commands

### Azure ExpressRoute
```bash
cd terraform/azure-expressroute

# Initialize
terraform init

# Validate
terraform validate

# Plan
terraform plan -var-file="../../configs/terraform/azure_config.tfvars" -out=tfplan

# Apply
terraform apply tfplan

# Show outputs
terraform output

# Destroy (cleanup)
terraform destroy -var-file="../../configs/terraform/azure_config.tfvars"
```

## Key Configuration Variables

### Azure ExpressRoute
Update these in `configs/terraform/azure_config.tfvars`:

- **`project_name`** - Your project name for resource naming
- **`azure_region`** - Azure region for deployment
- **`expressroute_peering_location`** - Your ExpressRoute peering location
- **`expressroute_service_provider`** - Your service provider (e.g., PacketFabric)
- **`expressroute_bandwidth`** - Circuit bandwidth in Mbps
- **`expressroute_shared_key`** - BGP shared key
- **`expressroute_peer_asn`** - Your ASN

## Security and Best Practices

- **Sensitive files** (`terraform.tfvars`) are automatically ignored by git
- **State files** are excluded from version control
- **Authentication** is required before deployment
- **Validation** is performed before applying changes

## Troubleshooting

### Common Issues

**Azure ExpressRoute:**
1. **Authentication Error**: Run `az login` and verify subscription
2. **Provider Version**: Ensure correct Azure provider version
3. **Resource Quotas**: Check Azure subscription limits
4. **Network Conflicts**: Verify IP address ranges

### Useful Commands

**Azure:**
```bash
# Check Terraform version
terraform version

# Check Azure CLI authentication
az account show

# List available peering locations
az network express-route list-service-providers

# Check resource group permissions
az role assignment list --assignee $(az account show --query user.name -o tsv)
```

## Cleanup

### Azure ExpressRoute
To destroy all Azure Terraform-managed resources:
```bash
cd terraform/azure-expressroute
terraform destroy -var-file="../../configs/terraform/azure_config.tfvars"
```

**⚠️ Warning**: These commands will permanently delete all created resources!

## Additional Resources

- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure ExpressRoute Documentation](https://docs.microsoft.com/en-us/azure/expressroute/)
- [Graphiant Playbooks Main Documentation](../README.md)
