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

    def global_prefix_set(self, config_payload, action="add", **kwargs):
        LOG.debug(f"global_prefix_set : {action.upper()} Global Prefix Set {kwargs.get("name")}")
        global_prefix_set = self.template._global_prefix_set(action=action, **kwargs)
        config_payload['global_prefix_sets'].update(global_prefix_set)

    def global_bgp_filter(self, config_payload, action="add", **kwargs):
        LOG.debug(f"global_bgp_filter : {action.upper()} Global BGP Filter {kwargs.get("name")}")
        global_bgp_filter = self.template._global_bgp_filter(action=action, **kwargs)
        config_payload['routing_policies'].update(global_bgp_filter)
    
    def edge_bgp_peering(self, config_payload, action="add", **kwargs):
        LOG.debug(f"edge_bgp_peering : {action.upper()} BGP Peering :\n {kwargs}")
        bgp_peering = self.template._edge_bgp_peering(action=action, **kwargs)
        config_payload.update(bgp_peering)
    
    def edge_interface(self, config_payload, action="add", **kwargs):
        LOG.debug(f"edge_interfaces : {action.upper()} Edge Interfaces :\n {kwargs}")
        interface = self.template._edge_interface(action=action, **kwargs)
        config_payload["interfaces"].update(interface.get("interfaces"))
        if interface.get('circuits'):
            config_payload['circuits'].update(interface.get("circuits"))
    