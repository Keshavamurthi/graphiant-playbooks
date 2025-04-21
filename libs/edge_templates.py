import os
import yaml
from jinja2 import Environment, FileSystemLoader
from .logger import setup_logger

LOG = setup_logger()

class EdgeTemplates(object):

    def __init__(self, config_template_path):
        self.template_env = Environment(loader=FileSystemLoader(config_template_path))

    def render_template(self, config_template_file, **kwargs):
        LOG.debug(f"edge_templates : _{config_template_file} (config) - \n{kwargs}")
        config_template = self.template_env.get_template(config_template_file)
        config_yaml = config_template.render(**kwargs)
        config = yaml.safe_load(config_yaml)
        LOG.debug(f"edge_templates : _{config_template_file} (rendered_data)- \n{config}")
        return config

    def _default_lan(self, **kwargs):
        return self.render_template("default_lan_template.yaml", **kwargs)

    def _interface_admin_shut(self, **kwargs):
        return self.render_template("interface_admin_shut_template.yaml", **kwargs)

    def _interface(self, **kwargs):
        return self.render_template("interface_template.yaml", **kwargs)
    
    def _lan_interface(self, **kwargs):
        return self.render_template("lan_interface_template.yaml", **kwargs)

    def _subinterface(self, **kwargs):
        return self.render_template("subinterface_template.yaml", **kwargs)
    
    def _vlan_interface_default(self, **kwargs):
        return self.render_template("vlan_interface_default_template.yaml", **kwargs)

    def _vlan_interface_delete(self, **kwargs):
        return self.render_template("vlan_interface_delete_template.yaml", **kwargs)

    def _vlan_interface(self, **kwargs):
        return self.render_template("vlan_interface_template.yaml", **kwargs)

    def _wan_circuit(self, **kwargs):
        return self.render_template("wan_circuit_template.yaml", **kwargs)

    def _wan_interface(self, **kwargs):
        return self.render_template("wan_interface_template.yaml", **kwargs)

"""
    def _configure_lan_interface(self, **kwargs):
        return self.render_template("configure_lan_interface_template.yaml")

    def _create_subinterface(self, **kwargs):
        return self.render_template("create_subinterface_template.yaml", **kwargs)

    def _configure_subinterface_vlan(self, **kwargs):
        return self.render_template("configure_subinterface_vlan_template.yaml", **kwargs)

    def _lan_subinterface_template(self, **kwargs):
        config = self.render_template("lan_subinterface_template.yaml", **kwargs)
        vlan_config = self._lan_subinterface_vlan_template(**kwargs)
        config["interfaces"][kwargs.get("interface_name")]["interface"]["subinterfaces"] = vlan_config
        return config

    def _default_lan_interface_template(self, **kwargs):
        return self.render_template("default_lan_interface_template.yaml", **kwargs)

    def _shutdown_interface_template(self, **kwargs):
        return self.render_template("shutdown_interface_template.yaml", **kwargs)
    
    def _default_vlan_interface_template(self, **kwargs):
        return self.render_template("default_vlan_interface_template.yaml", **kwargs)

    def _default_lan_subinterface_template(self, **kwargs):
        config = self._create_subinterface(**kwargs)
        vlan_config = self._default_vlan_interface_template(**kwargs)
        config["interfaces"][kwargs.get("interface_name")]["interface"]["subinterfaces"] = vlan_config
        return config
    
    def _delete_vlan_interface_template(self, **kwargs):
        return self.render_template("delete_vlan_interface_template.yaml", **kwargs)

    def _default_subinterface_template(self, **kwargs):
        config = self.render_template("lan_subinterface_template.yaml", **kwargs)
        vlan_config = self._default_subinterface_vlan_template(**kwargs)
        config["interfaces"][kwargs.get("interface_name")]["interface"]["subinterfaces"] = vlan_config
        return config
        """