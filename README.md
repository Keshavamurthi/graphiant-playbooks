

# Requirements:

# Install GCSSK for the virtual environment

# Clone git@gitlab.com:graphiant/oss/gcsdk.git
git clone git@gitlab.com:graphiant/oss/gcsdk.git

# Uninstall the previous swagger_client (if any) 
pip uninstall swagger_client -y

# create and Install GCSDK build
python setup.py sdist bdist_wheel
pip install dist/swagger_client-1.0.0-py3-none-any.whl --force-reinstall

# Graphiant-Playbooks

# Define all the Configurations under configs folder. 

Refer the samples and create one based on the requirement.

For Example : To define the BGP Peering refer sample_bgp_peering.yaml 

# Import the Edge Class
from libs.edge import Edge

# Instantiate the Object
host = "https://api.test.graphiant.io"
username = 'username'
password = 'password'
edge = Edge(base_url=host, username=username, password=password)

# To Configure the interfaces defined in sample_interface_config.yaml
edge.configure_interfaces("sample_interface_config.yaml")

# To deconfigure all the interfaces defined in sample_interface_config.yaml
edge.deconfigure_interfaces("sample_interface_config.yaml")

# To configure the Global Prefixes defined in sample_global_routing_policies.yaml
edge.configure_global_prefix("sample_global_routing_policies.yaml")

# To Configure the Global Prefixes defined in sample_global_routing_policies.yaml
edge.configure_global_bgp_routing_policies("sample_global_routing_policies.yaml")

# To Configure the BGP Peers defined in sample_bgp_peering.yaml
edge.configure_bgp_peers("sample_bgp_peering.yaml")

# To Unlink and deconfigure the BGP Peers defined in sample_global_routing_policies.yaml
edge.unlink_bgp_peers("sample_bgp_peering.yaml")
edge.deconfigure_bgp_peers("sample_bgp_peering.yaml")

# To Deconfigure the Global BGP Routing Policies
edge.deconfigure_global_bgp_routing_policies("sample_global_routing_policies.yaml")

# To Deconfigure the Global Prefixes
edge.deconfigure_global_prefix("sample_global_routing_policies.yaml")