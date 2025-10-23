"""
Refactored Edge Templates for Graphiant Playbooks.

This module provides a clean, maintainable interface for template rendering
with proper error handling, type hints, and reduced code duplication.
"""

import yaml
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, TemplateSyntaxError
from libs.logger import setup_logger
from libs.exceptions import TemplateError, ConfigurationError

LOG = setup_logger()


class EdgeTemplates:
    """
    Manages Jinja2 template rendering for Graphiant configurations.

    This class provides a clean interface for rendering configuration templates
    with proper error handling and type safety.
    """

    # Template mapping for different configuration types
    TEMPLATE_MAPPING = {
        'interface': 'interface_template.yaml',
        'circuit': 'circuit_template.yaml',
        'global_prefix_set': 'global_prefix_set_template.yaml',
        'global_bgp_filter': 'global_bgp_routing_policies_template.yaml',
        'bgp_peering': 'bgp_peering_template.yaml',
        'snmp_service': 'global_snmps_template.yaml',
        'syslog_service': 'global_syslog_template.yaml',
        'ipfix_service': 'global_ipfix_template.yaml',
        'vpn_profile': 'global_vpn_profile_template.yaml'
    }

    def __init__(self, config_template_path: str):
        """
        Initialize the EdgeTemplates with template directory path.

        Args:
            config_template_path: Path to the directory containing Jinja2 templates

        Raises:
            TemplateError: If template directory cannot be accessed
        """
        try:
            self.template_env = Environment(loader=FileSystemLoader(config_template_path))
            self.template_path = config_template_path
            LOG.debug(f"EdgeTemplates initialized with path: {config_template_path}")
        except Exception as e:
            raise TemplateError(f"Failed to initialize template environment: {str(e)}")

    def render_template(self, template_name: str, **kwargs) -> Dict[str, Any]:
        """
        Render a Jinja2 template with the provided variables and return parsed YAML.

        Args:
            template_name: Name of the Jinja2 template file to render
            **kwargs: Key-value pairs used to populate the template

        Returns:
            Parsed YAML configuration as a dictionary

        Raises:
            TemplateError: If template rendering fails
            ConfigurationError: If YAML parsing fails
        """
        try:
            LOG.debug(f"Rendering template '{template_name}' with kwargs: {kwargs}")

            # Get and render the template
            template = self.template_env.get_template(template_name)
            rendered_yaml = template.render(**kwargs)

            # Parse the rendered YAML
            config = yaml.safe_load(rendered_yaml)

            LOG.debug(f"Successfully rendered template '{template_name}'")
            return config

        except TemplateNotFound as e:
            error_msg = f"Template '{template_name}' not found in {self.template_path}"
            LOG.error(error_msg)
            raise TemplateError(error_msg) from e

        except TemplateSyntaxError as e:
            error_msg = f"Syntax error in template '{template_name}': {str(e)}"
            LOG.error(error_msg)
            raise TemplateError(error_msg) from e

        except yaml.YAMLError as e:
            error_msg = f"YAML parsing error for template '{template_name}': {str(e)}"
            LOG.error(error_msg)
            raise ConfigurationError(error_msg) from e

        except Exception as e:
            error_msg = f"Unexpected error rendering template '{template_name}': {str(e)}"
            LOG.error(error_msg)
            raise TemplateError(error_msg) from e

    def render_by_type(self, template_type: str, **kwargs) -> Dict[str, Any]:
        """
        Render a template by type using the predefined template mapping.

        Args:
            template_type: Type of template to render (key from TEMPLATE_MAPPING)
            **kwargs: Key-value pairs used to populate the template

        Returns:
            Parsed YAML configuration as a dictionary

        Raises:
            TemplateError: If template type is not found or rendering fails
        """
        if template_type not in self.TEMPLATE_MAPPING:
            available_types = list(self.TEMPLATE_MAPPING.keys())
            error_msg = f"Unknown template type '{template_type}'. Available types: {available_types}"
            LOG.error(error_msg)
            raise TemplateError(error_msg)

        template_name = self.TEMPLATE_MAPPING[template_type]
        return self.render_template(template_name, **kwargs)

    # Specific template rendering methods
    def render_interface(self, **kwargs) -> Dict[str, Any]:
        """Render interface template."""
        return self.render_by_type('interface', **kwargs)

    def render_circuit(self, **kwargs) -> Dict[str, Any]:
        """Render circuit template."""
        return self.render_by_type('circuit', **kwargs)

    def render_global_prefix_set(self, **kwargs) -> Dict[str, Any]:
        """Render global prefix set template."""
        return self.render_by_type('global_prefix_set', **kwargs)

    def render_global_bgp_filter(self, **kwargs) -> Dict[str, Any]:
        """Render global BGP filter template."""
        return self.render_by_type('global_bgp_filter', **kwargs)

    def render_bgp_peering(self, **kwargs) -> Dict[str, Any]:
        """Render BGP peering template."""
        return self.render_by_type('bgp_peering', **kwargs)

    def render_snmp_service(self, **kwargs) -> Dict[str, Any]:
        """Render SNMP service template."""
        return self.render_by_type('snmp_service', **kwargs)

    def render_syslog_service(self, **kwargs) -> Dict[str, Any]:
        """Render syslog service template."""
        return self.render_by_type('syslog_service', **kwargs)

    def render_ipfix_service(self, **kwargs) -> Dict[str, Any]:
        """Render IPFIX service template."""
        return self.render_by_type('ipfix_service', **kwargs)

    def render_vpn_profile(self, **kwargs) -> Dict[str, Any]:
        """
        Render VPN profile template with algorithm mapping.

        This method includes special handling for VPN algorithm mapping
        before template rendering.
        """
        try:
            # Apply VPN algorithm mapping if needed
            if 'vpn_profiles' in kwargs:
                from libs.vpn_mappings import map_vpn_profiles
                kwargs['vpn_profiles'] = map_vpn_profiles(kwargs['vpn_profiles'])
                LOG.info("Applied VPN algorithm mapping {}".format(kwargs['vpn_profiles']))

            return self.render_by_type('vpn_profile', **kwargs)

        except ImportError as e:
            error_msg = f"Failed to import VPN mappings: {str(e)}"
            LOG.error(error_msg)
            raise TemplateError(error_msg) from e
        except Exception as e:
            error_msg = f"Error in VPN profile rendering: {str(e)}"
            LOG.error(error_msg)
            raise TemplateError(error_msg) from e

    def get_available_templates(self) -> Dict[str, str]:
        """
        Get a dictionary of available template types and their file names.

        Returns:
            Dictionary mapping template types to file names
        """
        return self.TEMPLATE_MAPPING.copy()

    def validate_template(self, template_name: str) -> bool:
        """
        Validate that a template exists and is syntactically correct.

        Args:
            template_name: Name of the template to validate

        Returns:
            True if template is valid, False otherwise
        """
        try:
            template = self.template_env.get_template(template_name)
            # Try to render with empty context to check syntax
            template.render()
            return True
        except Exception as e:
            LOG.warning(f"Template '{template_name}' validation failed: {str(e)}")
            return False
