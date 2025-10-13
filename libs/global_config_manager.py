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
                self.configure_prefix_sets(config_yaml_file)

            # Configure routing policies (BGP filters)
            if 'routing_policies' in config_data:
                self.configure_bgp_filters(config_yaml_file)

            # Configure SNMP global objects (SNMPv3 NoAuthNoPriv, SNMPv3 AuthNoPriv, SNMPv3 AuthPriv, SNMPv2c)
            if 'snmps' in config_data:
                self.configure_snmp_services(config_yaml_file)

            # Configure syslog global objects (Global Syslog Server)
            if 'syslog_servers' in config_data:
                self.configure_syslog_services(config_yaml_file)

            # Configure IPFIX global objects (Global IPFIX Exporter)
            if 'ipfix_exporters' in config_data:
                self.configure_ipfix_services(config_yaml_file)

            # Configure VPN profiles (Global VPN Profile)
            if 'vpn_profiles' in config_data:
                self.configure_vpn_profiles(config_yaml_file)

            # Configure LAN segments (Global LAN Segments)
            if 'lan_segments' in config_data:
                self.configure_lan_segments(config_yaml_file)

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
                self.deconfigure_prefix_sets(config_yaml_file)

            # Deconfigure routing policies (BGP filters)
            if 'routing_policies' in config_data:
                self.deconfigure_bgp_filters(config_yaml_file)

            # Deconfigure SNMP global objects (SNMPv3 NoAuthNoPriv, SNMPv3 AuthNoPriv, SNMPv3 AuthPriv, SNMPv2c)
            if 'snmps' in config_data:
                self.deconfigure_snmp_services(config_yaml_file)

            # Deconfigure syslog global objects (Global Syslog Server)
            if 'syslog_servers' in config_data:
                self.deconfigure_syslog_services(config_yaml_file)

            # Deconfigure IPFIX global objects (Global IPFIX Exporter)
            if 'ipfix_exporters' in config_data:
                self.deconfigure_ipfix_services(config_yaml_file)

            # Deconfigure VPN profile global objects (Global VPN Profile)
            if 'vpn_profiles' in config_data:
                self.deconfigure_vpn_profiles(config_yaml_file)

            # Deconfigure LAN segments (Global LAN Segments)
            if 'lan_segments' in config_data:
                self.deconfigure_lan_segments(config_yaml_file)

        except Exception as e:
            LOG.error(f"Error in global deconfiguration: {str(e)}")
            raise ConfigurationError(f"Global deconfiguration failed: {str(e)}")

    def configure_prefix_sets(self, config_yaml_file: str) -> None:
        """Configure global prefix sets.

        Args:
            config_yaml_file: Path to the YAML file containing prefix set configurations
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            prefix_sets = config_data.get('global_prefix_sets', [])

            if not prefix_sets:
                LOG.info("No prefix sets found in configuration file")
                return

            config_payload = {"global_prefix_sets": {}}

            for prefix_config in prefix_sets:
                self.edge_utils.global_prefix_set(config_payload, action="add", **prefix_config)

            LOG.info(f"Configure prefix sets payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully configured {len(prefix_sets)} prefix sets")
        except Exception as e:
            LOG.error(f"Failed to configure prefix sets: {e}")
            raise ConfigurationError(f"Prefix sets configuration failed: {e}")

    def deconfigure_prefix_sets(self, config_yaml_file: str) -> None:
        """Deconfigure global prefix sets.

        Args:
            config_yaml_file: Path to the YAML file containing prefix set configurations to remove
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            prefix_sets = config_data.get('global_prefix_sets', [])

            if not prefix_sets:
                LOG.info("No prefix sets found in configuration file")
                return

            config_payload = {"global_prefix_sets": {}}

            for prefix_config in prefix_sets:
                self.edge_utils.global_prefix_set(config_payload, action="delete", **prefix_config)

            LOG.info(f"Deconfigure prefix sets payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully deconfigured {len(prefix_sets)} prefix sets")
        except Exception as e:
            LOG.error(f"Failed to deconfigure prefix sets: {e}")
            raise ConfigurationError(f"Prefix sets deconfiguration failed: {e}")

    def configure_bgp_filters(self, config_yaml_file: str) -> None:
        """Configure global BGP filters.

        Args:
            config_yaml_file: Path to the YAML file containing BGP filter configurations
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            routing_policies = config_data.get('routing_policies', [])

            if not routing_policies:
                LOG.info("No BGP filters found in configuration file")
                return

            config_payload = {"routing_policies": {}}

            for policy_config in routing_policies:
                self.edge_utils.global_bgp_filter(config_payload, action="add", **policy_config)

            LOG.info(f"Configure BGP filters payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully configured {len(routing_policies)} BGP filters")
        except Exception as e:
            LOG.error(f"Failed to configure BGP filters: {e}")
            raise ConfigurationError(f"BGP filters configuration failed: {e}")

    def deconfigure_bgp_filters(self, config_yaml_file: str) -> None:
        """Deconfigure global BGP filters.

        Args:
            config_yaml_file: Path to the YAML file containing BGP filter configurations to remove
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            routing_policies = config_data.get('routing_policies', [])

            if not routing_policies:
                LOG.info("No BGP filters found in configuration file")
                return

            config_payload = {"routing_policies": {}}

            for policy_config in routing_policies:
                self.edge_utils.global_bgp_filter(config_payload, action="delete", **policy_config)

            LOG.info(f"Deconfigure BGP filters payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully deconfigured {len(routing_policies)} BGP filters")
        except Exception as e:
            LOG.error(f"Failed to deconfigure BGP filters: {e}")
            raise ConfigurationError(f"BGP filters deconfiguration failed: {e}")

    def configure_snmp_services(self, config_yaml_file: str) -> None:
        """Configure global SNMP services.

        Args:
            config_yaml_file: Path to the YAML file containing SNMP service configurations
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            snmp_services = config_data.get('snmps', [])

            if not snmp_services:
                LOG.info("No SNMP services found in configuration file")
                return

            config_payload = {"snmps": {}}

            for snmp_config in snmp_services:
                self.edge_utils.global_snmp(config_payload, action="add", **snmp_config)

            LOG.debug(f"Configure SNMP services payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully configured {len(snmp_services)} SNMP global objects")
        except Exception as e:
            LOG.error(f"Failed to configure SNMP services: {e}")
            raise ConfigurationError(f"SNMP services configuration failed: {e}")

    def deconfigure_snmp_services(self, config_yaml_file: str) -> None:
        """Deconfigure global SNMP services.

        Args:
            config_yaml_file: Path to the YAML file containing SNMP service configurations to remove
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            snmp_services = config_data.get('snmps', [])

            if not snmp_services:
                LOG.info("No SNMP services found in configuration file")
                return

            config_payload = {"snmps": {}}

            for snmp_config in snmp_services:
                self.edge_utils.global_snmp(config_payload, action="delete", **snmp_config)

            LOG.debug(f"Deconfigure SNMP services payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully deconfigured {len(snmp_services)} SNMP global objects")
        except Exception as e:
            LOG.error(f"Failed to deconfigure SNMP services: {e}")
            raise ConfigurationError(f"SNMP services deconfiguration failed: {e}")

    def configure_syslog_services(self, config_yaml_file: str) -> None:
        """Configure global syslog services.

        Args:
            config_yaml_file: Path to the YAML file containing syslog service configurations
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            syslog_services = config_data.get('syslog_servers', [])

            if not syslog_services:
                LOG.info("No syslog services found in configuration file")
                return

            config_payload = {"syslog_servers": {}}

            for syslog_config in syslog_services:
                self.edge_utils.global_syslog(config_payload, action="add", **syslog_config)

            LOG.debug(f"Configure syslog services payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully configured {len(syslog_services)} syslog global objects")
        except Exception as e:
            LOG.error(f"Failed to configure syslog services: {e}")
            raise ConfigurationError(f"Syslog services configuration failed: {e}")

    def deconfigure_syslog_services(self, config_yaml_file: str) -> None:
        """Deconfigure global syslog services.

        Args:
            config_yaml_file: Path to the YAML file containing syslog service configurations to remove
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            syslog_services = config_data.get('syslog_servers', [])

            if not syslog_services:
                LOG.info("No syslog services found in configuration file")
                return

            config_payload = {"syslog_servers": {}}

            for syslog_config in syslog_services:
                self.edge_utils.global_syslog(config_payload, action="delete", **syslog_config)

            LOG.debug(f"Deconfigure syslog services payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully deconfigured {len(syslog_services)} syslog global objects")
        except Exception as e:
            LOG.error(f"Failed to deconfigure syslog services: {e}")
            raise ConfigurationError(f"Syslog services deconfiguration failed: {e}")

    def configure_ipfix_services(self, config_yaml_file: str) -> None:
        """Configure global IPFIX services.

        Args:
            config_yaml_file: Path to the YAML file containing IPFIX service configurations
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            ipfix_services = config_data.get('ipfix_exporters', [])

            if not ipfix_services:
                LOG.info("No IPFIX services found in configuration file")
                return

            config_payload = {"ipfix_exporters": {}}

            for ipfix_config in ipfix_services:
                self.edge_utils.global_ipfix(config_payload, action="add", **ipfix_config)

            LOG.debug(f"Configure IPFIX services payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully configured {len(ipfix_services)} IPFIX global objects")
        except Exception as e:
            LOG.error(f"Failed to configure IPFIX services: {e}")
            raise ConfigurationError(f"IPFIX services configuration failed: {e}")

    def deconfigure_ipfix_services(self, config_yaml_file: str) -> None:
        """Deconfigure global IPFIX services.

        Args:
            config_yaml_file: Path to the YAML file containing IPFIX service configurations to remove
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            ipfix_services = config_data.get('ipfix_exporters', [])

            if not ipfix_services:
                LOG.info("No IPFIX services found in configuration file")
                return

            config_payload = {"ipfix_exporters": {}}

            for ipfix_config in ipfix_services:
                self.edge_utils.global_ipfix(config_payload, action="delete", **ipfix_config)

            LOG.debug(f"Deconfigure IPFIX services payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully deconfigured {len(ipfix_services)} IPFIX global objects")
        except Exception as e:
            LOG.error(f"Failed to deconfigure IPFIX services: {e}")
            raise ConfigurationError(f"IPFIX services deconfiguration failed: {e}")

    def configure_vpn_profiles(self, config_yaml_file: str) -> None:
        """Configure global VPN profiles.

        Args:
            config_yaml_file: Path to the YAML file containing VPN profile configurations
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            vpn_profiles = config_data.get('vpn_profiles', [])

            if not vpn_profiles:
                LOG.info("No VPN profiles found in configuration file")
                return

            config_payload = {"vpn_profiles": {}}

            for vpn_config in vpn_profiles:
                self.edge_utils.global_vpn_profile(config_payload, action="add", **vpn_config)

            LOG.info(f"Configure VPN profiles payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully configured {len(vpn_profiles)} VPN profiles")
        except Exception as e:
            LOG.error(f"Failed to configure VPN profiles: {e}")
            raise ConfigurationError(f"VPN profiles configuration failed: {e}")

    def deconfigure_vpn_profiles(self, config_yaml_file: str) -> None:
        """Deconfigure global VPN profiles.

        Args:
            config_yaml_file: Path to the YAML file containing VPN profile configurations to remove
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            vpn_profiles = config_data.get('vpn_profiles', [])

            if not vpn_profiles:
                LOG.info("No VPN profiles found in configuration file")
                return

            config_payload = {"vpn_profiles": {}}

            for vpn_config in vpn_profiles:
                self.edge_utils.global_vpn_profile(config_payload, action="delete", **vpn_config)

            LOG.debug(f"Deconfigure VPN profiles payload: {config_payload}")
            self.gsdk.patch_global_config(**config_payload)
            LOG.info(f"Successfully deconfigured {len(vpn_profiles)} VPN profiles")
        except Exception as e:
            LOG.error(f"Failed to deconfigure VPN profiles: {e}")
            raise ConfigurationError(f"VPN profiles deconfiguration failed: {e}")

    def configure_lan_segments(self, config_yaml_file: str) -> None:
        """Configure global LAN segments.

        Args:
            config_yaml_file: Path to the YAML file containing LAN segment configurations
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            lan_segments = config_data.get('lan_segments', [])

            if not lan_segments:
                LOG.info("No LAN segments found in configuration file")
                return

            # Get existing LAN segments to check if they already exist
            existing_segments = self.gsdk.get_global_lan_segments()
            existing_names = {segment.name for segment in existing_segments}

            for segment_config in lan_segments:
                segment_name = segment_config.get('name')
                segment_description = segment_config.get('description', '')

                if segment_name in existing_names:
                    LOG.info(f"LAN segment '{segment_name}' already exists, skipping creation")
                else:
                    LOG.info(f"Creating LAN segment: {segment_name}")
                    response = self.gsdk.post_global_lan_segments(
                        name=segment_name,
                        description=segment_description
                    )
                    LOG.info(f"Successfully created LAN segment '{segment_name}' with ID: {response.id}")

            LOG.info(f"Successfully processed {len(lan_segments)} LAN segments")
        except Exception as e:
            LOG.error(f"Failed to configure LAN segments: {e}")
            raise ConfigurationError(f"LAN segment configuration failed: {e}")

    def deconfigure_lan_segments(self, config_yaml_file: str) -> None:
        """Deconfigure global LAN segments.

        Args:
            config_yaml_file: Path to the YAML file containing LAN segment configurations to remove
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            lan_segments = config_data.get('lan_segments', [])

            if not lan_segments:
                LOG.info("No LAN segments found in configuration file")
                return

            # Get existing LAN segments to find IDs for deletion
            existing_segments = self.gsdk.get_global_lan_segments()
            segments_by_name = {segment.name: segment for segment in existing_segments}

            deleted_count = 0
            skipped_count = 0

            for segment_config in lan_segments:
                segment_name = segment_config.get('name')

                if segment_name in segments_by_name:
                    segment = segments_by_name[segment_name]
                    # Check if segment has any references before deletion
                    if segment.site_list_references == 0 and segment.edge_references == 0 and \
                            segment.associated_interfaces == 0:
                        LOG.info(f"Deleting LAN segment '{segment_name}' (ID: {segment.id}) - no references found")
                        try:
                            success = self.gsdk.delete_global_lan_segments(segment.id)
                            if success:
                                LOG.info(f"Successfully deleted LAN segment '{segment_name}'")
                                deleted_count += 1
                            else:
                                LOG.warning(f"Failed to delete LAN segment '{segment_name}'")
                                skipped_count += 1
                        except Exception as delete_error:
                            LOG.warning(f"Failed to delete LAN segment '{segment_name}': {delete_error}")
                            skipped_count += 1
                    else:
                        LOG.warning(f"Cannot delete LAN segment '{segment_name}' - has references: "
                                    f"siteListReferences={segment.site_list_references}, "
                                    f"edgeReferences={segment.edge_references}, "
                                    f"associatedInterfaces={segment.associated_interfaces}")
                        skipped_count += 1
                else:
                    LOG.info(f"LAN segment '{segment_name}' not found, skipping deletion")
                    skipped_count += 1

            LOG.info(f"LAN segments deconfiguration completed: {deleted_count} deleted, {skipped_count} skipped")
        except Exception as e:
            LOG.error(f"Failed to deconfigure LAN segments: {e}")
            raise ConfigurationError(f"LAN segment deconfiguration failed: {e}")
