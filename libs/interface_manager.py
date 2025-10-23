"""
Interface Manager for Graphiant Playbooks.

This module handles interface and circuit configuration management,
including both regular interfaces and sub-interfaces.
"""

from libs.base_manager import BaseManager
from libs.logger import setup_logger
from libs.exceptions import ConfigurationError, DeviceNotFoundError

LOG = setup_logger()


class InterfaceManager(BaseManager):
    """
    Manages interface and circuit configurations.

    Handles the configuration and deconfiguration of network interfaces,
    including both regular interfaces and VLAN sub-interfaces.
    """

    def configure(self, interface_config_file: str, circuit_config_file: str = None) -> None:
        """
        Configure interfaces and circuits for multiple devices concurrently.
        This method combines all interface and circuit configurations in a single API call per device.

        Args:
            interface_config_file: Path to the YAML file containing interface configurations
            circuit_config_file: Optional path to the YAML file containing circuit configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            # Load interface configurations
            interface_config_data = self.render_config_file(interface_config_file)
            output_config = {}

            # Load circuit configurations if provided
            circuit_config_data = None
            if circuit_config_file:
                circuit_config_data = self.render_config_file(circuit_config_file)

            if 'interfaces' not in interface_config_data:
                LOG.warning(f"No interfaces configuration found in {interface_config_file}")
                return

            # Collect all device configurations first
            device_configs = {}

            # Collect interface configurations per device
            for device_info in interface_config_data.get("interfaces"):
                for device_name, config_list in device_info.items():
                    if device_name not in device_configs:
                        device_configs[device_name] = {"interfaces": [], "circuits": []}
                    device_configs[device_name]["interfaces"] = config_list

            # Collect circuit configurations per device if provided
            if circuit_config_data and 'circuits' in circuit_config_data:
                for device_info in circuit_config_data.get("circuits"):
                    for device_name, config_list in device_info.items():
                        if device_name not in device_configs:
                            device_configs[device_name] = {"interfaces": [], "circuits": []}
                        device_configs[device_name]["circuits"] = config_list

            # Process each device's configurations
            for device_name, configs in device_configs.items():
                try:
                    device_id = self.edge_utils.get_device_id(device_name)
                    output_config[device_id] = {
                        "device_id": device_id,
                        "edge": {"interfaces": {}, "circuits": {}}
                    }

                    # Collect circuit names referenced in this device's interfaces and subinterfaces
                    referenced_circuits = set()
                    for interface_config in configs.get("interfaces", []):
                        # Check main interface for circuit reference
                        if interface_config.get('circuit'):
                            referenced_circuits.add(interface_config['circuit'])
                        # Check subinterfaces for circuit references
                        if interface_config.get('sub_interfaces'):
                            for sub_interface in interface_config.get('sub_interfaces', []):
                                if sub_interface.get('circuit'):
                                    referenced_circuits.add(sub_interface['circuit'])

                    LOG.info(f"[configure] Processing device: {device_name} (ID: {device_id})")
                    LOG.info(f"Referenced circuits: {list(referenced_circuits)}")

                    # Process circuits for this device
                    circuits_configured = 0
                    for circuit_config in configs.get("circuits", []):
                        if circuit_config.get('circuit') in referenced_circuits:
                            self.edge_utils.edge_circuit(
                                output_config[device_id]["edge"],
                                action="add",
                                **circuit_config
                            )
                            circuits_configured += 1
                            LOG.info(f" ✓ To configure circuit '{circuit_config.get('circuit')}' "
                                     f"for device: {device_name}")
                        else:
                            LOG.info(f" ✗ Skipping circuit '{circuit_config.get('circuit')}' "
                                     f"- not referenced in interface configs")

                    # Process all interfaces for this device (both LAN and WAN)
                    interfaces_configured = 0
                    for interface_config in configs.get("interfaces", []):
                        # Check if this interface has any configuration (LAN or WAN)
                        has_lan_main = interface_config.get('lan') is not None
                        has_wan_main = interface_config.get('circuit') is not None
                        lan_subinterfaces = []
                        wan_subinterfaces = []

                        if interface_config.get('sub_interfaces'):
                            for sub_interface in interface_config.get('sub_interfaces', []):
                                if sub_interface.get('lan'):
                                    lan_subinterfaces.append(sub_interface)
                                if sub_interface.get('circuit'):
                                    wan_subinterfaces.append(sub_interface)

                        # Process this interface if it has any configuration
                        if has_lan_main or has_wan_main or lan_subinterfaces or wan_subinterfaces:
                            # Combine all subinterfaces
                            all_subinterfaces = lan_subinterfaces + wan_subinterfaces

                            if all_subinterfaces:
                                # Interface has subinterfaces
                                combined_config = interface_config.copy()
                                combined_config['sub_interfaces'] = all_subinterfaces
                                self.edge_utils.edge_interface(
                                    output_config[device_id]["edge"],
                                    action="add",
                                    **combined_config
                                )
                                interfaces_configured += 1 + len(all_subinterfaces)
                                LOG.info(f" ✓ To configure interface '{interface_config.get('name')}' "
                                         f"with {len(all_subinterfaces)} subinterfaces for device: {device_name}")
                            else:
                                # Interface has no subinterfaces
                                self.edge_utils.edge_interface(
                                    output_config[device_id]["edge"],
                                    action="add",
                                    **interface_config
                                )
                                interfaces_configured += 1
                                LOG.info(f" ✓ To configure interface '{interface_config.get('name')}' "
                                         f"for device: {device_name}")
                        else:
                            LOG.info(f" ✗ Skipping interface '{interface_config.get('name')}' "
                                     f"- no configuration found")

                    LOG.info(f"Device {device_name} summary: {circuits_configured} circuits, "
                             f"{interfaces_configured} interfaces to be configured")
                    LOG.info(f"Final config for {device_name}: {output_config[device_id]['edge']}")

                except DeviceNotFoundError:
                    LOG.error(f"Device not found: {device_name}")
                    raise
                except Exception as e:
                    LOG.error(f"Error configuring device {device_name}: {str(e)}")
                    raise ConfigurationError(f"Configuration failed for {device_name}: {str(e)}")

            if output_config:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, output_config)
                LOG.info(f"Successfully configured interfaces and circuits for {len(output_config)} devices")
            else:
                LOG.warning("No valid device configurations found")

        except Exception as e:
            LOG.error(f"Error in interface and circuit configuration: {str(e)}")
            raise ConfigurationError(f"Interface and circuit configuration failed: {str(e)}")

    def deconfigure(self, interface_config_file: str, circuit_config_file: str = None,
                    circuits_only: bool = False) -> None:
        """
        Deconfigure interfaces and circuits for multiple devices concurrently.
        This method combines all interface and circuit deconfigurations in a single API call per device.
        Circuits with staticRoutes configuration are explicitly deconfigured to ensure proper cleanup.

        Args:
            interface_config_file: Path to the YAML file containing interface configurations
            circuit_config_file: Optional path to the YAML file containing circuit configurations
            circuits_only: If True, only deconfigure circuits, skip interface deconfiguration

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            # Load interface configurations
            interface_config_data = self.render_config_file(interface_config_file)
            output_config = {}
            default_lan = f'default-{self.edge_utils.get_enterprise_id()}'

            # Load circuit configurations if provided
            circuit_config_data = None
            if circuit_config_file:
                circuit_config_data = self.render_config_file(circuit_config_file)

            if 'interfaces' not in interface_config_data:
                LOG.warning(f"No interfaces configuration found in {interface_config_file}")
                return

            # Collect all device configurations first
            device_configs = {}

            # Collect interface configurations per device
            for device_info in interface_config_data.get("interfaces"):
                for device_name, config_list in device_info.items():
                    if device_name not in device_configs:
                        device_configs[device_name] = {"interfaces": [], "circuits": []}
                    device_configs[device_name]["interfaces"] = config_list

            # Collect circuit configurations per device if provided
            if circuit_config_data and 'circuits' in circuit_config_data:
                for device_info in circuit_config_data.get("circuits"):
                    for device_name, config_list in device_info.items():
                        if device_name not in device_configs:
                            device_configs[device_name] = {"interfaces": [], "circuits": []}
                        device_configs[device_name]["circuits"] = config_list

            # Process each device's configurations
            for device_name, configs in device_configs.items():
                try:
                    device_id = self.edge_utils.get_device_id(device_name)
                    output_config[device_id] = {
                        "device_id": device_id,
                        "edge": {"interfaces": {}, "circuits": {}}
                    }

                    # Collect circuit names referenced in this device's interfaces and subinterfaces
                    referenced_circuits = set()
                    for interface_config in configs.get("interfaces", []):
                        # Check main interface for circuit reference
                        if interface_config.get('circuit'):
                            referenced_circuits.add(interface_config['circuit'])
                        # Check subinterfaces for circuit references
                        if interface_config.get('sub_interfaces'):
                            for sub_interface in interface_config.get('sub_interfaces', []):
                                if sub_interface.get('circuit'):
                                    referenced_circuits.add(sub_interface['circuit'])

                    LOG.info(f"[deconfigure] Processing device: {device_name} (ID: {device_id})")
                    LOG.info(f"Referenced circuits: {list(referenced_circuits)}")

                    # Process circuits for this device (explicit deconfiguration for circuits with staticRoutes)
                    circuits_deconfigured = 0
                    if circuits_only:
                        for circuit_config in configs.get("circuits", []):
                            if circuit_config.get('circuit') in referenced_circuits:
                                self.edge_utils.edge_circuit(
                                    output_config[device_id]["edge"],
                                    action="delete",
                                    **circuit_config
                                )
                                circuits_deconfigured += 1
                                LOG.info(f" ✓ To deconfigure circuit '{circuit_config.get('circuit')}' "
                                         f"for device: {device_name}")
                            else:
                                LOG.info(f" ✗ Skipping circuit '{circuit_config.get('circuit')}' "
                                         f"- not referenced in interface configs")

                    # Process all interfaces for this device (both LAN and WAN) - skip if circuits_only=True
                    interfaces_deconfigured = 0
                    if not circuits_only:
                        for interface_config in configs.get("interfaces", []):
                            # Check if this interface has any configuration (LAN or WAN)
                            has_lan_main = interface_config.get('lan') is not None
                            has_wan_main = interface_config.get('circuit') is not None
                            lan_subinterfaces = []
                            wan_subinterfaces = []

                            if interface_config.get('sub_interfaces'):
                                for sub_interface in interface_config.get('sub_interfaces', []):
                                    if sub_interface.get('lan'):
                                        lan_subinterfaces.append(sub_interface)
                                    if sub_interface.get('circuit'):
                                        wan_subinterfaces.append(sub_interface)

                            # Process this interface if it has any configuration
                            if has_lan_main or has_wan_main or lan_subinterfaces or wan_subinterfaces:
                                # Combine all subinterfaces
                                all_subinterfaces = lan_subinterfaces + wan_subinterfaces

                                if all_subinterfaces:
                                    # Interface has subinterfaces
                                    combined_config = interface_config.copy()
                                    combined_config['sub_interfaces'] = all_subinterfaces
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="delete",
                                        default_lan=default_lan,
                                        **combined_config
                                    )
                                    interfaces_deconfigured += 1 + len(all_subinterfaces)
                                    LOG.info(f" ✓ To deconfigure interface '{interface_config.get('name')}' "
                                             f"with {len(all_subinterfaces)} subinterfaces for device: {device_name}")
                                else:
                                    # Interface has no subinterfaces
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="delete",
                                        default_lan=default_lan,
                                        **interface_config
                                    )
                                    interfaces_deconfigured += 1
                                    LOG.info(f" ✓ To deconfigure interface '{interface_config.get('name')}' "
                                             f"for device: {device_name}")
                            else:
                                LOG.info(f" ✗ Skipping interface '{interface_config.get('name')}' "
                                         f"- no configuration found")
                    else:
                        LOG.info(" ✓ Skipping interface deconfiguration (circuits-only mode)")

                    if circuits_only:
                        LOG.info(f"Device {device_name} "
                                 f"summary: {circuits_deconfigured} circuits to be deconfigured (circuits-only mode)")
                    else:
                        LOG.info(f"Device {device_name} "
                                 f"summary: {circuits_deconfigured} circuits "
                                 f"and {interfaces_deconfigured} interfaces to be deconfigured")
                    LOG.info(f"Final config for {device_name}: {output_config[device_id]['edge']}")

                except DeviceNotFoundError:
                    LOG.error(f"Device not found: {device_name}")
                    raise
                except Exception as e:
                    LOG.error(f"Error deconfiguring device {device_name}: {str(e)}")
                    raise ConfigurationError(f"Deconfiguration failed for {device_name}: {str(e)}")

            if output_config:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, output_config)
                if circuits_only:
                    LOG.info(f"Successfully deconfigured circuits for {len(output_config)} "
                             f"devices (circuits-only mode)")
                else:
                    LOG.info(f"Successfully deconfigured interfaces and circuits for {len(output_config)} devices")
            else:
                if circuits_only:
                    LOG.warning("No valid circuit configurations found")
                else:
                    LOG.warning("No valid device configurations found")

        except Exception as e:
            LOG.error(f"Error in interface and circuit deconfiguration: {str(e)}")
            raise ConfigurationError(f"Interface and circuit deconfiguration failed: {str(e)}")

    def configure_interfaces(self, interface_config_file: str, circuit_config_file: str = None) -> None:
        """
        Configure all interfaces and circuits for multiple devices concurrently.
        This method calls the configure method to handle all configurations in a single API call per device.

        Args:
            interface_config_file: Path to the YAML file containing interface configurations
            circuit_config_file: Optional path to the YAML file containing circuit configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        self.configure(interface_config_file, circuit_config_file)

    def deconfigure_interfaces(self, interface_config_file: str, circuit_config_file: str = None,
                               circuits_only: bool = False) -> None:
        """
        Deconfigure all interfaces and circuits for multiple devices concurrently.
        This method calls the deconfigure method to handle all deconfigurations in a single API call per device.
        Circuits with staticRoutes configuration are explicitly deconfigured to ensure proper cleanup.

        Args:
            interface_config_file: Path to the YAML file containing interface configurations
            circuit_config_file: Optional path to the YAML file containing circuit configurations
            circuits_only: If True, only deconfigure circuits, skip interface deconfiguration

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        self.deconfigure(interface_config_file, circuit_config_file, circuits_only)

    def configure_circuits(self, circuit_config_file: str, interface_config_file: str) -> None:
        """
        Configure circuits only for multiple devices concurrently.
        This method uses configure_wan_circuits_interfaces with circuits_only=True.
        Only circuits referenced in the interface config will be configured.

        Args:
            circuit_config_file: Path to the YAML file containing circuit configurations
            interface_config_file: Path to the YAML file containing interface configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        LOG.info(f"Configuring circuits only using circuit config: {circuit_config_file} "
                 f"and interface config: {interface_config_file}")
        self.configure_wan_circuits_interfaces(circuit_config_file, interface_config_file, circuits_only=True)

    def deconfigure_circuits(self, circuit_config_file: str, interface_config_file: str) -> None:
        """
        Deconfigure circuits only (staticRoutes) for multiple devices concurrently.
        This method uses deconfigure_wan_circuits_interfaces with circuits_only=True.
        Only circuits referenced in the interface config will be deconfigured.

        Args:
            circuit_config_file: Path to the YAML file containing circuit configurations
            interface_config_file: Path to the YAML file containing interface configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        LOG.info(f"Deconfiguring circuits only using circuit config: {circuit_config_file} "
                 f"and interface config: {interface_config_file}")
        self.deconfigure_wan_circuits_interfaces(interface_config_file, circuit_config_file, circuits_only=True)

    def configure_lan_interfaces(self, interface_config_file: str) -> None:
        """
        Configure LAN interfaces for multiple devices concurrently.
        Only interfaces with 'lan' key will be configured.

        Args:
            interface_config_file: Path to the YAML file containing interface configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            config_data = self.render_config_file(interface_config_file)
            output_config = {}

            if 'interfaces' not in config_data:
                LOG.warning(f"No interfaces configuration found in {interface_config_file}")
                return

            for device_info in config_data.get("interfaces"):
                for device_name, config_list in device_info.items():
                    try:
                        device_id = self.edge_utils.get_device_id(device_name)
                        device_config = {"interfaces": {}}

                        lan_interfaces_configured = 0
                        for config in config_list:
                            # Check if this interface has any LAN configuration (main interface or subinterfaces)
                            has_lan_main = config.get('lan') is not None
                            lan_subinterfaces = []

                            if config.get('sub_interfaces'):
                                for sub_interface in config.get('sub_interfaces', []):
                                    if sub_interface.get('lan'):
                                        lan_subinterfaces.append(sub_interface)
                                        LOG.info(f" ✓ Found LAN subinterface "
                                                 f"'{config.get('name')}.{sub_interface.get('vlan')}' "
                                                 f"for device: {device_name}")

                            # Process this interface if it has any LAN configuration
                            if has_lan_main or lan_subinterfaces:
                                if has_lan_main and lan_subinterfaces:
                                    # Both main interface and subinterfaces have LAN config
                                    combined_config = config.copy()
                                    combined_config['sub_interfaces'] = lan_subinterfaces
                                    self.edge_utils.edge_interface(device_config, action="add", **combined_config)
                                    lan_interfaces_configured += 1 + len(lan_subinterfaces)
                                    LOG.info(f" ✓ To configure LAN main interface '{config.get('name')}' "
                                             f"and {len(lan_subinterfaces)} LAN subinterfaces "
                                             f"for device: {device_name}")

                                elif has_lan_main:
                                    # Only main interface has LAN config
                                    main_config = config.copy()
                                    main_config.pop('sub_interfaces', None)  # Remove subinterfaces
                                    self.edge_utils.edge_interface(device_config, action="add", **main_config)
                                    lan_interfaces_configured += 1
                                    LOG.info(f" ✓ To configure LAN main interface '{config.get('name')}' "
                                             f"for device: {device_name}")

                                elif lan_subinterfaces:
                                    # Only subinterfaces have LAN config - create minimal config
                                    subinterface_config = {
                                        'name': config.get('name'),
                                        'sub_interfaces': lan_subinterfaces
                                    }
                                    self.edge_utils.edge_interface(device_config, action="add", **subinterface_config)
                                    lan_interfaces_configured += len(lan_subinterfaces)
                                    LOG.info(f" ✓ Configure {len(lan_subinterfaces)} LAN subinterfaces for interface "
                                             f"'{config.get('name')}' on device: {device_name}")
                            else:
                                LOG.info(f" ✗ Skipping interface '{config.get('name')}' - no LAN configuration found")

                        if lan_interfaces_configured > 0:
                            output_config[device_id] = {
                                "device_id": device_id,
                                "edge": device_config
                            }
                            LOG.info(f"Device {device_name} "
                                     f"summary: {lan_interfaces_configured} LAN interfaces to be configured")
                        else:
                            LOG.info(f"Device {device_name}: No LAN interfaces found to configure")

                    except DeviceNotFoundError:
                        LOG.error(f"Device not found: {device_name}")
                        raise
                    except Exception as e:
                        LOG.error(f"Error configuring LAN interfaces for device {device_name}: {str(e)}")
                        raise ConfigurationError(f"LAN interface configuration failed for {device_name}: {str(e)}")

            if output_config:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, output_config)
                LOG.info(f"Successfully configured LAN interfaces for {len(output_config)} devices")
            else:
                LOG.warning("No LAN interface configurations to apply")

        except Exception as e:
            LOG.error(f"Error in LAN interface configuration: {str(e)}")
            raise ConfigurationError(f"LAN interface configuration failed: {str(e)}")

    def deconfigure_lan_interfaces(self, interface_config_file: str) -> None:
        """
        Deconfigure LAN interfaces for multiple devices concurrently.
        Only interfaces with 'lan' key will be deconfigured.

        Args:
            interface_config_file: Path to the YAML file containing interface configurations

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            config_data = self.render_config_file(interface_config_file)
            output_config = {}
            default_lan = f'default-{self.edge_utils.get_enterprise_id()}'

            if 'interfaces' not in config_data:
                LOG.warning(f"No interfaces configuration found in {interface_config_file}")
                return

            for device_info in config_data.get("interfaces"):
                for device_name, config_list in device_info.items():
                    try:
                        device_id = self.edge_utils.get_device_id(device_name)
                        device_config = {"interfaces": {}}

                        lan_interfaces_deconfigured = 0
                        for config in config_list:
                            # Check if this interface has any LAN configuration (main interface or subinterfaces)
                            has_lan_main = config.get('lan') is not None
                            lan_subinterfaces = []

                            if config.get('sub_interfaces'):
                                for sub_interface in config.get('sub_interfaces', []):
                                    if sub_interface.get('lan'):
                                        lan_subinterfaces.append(sub_interface)
                                        LOG.info(f" ✓ Found LAN subinterface "
                                                 f"'{config.get('name')}.{sub_interface.get('vlan')}' "
                                                 f"for device: {device_name}")

                            # Process this interface if it has any LAN configuration
                            if has_lan_main or lan_subinterfaces:
                                if has_lan_main and lan_subinterfaces:
                                    # Both main interface and subinterfaces have LAN config
                                    combined_config = config.copy()
                                    combined_config['sub_interfaces'] = lan_subinterfaces
                                    self.edge_utils.edge_interface(device_config, action="delete",
                                                                   **combined_config, default_lan=default_lan)
                                    lan_interfaces_deconfigured += 1 + len(lan_subinterfaces)
                                    LOG.info(f" ✓ To deconfigure LAN main interface '{config.get('name')}' "
                                             f"and {len(lan_subinterfaces)} LAN subinterfaces "
                                             f"for device: {device_name}")

                                elif has_lan_main:
                                    # Only main interface has LAN config
                                    main_config = config.copy()
                                    main_config.pop('sub_interfaces', None)  # Remove subinterfaces
                                    self.edge_utils.edge_interface(device_config, action="delete", **main_config,
                                                                   default_lan=default_lan)
                                    lan_interfaces_deconfigured += 1
                                    LOG.info(f" ✓ To deconfigure LAN main interface '{config.get('name')}' "
                                             f"for device: {device_name}")

                                elif lan_subinterfaces:
                                    # Only subinterfaces have LAN config - create minimal config
                                    subinterface_config = {
                                        'name': config.get('name'),
                                        'sub_interfaces': lan_subinterfaces
                                    }
                                    self.edge_utils.edge_interface(device_config, action="delete",
                                                                   **subinterface_config, default_lan=default_lan)
                                    lan_interfaces_deconfigured += len(lan_subinterfaces)
                                    LOG.info(f" ✓ Deconfigure {len(lan_subinterfaces)} LAN subinterfaces for interface"
                                             f" '{config.get('name')}' on device: {device_name}")
                            else:
                                LOG.info(f" ✗ Skipping interface '{config.get('name')}' - no LAN configuration found")

                        if lan_interfaces_deconfigured > 0:
                            output_config[device_id] = {
                                "device_id": device_id,
                                "edge": device_config
                            }
                            LOG.info(f"Device {device_name} "
                                     f"summary: {lan_interfaces_deconfigured} LAN interfaces to be deconfigured")
                        else:
                            LOG.info(f"Device {device_name}: No LAN interfaces found to deconfigure")

                    except DeviceNotFoundError:
                        LOG.error(f"Device not found: {device_name}")
                        raise
                    except Exception as e:
                        LOG.error(f"Error deconfiguring LAN interfaces for device {device_name}: {str(e)}")
                        raise ConfigurationError(f"LAN interface deconfiguration failed for {device_name}: {str(e)}")

            if output_config:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, output_config)
                LOG.info(f"Successfully deconfigured LAN interfaces for {len(output_config)} devices")
            else:
                LOG.warning("No LAN interface configurations to remove")

        except Exception as e:
            LOG.error(f"Error in LAN interface deconfiguration: {str(e)}")
            raise ConfigurationError(f"LAN interface deconfiguration failed: {str(e)}")

    def configure_wan_circuits_interfaces(self, circuit_config_file: str, interface_config_file: str,
                                          circuits_only: bool = False) -> None:
        """
        Configure both circuits and interfaces for multiple devices concurrently.
        This method combines circuit and interface configuration in a single operation.

        Args:
            circuit_config_file: Path to the YAML file containing circuit configurations
            interface_config_file: Path to the YAML file containing interface configurations
            circuits_only: If True, only configure circuits (not interfaces) that are referenced in interface config

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            # Load circuit configurations
            circuit_config_data = self.render_config_file(circuit_config_file)
            interface_config_data = self.render_config_file(interface_config_file)

            output_config = {}

            # Collect all device configurations first
            device_configs = {}

            # Collect interface configurations per device
            if 'interfaces' in interface_config_data:
                for device_info in interface_config_data.get("interfaces"):
                    for device_name, config_list in device_info.items():
                        if device_name not in device_configs:
                            device_configs[device_name] = {"interfaces": [], "circuits": []}
                        device_configs[device_name]["interfaces"] = config_list

            # Collect circuit configurations per device
            if 'circuits' in circuit_config_data:
                for device_info in circuit_config_data.get("circuits"):
                    for device_name, config_list in device_info.items():
                        if device_name not in device_configs:
                            device_configs[device_name] = {"interfaces": [], "circuits": []}
                        device_configs[device_name]["circuits"] = config_list

            # Process each device's configurations
            for device_name, configs in device_configs.items():
                try:
                    device_id = self.edge_utils.get_device_id(device_name)
                    output_config[device_id] = {
                        "device_id": device_id,
                        "edge": {"interfaces": {}, "circuits": {}}
                    }

                    # Collect circuit names referenced in this device's interfaces and subinterfaces
                    referenced_circuits = set()
                    for interface_config in configs.get("interfaces", []):
                        # Check main interface for circuit reference
                        if interface_config.get('circuit'):
                            referenced_circuits.add(interface_config['circuit'])
                        # Check subinterfaces for circuit references
                        if interface_config.get('sub_interfaces'):
                            for sub_interface in interface_config.get('sub_interfaces', []):
                                if sub_interface.get('circuit'):
                                    referenced_circuits.add(sub_interface['circuit'])

                    if circuits_only:
                        LOG.info(f"[configure_wan_circuits_interfaces] Processing device: {device_name} "
                                 f"(ID: {device_id}) - CIRCUITS ONLY MODE")
                    else:
                        LOG.info(f"[configure_wan_circuits_interfaces] Processing device: {device_name} "
                                 f"(ID: {device_id})")
                    LOG.info(f"Referenced circuits: {list(referenced_circuits)}")

                    # Process circuits for this device
                    circuits_configured = 0
                    for circuit_config in configs.get("circuits", []):
                        if circuit_config.get('circuit') in referenced_circuits:
                            self.edge_utils.edge_circuit(
                                output_config[device_id]["edge"],
                                action="add",
                                **circuit_config
                            )
                            circuits_configured += 1
                            LOG.info(f" ✓ To configure circuit '{circuit_config.get('circuit')}' "
                                     f"for device: {device_name}")
                        else:
                            LOG.info(f" ✗ Skipping circuit '{circuit_config.get('circuit')}' "
                                     f"- not referenced in interface configs")

                    # Process interfaces for this device (only if not circuits_only)
                    interfaces_configured = 0
                    if not circuits_only:
                        for interface_config in configs.get("interfaces", []):
                            # Check if this interface has any WAN configuration (main interface or subinterfaces)
                            has_wan_main = interface_config.get('circuit') is not None
                            wan_subinterfaces = []

                            if interface_config.get('sub_interfaces'):
                                for sub_interface in interface_config.get('sub_interfaces', []):
                                    if sub_interface.get('circuit'):
                                        wan_subinterfaces.append(sub_interface)
                                        LOG.info(f" ✓ Found WAN subinterface "
                                                 f"'{interface_config.get('name')}.{sub_interface.get('vlan')}' "
                                                 f"with circuit '{sub_interface.get('circuit')}' "
                                                 f"for device: {device_name}")

                            # Process this interface if it has any WAN configuration
                            if has_wan_main or wan_subinterfaces:
                                if has_wan_main and wan_subinterfaces:
                                    # Both main interface and subinterfaces have WAN config
                                    combined_config = interface_config.copy()
                                    combined_config['sub_interfaces'] = wan_subinterfaces
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="add",
                                        **combined_config
                                    )
                                    interfaces_configured += 1 + len(wan_subinterfaces)
                                    LOG.info(f" ✓ To configure WAN main interface '{interface_config.get('name')}' "
                                             f"with circuit '{interface_config.get('circuit')}' "
                                             f"and {len(wan_subinterfaces)} WAN subinterfaces "
                                             f"for device: {device_name}")

                                elif has_wan_main:
                                    # Only main interface has WAN config
                                    main_config = interface_config.copy()
                                    main_config.pop('sub_interfaces', None)  # Remove subinterfaces
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="add",
                                        **main_config
                                    )
                                    interfaces_configured += 1
                                    LOG.info(f" ✓ To configure WAN main interface '{interface_config.get('name')}' "
                                             f"with circuit '{interface_config.get('circuit')}' "
                                             f"for device: {device_name}")

                                elif wan_subinterfaces:
                                    # Only subinterfaces have WAN config - create minimal config
                                    subinterface_config = {
                                        'name': interface_config.get('name'),
                                        'sub_interfaces': wan_subinterfaces
                                    }
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="add",
                                        **subinterface_config
                                    )
                                    interfaces_configured += len(wan_subinterfaces)
                                    LOG.info(f" ✓ Configure {len(wan_subinterfaces)} WAN subinterfaces for interface "
                                             f"'{interface_config.get('name')}' on device: {device_name}")
                            else:
                                LOG.info(f" ✗ Skipping interface '{interface_config.get('name')}' "
                                         f"- no WAN configuration found")

                    if circuits_only:
                        LOG.info(f"Device {device_name} summary: {circuits_configured} circuits configured "
                                 f"(circuits-only mode)")
                    else:
                        LOG.info(f"Device {device_name} summary: {circuits_configured} circuits, "
                                 f"{interfaces_configured} WAN interfaces to be configured")
                    LOG.info(f"Final config for {device_name}: {output_config[device_id]['edge']}")

                except DeviceNotFoundError:
                    LOG.error(f"Device not found: {device_name}")
                    raise
                except Exception as e:
                    LOG.error(f"Error configuring device {device_name}: {str(e)}")
                    raise ConfigurationError(f"Configuration failed for {device_name}: {str(e)}")

            if output_config:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, output_config)
                if circuits_only:
                    LOG.info(f"Successfully configured circuits for {len(output_config)} devices (circuits-only mode)")
                else:
                    LOG.info(f"Successfully configured circuits and interfaces for {len(output_config)} devices")
            else:
                if circuits_only:
                    LOG.warning("No circuit configurations to apply")
                else:
                    LOG.warning("No circuit or interface configurations to apply")

        except Exception as e:
            LOG.error(f"Error in WAN circuits and interfaces configuration: {str(e)}")
            raise ConfigurationError(f"WAN circuits and interfaces configuration failed: {str(e)}")

    def deconfigure_wan_circuits_interfaces(self, interface_config_file: str, circuit_config_file: str = None,
                                            circuits_only: bool = False) -> None:
        """
        Deconfigure wan interfaces for multiple devices concurrently.
        if circuits_only is True, only deconfigure circuits, skip interface deconfiguration
            Circuits with staticRoutes configuration are explicitly deconfigured to ensure proper cleanup.
        if circuits_only is False, deconfigure interfaces only since circuits will be deconfigured automatically if
           circuits did not have staticRoutes configuration.

        Args:
            interface_config_file: Path to the YAML file containing interface configurations
            circuit_config_file: Optional path to the YAML file containing circuit configurations
            circuits_only: If True, only deconfigure circuits, skip interface deconfiguration

        Raises:
            ConfigurationError: If configuration processing fails
            DeviceNotFoundError: If any device cannot be found
        """
        try:
            interface_config_data = self.render_config_file(interface_config_file)

            # Load circuit configurations if provided
            circuit_config_data = None
            if circuit_config_file:
                circuit_config_data = self.render_config_file(circuit_config_file)

            output_config = {}
            default_lan = f'default-{self.edge_utils.get_enterprise_id()}'

            # Collect all device configurations first
            device_configs = {}

            # Collect interface configurations per device
            if 'interfaces' in interface_config_data:
                for device_info in interface_config_data.get("interfaces"):
                    for device_name, config_list in device_info.items():
                        if device_name not in device_configs:
                            device_configs[device_name] = {"interfaces": [], "circuits": []}
                        device_configs[device_name]["interfaces"] = config_list

            # Collect circuit configurations per device if provided
            if circuit_config_data and 'circuits' in circuit_config_data:
                for device_info in circuit_config_data.get("circuits"):
                    for device_name, config_list in device_info.items():
                        if device_name not in device_configs:
                            device_configs[device_name] = {"interfaces": [], "circuits": []}
                        device_configs[device_name]["circuits"] = config_list

            # Process each device's configurations
            for device_name, configs in device_configs.items():
                try:
                    device_id = self.edge_utils.get_device_id(device_name)
                    output_config[device_id] = {
                        "device_id": device_id,
                        "edge": {"interfaces": {}, "circuits": {}}
                    }

                    # Collect circuit names referenced in this device's interfaces and subinterfaces
                    referenced_circuits = set()
                    for interface_config in configs.get("interfaces", []):
                        # Check main interface for circuit reference
                        if interface_config.get('circuit'):
                            referenced_circuits.add(interface_config['circuit'])
                        # Check subinterfaces for circuit references
                        if interface_config.get('sub_interfaces'):
                            for sub_interface in interface_config.get('sub_interfaces', []):
                                if sub_interface.get('circuit'):
                                    referenced_circuits.add(sub_interface['circuit'])

                    LOG.info(f"[deconfigure_wan_circuits_interfaces] Processing device: {device_name} "
                             f"(ID: {device_id})")
                    LOG.info(f"Referenced circuits: {list(referenced_circuits)}")

                    # Process circuits for this device (explicit deconfiguration for circuits with staticRoutes)
                    circuits_deconfigured = 0
                    if circuits_only:
                        for circuit_config in configs.get("circuits", []):
                            if circuit_config.get('circuit') in referenced_circuits:
                                self.edge_utils.edge_circuit(
                                    output_config[device_id]["edge"],
                                    action="delete",
                                    **circuit_config
                                )
                                circuits_deconfigured += 1
                                LOG.info(f" ✓ To deconfigure circuit '{circuit_config.get('circuit')}' "
                                         f"for device: {device_name}")
                            else:
                                LOG.info(f" ✗ Skipping circuit '{circuit_config.get('circuit')}' "
                                         f"- not referenced in interface configs")

                    # Process interfaces for this device - skip if circuits_only=True
                    interfaces_deconfigured = 0
                    if not circuits_only:
                        for interface_config in configs.get("interfaces", []):
                            # Check if this interface has any WAN configuration (main interface or subinterfaces)
                            has_wan_main = interface_config.get('circuit') is not None
                            wan_subinterfaces = []

                            if interface_config.get('sub_interfaces'):
                                for sub_interface in interface_config.get('sub_interfaces', []):
                                    if sub_interface.get('circuit'):
                                        wan_subinterfaces.append(sub_interface)
                                        LOG.info(f" ✓ Found WAN subinterface "
                                                 f"'{interface_config.get('name')}.{sub_interface.get('vlan')}' "
                                                 f"with circuit '{sub_interface.get('circuit')}' "
                                                 f"for device: {device_name}")

                            # Process this interface if it has any WAN configuration
                            if has_wan_main or wan_subinterfaces:
                                if has_wan_main and wan_subinterfaces:
                                    # Both main interface and subinterfaces have WAN config
                                    combined_config = interface_config.copy()
                                    combined_config['sub_interfaces'] = wan_subinterfaces
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="delete",
                                        default_lan=default_lan,
                                        **combined_config
                                    )
                                    interfaces_deconfigured += 1 + len(wan_subinterfaces)
                                    LOG.info(f" ✓ To deconfigure WAN main interface '{interface_config.get('name')}' "
                                             f"with circuit '{interface_config.get('circuit')}' "
                                             f"and {len(wan_subinterfaces)} WAN subinterfaces "
                                             f"for device: {device_name}")

                                elif has_wan_main:
                                    # Only main interface has WAN config
                                    main_config = interface_config.copy()
                                    main_config.pop('sub_interfaces', None)  # Remove subinterfaces
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="delete",
                                        default_lan=default_lan,
                                        **main_config
                                    )
                                    interfaces_deconfigured += 1
                                    LOG.info(f" ✓ To deconfigure WAN main interface '{interface_config.get('name')}' "
                                             f"with circuit '{interface_config.get('circuit')}' "
                                             f"for device: {device_name}")

                                elif wan_subinterfaces:
                                    # Only subinterfaces have WAN config - create minimal config
                                    subinterface_config = {
                                        'name': interface_config.get('name'),
                                        'sub_interfaces': wan_subinterfaces
                                    }
                                    self.edge_utils.edge_interface(
                                        output_config[device_id]["edge"],
                                        action="delete",
                                        default_lan=default_lan,
                                        **subinterface_config
                                    )
                                    interfaces_deconfigured += len(wan_subinterfaces)
                                    LOG.info(f" ✓ Deconfigure {len(wan_subinterfaces)} WAN subinterfaces for interface "
                                             f"'{interface_config.get('name')}' on device: {device_name}")
                            else:
                                LOG.info(f" ✗ Skipping interface '{interface_config.get('name')}' "
                                         f"- no WAN configuration found")
                    else:
                        LOG.info(" ✓ Skipping WAN interface deconfiguration (circuits-only mode)")

                    if circuits_only:
                        LOG.info(f"Device {device_name} "
                                 f"summary: {circuits_deconfigured} circuits to be deconfigured (circuits-only mode)")
                    else:
                        LOG.info(f"Device {device_name} "
                                 f"summary: {circuits_deconfigured} circuits "
                                 f"and {interfaces_deconfigured} WAN interfaces to be deconfigured")
                    LOG.info(f"Final config for {device_name}: {output_config[device_id]['edge']}")

                except DeviceNotFoundError:
                    LOG.error(f"Device not found: {device_name}")
                    raise
                except Exception as e:
                    LOG.error(f"Error deconfiguring device {device_name}: {str(e)}")
                    raise ConfigurationError(f"Deconfiguration failed for {device_name}: {str(e)}")

            if output_config:
                self.execute_concurrent_tasks(self.gsdk.put_device_config, output_config)
                if circuits_only:
                    LOG.info(f"Successfully deconfigured circuits for {len(output_config)} "
                             f"devices (circuits-only mode)")
                else:
                    LOG.info(f"Successfully deconfigured circuits and interfaces for {len(output_config)} devices")
            else:
                if circuits_only:
                    LOG.warning("No circuit configurations to remove")
                else:
                    LOG.warning("No circuit or interface configurations to remove")

        except Exception as e:
            LOG.error(f"Error in WAN circuits and interfaces deconfiguration: {str(e)}")
            raise ConfigurationError(f"WAN circuits and interfaces deconfiguration failed: {str(e)}")
