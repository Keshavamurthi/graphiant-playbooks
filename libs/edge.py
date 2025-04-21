from .edge_utils import EdgeUtils
import yaml
from .logger import setup_logger

LOG = setup_logger()

class Edge(EdgeUtils):

    def __init__(self, base_url=None, username=None, password=None, **kwargs):
        super().__init__(base_url=base_url, username=username, password=password, **kwargs)
    
    def configure_interfaces(self, yaml_file):
        input_file_path = self.config_path + yaml_file
        with open(input_file_path, "r") as file:
            config_data = yaml.safe_load(file)
        output_config = {}
        for device_name, iface_configs in config_data.items():
            device_id = self.get_device_id(device_name=device_name)
            device_config = {"interfaces": {}, "circuits": {}}
            for iface, config_list in iface_configs.items():
                if iface == "wan":
                    for config in config_list:
                        self.create_wan(device_config, **config)
                if iface == "lan":
                    for config in config_list:
                        self.create_lan(device_config, **config)
            output_config[device_id] = {"device_id": device_id, "edge": device_config}
        self.concurrent_task_execution(self.gcsdk.put_device_config, output_config)

    def deconfigure_interfaces(self, yaml_file):
        input_file_path = self.config_path + yaml_file
        with open(input_file_path, "r") as file:
            config_data = yaml.safe_load(file)
        final_config_payload = {}
        default_lan = f'default-{self.get_enterprise_id()}'
        for device_name, iface_configs in config_data.items():
            device_id = self.get_device_id(device_name=device_name)
            default_lan_config = {"interfaces": {}}
            for iface, config_list in iface_configs.items():
                if iface == "wan":
                    for config in config_list:
                        self.configure_default_lan(default_lan, default_lan_config, **config)
                if iface == "lan":
                    for config in config_list:
                        self.configure_default_lan_for_vlan_interfaces(default_lan, default_lan_config, **config)
            final_config_payload[device_id] = {"device_id": device_id, "edge": default_lan_config}
        self.concurrent_task_execution(self.gcsdk.put_device_config, final_config_payload)

        final_config_payload = {}
        for device_name, iface_configs in config_data.items():
            device_id = self.get_device_id(device_name=device_name)
            shut_interfaces_config = {"interfaces": {}}
            for iface, config_list in iface_configs.items():
                if iface == "wan":
                    for config in config_list:
                        self.delete_interfaces(shut_interfaces_config, **config)
                if iface == "lan":
                    for config in config_list:
                        self.delete_vlan_interfaces(shut_interfaces_config, **config)
            final_config_payload[device_id] = {"device_id": device_id, "edge": shut_interfaces_config}
        self.concurrent_task_execution(self.gcsdk.put_device_config, final_config_payload)
