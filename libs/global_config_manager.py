"""
Global Configuration Manager for Graphiant Playbooks.

This module handles global configuration management including
prefix sets, routing policies, SNMP, syslog, IPFIX, and VPN profiles.
"""

from libs.base_manager import BaseManager
from libs.logger import setup_logger
from libs.exceptions import ConfigurationError

LOG = setup_logger()


class GlobalConfigManager(BaseManager):
    """
    Manages global configuration objects.

    Handles the configuration and deconfiguration of global objects
    such as prefix sets, routing policies, and system services.
    """

    def configure(self, config_yaml_file: str) -> None:
        """
        Configure global objects based on the provided YAML file.

        This method handles the configuration of all global objects including:
        - Prefix sets (global_prefix_sets)
        - BGP filters (routing_policies)
        - SNMP global objects (snmps)
        - Syslog global objects (syslog_servers)
        - IPFIX global objects (ipfix_exporters)
        - VPN profile global objects (vpn_profiles)

        Args:
            config_yaml_file: Path to the YAML file containing global configurations

        Raises:
            ConfigurationError: If configuration processing fails
        """
        try:
            config_data = self.render_config_file(config_yaml_file)

            # Configure prefix sets
            if 'global_prefix_sets' in config_data:
                self.configure_prefix_sets(config_data['global_prefix_sets'])

            # Configure routing policies (BGP filters)
            if 'routing_policies' in config_data:
                self.configure_bgp_filters(config_data['routing_policies'])

            # Configure SNMP global objects (SNMPv3 NoAuthNoPriv, SNMPv3 AuthNoPriv, SNMPv3 AuthPriv, SNMPv2c)
            if 'snmps' in config_data:
                self.configure_snmp_services(config_data['snmps'])

            # Configure syslog global objects (Global Syslog Server)
            if 'syslog_servers' in config_data:
                self.configure_syslog_services(config_data['syslog_servers'])

            # Configure IPFIX global objects (Global IPFIX Exporter)
            if 'ipfix_exporters' in config_data:
                self.configure_ipfix_services(config_data['ipfix_exporters'])

            # Configure VPN profiles (Global VPN Profile)
            if 'vpn_profiles' in config_data:
                self.configure_vpn_profiles(config_data['vpn_profiles'])

        except Exception as e:
            LOG.error(f"Error in global configuration: {str(e)}")
            raise ConfigurationError(f"Global configuration failed: {str(e)}")

    def deconfigure(self, config_yaml_file: str) -> None:
        """
        Deconfigure global objects based on the provided YAML file.

        This method handles the deconfiguration of all global objects including:
        - Prefix sets (global_prefix_sets)
        - BGP filters (routing_policies)
        - SNMP global objects (snmps)
        - Syslog global objects (syslog_servers)
        - IPFIX global objects (ipfix_exporters)
        - VPN profile global objects (vpn_profiles)

        Args:
            config_yaml_file: Path to the YAML file containing global configurations

        Raises:
            ConfigurationError: If configuration processing fails
        """
        try:
            config_data = self.render_config_file(config_yaml_file)

            # Deconfigure prefix sets (Global Prefix Sets)
            if 'global_prefix_sets' in config_data:
                self.deconfigure_prefix_sets(config_data['global_prefix_sets'])

            # Deconfigure routing policies (BGP filters)
            if 'routing_policies' in config_data:
                self.deconfigure_bgp_filters(config_data['routing_policies'])

            # Deconfigure SNMP global objects (SNMPv3 NoAuthNoPriv, SNMPv3 AuthNoPriv, SNMPv3 AuthPriv, SNMPv2c)
            if 'snmps' in config_data:
                self.deconfigure_snmp_services(config_data['snmps'])

            # Deconfigure syslog global objects (Global Syslog Server)
            if 'syslog_servers' in config_data:
                self.deconfigure_syslog_services(config_data['syslog_servers'])

            # Deconfigure IPFIX global objects (Global IPFIX Exporter)
            if 'ipfix_exporters' in config_data:
                self.deconfigure_ipfix_services(config_data['ipfix_exporters'])

            # Deconfigure VPN profile global objects (Global VPN Profile)
            if 'vpn_profiles' in config_data:
                self.deconfigure_vpn_profiles(config_data['vpn_profiles'])

        except Exception as e:
            LOG.error(f"Error in global deconfiguration: {str(e)}")
            raise ConfigurationError(f"Global deconfiguration failed: {str(e)}")

    def configure_prefix_sets(self, prefix_sets: list) -> None:
        """Configure global prefix sets.

        Args:
            prefix_sets: List of prefix set configurations
        """
        config_payload = {"global_prefix_sets": {}}

        for prefix_config in prefix_sets:
            self.edge_utils.global_prefix_set(config_payload, action="add", **prefix_config)

        LOG.info(f"Configure prefix sets payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully configured {len(prefix_sets)} prefix sets")

    def deconfigure_prefix_sets(self, prefix_sets: list) -> None:
        """Deconfigure global prefix sets.

        Args:
            prefix_sets: List of prefix set configurations to remove
        """
        config_payload = {"global_prefix_sets": {}}

        for prefix_config in prefix_sets:
            self.edge_utils.global_prefix_set(config_payload, action="delete", **prefix_config)

        LOG.info(f"Deconfigure prefix sets payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully deconfigured {len(prefix_sets)} prefix sets")

    def configure_bgp_filters(self, routing_policies: list) -> None:
        """Configure global BGP filters.

        Args:
            routing_policies: List of BGP filter configurations
        """
        config_payload = {"routing_policies": {}}

        for policy_config in routing_policies:
            self.edge_utils.global_bgp_filter(config_payload, action="add", **policy_config)

        LOG.info(f"Configure BGP filters payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully configured {len(routing_policies)} BGP filters")

    def deconfigure_bgp_filters(self, routing_policies: list) -> None:
        """Deconfigure global BGP filters.

        Args:
            routing_policies: List of BGP filter configurations to remove
        """
        config_payload = {"routing_policies": {}}

        for policy_config in routing_policies:
            self.edge_utils.global_bgp_filter(config_payload, action="delete", **policy_config)

        LOG.info(f"Deconfigure BGP filters payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully deconfigured {len(routing_policies)} BGP filters")

    def configure_snmp_services(self, snmp_services: list) -> None:
        """Configure global SNMP services.

        Args:
            snmp_services: List of SNMP service configurations
        """
        config_payload = {"snmps": {}}

        for snmp_config in snmp_services:
            self.edge_utils.global_snmp(config_payload, action="add", **snmp_config)

        LOG.debug(f"Configure SNMP services payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully configured {len(snmp_services)} SNMP global objects")

    def deconfigure_snmp_services(self, snmp_services: list) -> None:
        """Deconfigure global SNMP services.

        Args:
            snmp_services: List of SNMP service configurations to remove
        """
        config_payload = {"snmps": {}}

        for snmp_config in snmp_services:
            self.edge_utils.global_snmp(config_payload, action="delete", **snmp_config)

        LOG.debug(f"Deconfigure SNMP services payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully deconfigured {len(snmp_services)} SNMP global objects")

    def configure_syslog_services(self, syslog_services: list) -> None:
        """Configure global syslog services.

        Args:
            syslog_services: List of syslog service configurations
        """
        config_payload = {"syslog_servers": {}}

        for syslog_config in syslog_services:
            self.edge_utils.global_syslog(config_payload, action="add", **syslog_config)

        LOG.debug(f"Configure syslog services payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully configured {len(syslog_services)} syslog global objects")

    def deconfigure_syslog_services(self, syslog_services: list) -> None:
        """Deconfigure global syslog services.

        Args:
            syslog_services: List of syslog service configurations to remove
        """
        config_payload = {"syslog_servers": {}}

        for syslog_config in syslog_services:
            self.edge_utils.global_syslog(config_payload, action="delete", **syslog_config)

        LOG.debug(f"Deconfigure syslog services payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully deconfigured {len(syslog_services)} syslog global objects")

    def configure_ipfix_services(self, ipfix_services: list) -> None:
        """Configure global IPFIX services.

        Args:
            ipfix_services: List of IPFIX service configurations
        """
        config_payload = {"ipfix_exporters": {}}

        for ipfix_config in ipfix_services:
            self.edge_utils.global_ipfix(config_payload, action="add", **ipfix_config)

        LOG.debug(f"Configure IPFIX services payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully configured {len(ipfix_services)} IPFIX global objects")

    def deconfigure_ipfix_services(self, ipfix_services: list) -> None:
        """Deconfigure global IPFIX services.

        Args:
            ipfix_services: List of IPFIX service configurations to remove
        """
        config_payload = {"ipfix_exporters": {}}

        for ipfix_config in ipfix_services:
            self.edge_utils.global_ipfix(config_payload, action="delete", **ipfix_config)

        LOG.debug(f"Deconfigure IPFIX services payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully deconfigured {len(ipfix_services)} IPFIX global objects")

    def configure_vpn_profiles(self, vpn_profiles: list) -> None:
        """Configure global VPN profiles.

        Args:
            vpn_profiles: List of VPN profile configurations
        """
        config_payload = {"vpn_profiles": {}}

        for vpn_config in vpn_profiles:
            self.edge_utils.global_vpn_profile(config_payload, action="add", **vpn_config)

        LOG.info(f"Configure VPN profiles payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)
        LOG.info(f"Successfully configured {len(vpn_profiles)} VPN profiles")

    def deconfigure_vpn_profiles(self, vpn_profiles: list) -> None:
        """Deconfigure global VPN profiles.

        Args:
            vpn_profiles: List of VPN profile configurations to remove
        """
        config_payload = {"vpn_profiles": {}}

        for vpn_config in vpn_profiles:
            self.edge_utils.global_vpn_profile(config_payload, action="delete", **vpn_config)

        LOG.debug(f"Deconfigure VPN profiles payload: {config_payload}")
        self.gsdk.patch_global_config(**config_payload)

        LOG.info(f"Successfully deconfigured {len(vpn_profiles)} VPN profiles")
