from libs.portal_utils import PortalUtils
from libs.edge_templates import EdgeTemplates
from libs.logger import setup_logger

LOG = setup_logger()


class EdgeUtils(PortalUtils):

    def __init__(self, base_url=None, username=None, password=None, **kwargs):
        super().__init__(base_url=base_url, username=username, password=password, **kwargs)
        self.template = EdgeTemplates(self.templates)

    def global_prefix_set(self, config_payload, action="add", **kwargs):
        """
        Updates the global_prefix_sets section of configuration payload(config_payload)
        using a rendered template.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Returns:
            None: The global_prefix_sets section in config_payload dict is updated.
        """
        LOG.debug(f"global_prefix_set : {action.upper()} Global Prefix Set {kwargs.get('name')}")
        global_prefix_set = self.template._global_prefix_set(action=action, **kwargs)
        config_payload['global_prefix_sets'].update(global_prefix_set)

    def global_bgp_filter(self, config_payload, action="add", **kwargs):
        """
        Updates the routing_policies section of the configuration payload(config_payload)
        using the rendered template.

        Args:
            config_payload (dict): The configuration dictionary that holds routing policies.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional parameters used for rendering the template.

        Returns:
            None: The routing_policies section in config_payload is updated in-place.
        """
        LOG.debug(f"global_bgp_filter : {action.upper()} Global BGP Filter {kwargs.get('name')}")
        global_bgp_filter = self.template._global_bgp_filter(action=action, **kwargs)
        config_payload['routing_policies'].update(global_bgp_filter)

    def edge_bgp_peering(self, config_payload, action="add", **kwargs):
        """
        Updates the edge_bgp_peering section of configuration payload(config_payload)
        using a rendered template.

        Args:
            config_payload (dict): Dictionary to be updated with BGP peering configuration.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional parameters used for rendering the BGP peering configuration.

        Returns:
            None: The edge_bgp_peering section in config_payload is modified in-place.
        """
        global_ids = {}
        LOG.info(f"edge_bgp_peering : config_payload {config_payload}")
        if kwargs.get("route_policies"):
            for policy_name in kwargs.get("route_policies"):
                global_ids[policy_name] = self.get_global_routing_policy_id(policy_name)
                LOG.debug(f"edge_bgp_peering : Global ID for {policy_name} : {global_ids[policy_name]}")
        LOG.debug(f"edge_bgp_peering : {action.upper()} BGP Peering :\n {kwargs}")
        bgp_peering = self.template._edge_bgp_peering(action=action, global_ids=global_ids, **kwargs)
        config_payload.update(bgp_peering)

    def edge_interface(self, config_payload, action="add", **kwargs):
        """
        Updates the edge interfaces/circuits section of the configuration payload(config_payload)
        using a rendered template.

        Args:
            config_payload (dict): Dictionary to be updated with interface and circuit data.
            action (str, optional): Action to perform, either "add" or "default_lan" or "delete".
            Defaults to "add".
            **kwargs: Additional parameters passed to the template renderer.

        Returns:
            None: The interfaces and circuits section in config_payload is modified in-place.
        """
        LOG.debug(f"edge_interfaces : {action.upper()} Edge Interfaces :\n {kwargs}")
        interface = self.template._edge_interface(action=action, **kwargs)
        config_payload["interfaces"].update(interface.get("interfaces"))
        if interface.get('circuits'):
            config_payload['circuits'].update(interface.get("circuits"))

    def global_snmp(self, config_payload, action="add", **kwargs):
        """
        Updates the global_snmp_service section of configuration payload(config_payload)
        using a rendered template.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Returns:
            None: The gobal_snmp_service section in config_payload dict is updated.
        """
        LOG.debug(f"global_snmp_service : {action.upper()} Global SNMP Service {kwargs.get('name')}")
        global_snmp_service = self.template._global_snmps_service(action=action, **kwargs)
        if action == "add":
            config_payload['snmps'].update(global_snmp_service)
        else:  # delete
            config_payload['snmps'][kwargs.get('name')] = {}

    def global_syslog(self, config_payload, action="add", **kwargs):
        """
        Updates the syslogServers section of configuration payload(config_payload)
        using a rendered template.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Returns:
            None: The syslogServers section in config_payload dict is updated.
        """
        LOG.info(f"global_syslog_service : {action.upper()} Global Syslog Service {kwargs.get('name')}")
        LOG.info(f"global_syslog_service : kwargs received: {kwargs}")

        # Convert lanSegment to vrfId if present
        if 'target' in kwargs and 'lanSegment' in kwargs['target']:
            lan_segment = kwargs['target']['lanSegment']
            vrf_id = self.get_lan_segment_id(lan_segment)
            kwargs['target']['vrfId'] = vrf_id
            del kwargs['target']['lanSegment']
            LOG.info(f"global_syslog_service : converted lanSegment '{lan_segment}' to vrfId {vrf_id}")

        global_syslog_service = self.template._global_syslog_service(action=action, **kwargs)
        LOG.info(f"global_syslog_service : template result: {global_syslog_service}")
        if action == "add":
            config_payload['syslogServers'].update(global_syslog_service)
            LOG.info(f"global_syslog_service : config_payload after update: {config_payload}")
        else:  # delete
            config_payload['syslogServers'][kwargs.get('name')] = {}

    def global_ipfix(self, config_payload, action="add", **kwargs):
        """
        Updates the ipfixExporters section of configuration payload(config_payload)
        using a rendered template.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Returns:
            None: The ipfixExporters section in config_payload dict is updated.
        """
        LOG.info(f"global_ipfix_service : {action.upper()} Global IPFIX Service {kwargs.get('name')}")
        LOG.info(f"global_ipfix_service : kwargs received: {kwargs}")

        # Convert lanSegment to vrfId if present in exporter
        if 'exporter' in kwargs and 'lanSegment' in kwargs['exporter']:
            lan_segment = kwargs['exporter']['lanSegment']
            vrf_id = self.get_lan_segment_id(lan_segment)
            kwargs['exporter']['vrfId'] = vrf_id
            del kwargs['exporter']['lanSegment']
            LOG.info(f"global_ipfix_service : converted lanSegment '{lan_segment}' to vrfId {vrf_id}")

        global_ipfix_service = self.template._global_ipfix_service(action=action, **kwargs)
        LOG.info(f"global_ipfix_service : template result: {global_ipfix_service}")
        if action == "add":
            config_payload['ipfixExporters'].update(global_ipfix_service)
            LOG.info(f"global_ipfix_service : config_payload after update: {config_payload}")
        else:  # delete
            config_payload['ipfixExporters'][kwargs.get('name')] = {}

    def global_vpn_profile(self, config_payload, action="add", **kwargs):
        """
        Updates the vpnProfiles section of configuration payload(config_payload)
        using a rendered template.

        Args:
            config_payload (dict): The main configuration payload dict to be updated.
            action (str, optional): Action to perform, either "add" or "delete". Defaults to "add".
            **kwargs: Additional key-value pairs required for rendering the template.

        Returns:
            None: The vpnProfiles section in config_payload dict is updated.
        """
        LOG.debug(f"global_vpn_profile_service : {action.upper()} Global VPN Profile Service {kwargs.get('name')}")

        # Pass the VPN config as a list to match the template expectation
        vpn_profiles_list = [kwargs]
        global_vpn_profile_service = self.template._global_vpn_profile_service(vpnProfiles=vpn_profiles_list)

        if action == "add":
            # Extract the actual VPN profile data from the template result
            if 'vpnProfiles' in global_vpn_profile_service:
                vpn_profiles_data = global_vpn_profile_service['vpnProfiles']
                config_payload['vpnProfiles'].update(vpn_profiles_data)
            else:
                LOG.error("global_vpn_profile_service : No vpnProfiles in template result")
        else:  # delete
            config_payload['vpnProfiles'][kwargs.get('name')] = {}
