"""
This module provides standardized utility methods for building configuration payloads
using Jinja2 templates. All methods follow consistent patterns for better maintainability.
"""

from libs.portal_utils import PortalUtils
from libs.config_templates import ConfigTemplates
from libs.logger import setup_logger
from libs.exceptions import ConfigurationError

LOG = setup_logger()


class ConfigUtils(PortalUtils):
    """
    Standardized utility class for building device configuration payloads.

    This class provides consistent methods for rendering templates and updating
    configuration payloads with proper error handling and logging.
    """

    def __init__(self, base_url=None, username=None, password=None, **kwargs):
        """Initialize ConfigUtils with portal connection and template renderer."""
        super().__init__(base_url=base_url, username=username, password=password, **kwargs)
        self.template = ConfigTemplates(self.templates)

    def _validate_required_params(self, kwargs, required_params):
        """
        Validate that required parameters are present.

        Args:
            kwargs: Dictionary of parameters to validate
            required_params: List of required parameter names

        Raises:
            ConfigurationError: If any required parameters are missing
        """
        missing_params = [param for param in required_params if param not in kwargs]
        if missing_params:
            raise ConfigurationError(f"Missing required parameters: {missing_params}")

    def global_prefix_set(self, config_payload, action="add", **kwargs):
        """
        Update the global_prefix_sets section of configuration payload.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.debug(f"Global prefix set: {action.upper()} {kwargs.get('name')}")

        try:
            result = self.template.render_global_prefix_set(action=action, **kwargs)
            if action == "add":
                config_payload['global_prefix_sets'].update(result)
            else:  # delete
                config_payload['global_prefix_sets'][kwargs.get('name')] = {}
        except Exception as e:
            LOG.error(f"Failed to process global prefix set {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Global prefix set processing failed: {str(e)}")

    def global_bgp_filter(self, config_payload, action="add", **kwargs):
        """
        Update the routing_policies section of the configuration payload.

        Args:
            config_payload (dict): The configuration dictionary that holds routing policies.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional parameters used for rendering the template.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.debug(f"Global BGP filter: {action.upper()} {kwargs.get('name')}")

        try:
            result = self.template.render_global_bgp_filter(action=action, **kwargs)
            if action == "add":
                config_payload['routing_policies'].update(result)
            else:  # delete
                config_payload['routing_policies'][kwargs.get('name')] = {}
        except Exception as e:
            LOG.error(f"Failed to process global BGP filter {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Global BGP filter processing failed: {str(e)}")

    def device_bgp_peering(self, config_payload, action="add", **kwargs):
        """
        Update the Device neighbors section of configuration payload.

        Args:
            config_payload (dict): Dictionary to be updated with BGP peering configuration.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional parameters used for rendering the BGP peering configuration.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['segments'])
        LOG.debug(f"Edge BGP peering: {action.upper()} {kwargs.get('segments')}")

        try:
            # Handle route policies global ID resolution
            global_ids = {}
            if kwargs.get("route_policies"):
                for policy_name in kwargs.get("route_policies"):
                    global_ids[policy_name] = self.gsdk.get_global_routing_policy_id(policy_name)
                    LOG.debug(f"Global ID for {policy_name}: {global_ids[policy_name]}")

            result = self.template.render_bgp_peering(action=action, global_ids=global_ids, **kwargs)
            config_payload.update(result)
        except Exception as e:
            LOG.error(f"Failed to process device BGP peering {kwargs.get('segments')}: {str(e)}")
            raise ConfigurationError(f"Device BGP peering processing failed: {str(e)}")

    def device_interface(self, config_payload, action="add", **kwargs):
        """
        Update the device interfaces section of the configuration payload.

        Args:
            config_payload (dict): Dictionary to be updated with interface data.
            action (str, optional): Action to perform, either "add", "default_lan", or "delete".
            **kwargs: Additional parameters passed to the template renderer.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.info(f"Device interface: {action.upper()} {kwargs.get('name')}")

        try:
            result = self.template.render_interface(action=action, **kwargs)
            if "interfaces" in result:
                config_payload["interfaces"].update(result["interfaces"])
            else:
                LOG.warning(f"No interfaces found in template result for {kwargs.get('name')}")
        except Exception as e:
            LOG.error(f"Failed to process device interface {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Device interface processing failed: {str(e)}")

    def device_circuit(self, config_payload, action="add", **kwargs):
        """
        Update the device circuits section of the configuration payload.

        Args:
            config_payload (dict): Dictionary to be updated with circuit data.
            action (str, optional): Action to perform, either "add" or "delete".
            **kwargs: Additional parameters passed to the template renderer.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['circuit'])
        LOG.debug(f"Device circuit: {action.upper()} {kwargs.get('circuit')}")

        try:
            result = self.template.render_circuit(action=action, **kwargs)
            if "circuits" in result:
                config_payload["circuits"].update(result["circuits"])
            else:
                LOG.warning(f"No circuits found in template result for {kwargs.get('circuit')}")
        except Exception as e:
            LOG.error(f"Failed to process device circuit {kwargs.get('circuit')}: {str(e)}")
            raise ConfigurationError(f"Device circuit processing failed: {str(e)}")

    def global_snmp(self, config_payload, action="add", **kwargs):
        """
        Update the snmps section of configuration payload.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.debug(f"Global SNMP service: {action.upper()} {kwargs.get('name')}")

        try:
            result = self.template.render_snmp_service(action=action, **kwargs)
            if action == "add":
                config_payload['snmps'].update(result)
            else:  # delete
                config_payload['snmps'][kwargs.get('name')] = {}
        except Exception as e:
            LOG.error(f"Failed to process global SNMP service {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Global SNMP service processing failed: {str(e)}")

    def global_syslog(self, config_payload, action="add", **kwargs):
        """
        Update the syslogServers section of configuration payload.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.debug(f"Global syslog service: {action.upper()} {kwargs.get('name')}")

        try:
            # Convert lanSegment to vrfId if present
            if 'target' in kwargs and 'lanSegment' in kwargs['target']:
                lan_segment = kwargs['target']['lanSegment']
                vrf_id = self.gsdk.get_lan_segment_id(lan_segment)
                kwargs['target']['vrfId'] = vrf_id
                del kwargs['target']['lanSegment']
                LOG.debug(f"Converted lanSegment '{lan_segment}' to vrfId {vrf_id}")

            result = self.template.render_syslog_service(action=action, **kwargs)
            if action == "add":
                config_payload['syslog_servers'].update(result)
            else:  # delete
                config_payload['syslog_servers'][kwargs.get('name')] = {}
        except Exception as e:
            LOG.error(f"Failed to process global syslog service {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Global syslog service processing failed: {str(e)}")

    def global_ipfix(self, config_payload, action="add", **kwargs):
        """
        Update the ipfixExporters section of configuration payload.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.debug(f"Global IPFIX service: {action.upper()} {kwargs.get('name')}")

        try:
            # Convert lanSegment to vrfId if present in exporter
            if 'exporter' in kwargs and 'lanSegment' in kwargs['exporter']:
                lan_segment = kwargs['exporter']['lanSegment']
                vrf_id = self.gsdk.get_lan_segment_id(lan_segment)
                kwargs['exporter']['vrfId'] = vrf_id
                del kwargs['exporter']['lanSegment']
                LOG.debug(f"Converted lanSegment '{lan_segment}' to vrfId {vrf_id}")

            result = self.template.render_ipfix_service(action=action, **kwargs)
            if action == "add":
                config_payload['ipfix_exporters'].update(result)
            else:  # delete
                config_payload['ipfix_exporters'][kwargs.get('name')] = {}
        except Exception as e:
            LOG.error(f"Failed to process global IPFIX service {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Global IPFIX service processing failed: {str(e)}")

    def global_vpn_profile(self, config_payload, action="add", **kwargs):
        """
        Update the vpnProfiles section of configuration payload.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.debug(f"Global VPN profile service: {action.upper()} {kwargs.get('name')}")

        try:
            # Pass the VPN config as a list to match the template expectation
            vpn_profiles_list = [kwargs]
            result = self.template.render_vpn_profile(vpn_profiles=vpn_profiles_list)

            if action == "add":
                # Extract the actual VPN profile data from the template result
                if 'vpn_profiles' in result:
                    config_payload['vpn_profiles'].update(result['vpn_profiles'])
                else:
                    LOG.warning(f"No vpn_profiles found in template result for {kwargs.get('name')}")
            else:  # delete
                name = kwargs.get('name')
                if name:
                    config_payload['vpn_profiles'][name] = {}
        except Exception as e:
            LOG.error(f"Failed to process global VPN profile service {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Global VPN profile service processing failed: {str(e)}")

    def global_site_list(self, config_payload, action="add", **kwargs):
        """
        Update the site_lists section of configuration payload.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Raises:
            ConfigurationError: If required parameters are missing.
        """
        self._validate_required_params(kwargs, ['name'])
        LOG.debug(f"Global site list: {action.upper()} {kwargs.get('name')}")

        try:
            if action == "add":
                # Use template for complex payload generation
                result = self.template.render_site_list(action=action, **kwargs)
                config_payload['site_lists'].update(result)
            else:  # delete
                # Simple delete logic in code
                name = kwargs.get('name')
                if name:
                    config_payload['site_lists'][name] = {}
        except Exception as e:
            LOG.error(f"Failed to process global site list {kwargs.get('name')}: {str(e)}")
            raise ConfigurationError(f"Global site list processing failed: {str(e)}")
