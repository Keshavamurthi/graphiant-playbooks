from portal_utils import PortalUtils
from edge_templates import EdgeTemplates
from time import sleep
import yaml

class Edge(PortalUtils):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template = EdgeTemplates()

    def add_wan_interface(self, device_id, **kwargs):
        config = self.template._wan_interface_template(**kwargs)
        config.update(self.template._wan_circuit_template(**kwargs))
        output = self.gcsdk.put_device_config(device_id=device_id, edge=config)
        result = True if output.job_id else False
        return result

    def add_wan_interfaces_in_parallel(self, config_dict):
        self.concurrent_task_execution(self.add_wan_interface, config_dict)

    def add_lan_interface(self, device_id, **kwargs):
        config = self.template._lan_interface_template(**kwargs)
        output = self.gcsdk.put_device_config(device_id=device_id, edge=config)
        result = True if output.job_id else False
        return result

    def add_lan_interface_in_parallel(self, config_dict):
        self.concurrent_task_execution(self.add_lan_interface, config_dict)

    def move_interface_to_default_lan(self, device_id, **kwargs):
        config = self.template._default_lan_interface_template(**kwargs)
        if self.__class__.__name__ == "Core":
            output = self.gcsdk.put_device_config(device_id=device_id, core=config)
        else:
            output = self.gcsdk.put_device_config(device_id=device_id, edge=config)
        result = True if output.job_id else False
        return result      

    def delete_interface(self, device_id, **kwargs):
        result = self.move_interface_to_default_lan(device_id, **kwargs)
        config = self.template._default_interface_template(**kwargs)
        if self.__class__.__name__ == "Core":
            output = self.gcsdk.put_device_config(device_id=device_id, core=config)
        else:
            output = self.gcsdk.put_device_config(device_id=device_id, edge=config)
        result = result if output.job_id else False
        return result

    def delete_interfaces_in_parallel(self, config_dict):
        self.concurrent_task_execution(self.delete_interface, config_dict)

    def add_lan_subinterface(self, device_id, **kwargs):
        config = self.template._lan_subinterface_template(**kwargs)
        output = self.gcsdk.put_device_config(device_id=device_id, edge=config)
        result = True if output.job_id else False
        return result

    def move_subinterface_to_default_lan(self, device_id, **kwargs):
        config = self.template._default_lan_subinterface_template(**kwargs)
        output = self.gcsdk.put_device_config(device_id=device_id, edge=config)
        result = True if output.job_id else False
        return result

    def add_lan_subinterface_in_parallel(self, config_dict):
        self.concurrent_task_execution(self.add_lan_subinterface, config_dict)

    def delete_subinterface(self, device_id, **kwargs):
        result = self.move_subinterface_to_default_lan(device_id, **kwargs)
        config = self.template._default_subinterface_template(**kwargs)
        output = self.gcsdk.put_device_config(device_id=device_id, edge=config)
        result = result if output.job_id else False
        return result

    def delete_subinterfaces_in_parallel(self, config_dict):
        self.concurrent_task_execution(self.delete_subinterface, config_dict)
    
    def add_multiple_interfaces_from_yaml(self, yaml_file):
        input_file_path = self.templates_path + yaml_file
        with open(input_file_path, "r") as file:
            config_data = yaml.safe_load(file)
        output_config = {}
        for device_id, iface_configs in config_data.items():
            device_config = {"interfaces": {}, "circuits": {}}
            for iface, config_list in iface_configs.items():
                if iface == "wan":
                    for config in config_list:
                        device_config["circuits"].update(self.template._wan_circuit_template(**config)["circuits"])
                        device_config["interfaces"].update(self.template._wan_interface_template(**config)["interfaces"])
                if iface == "lan":
                    for config in config_list:
                        if "vlan" in config.keys():
                            try:
                                if device_config["interfaces"].get(config["interface_name"]).get("interface").get("subinterfaces"):
                                    vlan_interface = self.template._lan_subinterface_vlan_template(**config)
                                    device_config["interfaces"][config["interface_name"]]["interface"]["subinterfaces"].update(vlan_interface)
                            except AttributeError:
                                device_config["interfaces"].update(self.template._lan_subinterface_template(**config)["interfaces"])
                        else:
                            device_config["interfaces"].update(self.template._lan_interface_template(**config)["interfaces"])
            output_config[device_id] = {"device_id": device_id, "edge": device_config}
        self.concurrent_task_execution(self.gcsdk.put_device_config, output_config)

    def delete_multiple_interfaces_from_yaml(self, yaml_file):
        input_file_path = self.templates_path + yaml_file
        with open(input_file_path, "r") as file:
            config_data = yaml.safe_load(file)
        default_lan_config = {}
        default_interface_config = {}
        for device_id, iface_configs in config_data.items():
            default_lan_device_config = {"interfaces": {}}
            default_interface_device_config = {"interfaces": {}}
            for iface, config_list in iface_configs.items():
                if iface == "wan":
                    for config in config_list:
                        default_lan_device_config["interfaces"].update(self.template._default_lan_interface_template(**config)["interfaces"])
                        default_interface_device_config["interfaces"].update(self.template._default_interface_template(**config)["interfaces"])
                if iface == "lan":
                    for config in config_list:
                        if "vlan" in config.keys():
                            try:
                                if default_lan_device_config["interfaces"].get(config["interface_name"]).get("interface").get("subinterfaces"):
                                    default_lan_vlan_interface = self.template._default_lan_subinterface_vlan_template(**config)
                                    default_lan_device_config["interfaces"][config["interface_name"]]["interface"]["subinterfaces"].update(default_lan_vlan_interface)
                                    default_interface_vlan_config = self.template._default_subinterface_vlan_template(**config)
                                    default_interface_device_config["interfaces"][config["interface_name"]]["interface"]["subinterfaces"].update(default_interface_vlan_config)
                            except AttributeError:
                                default_lan_device_config["interfaces"].update(self.template._default_lan_subinterface_template(**config)["interfaces"])
                                default_interface_device_config["interfaces"].update(self.template._default_subinterface_template(**config)["interfaces"])
                        else:
                            default_lan_device_config["interfaces"].update(self.template._default_lan_interface_template(**config)["interfaces"])
                            default_interface_device_config["interfaces"].update(self.template._default_interface_template(**config)["interfaces"])
            default_lan_config[device_id] = {"device_id": device_id, "edge": default_lan_device_config}
            default_interface_config[device_id] = {"device_id": device_id, "edge": default_interface_device_config}
        self.concurrent_task_execution(self.gcsdk.put_device_config, default_lan_config)
        self.concurrent_task_execution(self.gcsdk.put_device_config, default_interface_config)

