# Graphiant Playbooks Terraform Infrastructure as Code

Graphiant Playbooks includes production-ready Terraform modules for deploying cloud networking infrastructure that seamlessly integrates with Graphiant Edge and Gateway devices.

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

terraform/configs/
├── azure_config.tfvars           # Azure variable configuration
├── aws_config.tfvars             # AWS variable configuration
```

## 🔧 Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.12+ | Core runtime for Graphiant SDK |
| **Terraform CLI** | >= 1.1.0 | Infrastructure provisioning |
| **Azure CLI** | Latest | Azure authentication and management |
| **AWS CLI** | Latest | AWS resource management (for future AWS modules) |
| **Cloud Account** | Active | Azure subscription |
| **Permissions** | Required | Resource creation and management rights |

## Python Installation

### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.12

# Or download from python.org
```

### Windows
```bash
# Using Chocolatey
choco install python --version=3.12.0

# Or download from python.org
```

### Linux (Ubuntu/Debian)
```bash
# Add deadsnakes PPA for latest Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

## Terraform Installation

### macOS
```bash
# Using Homebrew
brew install terraform

# Verify installation
terraform version
```

### Windows
```bash
# Using Chocolatey
choco install terraform

# Or download from https://www.terraform.io/downloads
```

### Linux (Ubuntu/Debian)
```bash
# Add HashiCorp GPG key
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -

# Add repository
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

# Install Terraform
sudo apt-get update && sudo apt-get install terraform
```

## Azure CLI Installation

### macOS
```bash
# Using Homebrew
brew install azure-cli

# Verify installation
az version
```

### Windows
```bash
# Using Chocolatey
choco install azure-cli

# Or download from Microsoft
```

### Linux (Ubuntu/Debian)
```bash
# Install azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify installation
az version
```

## AWS CLI Installation

### macOS
```bash
# Using Homebrew
brew install awscli

# Verify installation
aws --version
```

### Windows
```bash
# Using Chocolatey
choco install awscli

# Or download from aws
```

### Linux (Ubuntu/Debian)
```bash
# Install aws CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

## Cloud Authentication

### Azure Authentication
```bash
# Login to azure
az login

# Set subscription (if multiple)
az account set --subscription "your-subscription-id"

# Verify authentication
az account show
```

### AWS Authentication
```bash
# Configure aws credentials
aws configure

# Or use environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"

# Verify authentication
aws sts get-caller-identity
```

### Verification

```bash
# Check all installations
python3 --version    # Should show Python 3.12+
terraform version    # Should show Terraform 1.1.0+
az version          # Should show azure CLI
aws --version       # Should show aws CLI
```

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
nano terraform/configs/azure_config.tfvars

# Or copy and modify if needed
cp terraform/configs/azure_config.tfvars terraform/configs/my-azure-config.tfvars
```

#### 3. Deploy Infrastructure
```bash
cd terraform/azure-expressroute

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Create and review plan
terraform plan -var-file="../../terraform/configs/azure_config.tfvars" -out=tfplan

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
from libs.graphiant_config import GraphiantConfig

# Initialize Graphiant Edge
graphiant_config = GraphiantConfig(base_url='https://api.graphiant.com', username='user', password='pass')

# Get Terraform outputs for circuit information
# Use these values in your BGP peering configuration
graphiant_config.configure_bgp_peers("your_bgp_config.yaml")
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
terraform plan -var-file="../../terraform/configs/azure_config.tfvars" -out=tfplan

# Apply
terraform apply tfplan

# Show outputs
terraform output

# Destroy (cleanup)
terraform destroy -var-file="../../terraform/configs/azure_config.tfvars"
```

## Key Configuration Variables

### Azure ExpressRoute
Update these in `terraform/configs/azure_config.tfvars`:

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

**Python/Graphiant SDK:**
1. **Python Version**: Ensure Python 3.12+ is installed
2. **Virtual Environment**: Use virtual environment for isolation
3. **Dependencies**: Install required packages with `pip install -r requirements.txt`
4. **PYTHONPATH**: Set PYTHONPATH for Graphiant SDK access

### Useful Commands

**Azure:**
```bash
# Check Terraform version
terraform version

# Check azure CLI authentication
az account show

# List available peering locations
az network express-route list-service-providers

# Check resource group permissions
az role assignment list --assignee $(az account show --query user.name -o tsv)
```

**Python/Graphiant:**
```bash
# Check Python version
python3 --version

# Check Graphiant SDK installation
python3 -c "import graphiant_sdk; print('Graphiant SDK installed')"

# Test Graphiant connection
python3 -c "from libs.graphiant_config import GraphiantConfig; print('Graphiant Playbooks ready')"
```

**AWS:**
```bash
# Check aws CLI version
aws --version

# Check aws authentication
aws sts get-caller-identity

# List available regions
aws ec2 describe-regions --query 'Regions[].RegionName'
```

## Cleanup

### Azure ExpressRoute
To destroy all Azure Terraform-managed resources:
```bash
cd terraform/azure-expressroute
terraform destroy -var-file="../../terraform/configs/azure_config.tfvars"
```

**⚠️ Warning**: These commands will permanently delete all created resources!

## Additional Resources

- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure ExpressRoute Documentation](https://docs.microsoft.com/en-us/azure/expressroute/)
- [AWS Direct Connect Documentation](https://docs.aws.amazon.com/directconnect/)
- [Graphiant Playbooks Main Documentation](../README.md)