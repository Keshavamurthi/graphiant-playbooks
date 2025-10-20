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
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Development](#development)
- [Contributing](#contributing)
- [Support](#support)

### 📚 Additional Documentation
- [🐳 Docker Support](Docker.md) - Docker setup and usage
- [🏗️ Terraform Infrastructure](terraform/README.md) - Infrastructure as Code with cloud authentication
- [🔄 CI/CD Pipelines](pipelines/README.md) - CI/CD configuration
- [☁️ Cloud-Init Generator](scripts/cloud-init-generator/README.md) - Device onboarding
- [📦 Ansible Collection](ansible_collection/graphiant/graphiant_playbooks/README.md) - Ansible automation

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
from libs.graphiant_config import GraphiantConfig

# Initialize Edge manager
graphiant_config = GraphiantConfig(
    base_url="https://api.graphiant.com",
    username="your_username", 
    password="your_password"
)

# Configure interfaces
graphiant_config.interfaces.configure_lan_interfaces("sample_interface_config.yaml")
``` 

## 📁 Directory Structure

```
graphiant-playbooks/
├── 📄 LICENSE                    # MIT License
├── 📄 README.md                  # Main documentation
├── 📄 Docker.md                  # Docker documentation
├── 📄 requirements.txt           # Python dependencies
├── 📄 setup.cfg                  # Python package configuration
├── 🐳 Dockerfile                 # Docker container configuration
├── 📁 configs/                   # Configuration files
│   ├── sample_*.yaml            # Sample configuration templates
│   └── terraform/               # Terraform variable files
│       └── azure_config.tfvars  # Azure configuration
├── 📁 libs/                      # Core Python libraries
│   ├── __init__.py              # Package initialization
│   ├── graphiant_config.py      # Main Configuration management class
│   ├── gcsdk_client.py          # Graphiant SDK client wrapper
│   ├── base_manager.py          # Base manager class
│   ├── bgp_manager.py           # BGP configuration management
│   ├── interface_manager.py     # Interface configuration management
│   ├── global_config_manager.py # Global object management
│   ├── site_manager.py          # Site attachment management
│   ├── data_exchange_manager.py # Data Exchange management
│   ├── config_utils.py          # Utility functions
│   ├── config_templates.py      # Template rendering utilities
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
│   └── data_exchange_*_template.yaml    # Data Exchange templates
├── 📁 terraform/                 # Infrastructure as Code
│   ├── README.md                # Terraform documentation
│   └── azure-expressroute/      # Azure ExpressRoute modules
│       ├── main.tf             # Main Terraform configuration
│       ├── variables.tf        # Variable definitions
│       └── outputs.tf          # Output values
├── 📁 scripts/                   # Standalone utilities
│   └── cloud-init-generator/    # Device onboarding tool
│       ├── generate-cloud-init.sh  # Interactive cloud-init generator
│       └── README.md               # Generator documentation
├── 📁 pipelines/                 # CI/CD pipeline definitions
│   ├── README.md                # CI/CD documentation
│   ├── docker.yml              # Docker build pipeline
│   ├── lint.yml                # Code quality pipeline
│   └── run.yml                 # Test execution pipeline
├── 📁 ansible_collection/        # Ansible collection
│   └── graphiant/
│       └── graphiant_playbooks/
│           └── README.md        # Ansible documentation
└── 📁 test/                      # Testing framework
    ├── test.py                 # Main test suite
    └── test.ini                # Test configuration
```

### 📂 Directory Descriptions

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| **`configs/`** | Input configuration files | `sample_*.yaml`, `terraform/*.tfvars` |
| **`libs/`** | Core Python libraries | `graphiant_config.py`, `*_manager.py`, `gcsdk_client.py` |
| **`templates/`** | Jinja2 configuration templates | `*_template.yaml` |
| **`terraform/`** | Infrastructure as Code | `README.md`, `azure-expressroute/` |
| **`scripts/`** | Standalone utilities | `cloud-init-generator/README.md` |
| **`pipelines/`** | CI/CD definitions | `README.md`, `docker.yml`, `lint.yml`, `run.yml` |
| **`ansible_collection/`** | Ansible automation | `graphiant/graphiant_playbooks/README.md` |
| **`test/`** | Testing framework | `test.py`, `test.ini` |

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
- sample_data_exchange_services.yaml
- sample_data_exchange_customers.yaml
- sample_data_exchange_matches.yaml

Note: Also refer the templates under templates/ dir for more details on the supported arguments.

### Step 2: Import and Use graphiant-playbooks
```sh
from libs.graphiant_config import GraphiantConfig

host = "https://api.graphiant.com"
username = 'username'
password = 'password'
graphiant_config = GraphiantConfig(base_url=host, username=username, password=password)
```

### Step 3: Interface Configuration Methods

#### 1. Configure/Deconfigure LAN Interfaces (Subinterfaces)
```sh
# Configure LAN interfaces
graphiant_config.interfaces.configure_lan_interfaces("sample_interface_config.yaml")

# Deconfigure LAN interfaces
graphiant_config.interfaces.deconfigure_lan_interfaces("sample_interface_config.yaml")
```

#### 2. Configure/Deconfigure WAN Interfaces (Subinterfaces)
```sh
# Configure WAN circuits and interfaces
graphiant_config.interfaces.configure_wan_circuits_interfaces(
    circuit_config_file="sample_circuit_config.yaml",
    interface_config_file="sample_interface_config.yaml"
)

# Configure circuits only (can be called separately after interface is configured)
graphiant_config.interfaces.configure_circuits(
    circuit_config_file="sample_circuit_config.yaml",
    interface_config_file="sample_interface_config.yaml"
)

# Deconfigure circuits (removes static routes if any)
graphiant_config.interfaces.deconfigure_circuits(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)

# Deconfigure WAN circuits and interfaces
graphiant_config.interfaces.deconfigure_wan_circuits_interfaces(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)
```

**Note:** `configure_circuits` can be separately called after interface is configured already just to update circuits configuration (including static routes in the circuits).

**Note:** `deconfigure_circuits` will remove static routes (if any) in the circuit. This is required before deconfiguring WAN interfaces.

#### 3. Configure All Interfaces in One Single Config Push
```sh
graphiant_config.interfaces.configure_interfaces(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)
```

#### 4. Deconfigure All Interfaces (Reset parent interface to default LAN and delete subinterfaces)
```sh
graphiant_config.interfaces.deconfigure_interfaces(
    interface_config_file="sample_interface_config.yaml",
    circuit_config_file="sample_circuit_config.yaml"
)
```

**Note:** `deconfigure_circuits` might be required before running `deconfigure_interfaces` so that static routes are deconfigured before deconfiguring WAN interfaces.

### Step 4: Global Object Configurations

**Note:** Global configurations can be managed using either:
- **General methods**: `configure()` and `deconfigure()` - automatically detects and processes all configuration types in the YAML file
- **Specific methods**: `configure_*()` and `deconfigure_*()` - processes only the specific configuration type

#### Global Config LAN Segments
```sh
# Configure global LAN segments (using general configure method)
graphiant_config.global_config.configure("sample_global_lan_segments.yaml")

# Deconfigure global LAN segments (using general deconfigure method)
graphiant_config.global_config.deconfigure("sample_global_lan_segments.yaml")
```

#### Global Site Lists
```sh
# Configure global site lists (using general configure method)
graphiant_config.global_config.configure("sample_global_site_lists.yaml")

# Deconfigure global site lists (using general deconfigure method)
graphiant_config.global_config.deconfigure("sample_global_site_lists.yaml")
```

#### Global Config Prefix Lists
```sh
# Configure global prefix sets
graphiant_config.global_config.configure("sample_global_prefix_lists.yaml")

# Deconfigure global prefix sets
graphiant_config.global_config.deconfigure("sample_global_prefix_lists.yaml")
```

#### Global Config BGP Filters
```sh
# Configure global BGP filters
graphiant_config.global_config.configure("sample_global_bgp_filters.yaml")

# Deconfigure global BGP filters
graphiant_config.global_config.deconfigure("sample_global_bgp_filters.yaml")
```

#### Global Config SNMP System Objects
```sh
# Configure global SNMP services
graphiant_config.global_config.configure("sample_global_snmp_services.yaml")

# Deconfigure global SNMP services
graphiant_config.global_config.deconfigure("sample_global_snmp_services.yaml")
```

#### Global Config Syslog System Objects
```sh
# Configure global syslog services
graphiant_config.global_config.configure("sample_global_syslog_servers.yaml")

# Deconfigure global syslog services
graphiant_config.global_config.deconfigure("sample_global_syslog_servers.yaml")
```

#### Global Config IPFIX System Objects
```sh
# Configure global IPFIX services
graphiant_config.global_config.configure("sample_global_ipfix_exporters.yaml")

# Deconfigure global IPFIX services
graphiant_config.global_config.deconfigure("sample_global_ipfix_exporters.yaml")
```

#### Global Config VPN Profiles
```sh
# Configure global VPN profiles
graphiant_config.global_config.configure("sample_global_vpn_profiles.yaml")

# Deconfigure global VPN profiles
graphiant_config.global_config.deconfigure("sample_global_vpn_profiles.yaml")
```

### Step 5: Site Management

#### Site Creation and Object Attachment
```sh
# Configure sites (create sites and attach global objects)
graphiant_config.sites.configure("sample_sites.yaml")

# Deconfigure sites (detach objects and delete sites)
graphiant_config.sites.deconfigure("sample_sites.yaml")
```

#### Site-Only Operations
```sh
# Create sites only
graphiant_config.sites.configure_sites("sample_sites.yaml")

# Delete sites only
graphiant_config.sites.deconfigure_sites("sample_sites.yaml")
```

#### Object Attachment Operations
```sh
# Attach global objects to existing sites
graphiant_config.sites.attach_objects("sample_sites.yaml")

# Detach global objects from sites
graphiant_config.sites.detach_objects("sample_sites.yaml")
```

### Step 6: BGP Peering Neighbors Configurations

#### Configure BGP Peering and Attach Global Config BGP Filters
```sh
# Configure BGP peering neighbors
graphiant_config.bgp.configure("sample_bgp_peering.yaml")
```

#### Detach Global Config BGP Filters from BGP Peers
```sh
# Detach policies from BGP peers
graphiant_config.bgp.detach_policies("sample_bgp_peering.yaml")
```

#### Deconfigure BGP Peering
```sh
# Deconfigure BGP peering neighbors
graphiant_config.bgp.deconfigure("sample_bgp_peering.yaml")
```

### Step 7: Data Exchange Management

#### Create Data Exchange Services
```sh
# Create Data Exchange services
graphiant_config.data_exchange.create_services("sample_data_exchange_services.yaml")
```

#### Create Data Exchange Customers
```sh
# Create Data Exchange customers
graphiant_config.data_exchange.create_customers("sample_data_exchange_customers.yaml")
```

#### Match Services to Customers
```sh
# Match services to customers
graphiant_config.data_exchange.match_service_to_customers("sample_data_exchange_matches.yaml")
```

#### Get Summaries
```sh
# Get services summary
services_summary = graphiant_config.data_exchange.get_services_summary()

# Get customers summary
customers_summary = graphiant_config.data_exchange.get_customers_summary()
```

## 📚 API Reference

### Core Classes

#### `GraphiantConfig` Class
The main entry point for all Graphiant Playbooks operations.

```python
from libs.graphiant_config import GraphiantConfig

# Initialize Edge manager
graphiant_config = GraphiantConfig(
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
| **`DataExchangeManager`** | Data Exchange management | `create_services()`, `create_customers()`, `match_service_to_customers()` |

### Interface Management

#### LAN Interface Configuration
```python
# Configure LAN interfaces
graphiant_config.interfaces.configure_lan_interfaces("configs/sample_interface_config.yaml")

# Deconfigure LAN interfaces
graphiant_config.interfaces.deconfigure_lan_interfaces("configs/sample_interface_config.yaml")
```

#### WAN Interface Configuration
```python
# Configure WAN circuits and interfaces
graphiant_config.interfaces.configure_wan_circuits_interfaces(
    circuit_config_file="configs/sample_circuit_config.yaml",
    interface_config_file="configs/sample_interface_config.yaml"
)

# Configure circuits only
graphiant_config.interfaces.configure_circuits(
    circuit_config_file="configs/sample_circuit_config.yaml",
    interface_config_file="configs/sample_interface_config.yaml"
)

# Deconfigure circuits (removes static routes)
graphiant_config.interfaces.deconfigure_circuits(
    interface_config_file="configs/sample_interface_config.yaml",
    circuit_config_file="configs/sample_circuit_config.yaml"
)
```

#### Complete Interface Management
```python
# Configure all interfaces in one operation
graphiant_config.interfaces.configure_interfaces(
    interface_config_file="configs/sample_interface_config.yaml",
    circuit_config_file="configs/sample_circuit_config.yaml"
)

# Deconfigure all interfaces
graphiant_config.interfaces.deconfigure_interfaces(
    interface_config_file="configs/sample_interface_config.yaml",
    circuit_config_file="configs/sample_circuit_config.yaml"
)
```

### Global Object Management

#### Prefix Lists
```python
# Configure global prefix sets
graphiant_config.global_config.configure("configs/sample_global_prefix_lists.yaml")

# Deconfigure global prefix sets
graphiant_config.global_config.deconfigure("configs/sample_global_prefix_lists.yaml")
```

#### BGP Filters
```python
# Configure global BGP filters
graphiant_config.global_config.configure("configs/sample_global_bgp_filters.yaml")

# Deconfigure global BGP filters
graphiant_config.global_config.deconfigure("configs/sample_global_bgp_filters.yaml")
```

#### System Objects
```python
# SNMP Services
graphiant_config.global_config.configure("configs/sample_global_snmp_services.yaml")

# Syslog Servers
graphiant_config.global_config.configure("configs/sample_global_syslog_servers.yaml")

# IPFIX Exporters
graphiant_config.global_config.configure("configs/sample_global_ipfix_exporters.yaml")

# VPN Profiles
graphiant_config.global_config.configure("configs/sample_global_vpn_profiles.yaml")

# LAN Segments
graphiant_config.global_config.configure("configs/sample_global_lan_segments.yaml")

# Site Lists
graphiant_config.global_config.configure("configs/sample_global_site_lists.yaml")
```

### BGP Peering Management

```python
# Configure BGP peering neighbors
graphiant_config.bgp.configure("configs/sample_bgp_peering.yaml")

# Detach policies from BGP peers
graphiant_config.bgp.detach_policies("configs/sample_bgp_peering.yaml")

# Deconfigure BGP peering
graphiant_config.bgp.deconfigure("configs/sample_bgp_peering.yaml")
```

### Site Management

```python
# Configure sites (create sites and attach objects)
graphiant_config.sites.configure("sample_sites.yaml")

# Deconfigure sites (detach objects and delete sites)
graphiant_config.sites.deconfigure("sample_sites.yaml")

# Create sites only
graphiant_config.sites.configure_sites("sample_sites.yaml")

# Delete sites only
graphiant_config.sites.deconfigure_sites("sample_sites.yaml")

# Attach objects to existing sites
graphiant_config.sites.attach_objects("sample_sites.yaml")

# Detach objects from sites
graphiant_config.sites.detach_objects("sample_sites.yaml")
```

### Data Exchange Management

```python
# Create Data Exchange services
graphiant_config.data_exchange.create_services("sample_data_exchange_services.yaml")

# Create Data Exchange customers
graphiant_config.data_exchange.create_customers("sample_data_exchange_customers.yaml")

# Match services to customers
graphiant_config.data_exchange.match_service_to_customers("sample_data_exchange_matches.yaml")

# Get summaries
services_summary = graphiant_config.data_exchange.get_services_summary()
customers_summary = graphiant_config.data_exchange.get_customers_summary()
```

### Utility Functions

#### Enterprise Operations
```python
# Get enterprise ID
enterprise_id = graphiant_config.config_utils.gsdk.get_enterprise_id()

# Get all LAN segments
lan_segments = graphiant_config.config_utils.gsdk.get_lan_segments_dict()
```

#### Template Rendering
```python
# Render configuration templates
from libs.config_templates import render_template

rendered_config = render_template(
    template_file="templates/interface_template.yaml",
    config_data=config_dict
)
```

### Error Handling

```python
from libs.exceptions import GraphiantPlaybooksError

try:
    graphiant_config.interfaces.configure_lan_interfaces("config.yaml")
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

**📖 [Terraform Documentation](terraform/README.md)** - Complete infrastructure setup, deployment, and management guide.

## 🐳 Docker Support

Graphiant Playbooks includes Docker support for consistent development and deployment environments.

**📖 [Docker Documentation](Docker.md)** - Complete Docker setup, usage, and troubleshooting guide.

## 🔄 CI/CD Pipelines

The project includes pre-configured CI/CD pipelines for automated testing and deployment.

**📖 [CI/CD Documentation](pipelines/README.md)** - Complete pipeline configuration, usage, and troubleshooting guide.

## ☁️ Cloud-Init Generator

The cloud-init generator is an interactive tool for creating device onboarding configurations.

**📖 [Cloud-Init Generator Documentation](scripts/cloud-init-generator/README.md)** - Complete setup, usage, and configuration guide.

## 📦 Ansible Collection

The project includes a comprehensive Ansible collection for automation workflows.

**📖 [Ansible Collection Documentation](ansible_collection/graphiant/graphiant_playbooks/README.md)** - Complete Ansible automation guide.

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