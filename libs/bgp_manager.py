"""
BGP Manager for Graphiant Playbooks.

This module handles BGP peering configuration management,
including policy attachment and detachment.
"""

from libs.base_manager import BaseManager
from libs.logger import setup_logger
from libs.exceptions import ConfigurationError, DeviceNotFoundError

LOG = setup_logger()


class BGPManager(BaseManager):
    """
    Manages BGP peering configurations.

    Handles the configuration, deconfiguration, and policy management
    for BGP peering relationships.
    """

    def configure(self, config_yaml_file: str) -> None:
        """
        Configure BGP peers for multiple devices concurrently.

        Args:
            config_yaml_file: Path to the YAML file containing BGP peering configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            final_config_payload = {}

            if 'bgp_peering' not in config_data:
                LOG.warning(f"No BGP peering configuration found in {config_yaml_file}")
                return

            for device_config in config_data.get('bgp_peering'):
                for device_name, config in device_config.items():
                    try:
                        device_id = self.edge_utils.get_device_id(device_name)
                        config_payload = {}
                        self.edge_utils.edge_bgp_peering(config_payload, **config)

                        final_config_payload[device_id] = {
                            "device_id": device_id,
                            "edge": config_payload
                        }

                        LOG.info(f"Configured BGP peering for device: {device_name} (ID: {device_id})")

                    except DeviceNotFoundError:
                        LOG.error(f"Device '{device_name}' not found, skipping BGP configuration")
                        raise
                    except Exception as e:
                        LOG.error(f"Error configuring BGP for device '{device_name}': {str(e)}")
                        raise ConfigurationError(f"Failed to configure BGP for {device_name}: {str(e)}")

            if final_config_payload:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, final_config_payload)
                LOG.info(f"Successfully configured BGP peering for {len(final_config_payload)} devices")
            else:
                LOG.warning("No valid BGP configurations found")

        except Exception as e:
            LOG.error(f"Error in BGP configuration: {str(e)}")
            raise ConfigurationError(f"BGP configuration failed: {str(e)}")

    def deconfigure(self, config_yaml_file: str) -> None:
        """
        Deconfigure BGP peers for multiple devices concurrently.

        Args:
            config_yaml_file: Path to the YAML file containing BGP peering configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            final_config_payload = {}

            if 'bgp_peering' not in config_data:
                LOG.warning(f"No BGP peering configuration found in {config_yaml_file}")
                return

            for device_config in config_data.get('bgp_peering'):
                for device_name, config in device_config.items():
                    try:
                        device_id = self.edge_utils.get_device_id(device_name)
                        config_payload = {}
                        self.edge_utils.edge_bgp_peering(config_payload, action="delete", **config)

                        final_config_payload[device_id] = {
                            "device_id": device_id,
                            "edge": config_payload
                        }

                        LOG.info(f"Deconfigured BGP peering for device: {device_name} (ID: {device_id})")

                    except DeviceNotFoundError:
                        LOG.error(f"Device '{device_name}' not found, skipping BGP deconfiguration")
                        raise
                    except Exception as e:
                        LOG.error(f"Error deconfiguring BGP for device '{device_name}': {str(e)}")
                        raise ConfigurationError(f"Failed to deconfigure BGP for {device_name}: {str(e)}")

            if final_config_payload:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, final_config_payload)
                LOG.info(f"Successfully deconfigured BGP peering for {len(final_config_payload)} devices")
            else:
                LOG.warning("No valid BGP configurations found")

        except Exception as e:
            LOG.error(f"Error in BGP deconfiguration: {str(e)}")
            raise ConfigurationError(f"BGP deconfiguration failed: {str(e)}")

    def detach_policies(self, config_yaml_file: str) -> None:
        """
        Detach routing policies from BGP peers.

        Args:
            config_yaml_file: Path to the YAML file containing BGP peering configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            config_data = self.render_config_file(config_yaml_file)
            final_config_payload = {}

            if 'bgp_peering' not in config_data:
                LOG.warning(f"No BGP peering configuration found in {config_yaml_file}")
                return

            for device_config in config_data.get('bgp_peering'):
                for device_name, config in device_config.items():
                    try:
                        device_id = self.edge_utils.get_device_id(device_name)
                        config_payload = {}
                        self.edge_utils.edge_bgp_peering(config_payload, action="unlink", **config)

                        final_config_payload[device_id] = {
                            "device_id": device_id,
                            "edge": config_payload
                        }

                        LOG.info(f"Detached policies from BGP peers for device: {device_name} (ID: {device_id})")

                    except DeviceNotFoundError:
                        LOG.error(f"Device '{device_name}' not found, skipping policy detachment")
                        raise
                    except Exception as e:
                        LOG.error(f"Error detaching policies for device '{device_name}': {str(e)}")
                        raise ConfigurationError(f"Failed to detach policies for {device_name}: {str(e)}")

            if final_config_payload:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, final_config_payload)
                LOG.info(f"Successfully detached policies from BGP peers for {len(final_config_payload)} devices")
            else:
                LOG.warning("No valid BGP configurations found")

        except Exception as e:
            LOG.error(f"Error in policy detachment: {str(e)}")
            raise ConfigurationError(f"Policy detachment failed: {str(e)}")

    # Backward compatibility methods
    def configure_bgp_peers(self, config_yaml_file: str) -> None:
        """Alias for configure method for backward compatibility."""
        self.configure(config_yaml_file)

    def deconfigure_bgp_peers(self, config_yaml_file: str) -> None:
        """Alias for deconfigure method for backward compatibility."""
        self.deconfigure(config_yaml_file)

    def detach_policies_from_bgp_peers(self, config_yaml_file: str) -> None:
        """Alias for detach_policies method for backward compatibility."""
        self.detach_policies(config_yaml_file)
