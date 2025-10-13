#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ansible module for managing Graphiant BGP peering and routing policies.

This module provides BGP management capabilities including:
- BGP peering configuration and deconfiguration
- Policy attachment and detachment
- Routing policy management
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
    Main function for the Graphiant BGP module.
    """

    # Define module arguments
    argument_spec = dict(
        host=dict(type='str', required=True, aliases=['base_url']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        bgp_config_file=dict(type='str', required=True),
        operation=dict(
            type='str',
            required=False,
            choices=[
                'configure',
                'deconfigure',
                'detach_policies'
            ]
        ),
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
    bgp_config_file = params['bgp_config_file']

    # Validate that at least one of operation or state is provided
    if not operation and not state:
        supported_operations = ['configure', 'deconfigure', 'detach_policies']
        module.fail_json(
            msg="Either 'operation' or 'state' parameter must be provided. "
                f"Supported operations: {', '.join(supported_operations)}"
        )

    # If operation is not specified, use state to determine operation
    if not operation:
        if state == 'present':
            operation = 'configure'
        elif state == 'absent':
            operation = 'deconfigure'

    # If operation is specified, it takes precedence over state
    # No additional mapping needed as operation is explicit

    # Validate configuration file
    if not validate_config_file(bgp_config_file):
        module.fail_json(
            msg=f"BGP configuration file not found or not readable: {bgp_config_file}"
        )

    # Handle check mode
    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f"Check mode: Would execute {operation}",
            operation=operation,
            bgp_config_file=bgp_config_file
        )

    try:
        # Get Graphiant connection
        connection = get_graphiant_connection(params)
        edge = connection.edge

        # Execute the requested operation
        changed = False
        result_msg = ""

        if operation == 'configure':
            result = execute_with_logging(module, edge.bgp.configure, bgp_config_file,
                                          success_msg="Successfully configured BGP peering and attached policies")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'detach_policies':
            result = execute_with_logging(module, edge.bgp.detach_policies, bgp_config_file,
                                          success_msg="Successfully detached policies from BGP peers")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure':
            result = execute_with_logging(module, edge.bgp.deconfigure, bgp_config_file,
                                          success_msg="Successfully deconfigured BGP peering")
            changed = result['changed']
            result_msg = result['result_msg']

        # Return success
        module.exit_json(
            changed=changed,
            msg=result_msg,
            operation=operation,
            bgp_config_file=bgp_config_file
        )

    except Exception as e:
        error_msg = handle_graphiant_exception(e, operation)
        module.fail_json(msg=error_msg, operation=operation)


if __name__ == '__main__':
    main()
