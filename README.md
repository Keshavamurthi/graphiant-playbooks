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

### 2. Create and activate python virtual environment
```sh
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install the requirement packages
```sh
pip3 install -r requirements.txt
```

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
