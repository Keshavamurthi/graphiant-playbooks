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

    def _edge_interface(self, **kwargs):
        return self.render_template("interface_template.yaml", **kwargs)

    def _global_prefix_set(self, **kwargs):
        return self.render_template("global_prefix_set_template.yaml", **kwargs)
    
    def _global_bgp_filter(self, **kwargs):
        return self.render_template("global_bgp_routing_policies_template.yaml", **kwargs)
    
    def _edge_bgp_peering(self, **kwargs):
        return self.render_template("bgp_peering_template.yaml", **kwargs)