edge = Edge()
edge.delete_multiple_interfaces_from_yaml("edge_configs.yaml")

#config_dict = { 30000050144 : {"device_id": 30000050144, "interface_name": "GigabitEthernet8/0/0", "ipv4_address": "10.1.8.2/24", "gw_address": "10.1.8.1/24", "ipv6_address": "2001:10:1:8::1/64", "lan": "lan-8-bgpfilters-new", "default_lan": "default-10000000288", "vlan": 28, "circuit_name": "c-gigabitethernet8-0-0"},
#                30000050145 : {"device_id": 30000050145, "interface_name": "GigabitEthernet8/0/0", "ipv4_address": "10.1.8.3/24", "gw_address": "10.1.8.1/24", "ipv6_address": "2001:10:1:8::2/64", "lan": "lan-8-bgpfilters-new", "default_lan": "default-10000000288", "vlan": 28, "circuit_name": "c-gigabitethernet8-0-0"},
#                30000050143 : {"device_id": 30000050143, "interface_name": "GigabitEthernet8/0/0", "ipv4_address": "10.1.8.4/24", "gw_address": "10.1.8.1/24", "ipv6_address": "2001:10:1:8::3/64", "lan": "lan-8-bgpfilters-new", "default_lan": "default-10000000288", "vlan": 28, "circuit_name": "c-gigabitethernet8-0-0"},}
#edge.delete_interfaces_in_parallel(config_dict=config_dict)

#edge = Edge()
#result = edge.add_lan_interface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", ipv4_address="10.1.8.1/24", 
#                                ipv6_address="2001:10:1:8::1/64", lan="lan-8-bgpfilters-new")
#result = edge.delete_interface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", default_lan="default-10000000288")
#result = edge.add_lan_subinterface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", ipv4_address="10.1.8.1/24", 
#                                   ipv6_address="2001:10:1:8::1/64", lan="lan-8-bgpfilters-new", vlan=19)
#result = edge.delete_subinterface(device_id=30000050144, interface_name="GigabitEthernet8/0/0", default_lan="default-10000000288", vlan=19)
#result = core.gcsdk.get_all_devices()
#result = edge.add_wan_interface(device_id=30000050144, interface_name="GigabitEthernet5/0/0", ipv4_address="100.64.194.144/20", gw_address="92.93.94.98", circuit_name="c-gigabitethernet5-0-0")
#result = edge.delete_interface(device_id=30000050144, interface_name="GigabitEthernet5/0/0", default_lan="default-10000000288")
#print(result)