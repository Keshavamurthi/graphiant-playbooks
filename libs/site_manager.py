"""
Site Manager for Graphiant Playbooks.

This module handles site management operations including
attachment and detachment of global system objects to/from sites.
"""

from typing import Dict, Any, Union
from libs.base_manager import BaseManager
from libs.logger import setup_logger
from libs.exceptions import ConfigurationError, SiteNotFoundError, ValidationError

LOG = setup_logger()


class SiteManager(BaseManager):
    """
    Manages site operations and global object attachments.

    Handles the attachment and detachment of global system objects
    (SNMP, Syslog, IPFIX, VPN profiles) to/from specific sites.
    """

    def configure(self, config_yaml_file: str) -> None:
        """
        Attach global system objects to sites.

        Args:
            config_yaml_file: Path to the YAML file containing site attachment configurations

        Raises:
            ConfigurationError: If configuration processing fails
            SiteNotFoundError: If any site cannot be found
            ValidationError: If configuration data is invalid
        """
        self._manage_site_objects(config_yaml_file, operation="attach")

    def deconfigure(self, config_yaml_file: str) -> None:
        """
        Detach global system objects from sites.

        Args:
            config_yaml_file: Path to the YAML file containing site attachment configurations

        Raises:
            ConfigurationError: If configuration processing fails
            SiteNotFoundError: If any site cannot be found
            ValidationError: If configuration data is invalid
        """
        self._manage_site_objects(config_yaml_file, operation="detach")

    def _manage_site_objects(self, config_yaml_file: str, operation: str) -> None:
        """
        Manage global system objects on sites (attach or detach).

        Args:
            config_yaml_file: Path to the YAML file containing site management definitions
            operation: Operation to perform - "attach" or "detach"

        Raises:
            ConfigurationError: If configuration processing fails
            SiteNotFoundError: If any site cannot be found
            ValidationError: If configuration data is invalid
        """
        try:
            config_data = self.render_config_file(config_yaml_file)

            if 'site_attachments' not in config_data:
                LOG.warning(f"No site attachments configuration found in {config_yaml_file}")
                return

            default_operation = 'Attach' if operation.lower() == "attach" else 'Detach'
            processed_sites = 0

            for site_config in config_data.get('site_attachments'):
                try:
                    # Get the site name from the first (and only) key in the site config
                    site_name = list(site_config.keys())[0]
                    site_data = site_config[site_name]

                    site_id = self.get_site_id(site_name)
                    site_payload = {"site": {"name": site_name}}

                    # Process SNMP operations
                    if 'snmp_servers' in site_data:
                        site_payload['site']['snmpOps'] = {}
                        for snmp_name in site_data.get('snmp_servers'):
                            site_payload['site']['snmpOps'][snmp_name] = default_operation

                    # Process Syslog operations
                    if 'syslog_servers' in site_data:
                        site_payload['site']['syslogServerOpsV2'] = {}
                        for syslog_config in site_data.get('syslog_servers'):
                            self._process_syslog_config(site_payload, syslog_config, default_operation)

                    # Process IPFIX operations
                    if 'ipfix_exporters' in site_data:
                        site_payload['site']['ipfixExporterOpsV2'] = {}
                        for ipfix_config in site_data.get('ipfix_exporters'):
                            self._process_ipfix_config(site_payload, ipfix_config, default_operation)

                    # Execute the site configuration
                    self.gsdk.post_site_config(site_id=site_id, site_config=site_payload)
                    processed_sites += 1

                    LOG.info(f"Successfully {operation.lower()}ed global objects for site: {site_name} (ID: {site_id})")

                except SiteNotFoundError:
                    LOG.error(f"Site '{site_name}' not found, skipping {operation} operation")
                    raise
                except Exception as e:
                    LOG.error(f"Error {operation.lower()}ing objects for site '{site_name}': {str(e)}")
                    raise ConfigurationError(f"Failed to {operation.lower()} objects for {site_name}: {str(e)}")

            LOG.info(f"Successfully {operation.lower()}ed global objects for {processed_sites} sites")

        except Exception as e:
            LOG.error(f"Error in site {operation} operation: {str(e)}")
            raise ConfigurationError(f"Site {operation} operation failed: {str(e)}")

    def _process_syslog_config(self, site_payload: Dict[str, Any],
                               syslog_config: Union[str, Dict], default_operation: str) -> None:
        """
        Process syslog configuration for site attachment/detachment.

        Args:
            site_payload: The site payload dictionary to update
            syslog_config: Syslog configuration (string or dict)
            default_operation: The operation to perform (Attach/Detach)
        """
        if isinstance(syslog_config, str):
            # Backward compatibility: simple string format
            syslog_name = syslog_config
            site_payload['site']['syslogServerOpsV2'][syslog_name] = {
                "operation": default_operation
            }
        else:
            # New format: object with interface specification
            syslog_name = syslog_config.get('name')
            interface = syslog_config.get('interface')

            if not syslog_name:
                raise ValidationError("Syslog configuration must include 'name' field")

            site_payload['site']['syslogServerOpsV2'][syslog_name] = {
                "operation": default_operation,
                "interface": {
                    "interface": interface
                }
            }

    def _process_ipfix_config(self, site_payload: Dict[str, Any],
                              ipfix_config: Union[str, Dict], default_operation: str) -> None:
        """
        Process IPFIX configuration for site attachment/detachment.

        Args:
            site_payload: The site payload dictionary to update
            ipfix_config: IPFIX configuration (string or dict)
            default_operation: The operation to perform (Attach/Detach)
        """
        if isinstance(ipfix_config, str):
            # Backward compatibility: simple string format
            ipfix_name = ipfix_config
            site_payload['site']['ipfixExporterOpsV2'][ipfix_name] = {
                "operation": default_operation
            }
        else:
            # New format: object with interface specification
            ipfix_name = ipfix_config.get('name')
            interface = ipfix_config.get('interface')

            if not ipfix_name:
                raise ValidationError("IPFIX configuration must include 'name' field")

            site_payload['site']['ipfixExporterOpsV2'][ipfix_name] = {
                "operation": default_operation,
                "interface": {
                    "interface": interface
                }
            }

    def attach_objects(self, config_yaml_file: str) -> None:
        """
        Attach global system objects to sites.

        Args:
            config_yaml_file: Path to the YAML file containing site attachment configurations
        """
        self._manage_site_objects(config_yaml_file, operation="attach")

    def detach_objects(self, config_yaml_file: str) -> None:
        """
        Detach global system objects from sites.

        Args:
            config_yaml_file: Path to the YAML file containing site attachment configurations
        """
        self._manage_site_objects(config_yaml_file, operation="detach")

    # Backward compatibility methods
    def manage_global_system_objects_on_site(self, config_yaml_file: str, operation: str = "attach") -> None:
        """
        Manage global system objects on sites (attach or detach).

        Args:
            config_yaml_file: Path to the YAML file containing site management definitions
            operation: Operation to perform - "attach" or "detach". Defaults to "attach"
        """
        self._manage_site_objects(config_yaml_file, operation)
