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
from ansible_collections.graphiant.graphiant_playbooks.plugins.module_utils.logging_decorator import (
    capture_library_logs
)


@capture_library_logs
def execute_with_logging(module, func, *args, **kwargs):
    """
    Execute a function with optional detailed logging.

    Args:
        module: Ansible module instance
        func: Function to execute
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        dict: Result with 'changed' and 'result_msg' keys
    """
    # Extract success_msg from kwargs before passing to func
    success_msg = kwargs.pop('success_msg', 'Operation completed successfully')

    try:
        func(*args, **kwargs)
        return {
            'changed': True,
            'result_msg': success_msg
        }
    except Exception as e:
        raise e


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
            required=False,
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
        ),
        detailed_logs=dict(
            type='bool',
            required=False,
            default=False,
            description='Enable detailed logging output from library operations'
        )
    )

    # Create Ansible module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    # Get parameters
    params = module.params
    operation = params.get('operation')
    state = params.get('state', 'present')
    interface_config_file = params['interface_config_file']
    circuit_config_file = params.get('circuit_config_file')
    circuits_only = params.get('circuits_only', False)

    # Validate that at least one of operation or state is provided
    if not operation and not state:
        supported_operations = [
            'configure_interfaces', 'deconfigure_interfaces', 'configure_lan_interfaces',
            'deconfigure_lan_interfaces', 'configure_wan_circuits_interfaces',
            'deconfigure_wan_circuits_interfaces', 'configure_circuits', 'deconfigure_circuits'
        ]
        module.fail_json(
            msg="Either 'operation' or 'state' parameter must be provided. "
                f"Supported operations: {', '.join(supported_operations)}"
        )

    # If operation is not specified, use state to determine operation
    if not operation:
        if state == 'present':
            operation = 'configure_interfaces'
        elif state == 'absent':
            operation = 'deconfigure_interfaces'

    # If operation is specified, it takes precedence over state
    # No additional mapping needed as operation is explicit

    # Validate configuration files
    if not validate_config_file(interface_config_file):
        module.fail_json(
            msg=f"Interface configuration file not found or not readable: {interface_config_file}"
        )

    if circuit_config_file and not validate_config_file(circuit_config_file):
        module.fail_json(
            msg=f"Circuit configuration file not found or not readable: {circuit_config_file}"
        )

    # Validate operation-specific requirements
    circuit_operations = [
        'configure_wan_circuits_interfaces',
        'deconfigure_wan_circuits_interfaces',
        'configure_circuits',
        'deconfigure_circuits'
    ]

    if operation in circuit_operations and not circuit_config_file:
        module.fail_json(
            msg=f"Operation '{operation}' requires 'circuit_config_file' parameter"
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
        graphiant_config = connection.graphiant_config

        # Execute the requested operation
        changed = False
        result_msg = ""

        if operation == 'configure_interfaces':
            result = execute_with_logging(module, graphiant_config.interfaces.configure_interfaces,
                                          interface_config_file, circuit_config_file,
                                          success_msg="Successfully configured all interfaces")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_interfaces':
            result = execute_with_logging(module, graphiant_config.interfaces.deconfigure_interfaces,
                                          interface_config_file, circuit_config_file, circuits_only,
                                          success_msg="Successfully deconfigured all interfaces")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_lan_interfaces':
            result = execute_with_logging(module, graphiant_config.interfaces.configure_lan_interfaces,
                                          interface_config_file,
                                          success_msg="Successfully configured LAN interfaces")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_lan_interfaces':
            result = execute_with_logging(module, graphiant_config.interfaces.deconfigure_lan_interfaces,
                                          interface_config_file,
                                          success_msg="Successfully deconfigured LAN interfaces")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_wan_circuits_interfaces':
            result = execute_with_logging(module, graphiant_config.interfaces.configure_wan_circuits_interfaces,
                                          circuit_config_file, interface_config_file,
                                          success_msg="Successfully configured WAN circuits and interfaces")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_wan_circuits_interfaces':
            result = execute_with_logging(module, graphiant_config.interfaces.deconfigure_wan_circuits_interfaces,
                                          interface_config_file, circuit_config_file, circuits_only,
                                          success_msg="Successfully deconfigured WAN circuits and interfaces")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_circuits':
            result = execute_with_logging(module, graphiant_config.interfaces.configure_circuits,
                                          circuit_config_file, interface_config_file,
                                          success_msg="Successfully configured circuits")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_circuits':
            result = execute_with_logging(module, graphiant_config.interfaces.deconfigure_circuits,
                                          circuit_config_file, interface_config_file,
                                          success_msg="Successfully deconfigured circuits")
            changed = result['changed']
            result_msg = result['result_msg']

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
