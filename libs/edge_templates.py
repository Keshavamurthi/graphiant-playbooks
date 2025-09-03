import yaml
from jinja2 import Environment, FileSystemLoader
from libs.logger import setup_logger

LOG = setup_logger()


class EdgeTemplates(object):

    def __init__(self, config_template_path):
        self.template_env = Environment(loader=FileSystemLoader(config_template_path))

    def render_template(self, config_template_file, **kwargs):
        """
        Renders config_template_file(Jinja2 template) with the provided variables
        and returns the parsed YAML.

        Args:
            config_template_file (str): The name of the Jinja2 template file to render.
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration generated from the rendered template.
        """
        LOG.debug(f"render_template : _{config_template_file} (config) - \n{kwargs}")
        config_template = self.template_env.get_template(config_template_file)
        config_yaml = config_template.render(**kwargs)
        config = yaml.safe_load(config_yaml)
        LOG.debug(f"render_template : _{config_template_file} (rendered_data)- \n{config}")
        return config

    def _edge_interface(self, **kwargs):
        """
        Renders the interface_template.yaml(Jinja2 template) with the provided variables.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        return self.render_template("interface_template.yaml", **kwargs)

    def _global_prefix_set(self, **kwargs):
        """
        Renders the global_prefix_set_template.yaml(Jinja2 template) with the provided variables.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        return self.render_template("global_prefix_set_template.yaml", **kwargs)

    def _global_bgp_filter(self, **kwargs):
        """
        Renders the global_bgp_routing_policies_template.yaml(Jinja2 template)
        with the provided variables.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        return self.render_template("global_bgp_routing_policies_template.yaml", **kwargs)

    def _edge_bgp_peering(self, **kwargs):
        """
        Renders the bgp_peering_template.yaml(Jinja2 template) with the provided variables.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        return self.render_template("bgp_peering_template.yaml", **kwargs)

    def _global_snmps_service(self, **kwargs):
        """
        Renders the global_snmp_service.yaml(Jinja2 template) with the provided variables.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        return self.render_template("global_snmps_template.yaml", **kwargs)

    def _global_syslog_service(self, **kwargs):
        """
        Renders the global_syslog_template.yaml(Jinja2 template) with the provided variables.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        return self.render_template("global_syslog_template.yaml", **kwargs)

    def _global_ipfix_service(self, **kwargs):
        """
        Renders the global_ipfix_template.yaml(Jinja2 template) with the provided variables.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        return self.render_template("global_ipfix_template.yaml", **kwargs)

    def _global_vpn_profile_service(self, **kwargs):
        """
        Renders the global_vpn_profile_template.yaml(Jinja2 template) with the provided variables.
        Applies VPN algorithm mapping at the template creation level.

        Args:
            **kwargs: Key-value pairs used to populate the template.

        Returns:
            dict: Parsed YAML configuration.
        """
        from libs.vpn_mappings import map_vpn_profiles

        # Map VPN profiles if they exist in kwargs
        if 'vpnProfiles' in kwargs:
            kwargs['vpnProfiles'] = map_vpn_profiles(kwargs['vpnProfiles'])

        return self.render_template("global_vpn_profile_template.yaml", **kwargs)
