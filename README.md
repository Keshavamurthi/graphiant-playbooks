# Graphiant-Playbooks

Playbooks for [Graphiant NaaS](https://www.graphiant.com). 

Refer [Graphiant-Playbooks User Guide](https://docs.graphiant.com/docs/graphiant-playbooks) under [Automation Section](https://docs.graphiant.com/docs/automation) in [Graphiant Documentation](https://docs.graphiant.com/) for getting started instructions.

Graphiant Playbooks are a collection of automated scripts that are designed to streamline 
and manage network infrastructure and policies. These playbooks are built using Python and 
Jinja2 templates to create and apply configurations for multiple Graphiant Edge Devices 
concurrently using GCSDK API. 

```sh
graphiant-playbooks/
├── LICENSE               # Project License file
├── README.md             # Project overview/documentation
├── requirements.txt      # Python dependencies
├── configs/              # Input YAML configuration files
├── libs/                 # Python libraries and modules required by the playbooks
├── templates/            # Jinja2 configuration template
├── test/                 # Sample Python test scripts and Config file 
└── scripts/              # Standalone scripts e.g. cloud-init interactive generator 

# configs/
Contains input configuration YAML files used to drive the execution of various playbooks.

# libs/
Includes all necessary Python libraries and helper modules required by the playbooks.

# logs/
Stores all log files generated during execution. Each run creates a timestamped log 
for auditability and debugging purposes.

# templates/
Contains Jinja2 config templates. These templates are dynamically rendered using the 
input from the configs/ directory to produce finalized configuration artifacts.

# test/
Contains Sample Python test files to validate the packages are installed correctly.

# scripts/
Standalone scripts e.g. cloud-init interactive generator.
```

## Pre-requisites

```sh
cd graphiant-playbooks/
```

### 1. Install Python 3.12+

### 2. Install Terraform CLI
```bash
# macOS (using Homebrew)
brew install terraform

# Windows (using Chocolatey)
choco install terraform

# Linux (Ubuntu/Debian)
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs)"
sudo apt-get update && sudo apt-get install terraform

# Or download from https://www.terraform.io/downloads
```

### 3. Install Azure CLI
```bash
# macOS (using Homebrew)
brew install azure-cli

# Windows (using Chocolatey)
choco install azure-cli

# Linux (Ubuntu/Debian)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Or download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

### 4. Authenticate with Azure
```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "your-subscription-id"

# Verify authentication
az account show
```

### 5. Verify Installations
```bash
# Check Terraform version
terraform version

# Check Azure CLI version
az version

# Check Python version
python3 --version
```

### 6. Create and activate python virtual environment
```sh
python3.12 -m venv venv
source venv/bin/activate
```

### 7. Install the Python requirement packages
```sh
pip3 install -r requirements.txt
```

**Note**: Terraform and Azure CLI are **system-level tools** that must be installed separately (see steps 2-4 above). They cannot be installed via `pip` or included in `requirements.txt` as they are not Python packages.

### System Tools vs Python Packages

| Tool | Type | Installation Method | Purpose |
|------|------|-------------------|---------|
| **Terraform** | System Tool | Package manager (brew, choco, apt) | Infrastructure as Code |
| **Azure CLI** | System Tool | Package manager (brew, choco, apt) | Azure resource management |
| **Python packages** | Python Dependencies | pip install -r requirements.txt | Graphiant SDK and utilities |

## Testing virtual environment

### 1. Update the PYTHONPATH env variable
```sh
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### 2. Enter the host URL and credentials under test.ini
```sh
[credentials]
username = username
password = password
[host]
url = https://api.graphiant.com
```

### 3. Enable the sanity test under test/test.py to fetch the enterprise ID
```sh
suite.addTest(TestGraphiantPlaybooks('test_get_enterprise_id'))
```

### 4. Run the sanity test and verify the enterprise ID is fetched
```sh
python3 test/test.py
```

## Getting Started

### Step 1: Define Configurations

All input configs should be placed in the configs/ folder.

- sample_bgp_peering.yaml
- sample_interface_config.yaml
- sample_global_bgp_filters.yaml
- sample_global_snmp_services.yaml
- sample_global_syslog_servers.yaml
- sample_global_ipfix_exporters.yaml
- sample_global_vpn_profiles.yaml
- sample_site_attachments.yaml

Note : Also refer the templates under templates/ dir for more details on the supported arguments.

### Step 2: Import and Use graphiant-playbooks
```sh
from libs.edge import Edge

host = "https://api.graphiant.com"
username = 'username'
password = 'password'
edge = Edge(base_url=host, username=username, password=password)
```
### Step 3: Interface Configuration Methods

#### 1. Configure/Deconfigure LAN Interfaces (Subinterfaces)
```sh
# Configure LAN interfaces
edge.interfaces.configure_lan_interfaces("sample_interface_config.yaml")

# Deconfigure LAN interfaces
edge.interfaces.deconfigure_lan_interfaces("sample_interface_config.yaml")
```

#### 2. Configure/Deconfigure WAN Interfaces (Subinterfaces)
```sh
# Configure WAN circuits and interfaces
edge.interfaces.configure_wan_circuits_interfaces(
    circuit_config_file="sample_circuit_config.yaml",
    interface_config_file="sample_interface_config.yaml"
)

# Configure circuits only (can be called separately after interface is configured)
edge.interfaces.configure_circuits(
    circuit_config_file="sample_circuit_config.yaml",
    interface_config_file="sample_interface_config.yaml"
)

# Deconfigure circuits (removes static routes if any)
edge.interfaces.deconfigure_circuits(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)

# Deconfigure WAN circuits and interfaces
edge.interfaces.deconfigure_wan_circuits_interfaces(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)
```

**Note:** `configure_circuits` can be separately called after interface is configured already just to update circuits configuration (including static routes in the circuits).

**Note:** `deconfigure_circuits` will remove static routes (if any) in the circuit. This is required before deconfiguring WAN interfaces.

#### 3. Configure All Interfaces in One Single Config Push
```sh
edge.interfaces.configure_interfaces(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)
```

#### 4. Deconfigure All Interfaces (Reset parent interface to default LAN and delete subinterfaces)
```sh
edge.interfaces.deconfigure_interfaces(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)
```

**Note:** `deconfigure_circuits` might be required before running `deconfigure_interfaces` so that static routes are deconfigured before deconfiguring WAN interfaces.

### Step 4: Global Object Configurations

#### Global Config Prefix Lists
```sh
# Configure global prefix sets
edge.global_config.configure("sample_global_prefix_lists.yaml")

# Deconfigure global prefix sets
edge.global_config.deconfigure("sample_global_prefix_lists.yaml")
```

#### Global Config BGP Filters
```sh
# Configure global BGP filters
edge.global_config.configure("sample_global_bgp_filters.yaml")

# Deconfigure global BGP filters
edge.global_config.deconfigure("sample_global_bgp_filters.yaml")
```

## Terraform Infrastructure as Code

This project includes Terraform configurations for deploying cloud networking infrastructure (Azure ExpressRoute and AWS Direct Connect) that integrates with Graphiant Edge devices.

### Terraform Directory Structure
```
terraform/
├── azure-expressroute/           # Azure ExpressRoute infrastructure
│   ├── main.tf                   # Main Terraform configuration
│   ├── variables.tf              # Variable definitions
│   ├── outputs.tf                # Output values
│   └── README.md                 # Azure-specific documentation
└── aws-directconnect/            # AWS Direct Connect infrastructure
    ├── main.tf                   # Main Terraform configuration
    ├── variables.tf              # Variable definitions
    ├── outputs.tf                # Output values
    └── README.md                 # AWS-specific documentation

configs/
└── terraform/
    ├── azure_config.tfvars       # Azure Terraform variable configuration
    └── aws_config.tfvars         # AWS Terraform variable configuration
```

### Prerequisites for Terraform

1. **Terraform CLI** (>= 1.1.0)
2. **Cloud Provider CLI** with authentication:
   - **Azure CLI** for Azure ExpressRoute
   - **AWS CLI** for AWS Direct Connect
3. **Cloud Subscription/Account** with appropriate permissions

### Quick Start with Terraform

#### Azure ExpressRoute Setup

##### 1. Authenticate with Azure
```bash
az login
az account set --subscription "your-subscription-id"
```

##### 2. Configure Variables
```bash
# Edit the configuration file
nano configs/terraform/azure_config.tfvars

# Or copy and modify if needed
cp configs/terraform/azure_config.tfvars configs/terraform/my-azure-config.tfvars
```

##### 3. Deploy Infrastructure
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

#### AWS Direct Connect Setup

##### 1. Authenticate with AWS
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, region, and output format
```

##### 2. Configure Variables
```bash
# Edit the configuration file
nano configs/terraform/aws_config.tfvars

# Or copy and modify if needed
cp configs/terraform/aws_config.tfvars configs/terraform/my-aws-config.tfvars
```

##### 3. Deploy Infrastructure
```bash
cd terraform/aws-directconnect

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Create and review plan
terraform plan -var-file="../../configs/terraform/aws_config.tfvars" -out=tfplan

# Apply the configuration
terraform apply tfplan
```

### What Terraform Creates

#### Azure ExpressRoute Infrastructure
The Azure Terraform configuration deploys:

- **Resource Group** - Container for all resources
- **Virtual Network** - Network infrastructure with subnets
- **ExpressRoute Circuit** - Primary and secondary circuits for redundancy
- **ExpressRoute Gateway** - Gateway for connecting to ExpressRoute
- **Virtual Hub** - Central networking hub (if enabled)
- **BGP Peering** - Border Gateway Protocol configuration
- **ExpressRoute Connection** - Connection between Gateway and Circuit (conditional)

**Note**: The ExpressRoute Connection is only created after the service provider provisions the physical circuit. This prevents deployment failures while waiting for service provider provisioning.

#### AWS Direct Connect Infrastructure
The AWS Terraform configuration deploys:

- **VPC** - Virtual Private Cloud with public and private subnets
- **Direct Connect Connection** - Dedicated network connection to AWS
- **Direct Connect Gateway** - Gateway for routing between VPCs
- **VPN Gateway** - Backup connectivity option
- **NAT Gateway** - Network Address Translation for private subnets
- **Security Groups** - Network security rules
- **Route Tables** - Network routing configuration

**Note**: The physical Direct Connect connection requires coordination with a Direct Connect partner (e.g., Equinix) to provision the actual network link.

### Integration with Graphiant Playbooks

After deploying the ExpressRoute infrastructure with Terraform, you can use the outputs to configure BGP peering with your Graphiant edge devices:

```python
from libs.edge import Edge

# Initialize Graphiant Edge
edge = Edge(base_url='https://api.graphiant.com', username='user', password='pass')

# Get Terraform outputs for circuit information
# Use these values in your BGP peering configuration
edge.configure_bgp_peers("your_bgp_config.yaml")
```

### Terraform Commands

#### Azure ExpressRoute
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

#### AWS Direct Connect
```bash
cd terraform/aws-directconnect

# Initialize
terraform init

# Validate
terraform validate

# Plan
terraform plan -var-file="../../configs/terraform/aws_config.tfvars" -out=tfplan

# Apply
terraform apply tfplan

# Show outputs
terraform output

# Destroy (cleanup)
terraform destroy -var-file="../../configs/terraform/aws_config.tfvars"
```

### Key Configuration Variables

#### Azure ExpressRoute
Update these in `configs/terraform/azure_config.tfvars`:

- **`project_name`** - Your project name for resource naming
- **`azure_region`** - Azure region for deployment
- **`expressroute_peering_location`** - Your ExpressRoute peering location
- **`expressroute_service_provider`** - Your service provider (e.g., PacketFabric)
- **`expressroute_bandwidth`** - Circuit bandwidth in Mbps
- **`expressroute_shared_key`** - BGP shared key
- **`expressroute_peer_asn`** - Your ASN

#### AWS Direct Connect
Update these in `configs/terraform/aws_config.tfvars`:

- **`project_name`** - Your project name for resource naming
- **`aws_region`** - AWS region for deployment
- **`dx_location`** - Direct Connect location (e.g., EqDC2 for Equinix DC2)
- **`dx_bandwidth`** - Connection bandwidth (1Gbps, 10Gbps)
- **`dx_gateway_asn`** - ASN for Direct Connect Gateway
- **`customer_asn`** - Your ASN for BGP peering

### Security and Best Practices

- **Sensitive files** (`terraform.tfvars`) are automatically ignored by git
- **State files** are excluded from version control
- **Authentication** is required before deployment
- **Validation** is performed before applying changes

### Troubleshooting

#### Common Issues

**Azure ExpressRoute:**
1. **Authentication Error**: Run `az login` and verify subscription
2. **Provider Version**: Ensure correct Azure provider version
3. **Resource Quotas**: Check Azure subscription limits
4. **Network Conflicts**: Verify IP address ranges

**AWS Direct Connect:**
1. **Authentication Error**: Run `aws configure` and verify credentials
2. **Provider Version**: Ensure correct AWS provider version
3. **Resource Limits**: Check AWS account limits
4. **Location Availability**: Verify Direct Connect location availability

#### Useful Commands

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

**AWS:**
```bash
# Check Terraform version
terraform version

# Check AWS CLI authentication
aws sts get-caller-identity

# List available Direct Connect locations
aws directconnect describe-locations

# Check Direct Connect connections
aws directconnect describe-connections
```

### Cleanup

#### Azure ExpressRoute
To destroy all Azure Terraform-managed resources:
```bash
cd terraform/azure-expressroute
terraform destroy -var-file="../../configs/terraform/azure_config.tfvars"
```

#### AWS Direct Connect
To destroy all AWS Terraform-managed resources:
```bash
cd terraform/aws-directconnect
terraform destroy -var-file="../../configs/terraform/aws_config.tfvars"
```

**⚠️ Warning**: These commands will permanently delete all created resources!

## Source code linter checks
Error linters point out syntax errors or other code that will result in unhandled exceptions and crashes. (pylint, flake8)
Style linters point out issues that don't cause bugs but make the code less readable or are not in line with style guides such as Python's PEP 8. (pylint, flake8)

flake8
```
flake8 ./libs
flake8 ./test
```

pylint
```
pylint --errors-only ./libs
```

jinjalint
```
djlint configs -e yaml
djlint templates -e yaml
```

Most modern IDE also have excellent support for python linting tools. For example:

- https://plugins.jetbrains.com/plugin/11084-pylint
- https://plugins.jetbrains.com/plugin/11563-flake8-support

- https://marketplace.visualstudio.com/items?itemName=ms-python.flake8
- https://marketplace.visualstudio.com/items?itemName=ms-python.pylint

## Pre-commit checks
[pre-commit](https://pre-commit.com/) can be used to install/manage git hooks that will run these linting checks before committing.
``` shell
pre-commit install
```
