
```sh
graphiant-playbooks/

- configs/        # Input YAML configurations
- gcsdk_dist/     # GCSDK build
- libs/           # Python libraries and modules
- logs/           # Execution logs
- templates/      # Jinja2 config templates
```

# configs/
Contains input configuration YAML files used to drive the execution of various playbooks.

# gcsdk_dist/
Contains the GCSDK build distributions(Pre-requiste for graphiant-playbooks)

# libs/
Includes all necessary Python libraries and helper modules required by the playbooks.

# logs/
Stores all log files generated during execution. Each run creates a timestamped log 
for auditability and debugging purposes.

# templates/
Contains Jinja2 config templates. These templates are dynamically rendered using the 
input from the configs/ directory to produce finalized configuration artifacts.

# Pre-requisites:

# 1. Install Python 3.12+

# 2. Create and activate python virtual environment
```sh
python3.12 -m venv venv
source venv/bin/activate
```

# 3. Install the GCSDK build from gcsdk_dist/
```sh
pip3.12 install -r requirements.txt
```

# Testing virtual environment

# 1. Enter the host URL and credentials under test.ini
```sh
[credentials]
username = username
password = password
[host]
url = https://api.graphiant.com
```

# 2. Run the sample test and verify the enterprise ID is fetched
```sh
python3.12 test.py
```

# Getting Started

# Step 1: Define Configurations

All input configs should be placed in the configs/ folder.

Refer to the sample files provided and create a one based on your requirement:

- sample_bgp_peering.yaml
- sample_interface_config.yaml
- sample_global_routing_policies.yaml 

# Step 2: Import and Use graphiant-playbooks
```sh
from libs.edge import Edge

host = "https://api.graphiant.com"
username = 'username'
password = 'password'
edge = Edge(base_url=host, username=username, password=password)
```
# Step 3: 
# To Configure the interfaces defined in sample_interface_config.yaml
```sh
Configure Interfaces: edge.configure_interfaces("sample_interface_config.yaml")
```

# To Deconfigure the interfaces defined in sample_interface_config.yaml
```sh
Deconfigure Interfaces: edge.deconfigure_interfaces("sample_interface_config.yaml")
```

# To configure the Global Prefixes, Routing Policies and BGP Peering
```sh
Configure Global Prefixes: edge.configure_global_prefix("sample_global_routing_policies.yaml")
Configure Global Routing Policies: edge.configure_global_bgp_routing_policies("sample_global_routing_policies.yaml")
Configure BGP Peering: edge.configure_bgp_peers("sample_bgp_peering.yaml")
```

# To unlink and deconfigure the BGP Peers
```sh
edge.unlink_bgp_peers("sample_bgp_peering.yaml")
edge.deconfigure_bgp_peers("sample_bgp_peering.yaml")
```

# To Deconfigure the Global BGP Routing Policies
```sh
edge.deconfigure_global_bgp_routing_policies("sample_global_routing_policies.yaml")

Note: Make sure the routing policies are not attached to any BGP peering configs before deconfigure
```

# To Deconfigure the Global Prefixes
```sh
edge.deconfigure_global_prefix("sample_global_routing_policies.yaml")

Note: Make sure the Global Prefixes are not attached before deconfigure
```
