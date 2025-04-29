

graphiant-playbooks.zip has below repos,

graphiant-playbooks/
- configs/        # Input YAML configurations
- gcsdk_dist/     # GCSDK build
- libs/           # Python libraries and modules
- logs/           # Execution logs
- templates/      # Jinja2 config templates

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

# 1. Install Python 3.13+

# 2. Create and activate python virtual environment
```sh
python3.13 -m venv venv
source venv/bin/activate
```

# 3. Install the GCSDK build from gcsdk_dist/
```sh
pip install gcsdk_dist/swagger-client-1.0.0.tar.gz --force-reinstall
```

# Getting Started

# Step 1 : Define Configurations

All input configs should be placed in the configs/ folder.

Refer to the sample files provided and create a one based on your requirement:

- sample_bgp_peering.yaml
- sample_interface_config.yaml
- sample_global_routing_policies.yaml 

# Import and Use graphiant-playbooks
```sh
from libs.edge import Edge

host = "https://api.test.graphiant.io"
username = 'username'
password = 'password'
edge = Edge(base_url=host, username=username, password=password)
```
# To Configure the interfaces defined in sample_interface_config.yaml
```sh
edge.configure_interfaces("sample_interface_config.yaml")
```

# To deconfigure all the interfaces defined in sample_interface_config.yaml
```sh
edge.deconfigure_interfaces("sample_interface_config.yaml")
```

# To configure the Global Prefixes defined in sample_global_routing_policies.yaml
```sh
edge.configure_global_prefix("sample_global_routing_policies.yaml")
```

# To Configure the Global Prefixes defined in sample_global_routing_policies.yaml
```sh
edge.configure_global_bgp_routing_policies("sample_global_routing_policies.yaml")
```

# To Configure the BGP Peers defined in sample_bgp_peering.yaml
```sh
edge.configure_bgp_peers("sample_bgp_peering.yaml")
```

# To Unlink and deconfigure the BGP Peers defined in sample_global_routing_policies.yaml
```sh
edge.unlink_bgp_peers("sample_bgp_peering.yaml")
edge.deconfigure_bgp_peers("sample_bgp_peering.yaml")
```

# To Deconfigure the Global BGP Routing Policies
```sh
edge.deconfigure_global_bgp_routing_policies("sample_global_routing_policies.yaml")
```

# To Deconfigure the Global Prefixes
```sh
edge.deconfigure_global_prefix("sample_global_routing_policies.yaml")
```
