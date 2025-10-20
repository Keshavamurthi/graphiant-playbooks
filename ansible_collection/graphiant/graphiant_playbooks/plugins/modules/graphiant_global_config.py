#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ansible module for managing Graphiant global configuration objects.

This module provides global configuration management capabilities including:
- Prefix sets configuration and deconfiguration
- BGP filters (routing policies) management
- SNMP services management
- Syslog services management
- IPFIX services management
- VPN profiles management
- LAN segments management
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
    Main function for the Graphiant global configuration module.
    """

    # Define module arguments
    argument_spec = dict(
        host=dict(type='str', required=True, aliases=['base_url']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        config_file=dict(type='str', required=True),
        operation=dict(
            type='str',
            required=False,
            choices=[
                'configure',
                'deconfigure',
                'configure_prefix_sets',
                'deconfigure_prefix_sets',
                'configure_bgp_filters',
                'deconfigure_bgp_filters',
                'configure_snmp_services',
                'deconfigure_snmp_services',
                'configure_syslog_services',
                'deconfigure_syslog_services',
                'configure_ipfix_services',
                'deconfigure_ipfix_services',
                'configure_vpn_profiles',
                'deconfigure_vpn_profiles',
                'configure_lan_segments',
                'deconfigure_lan_segments',
                'configure_site_lists',
                'deconfigure_site_lists'
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
    config_file = params['config_file']

    # Validate that at least one of operation or state is provided
    if not operation and not state:
        supported_operations = [
            'configure', 'deconfigure', 'configure_prefix_sets', 'deconfigure_prefix_sets',
            'configure_bgp_filters', 'deconfigure_bgp_filters', 'configure_snmp_services',
            'deconfigure_snmp_services', 'configure_syslog_services', 'deconfigure_syslog_services',
            'configure_ipfix_services', 'deconfigure_ipfix_services', 'configure_vpn_profiles',
            'deconfigure_vpn_profiles', 'configure_lan_segments', 'deconfigure_lan_segments',
            'configure_site_lists', 'deconfigure_site_lists'
        ]
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
    if not validate_config_file(config_file):
        module.fail_json(
            msg=f"Configuration file not found or not readable: {config_file}"
        )

    # Handle check mode
    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f"Check mode: Would execute {operation}",
            operation=operation,
            config_file=config_file
        )

    try:
        # Get Graphiant connection
        connection = get_graphiant_connection(params)
        graphiant_config = connection.graphiant_config

        # Execute the requested operation
        changed = False
        result_msg = ""

        if operation == 'configure':
            result = execute_with_logging(module, graphiant_config.global_config.configure, config_file,
                                          success_msg="Successfully configured all global objects")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure, config_file,
                                          success_msg="Successfully deconfigured all global objects")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_prefix_sets':
            result = execute_with_logging(module, graphiant_config.global_config.configure_prefix_sets,
                                          config_file,
                                          success_msg="Successfully configured global prefix sets")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_prefix_sets':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_prefix_sets,
                                          config_file,
                                          success_msg="Successfully deconfigured global prefix sets")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_bgp_filters':
            result = execute_with_logging(module, graphiant_config.global_config.configure_bgp_filters,
                                          config_file,
                                          success_msg="Successfully configured global BGP filters")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_bgp_filters':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_bgp_filters,
                                          config_file,
                                          success_msg="Successfully deconfigured global BGP filters")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_snmp_services':
            result = execute_with_logging(module, graphiant_config.global_config.configure_snmp_services,
                                          config_file,
                                          success_msg="Successfully configured global SNMP services")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_snmp_services':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_snmp_services,
                                          config_file,
                                          success_msg="Successfully deconfigured global SNMP services")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_syslog_services':
            result = execute_with_logging(module, graphiant_config.global_config.configure_syslog_services,
                                          config_file,
                                          success_msg="Successfully configured global syslog services")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_syslog_services':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_syslog_services,
                                          config_file,
                                          success_msg="Successfully deconfigured global syslog services")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_ipfix_services':
            result = execute_with_logging(module, graphiant_config.global_config.configure_ipfix_services,
                                          config_file,
                                          success_msg="Successfully configured global IPFIX services")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_ipfix_services':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_ipfix_services,
                                          config_file,
                                          success_msg="Successfully deconfigured global IPFIX services")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_vpn_profiles':
            result = execute_with_logging(module, graphiant_config.global_config.configure_vpn_profiles,
                                          config_file,
                                          success_msg="Successfully configured global VPN profiles")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_vpn_profiles':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_vpn_profiles,
                                          config_file,
                                          success_msg="Successfully deconfigured global VPN profiles")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_lan_segments':
            result = execute_with_logging(module, graphiant_config.global_config.configure_lan_segments,
                                          config_file,
                                          success_msg="Successfully configured global LAN segments")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_lan_segments':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_lan_segments,
                                          config_file,
                                          success_msg="Successfully deconfigured global LAN segments")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'configure_site_lists':
            result = execute_with_logging(module, graphiant_config.global_config.configure_site_lists,
                                          config_file,
                                          success_msg="Successfully configured global site lists")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'deconfigure_site_lists':
            result = execute_with_logging(module, graphiant_config.global_config.deconfigure_site_lists,
                                          config_file,
                                          success_msg="Successfully deconfigured global site lists")
            changed = result['changed']
            result_msg = result['result_msg']

        # Return success
        module.exit_json(
            changed=changed,
            msg=result_msg,
            operation=operation,
            config_file=config_file
        )

    except Exception as e:
        error_msg = handle_graphiant_exception(e, operation)
        module.fail_json(msg=error_msg, operation=operation)


if __name__ == '__main__':
    main()
