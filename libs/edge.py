from libs.edge_utils import EdgeUtils
from libs.logger import setup_logger

LOG = setup_logger()


class Edge(EdgeUtils):

    def __init__(self, base_url=None, username=None, password=None, **kwargs):
        super().__init__(base_url=base_url, username=username, password=password, **kwargs)

    def configure_global_config_prefix_lists(self, config_yaml_file):
        """
        Configures Global prefix sets based on the provided YAML configuration file.

        This method reads the configuration file, parses the global prefix set entries,
        and constructs the payload using the Jinja2 templates and configure
        the global prefixes using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the
            global prefix set definitions.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        final_config_payload = {"global_prefix_sets": {}}
        config_payload = {}
        if 'global_prefix_sets' in config_data:
            config_payload.update({'global_prefix_sets': {}})
            for prefix_config in config_data.get('global_prefix_sets'):
                self.global_prefix_set(config_payload, action="add", **prefix_config)
            final_config_payload["global_prefix_sets"].update(config_payload)
        LOG.debug(f"configure_global_config_prefix_lists: \
                  final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.patch_global_config, final_config_payload)

    def deconfigure_global_config_prefix_lists(self, config_yaml_file):
        """
        Removes Global prefix sets based on the provided YAML configuration file.

        This method reads the YAML file, extracts global prefix set configurations, and
        constructs a payload using the Jinja2 templates to delete them from the system
        using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the global
            prefix set definitions to be removed.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        final_config_payload = {"global_config": {}}
        config_payload = {}
        if 'global_prefix_sets' in config_data:
            config_payload.update({'global_prefix_sets': {}})
            for prefix_config in config_data.get('global_prefix_sets'):
                self.global_prefix_set(config_payload, action="delete", **prefix_config)
            final_config_payload["global_config"].update(config_payload)
        LOG.debug(f"deconfigure_global_config_prefix_lists: \
                  final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.patch_global_config, final_config_payload)

    def configure_global_config_routing_policies(self, config_yaml_file):
        """
        Configures Global BGP routing filter policies using the provided YAML configuration file.

        This method parses the input YAML file to extract BGP routing filter policy definitions,
        builds the appropriate payload using the templates, and applies the configuration
        via the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing routing policy definitions.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        final_config_payload = {"global_config": {}}
        config_payload = {}
        if 'routing_policies' in config_data:
            config_payload.update({'routing_policies': {}})
            for policy_config in config_data.get('routing_policies'):
                self.global_bgp_filter(config_payload, action="add", **policy_config)
            final_config_payload["global_config"].update(config_payload)
        LOG.debug(f"configure_global_config_routing_policies: \
                  final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.patch_global_config, final_config_payload)

    def deconfigure_global_config_routing_policies(self, config_yaml_file):
        """
        Removes Global BGP routing filter policies using the provided YAML configuration file.

        This method parses the input YAML file to extract BGP routing policy definitions
        and constructs the payload using the templates to remove the specified policies
        using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing routing policy definitions.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        final_config_payload = {"global_config": {}}
        config_payload = {}
        if 'routing_policies' in config_data:
            config_payload.update({'routing_policies': {}})
            for policy_config in config_data.get('routing_policies'):
                self.global_bgp_filter(config_payload, action="delete", **policy_config)
            final_config_payload["global_config"].update(config_payload)
        LOG.debug(f"deconfigure_global_config_routing_policies: \
                  final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.patch_global_config, final_config_payload)

    def configure_bgp_peers(self, config_yaml_file):
        """
        Configures BGP peers based on the provided YAML configuration file
        concurrently across multiple devices

        This method parses the input YAML file to extract BGP Peers definition
        and constructs the payload using the templates and apply the configurations
        concurrently across multiple devices using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the BGP peering configurations.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        final_config_payload = {}
        if 'bgp_peering' in config_data:
            for device_config in config_data.get('bgp_peering'):
                for device_name, config in device_config.items():
                    device_id = self.get_device_id(device_name=device_name)
                    config_payload = {}
                    self.edge_bgp_peering(config_payload, **config)
                    final_config_payload[device_id] = {"device_id": device_id,
                                                       "edge": config_payload}
        LOG.debug(f"configure_bgp_peers: final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.put_device_config, final_config_payload)

    def detach_policies_from_bgp_peers(self, config_yaml_file):
        """
        Detach routing filter policies from BGP peers based on the provided YAML configuration
        file.

        This method parses the input YAML file to extract BGP Peers and policy definition
        and constructs the payload using the templates to detach the policies and apply the
        configurations concurrently across multiple devices using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the BGP peering configurations.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        final_config_payload = {}
        if 'bgp_peering' in config_data:
            for device_config in config_data.get('bgp_peering'):
                for device_name, config in device_config.items():
                    device_id = self.get_device_id(device_name=device_name)
                    config_payload = {}
                    self.edge_bgp_peering(config_payload, action="unlink", **config)
                    final_config_payload[device_id] = {"device_id": device_id,
                                                       "edge": config_payload}
        LOG.debug(f"detach_policies_from_bgp_peers: final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.put_device_config, final_config_payload)

    def deconfigure_bgp_peers(self, config_yaml_file):
        """
        Deconfigures BGP peers provided in configuration YAML file and
        apply them concurrently using GCSDK APIs across multiple devices.

        Args:
            config_yaml_file (str): Path to the YAML configuration file containing BGP peer
            configurations to be removed.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        final_config_payload = {}
        if 'bgp_peering' in config_data:
            for device_config in config_data.get('bgp_peering'):
                for device_name, config in device_config.items():
                    device_id = self.get_device_id(device_name=device_name)
                    config_payload = {}
                    self.edge_bgp_peering(config_payload, action="delete", **config)
                    final_config_payload[device_id] = {"device_id": device_id,
                                                       "edge": config_payload}
        LOG.debug(f"deconfigure_bgp_peers: final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.put_device_config, final_config_payload)

    def configure_interfaces(self, config_yaml_file):
        """
        Configures the interfaces/sub-interfaces for multiple devices concurrently
        as specified in the provided YAML file.

        Args:
            config_yaml_file (str): Path to the YAML file containing interface configurations.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        output_config = {}
        if 'interfaces' in config_data:
            for device_info in config_data.get("interfaces"):
                for device_name, config_list in device_info.items():
                    if device_id := self.get_device_id(device_name=device_name):
                        device_config = {"interfaces": {}, "circuits": {}}
                        for config in config_list:
                            self.edge_interface(device_config, action="add", **config)
                        output_config[device_id] = {"device_id": device_id,
                                                    "edge": device_config}
                    else:
                        LOG.error(f"configure_interfaces : \
                                  {device_name} unable to fetch device-id")
                        return
        self.concurrent_task_execution(self.gsdk.put_device_config, output_config)

    def deconfigure_interfaces(self, config_yaml_file):
        """
        Configures the interfaces/sub-interfaces into default_lan for multiple devices
        concurrently as specified in the provided YAML file.

        Args:
            config_yaml_file (str): Path to the YAML file containing interface configurations.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        output_config = {}
        default_lan = f'default-{self.get_enterprise_id()}'
        if 'interfaces' in config_data:
            for device_info in config_data.get("interfaces"):
                for device_name, config_list in device_info.items():
                    if device_id := self.get_device_id(device_name=device_name):
                        device_config = {"interfaces": {}, "circuits": {}}
                        for config in config_list:
                            self.edge_interface(device_config, action="delete",
                                                default_lan=default_lan, **config)
                        output_config[device_id] = {"device_id": device_id,
                                                    "edge": device_config}
                    else:
                        LOG.error(f"deconfigure_interfaces : \
                                  {device_name} unable to fetch device-id")
                        return
        self.concurrent_task_execution(self.gsdk.put_device_config, output_config)

    def configure_global_snmp_service(self, config_yaml_file):
        """
        Configures Global SNMP based on the provided YAML configuration file.

        This method reads the configuration file, parses the global SNMP entries,
        and constructs the payload using the Jinja2 templates and configure
        the global SNMP using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the
            global SNMP definitions.

        Returns:
            None
       """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return
        final_config_payload = {"snmps": {}}
        config_payload = {}
        if 'snmps' in config_data:
            config_payload.update({'snmps': {}})
            for snmp_config in config_data.get('snmps'):
                self.global_snmp(config_payload, action="add", **snmp_config)
            final_config_payload["snmps"].update(config_payload)
        LOG.debug(f"configure_global_snmp_service: \
                         final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.patch_global_config, final_config_payload)

    def deconfigure_global_snmp_service(self, config_yaml_file):
        """
        Removes Global SNMP services using the provided YAML configuration file.

        This method parses the input YAML file to extract SNMP service definitions
        and constructs the payload using the templates to remove the specified services
        using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing SNMP service definitions.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return
        final_config_payload = {"snmps": {}}
        config_payload = {}
        if 'snmps' in config_data:
            config_payload.update({'snmps': {}})
            for snmp_config in config_data.get('snmps'):
                self.global_snmp(config_payload, action="delete", **snmp_config)
            final_config_payload["snmps"].update(config_payload)
        LOG.debug(f"deconfigure_global_snmp_service: \
                  final_config_payload {final_config_payload}")
        self.concurrent_task_execution(self.gsdk.patch_global_config, final_config_payload)

    def configure_global_syslog_service(self, config_yaml_file):
        """
        Configures Global Syslog based on the provided YAML configuration file.

        This method reads the configuration file, parses the global syslog entries,
        and constructs the payload using the Jinja2 templates and configure
        the global syslog using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the
            global syslog definitions.

        Returns:
            None
       """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return
        final_config_payload = {"syslog_servers": {}}
        config_payload = {}
        if 'syslogServers' in config_data:
            config_payload.update({'syslogServers': {}})
            for syslog_config in config_data.get('syslogServers'):
                self.global_syslog(config_payload, action="add", **syslog_config)
            final_config_payload["syslog_servers"].update(config_payload.get('syslogServers', {}))
        LOG.debug(f"configure_global_syslog_service: final_config_payload {final_config_payload}")
        self.gsdk.patch_global_config(**final_config_payload)

    def deconfigure_global_syslog_service(self, config_yaml_file):
        """
        Removes Global Syslog services using the provided YAML configuration file.

        This method parses the input YAML file to extract syslog service definitions
        and constructs the payload using the templates to remove the specified services
        using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing syslog service definitions.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return
        final_config_payload = {"syslog_servers": {}}
        config_payload = {}
        if 'syslogServers' in config_data:
            config_payload.update({'syslogServers': {}})
            for syslog_config in config_data.get('syslogServers'):
                self.global_syslog(config_payload, action="delete", **syslog_config)
            final_config_payload["syslog_servers"].update(config_payload.get('syslogServers', {}))
        LOG.debug(f"deconfigure_global_syslog_service: \
                  final_config_payload {final_config_payload}")
        self.gsdk.patch_global_config(**final_config_payload)

    def configure_global_ipfix_service(self, config_yaml_file):
        """
        Configures Global IPFIX based on the provided YAML configuration file.

        This method reads the configuration file, parses the global IPFIX entries,
        and constructs the payload using the Jinja2 templates and configure
        the global IPFIX using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the
            global IPFIX definitions.

        Returns:
            None
       """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return
        final_config_payload = {"ipfix_exporters": {}}
        config_payload = {}
        if 'ipfixExporters' in config_data:
            config_payload.update({'ipfixExporters': {}})
            for ipfix_config in config_data.get('ipfixExporters'):
                self.global_ipfix(config_payload, action="add", **ipfix_config)
            final_config_payload["ipfix_exporters"].update(config_payload.get('ipfixExporters', {}))
        LOG.debug(f"configure_global_ipfix_service: \
                         final_config_payload {final_config_payload}")
        self.gsdk.patch_global_config(**final_config_payload)

    def deconfigure_global_ipfix_service(self, config_yaml_file):
        """
        Removes Global IPFIX services using the provided YAML configuration file.

        This method parses the input YAML file to extract IPFIX service definitions
        and constructs the payload using the templates to remove the specified services
        using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing IPFIX service definitions.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return
        final_config_payload = {"ipfix_exporters": {}}
        config_payload = {}
        if 'ipfixExporters' in config_data:
            config_payload.update({'ipfixExporters': {}})
            for ipfix_config in config_data.get('ipfixExporters'):
                self.global_ipfix(config_payload, action="delete", **ipfix_config)
            final_config_payload["ipfix_exporters"].update(config_payload.get('ipfixExporters', {}))
        LOG.debug(f"deconfigure_global_ipfix_service: \
                  final_config_payload {final_config_payload}")
        self.gsdk.patch_global_config(**final_config_payload)

    def configure_global_vpn_profile_service(self, config_yaml_file):
        """
        Configures Global VPN Profile based on the provided YAML configuration file.

        This method reads the configuration file, parses the global VPN profile entries,
        and constructs the payload using the Jinja2 templates and configure
        the global VPN profile using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing the
            global VPN profile definitions.

        Returns:
            None
       """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return

        final_config_payload = {"vpnProfiles": {}}
        config_payload = {}
        if 'vpnProfiles' in config_data:
            config_payload.update({'vpnProfiles': {}})
            for vpn_config in config_data.get('vpnProfiles'):
                self.global_vpn_profile(config_payload, action="add", **vpn_config)
            # Fix the nested structure and convert camelCase to snake_case for API
            final_config_payload = {}
            if 'vpnProfiles' in config_payload:
                final_config_payload['vpn_profiles'] = config_payload['vpnProfiles']
        LOG.debug(f"configure_global_vpn_profile_service: \
                         final_config_payload {final_config_payload}")
        self.gsdk.patch_global_config(**final_config_payload)

    def deconfigure_global_vpn_profile_service(self, config_yaml_file):
        """
        Removes Global VPN Profile services using the provided YAML configuration file.

        This method parses the input YAML file to extract VPN profile service definitions
        and constructs the payload using the templates to remove the specified services
        using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing VPN profile service definitions.

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return
        final_config_payload = {"vpnProfiles": {}}
        config_payload = {}
        if 'vpnProfiles' in config_data:
            config_payload.update({'vpnProfiles': {}})
            for vpn_config in config_data.get('vpnProfiles'):
                self.global_vpn_profile(config_payload, action="delete", **vpn_config)
            # Fix the nested structure and convert camelCase to snake_case for API
            final_config_payload = {}
            if 'vpnProfiles' in config_payload:
                final_config_payload['vpn_profiles'] = config_payload['vpnProfiles']
        LOG.debug(f"deconfigure_global_vpn_profile_service: \
                  final_config_payload {final_config_payload}")
        self.gsdk.patch_global_config(**final_config_payload)

    def manage_global_system_objects_on_site(self, config_yaml_file, operation="attach"):
        """
        Manages global system objects (SNMP, Syslog, IPFIX, VPN profiles) on sites
        based on the provided YAML configuration file. Supports both attach and detach operations.

        This method reads the configuration file, parses the site management entries,
        and constructs the payload to attach or detach global system objects to/from specific sites
        using the GCSDK APIs.

        Args:
            config_yaml_file (str): Path to the YAML file containing site management definitions.
            operation (str): Operation to perform - "attach" or "detach". Defaults to "attach".

        Returns:
            None
        """
        config_data = self.render_config_file(yaml_file=config_yaml_file)
        if config_data is None:
            LOG.error(f"Failed to load configuration file: {config_yaml_file}")
            return

        default_operation = 'Attach' if operation.lower() == "attach" else 'Detach'

        if 'site_attachments' in config_data:
            for site_config in config_data.get('site_attachments'):
                # Get the site name from the first (and only) key in the site config
                site_name = list(site_config.keys())[0]
                site_data = site_config[site_name]
                if site_id := self.get_site_id(site_name=site_name):
                    site_payload = {"site": {"name": site_name}}

                    # Handle SNMP operations
                    if 'snmpServers' in site_data:
                        site_payload['site']['snmpOps'] = {}
                        for snmp_name in site_data.get('snmpServers'):
                            site_payload['site']['snmpOps'][snmp_name] = default_operation

                    # Handle Syslog operations
                    if 'syslogServers' in site_data:
                        site_payload['site']['syslogServerOpsV2'] = {}
                        for syslog_config in site_data.get('syslogServers'):
                            # Handle both string format (backward compatibility) and object format
                            if isinstance(syslog_config, str):
                                syslog_name = syslog_config
                                site_payload['site']['syslogServerOpsV2'][syslog_name] = {
                                    "operation": default_operation
                                }
                            else:
                                syslog_name = syslog_config.get('name')
                                interface = syslog_config.get('interface')
                                site_payload['site']['syslogServerOpsV2'][syslog_name] = {
                                    "operation": default_operation,
                                    "interface": {
                                        "interface": interface
                                    }
                                }

                    # Handle IPFIX operations
                    if 'ipfixExporters' in site_data:
                        site_payload['site']['ipfixExporterOpsV2'] = {}
                        for ipfix_config in site_data.get('ipfixExporters'):
                            # Handle both string format (backward compatibility) and object format
                            if isinstance(ipfix_config, str):
                                ipfix_name = ipfix_config
                                site_payload['site']['ipfixExporterOpsV2'][ipfix_name] = {
                                    "operation": default_operation
                                }
                            else:
                                ipfix_name = ipfix_config.get('name')
                                interface = ipfix_config.get('interface')
                                site_payload['site']['ipfixExporterOpsV2'][ipfix_name] = {
                                    "operation": default_operation,
                                    "interface": {
                                        "interface": interface
                                    }
                                }

                    # Use the sites API instead of device config API
                    self.gsdk.post_site_config(site_id=site_id, site_config=site_payload)
                else:
                    LOG.error(f"manage_global_system_objects_on_site: {site_name} unable to fetch device-id")
                    return

        LOG.debug(f"manage_global_system_objects_on_site ({operation}): completed successfully")
