#from edge_utils import Edge

# host = "https://api.test.graphiant.io"
# username = "email"
# password = "xxxx"
# edge = Edge(base_url=host, username=username, password=password)

#edge = Edge()
#edge.add_multiple_interfaces_from_yaml(yaml_file="edge_configs.yaml")
#edge.delete_multiple_interfaces_from_yaml(yaml_file="edge_configs.yaml")

#config_dict = { 30000050144 : {"device_id": 30000050144, "interface_name": "GigabitEthernet8/0/0", "ipv4_address": "10.1.8.2/24", "gw_address": "10.1.8.1/24", "ipv6_address": "2001:10:1:8::1/64", "lan": "lan-8-bgpfilters-new", "default_lan": "default-10000000288", "vlan": 28, "circuit_name": "c-gigabitethernet8-0-0"},
#                30000050145 : {"device_id": 30000050145, "interface_name": "GigabitEthernet8/0/0", "ipv4_address": "10.1.8.3/24", "gw_address": "10.1.8.1/24", "ipv6_address": "2001:10:1:8::2/64", "lan": "lan-8-bgpfilters-new", "default_lan": "default-10000000288", "vlan": 28, "circuit_name": "c-gigabitethernet8-0-0"},
#                30000050143 : {"device_id": 30000050143, "interface_name": "GigabitEthernet8/0/0", "ipv4_address": "10.1.8.4/24", "gw_address": "10.1.8.1/24", "ipv6_address": "2001:10:1:8::3/64", "lan": "lan-8-bgpfilters-new", "default_lan": "default-10000000288", "vlan": 28, "circuit_name": "c-gigabitethernet8-0-0"},}
#edge.delete_interfaces_in_parallel(config_dict=config_dict)

#result = edge.add_lan_interface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", ipv4_address="10.1.8.1/24", 
#                                ipv6_address="2001:10:1:8::1/64", lan="lan-8-bgpfilters-new")
#result = edge.delete_interface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", default_lan="default-10000000288")

#result = edge.add_lan_subinterface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", ipv4_address="10.1.8.1/24", 
#                                   ipv6_address="2001:10:1:8::1/64", lan="lan-8-bgpfilters-new", vlan=19)
#result = edge.delete_subinterface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", default_lan="default-10000000288", vlan=19)

#result = edge.add_wan_interface(device_id=30000050144, interface_name="GigabitEthernet5/0/0", ipv4_address="100.64.194.144/20", gw_address="92.93.94.98", circuit_name="c-gigabitethernet5-0-0")
#result = edge.delete_interface(device_id=30000050144, interface_name="GigabitEthernet5/0/0", default_lan="default-10000000288")

#print(result)

#edge.update_multiple_devices_bringup_status(yaml_file="edge_lifecycle_status.yaml")