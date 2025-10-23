# Graphiant Playbooks

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Graphiant SDK](https://img.shields.io/badge/Graphiant%20SDK-25.6.2+-green.svg)](https://pypi.org/project/graphiant-sdk/)

> **Automated network infrastructure management for Graphiant NaaS**

Graphiant Playbooks is a comprehensive automation framework for managing Graphiant Edge Devices and network infrastructure. Built with Python and Jinja2 templates, it provides a powerful toolkit for network configuration, infrastructure provisioning, and device management.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Terraform Infrastructure](#terraform-infrastructure)
- [Docker Support](#docker-support)
- [CI/CD Pipelines](#cicd-pipelines)
- [Cloud-Init Generator](#cloud-init-generator)
- [API Reference](#api-reference)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

Graphiant Playbooks streamlines network infrastructure management through:

- **Automated Configuration**: Deploy and manage network configurations across multiple devices
- **Infrastructure as Code**: Terraform modules for Azure ExpressRoute and AWS Direct Connect
- **Template-Based Management**: Jinja2 templates for consistent configuration deployment
- **Multi-Cloud Support**: Native integration with Azure and AWS cloud services
- **Device Onboarding**: Cloud-init generator for automated device provisioning
- **CI/CD Integration**: Built-in pipelines for automated testing and deployment

## ✨ Features

### Core Capabilities
- **Edge Device Management**: Configure interfaces, BGP peering, and global objects
- **Multi-Device Operations**: Apply configurations across multiple devices simultaneously
- **Template Engine**: Jinja2-based configuration templates with dynamic rendering
- **API Integration**: Full Graphiant SDK integration for seamless API interactions

### Infrastructure Management
- **Azure ExpressRoute**: Automated ExpressRoute circuit and gateway provisioning
- **AWS Direct Connect**: Direct Connect connection and gateway management
- **Terraform Modules**: Production-ready Infrastructure as Code templates
- **Cloud Integration**: Seamless integration with cloud networking services

### Development & Operations
- **Docker Support**: Containerized environment for consistent deployments
- **CI/CD Pipelines**: Automated testing, linting, and deployment workflows
- **Cloud-Init Generator**: Interactive tool for device onboarding configuration
- **Comprehensive Testing**: Unit tests and validation frameworks

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/graphiant/graphiant-playbooks.git
cd graphiant-playbooks
```

### 2. Install Dependencies
```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Authentication
```bash
# Edit test configuration
nano test/test.ini

[credentials]
username = your_username
password = your_password
[host]
url = https://api.graphiant.com
```

### 4. Run Basic Test
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 test/test.py
```

### 5. Start Using Playbooks
```python
from libs.edge import Edge

# Initialize Edge manager
edge = Edge(
    base_url="https://api.graphiant.com",
    username="your_username", 
    password="your_password"
)

# Configure interfaces
edge.interfaces.configure_lan_interfaces("configs/sample_interface_config.yaml")
``` 

## 📁 Directory Structure

```
graphiant-playbooks/
├── 📄 LICENSE                    # MIT License
├── 📄 README.md                  # This documentation
├── 📄 requirements.txt           # Python dependencies
├── 📄 setup.cfg                  # Python package configuration
├── 🐳 Dockerfile                 # Docker container configuration
├── 📁 configs/                   # Configuration files
│   ├── sample_*.yaml            # Sample configuration templates
│   └── terraform/               # Terraform variable files
│       ├── azure_config.tfvars  # Azure configuration
│       └── aws_config.tfvars    # AWS configuration
├── 📁 libs/                      # Core Python libraries
│   ├── __init__.py              # Package initialization
│   ├── edge.py                  # Main Edge management class
│   ├── gcsdk_client.py          # Graphiant SDK client wrapper
│   ├── base_manager.py          # Base manager class
│   ├── bgp_manager.py           # BGP configuration management
│   ├── interface_manager.py     # Interface configuration management
│   ├── global_config_manager.py # Global object management
│   ├── site_manager.py          # Site attachment management
│   ├── edge_utils.py            # Utility functions
│   ├── edge_templates.py        # Template rendering utilities
│   ├── portal_utils.py          # Portal integration utilities
│   ├── vpn_mappings.py          # VPN configuration mappings
│   ├── poller.py                # Async operation polling
│   ├── logger.py                # Logging configuration
│   └── exceptions.py            # Custom exceptions
├── 📁 templates/                 # Jinja2 configuration templates
│   ├── interface_template.yaml           # Interface configuration template
│   ├── circuit_template.yaml            # Circuit configuration template
│   ├── bgp_peering_template.yaml        # BGP peering template
│   ├── global_*_template.yaml           # Global object templates
│   └── ...
├── 📁 terraform/                 # Infrastructure as Code
│   ├── azure-expressroute/      # Azure ExpressRoute modules
│   │   ├── main.tf             # Main Terraform configuration
│   │   ├── variables.tf        # Variable definitions
│   │   └── outputs.tf          # Output values
│   └── aws-directconnect/       # AWS Direct Connect modules
│       ├── main.tf             # Main Terraform configuration
│       ├── variables.tf        # Variable definitions
│       └── outputs.tf          # Output values
├── 📁 scripts/                   # Standalone utilities
│   └── cloud-init-generator/    # Device onboarding tool
│       ├── generate-cloud-init.sh  # Interactive cloud-init generator
│       └── README.md               # Generator documentation
├── 📁 pipelines/                 # CI/CD pipeline definitions
│   ├── docker.yml              # Docker build pipeline
│   ├── lint.yml                # Code quality pipeline
│   └── run.yml                 # Test execution pipeline
└── 📁 test/                      # Testing framework
    ├── test.py                 # Main test suite
    └── test.ini                # Test configuration
```

### 📂 Directory Descriptions

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| **`configs/`** | Input configuration files | `sample_*.yaml`, `terraform/*.tfvars` |
| **`libs/`** | Core Python libraries | `edge.py`, `*_manager.py`, `gcsdk_client.py` |
| **`templates/`** | Jinja2 configuration templates | `*_template.yaml` |
| **`terraform/`** | Infrastructure as Code | `azure-expressroute/`, `aws-directconnect/` |
| **`scripts/`** | Standalone utilities | `cloud-init-generator/` |
| **`pipelines/`** | CI/CD definitions | `docker.yml`, `lint.yml`, `run.yml` |
| **`test/`** | Testing framework | `test.py`, `test.ini` |

## 📋 Prerequisites

### Required Software

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Python** | 3.12+ | Core runtime | [Download](https://www.python.org/downloads/) |
| **Terraform** | 1.1.0+ | Infrastructure as Code | [Installation Guide](#terraform-installation) |
| **Azure CLI** | Latest | Azure resource management | [Installation Guide](#azure-cli-installation) |
| **AWS CLI** | Latest | AWS resource management | [Installation Guide](#aws-cli-installation) |

### Python Installation

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.12

# Or download from python.org
```

#### Windows
```bash
# Using Chocolatey
choco install python --version=3.12.0

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
# Add deadsnakes PPA for latest Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

### Terraform Installation

#### macOS
```bash
# Using Homebrew
brew install terraform

# Verify installation
terraform version
```

#### Windows
```bash
# Using Chocolatey
choco install terraform

# Or download from https://www.terraform.io/downloads
```

#### Linux (Ubuntu/Debian)
```bash
# Add HashiCorp GPG key
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -

# Add repository
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

# Install Terraform
sudo apt-get update && sudo apt-get install terraform
```

### Azure CLI Installation

#### macOS
```bash
# Using Homebrew
brew install azure-cli

# Verify installation
az version
```

#### Windows
```bash
# Using Chocolatey
choco install azure-cli

# Or download from Microsoft
```

#### Linux (Ubuntu/Debian)
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify installation
az version
```

### AWS CLI Installation

#### macOS
```bash
# Using Homebrew
brew install awscli

# Verify installation
aws --version
```

#### Windows
```bash
# Using Chocolatey
choco install awscli

# Or download from AWS
```

#### Linux (Ubuntu/Debian)
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

### Cloud Authentication

#### Azure Authentication
```bash
# Login to Azure
az login

# Set subscription (if multiple)
az account set --subscription "your-subscription-id"

# Verify authentication
az account show
```


### Verification

```bash
# Check all installations
python3 --version    # Should show Python 3.12+
terraform version    # Should show Terraform 1.1.0+
az version          # Should show Azure CLI
```

## 🐳 Docker Support

Graphiant Playbooks includes Docker support for consistent development and deployment environments.

### Building the Docker Image

```bash
# Build the Docker image
docker build -t graphiant-playbooks .

# Build with specific commit SHA
docker build --build-arg COMMIT_SHA=$(git rev-parse HEAD) -t graphiant-playbooks .
```

### Running with Docker

```bash
# Run interactive container
docker run -it graphiant-playbooks

# Run with volume mount for development
docker run -it -v $(pwd):/home/graphiant-playbooks graphiant-playbooks

# Run with environment variables
docker run -it -e GRAPHIANT_API_URL=https://api.graphiant.com graphiant-playbooks
```

### Docker Features

- **Multi-stage build** for optimized image size
- **Python 3.11.5** runtime environment
- **Pre-installed dependencies** from requirements.txt
- **Development tools** (vim, git, sshpass)
- **Version tracking** via COMMIT_SHA build arg

## 🔄 CI/CD Pipelines

The project includes pre-configured CI/CD pipelines for automated testing and deployment.

### Pipeline Structure

| Pipeline | Purpose | Triggers |
|----------|---------|----------|
| **`docker.yml`** | Docker image build and push | Push to main branch |
| **`lint.yml`** | Code quality checks | Pull requests |
| **`run.yml`** | Test execution | Pull requests, pushes |

### Pipeline Features

- **Automated Testing**: Runs test suite on every PR
- **Code Quality**: Flake8 and Pylint checks
- **Template Validation**: Jinja2 template linting
- **Docker Builds**: Automated container image creation
- **Multi-Environment**: Support for different deployment targets

### Local Pipeline Testing

```bash
# Run linting checks locally
flake8 ./libs ./test
pylint --errors-only ./libs
djlint configs -e yaml
djlint templates -e yaml

# Run tests
python3 test/test.py
```

## ☁️ Cloud-Init Generator

The cloud-init generator is an interactive tool for creating device onboarding configurations.

### Features

- **Interactive Configuration**: Step-by-step parameter collection
- **Multiple Environments**: Support for production and test environments
- **Flexible Networking**: DHCP or static IP configuration
- **Custom Interfaces**: Configurable management and WAN interfaces
- **Onboarding Tokens**: Optional token inclusion for secure onboarding
- **Multiple Output Formats**: ISO, QCOW2, and other cloud image formats

### Usage

```bash
# Navigate to the generator
cd scripts/cloud-init-generator

# Make executable
chmod +x generate-cloud-init.sh

# Run the generator
./generate-cloud-init.sh
```

### Example Configuration

The generator will prompt for:

1. **Environment**: `prod` or `test`
2. **Device Role**: `cpe`, `gateway`, or `core`
3. **Onboarding Token**: Optional secure token
4. **Management Interface**: Default or custom interface name
5. **WAN Interface**: Default or custom interface name
6. **Network Configuration**: DHCP or static IP settings
7. **DNS Servers**: Custom or default DNS configuration
8. **Web Server Password**: Local management password
9. **Hostname**: Custom device hostname
10. **Output Format**: ISO, QCOW2, or other formats

### Output

The generator creates a cloud-init configuration with:
- **User Data**: Device configuration and networking setup
- **Meta Data**: Instance metadata and device identification
- **Cloud Image**: Ready-to-deploy image file

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/graphiant/graphiant-playbooks.git
cd graphiant-playbooks
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### 4. Configure Authentication
```bash
# Edit test configuration
nano test/test.ini

# Add your credentials
[credentials]
username = your_username
password = your_password
[host]
url = https://api.graphiant.com
```

### 5. Run Basic Tests
```bash
# Run sanity tests
python3 test/test.py

# Enable specific tests in test.py if needed
# suite.addTest(TestGraphiantPlaybooks('test_get_enterprise_id'))
```

## 🚀 Getting Started

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

#### Global Config SNMP System Objects
```sh
# Configure global SNMP services
edge.global_config.configure("sample_global_snmp_services.yaml")

# Deconfigure global SNMP services
edge.global_config.deconfigure("sample_global_snmp_services.yaml")
```

#### Global Config Syslog System Objects
```sh
# Configure global syslog services
edge.global_config.configure("sample_global_syslog_servers.yaml")

# Deconfigure global syslog services
edge.global_config.deconfigure("sample_global_syslog_servers.yaml")
```

#### Global Config IPFIX System Objects
```sh
# Configure global IPFIX services
edge.global_config.configure("sample_global_ipfix_exporters.yaml")

# Deconfigure global IPFIX services
edge.global_config.deconfigure("sample_global_ipfix_exporters.yaml")
```

#### Global Config VPN Profiles
```sh
# Configure global VPN profiles
edge.global_config.configure("sample_global_vpn_profiles.yaml")

# Deconfigure global VPN profiles
edge.global_config.deconfigure("sample_global_vpn_profiles.yaml")
```

### Step 5: BGP Peering Neighbors Configurations

#### Configure BGP Peering and Attach Global Config BGP Filters
```sh
# Configure BGP peering neighbors
edge.bgp.configure("sample_bgp_peering.yaml")
```

#### Detach Global Config BGP Filters from BGP Peers
```sh
# Detach policies from BGP peers
edge.bgp.detach_policies("sample_bgp_peering.yaml")
```

#### Deconfigure BGP Peering
```sh
# Deconfigure BGP peering neighbors
edge.bgp.deconfigure("sample_bgp_peering.yaml")
```

### Step 6: Attaching System Objects to and from Sites

#### Attach Global System Objects to Sites
```sh
edge.sites.manage_global_system_objects_on_site("sample_site_attachments.yaml", "attach")
```

#### Detach Global System Objects from Sites
```sh
edge.sites.manage_global_system_objects_on_site("sample_site_attachments.yaml", "detach")
```

**Configuration Format:**
The `sample_site_attachments.yaml` uses a simple, user-friendly format:
```yaml
site_attachments:
  - San Jose-sdktest:
      syslogServers:
        - syslog-global-test
      snmpServers:
        - snmp-global-test-noauth
      ipfixExporters:
        - ipfix-global-test
```

**Note:** Just specify the object names in simple lists. The system automatically converts them to the proper API format with "Attach" or "Detach" operations based on the function parameter.

## 📚 API Reference

### Core Classes

#### `Edge` Class
The main entry point for all Graphiant Playbooks operations.

```python
from libs.edge import Edge

# Initialize Edge manager
edge = Edge(
    base_url="https://api.graphiant.com",
    username="your_username",
    password="your_password"
)
```

#### Manager Classes

| Manager | Purpose | Key Methods |
|---------|---------|-------------|
| **`InterfaceManager`** | Interface configuration | `configure_lan_interfaces()`, `configure_wan_circuits_interfaces()` |
| **`BGPManager`** | BGP peering management | `configure()`, `detach_policies()`, `deconfigure()` |
| **`GlobalConfigManager`** | Global object management | `configure()`, `deconfigure()` |
| **`SiteManager`** | Site attachment management | `manage_global_system_objects_on_site()` |

### Interface Management

#### LAN Interface Configuration
```python
# Configure LAN interfaces
edge.interfaces.configure_lan_interfaces("configs/sample_interface_config.yaml")

# Deconfigure LAN interfaces
edge.interfaces.deconfigure_lan_interfaces("configs/sample_interface_config.yaml")
```

#### WAN Interface Configuration
```python
# Configure WAN circuits and interfaces
edge.interfaces.configure_wan_circuits_interfaces(
    circuit_config_file="configs/sample_circuit_config.yaml",
    interface_config_file="configs/sample_interface_config.yaml"
)

# Configure circuits only
edge.interfaces.configure_circuits(
    circuit_config_file="configs/sample_circuit_config.yaml",
    interface_config_file="configs/sample_interface_config.yaml"
)

# Deconfigure circuits (removes static routes)
edge.interfaces.deconfigure_circuits(
    interface_config_file="configs/sample_interface_config.yaml",
    circuit_config_file="configs/sample_circuit_config.yaml"
)
```

#### Complete Interface Management
```python
# Configure all interfaces in one operation
edge.interfaces.configure_interfaces(
    interface_config_file="configs/sample_interface_config.yaml",
    circuit_config_file="configs/sample_circuit_config.yaml"
)

# Deconfigure all interfaces
edge.interfaces.deconfigure_interfaces(
    interface_config_file="configs/sample_interface_config.yaml",
    circuit_config_file="configs/sample_circuit_config.yaml"
)
```

### Global Object Management

#### Prefix Lists
```python
# Configure global prefix sets
edge.global_config.configure("configs/sample_global_prefix_lists.yaml")

# Deconfigure global prefix sets
edge.global_config.deconfigure("configs/sample_global_prefix_lists.yaml")
```

#### BGP Filters
```python
# Configure global BGP filters
edge.global_config.configure("configs/sample_global_bgp_filters.yaml")

# Deconfigure global BGP filters
edge.global_config.deconfigure("configs/sample_global_bgp_filters.yaml")
```

#### System Objects
```python
# SNMP Services
edge.global_config.configure("configs/sample_global_snmp_services.yaml")

# Syslog Servers
edge.global_config.configure("configs/sample_global_syslog_servers.yaml")

# IPFIX Exporters
edge.global_config.configure("configs/sample_global_ipfix_exporters.yaml")

# VPN Profiles
edge.global_config.configure("configs/sample_global_vpn_profiles.yaml")
```

### BGP Peering Management

```python
# Configure BGP peering neighbors
edge.bgp.configure("configs/sample_bgp_peering.yaml")

# Detach policies from BGP peers
edge.bgp.detach_policies("configs/sample_bgp_peering.yaml")

# Deconfigure BGP peering
edge.bgp.deconfigure("configs/sample_bgp_peering.yaml")
```

### Site Management

```python
# Attach global system objects to sites
edge.sites.manage_global_system_objects_on_site(
    "configs/sample_site_attachments.yaml", 
    "attach"
)

# Detach global system objects from sites
edge.sites.manage_global_system_objects_on_site(
    "configs/sample_site_attachments.yaml", 
    "detach"
)
```

### Utility Functions

#### Enterprise Operations
```python
# Get enterprise ID
enterprise_id = edge.edge_utils.get_enterprise_id()

# Get all LAN segments
lan_segments = edge.edge_utils.get_all_lan_segments()
```

#### Template Rendering
```python
# Render configuration templates
from libs.edge_templates import render_template

rendered_config = render_template(
    template_file="templates/interface_template.yaml",
    config_data=config_dict
)
```

### Error Handling

```python
from libs.exceptions import GraphiantPlaybooksError

try:
    edge.interfaces.configure_lan_interfaces("config.yaml")
except GraphiantPlaybooksError as e:
    print(f"Configuration failed: {e}")
```

### Logging

```python
from libs.logger import setup_logger

# Setup logging
logger = setup_logger()
logger.info("Starting configuration process")
```

## 🏗️ Terraform Infrastructure as Code

Graphiant Playbooks includes production-ready Terraform modules for deploying cloud networking infrastructure that seamlessly integrates with Graphiant Edge devices.

### 🎯 What Terraform Creates

#### Azure ExpressRoute Infrastructure
- **Resource Group**: Container for all Azure resources
- **Virtual Network**: Network infrastructure with subnets
- **ExpressRoute Circuit**: Primary and secondary circuits for redundancy
- **ExpressRoute Gateway**: Gateway for connecting to ExpressRoute
- **Virtual Hub**: Central networking hub (optional)
- **BGP Peering**: Border Gateway Protocol configuration
- **ExpressRoute Connection**: Connection between Gateway and Circuit


### 📁 Terraform Directory Structure

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

### 🔧 Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Terraform CLI** | >= 1.1.0 | Infrastructure provisioning |
| **Azure CLI** | Latest | Azure authentication and management |
| **Cloud Account** | Active | Azure subscription |
| **Permissions** | Required | Resource creation and management rights |

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


### Cleanup

#### Azure ExpressRoute
To destroy all Azure Terraform-managed resources:
```bash
cd terraform/azure-expressroute
terraform destroy -var-file="../../configs/terraform/azure_config.tfvars"
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

## 🛠️ Development

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/graphiant/graphiant-playbooks.git
cd graphiant-playbooks

# Create development environment
python3.12 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Set up PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Code Quality Standards

#### Linting Tools
- **Flake8**: Code style and error detection
- **Pylint**: Advanced code analysis and error detection
- **djlint**: Jinja2 template linting

#### Running Linters
```bash
# Run all linting checks
flake8 ./libs ./test
pylint --errors-only ./libs
djlint configs -e yaml
djlint templates -e yaml

# Run pre-commit hooks
pre-commit run --all-files
```

#### IDE Integration
- **PyCharm**: [Pylint Plugin](https://plugins.jetbrains.com/plugin/11084-pylint), [Flake8 Support](https://plugins.jetbrains.com/plugin/11563-flake8-support)
- **VS Code**: [Flake8 Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8), [Pylint Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)

### Testing

#### Running Tests
```bash
# Run all tests
python3 test/test.py

# Run specific test
python3 -m unittest test.test.TestGraphiantPlaybooks.test_get_enterprise_id
```

#### Test Configuration
Update `test/test.ini` with your credentials:
```ini
[credentials]
username = your_username
password = your_password
[host]
url = https://api.graphiant.com
```

### Adding New Features

#### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

#### 2. Implement Changes
- Follow existing code patterns
- Add appropriate error handling
- Include logging statements
- Update documentation

#### 3. Add Tests
- Create test cases for new functionality
- Ensure existing tests still pass
- Add integration tests if applicable

#### 4. Code Review
- Run linting tools
- Ensure all tests pass
- Update documentation
- Create pull request

### Documentation Standards

#### Code Documentation
- Use docstrings for all public methods
- Follow Google docstring format
- Include type hints for parameters and return values

#### README Updates
- Update relevant sections when adding features
- Include usage examples
- Update API reference if applicable

### Release Process

#### Version Management
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update version in relevant files
- Create release notes

#### Docker Images
- Docker images are automatically built on main branch pushes
- Images are tagged with commit SHA and version tags

## 🤝 Contributing

We welcome contributions to Graphiant Playbooks! Here's how you can help:

### Ways to Contribute

1. **Bug Reports**: Report issues and bugs
2. **Feature Requests**: Suggest new features and improvements
3. **Code Contributions**: Submit pull requests with fixes or features
4. **Documentation**: Improve documentation and examples
5. **Testing**: Add test cases and improve test coverage

### Contribution Guidelines

#### Before Contributing
1. Check existing issues and pull requests
2. Fork the repository
3. Create a feature branch
4. Set up development environment

#### Pull Request Process
1. **Code Quality**: Ensure all linting checks pass
2. **Testing**: Add tests for new functionality
3. **Documentation**: Update relevant documentation
4. **Commit Messages**: Use clear, descriptive commit messages
5. **Pull Request**: Provide detailed description of changes

#### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Include docstrings for all public methods
- Write comprehensive tests
- Update documentation as needed

### Issue Reporting

When reporting issues, please include:
- **Environment**: Python version, OS, dependencies
- **Steps to Reproduce**: Clear steps to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Logs**: Relevant error messages and logs

### Getting Help

- **Documentation**: Check this README and inline documentation
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Support**: Contact Graphiant support for enterprise issues

## 📞 Support

### Community Support
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community help
- **Documentation**: Comprehensive guides and API reference

### Enterprise Support
- **Graphiant Support**: [support@graphiant.com](mailto:support@graphiant.com)
- **Documentation Portal**: [docs.graphiant.com](https://docs.graphiant.com/)
- **Graphiant Website**: [graphiant.com](https://www.graphiant.com/)

### Resources
- **Graphiant SDK**: [PyPI Package](https://pypi.org/project/graphiant-sdk/)
- **API Documentation**: [Graphiant API Docs](https://docs.graphiant.com/docs/api)
- **Automation Guide**: [Graphiant Playbooks User Guide](https://docs.graphiant.com/docs/graphiant-playbooks)

---

**Made with ❤️ by the Graphiant Team**
