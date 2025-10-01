#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ansible module for managing Graphiant interfaces and circuits.

This module provides comprehensive interface management capabilities including:
- LAN interface configuration and deconfiguration
- WAN interface and circuit management
- Circuit-only operations (for static routes)
- Combined interface operations
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.graphiant.graphiant_playbooks.plugins.module_utils.graphiant_utils import (
    get_graphiant_connection,
    handle_graphiant_exception,
    validate_config_file
)


def main():
    """
    Main function for the Graphiant interfaces module.
    """

    # Define module arguments
    argument_spec = dict(
        host=dict(type='str', required=True, aliases=['base_url']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        interface_config_file=dict(type='str', required=True),
        circuit_config_file=dict(type='str', required=False, default=None),
        operation=dict(
            type='str',
            required=True,
            choices=[
                'configure_interfaces',
                'deconfigure_interfaces',
                'configure_lan_interfaces',
                'deconfigure_lan_interfaces',
                'configure_wan_circuits_interfaces',
                'deconfigure_wan_circuits_interfaces',
                'configure_circuits',
                'deconfigure_circuits'
            ]
        ),
        circuits_only=dict(type='bool', required=False, default=False),
        state=dict(
            type='str',
            required=False,
            default='present',
            choices=['present', 'absent']
        )
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_together=[
            ['configure_wan_circuits_interfaces', 'circuit_config_file'],
            ['deconfigure_wan_circuits_interfaces', 'circuit_config_file'],
            ['configure_circuits', 'circuit_config_file'],
            ['deconfigure_circuits', 'circuit_config_file']
        ]
    )

    # Get parameters
    params = module.params
    operation = params['operation']
    interface_config_file = params['interface_config_file']
    circuit_config_file = params.get('circuit_config_file')
    circuits_only = params.get('circuits_only', False)

    # Validate configuration files
    if not validate_config_file(interface_config_file):
        module.fail_json(
            msg=f"Interface configuration file not found or not readable: {interface_config_file}"
        )

    if circuit_config_file and not validate_config_file(circuit_config_file):
        module.fail_json(
            msg=f"Circuit configuration file not found or not readable: {circuit_config_file}"
        )

    # Handle check mode
    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f"Check mode: Would execute {operation}",
            operation=operation,
            interface_config_file=interface_config_file,
            circuit_config_file=circuit_config_file
        )

    try:
        # Get Graphiant connection
        connection = get_graphiant_connection(params)
        edge = connection.edge

        # Execute the requested operation
        changed = False
        result_msg = ""

        if operation == 'configure_interfaces':
            edge.interfaces.configure_interfaces(interface_config_file, circuit_config_file)
            changed = True
            result_msg = "Successfully configured all interfaces"

        elif operation == 'deconfigure_interfaces':
            edge.interfaces.deconfigure_interfaces(interface_config_file, circuit_config_file, circuits_only)
            changed = True
            result_msg = "Successfully deconfigured all interfaces"

        elif operation == 'configure_lan_interfaces':
            edge.interfaces.configure_lan_interfaces(interface_config_file)
            changed = True
            result_msg = "Successfully configured LAN interfaces"

        elif operation == 'deconfigure_lan_interfaces':
            edge.interfaces.deconfigure_lan_interfaces(interface_config_file)
            changed = True
            result_msg = "Successfully deconfigured LAN interfaces"

        elif operation == 'configure_wan_circuits_interfaces':
            edge.interfaces.configure_wan_circuits_interfaces(circuit_config_file, interface_config_file)
            changed = True
            result_msg = "Successfully configured WAN circuits and interfaces"

        elif operation == 'deconfigure_wan_circuits_interfaces':
            edge.interfaces.deconfigure_wan_circuits_interfaces(interface_config_file,
                                                                circuit_config_file, circuits_only)
            changed = True
            result_msg = "Successfully deconfigured WAN circuits and interfaces"

        elif operation == 'configure_circuits':
            edge.interfaces.configure_circuits(circuit_config_file, interface_config_file)
            changed = True
            result_msg = "Successfully configured circuits"

        elif operation == 'deconfigure_circuits':
            edge.interfaces.deconfigure_circuits(circuit_config_file, interface_config_file)
            changed = True
            result_msg = "Successfully deconfigured circuits"

        # Return success
        module.exit_json(
            changed=changed,
            msg=result_msg,
            operation=operation,
            interface_config_file=interface_config_file,
            circuit_config_file=circuit_config_file,
            circuits_only=circuits_only
        )

    except Exception as e:
        error_msg = handle_graphiant_exception(e, operation)
        module.fail_json(msg=error_msg, operation=operation)


if __name__ == '__main__':
    main()
