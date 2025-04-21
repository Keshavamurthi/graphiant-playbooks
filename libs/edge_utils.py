from .portal_utils import PortalUtils
from .edge_templates import EdgeTemplates
from time import sleep
import copy
import yaml
from .logger import setup_logger

LOG = setup_logger()

class EdgeUtils(PortalUtils):

    def __init__(self, base_url=None, username=None, password=None, **kwargs):
        super().__init__(base_url=base_url, username=username, password=password, **kwargs)
        self.template = EdgeTemplates(self.templates)
    
    def create_wan(self, config_payload, **kwargs):
        config_payload["circuits"].update(self.template._wan_circuit(**kwargs))
        config_payload["interfaces"].update(self.template._wan_interface(**kwargs))

    def create_interfaces(self, config_payload, **kwargs):
        if not config_payload["interfaces"].get(kwargs["interface_name"]):
            LOG.debug(f"create_interfaces: Adding interface {kwargs.get("interface_name")}")
            interface_config = self.template._interface(**kwargs)
            config_payload["interfaces"].update(interface_config)

    def create_subinterfaces(self, config_payload, **kwargs):
        if not config_payload["interfaces"].get(kwargs["interface_name"]).get("interface").get("subinterfaces"):
            LOG.debug(f"create_subinterfaces: Adding subinterfaces under {kwargs.get("interface_name")}")
            sub_interface = self.template._subinterface(**kwargs)
            config_payload["interfaces"].get(kwargs["interface_name"]).get("interface").update(sub_interface)

    def create_lan(self, config_payload, **kwargs):
        self.create_interfaces(config_payload, **kwargs)
        if "vlan" in kwargs.keys():
            self.create_vlan_interface(config_payload, **kwargs)
        else:
            LOG.debug(f"create_lan: Adding lan interface {kwargs.get("lan")}")
            config_payload["interfaces"][kwargs["interface_name"]].update(self.template._lan_interface(**kwargs))

    def create_vlan_interface(self, config_payload, **kwargs):
        self.create_subinterfaces(config_payload, **kwargs)
        LOG.debug(f"create_vlan_interface: Adding vlan interface {kwargs.get('vlan')}")  
        vlan_interface = self.template._vlan_interface(**kwargs)
        config_payload["interfaces"][kwargs["interface_name"]]["interface"]["subinterfaces"].update(vlan_interface)

    def configure_default_lan(self, default_lan, config_payload, **kwargs):
        self.create_interfaces(config_payload, **kwargs)
        LOG.debug(f"configure_default_lan: Configuring {kwargs.get("interface_name")} : {default_lan}(default lan)")
        kwargs['default_lan'] = default_lan
        config_payload["interfaces"][kwargs["interface_name"]]["interface"].update(self.template._default_lan(**kwargs))
    
    def configure_default_lan_for_vlan_interfaces(self, default_lan, config_payload, **kwargs):
        self.create_interfaces(config_payload, **kwargs)
        if "vlan" in kwargs.keys():
            self.create_subinterfaces(config_payload, **kwargs)
            LOG.debug(f"configure_default_lan_for_vlan_interfaces: Configuring {kwargs.get("vlan")} : {default_lan}(default lan)")
            kwargs['default_lan'] = default_lan
            defaut_lan_vlan = self.template._vlan_interface_default(**kwargs)
            config_payload["interfaces"].get(kwargs["interface_name"]).get("interface").get("subinterfaces").update(defaut_lan_vlan)
        else:
            self.configure_default_lan(default_lan, config_payload, **kwargs)

    def delete_interfaces(self, config_payload, **kwargs):
        self.create_interfaces(config_payload, **kwargs)
        LOG.debug(f"delete_interfaces: Deleting {kwargs.get("interface_name")}")
        config_payload["interfaces"][kwargs["interface_name"]]["interface"].update(self.template._interface_admin_shut(**kwargs))

    def delete_vlan_interfaces(self, config_payload, **kwargs):
        self.create_interfaces(config_payload, **kwargs)
        if "vlan" in kwargs.keys():
            self.create_subinterfaces(config_payload, **kwargs)
            LOG.debug(f"delete_vlan_interfaces: Configuring {kwargs.get("vlan")}")
            delete_vlan_interface = self.template._vlan_interface_delete(**kwargs)
            config_payload["interfaces"].get(kwargs["interface_name"]).get("interface").get("subinterfaces").update(delete_vlan_interface)
        else:
            self.delete_interfaces(config_payload, **kwargs)
