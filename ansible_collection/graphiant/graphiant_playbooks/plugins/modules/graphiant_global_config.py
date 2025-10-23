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
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.graphiant.graphiant_playbooks.plugins.module_utils.graphiant_utils import (
    get_graphiant_connection,
    handle_graphiant_exception,
    validate_config_file
)


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
            required=True,
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
                'deconfigure_vpn_profiles'
            ]
        ),
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
        supports_check_mode=True
    )

    # Get parameters
    params = module.params
    operation = params['operation']
    config_file = params['config_file']

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
        edge = connection.edge

        # Execute the requested operation
        changed = False
        result_msg = ""

        if operation == 'configure':
            edge.global_config.configure(config_file)
            changed = True
            result_msg = "Successfully configured all global objects"

        elif operation == 'deconfigure':
            edge.global_config.deconfigure(config_file)
            changed = True
            result_msg = "Successfully deconfigured all global objects"

        elif operation == 'configure_prefix_sets':
            edge.global_config.configure_prefix_sets(config_file)
            changed = True
            result_msg = "Successfully configured global prefix sets"

        elif operation == 'deconfigure_prefix_sets':
            edge.global_config.deconfigure_prefix_sets(config_file)
            changed = True
            result_msg = "Successfully deconfigured global prefix sets"

        elif operation == 'configure_bgp_filters':
            edge.global_config.configure_bgp_filters(config_file)
            changed = True
            result_msg = "Successfully configured global BGP filters"

        elif operation == 'deconfigure_bgp_filters':
            edge.global_config.deconfigure_bgp_filters(config_file)
            changed = True
            result_msg = "Successfully deconfigured global BGP filters"

        elif operation == 'configure_snmp_services':
            edge.global_config.configure_snmp_services(config_file)
            changed = True
            result_msg = "Successfully configured global SNMP services"

        elif operation == 'deconfigure_snmp_services':
            edge.global_config.deconfigure_snmp_services(config_file)
            changed = True
            result_msg = "Successfully deconfigured global SNMP services"

        elif operation == 'configure_syslog_services':
            edge.global_config.configure_syslog_services(config_file)
            changed = True
            result_msg = "Successfully configured global syslog services"

        elif operation == 'deconfigure_syslog_services':
            edge.global_config.deconfigure_syslog_services(config_file)
            changed = True
            result_msg = "Successfully deconfigured global syslog services"

        elif operation == 'configure_ipfix_services':
            edge.global_config.configure_ipfix_services(config_file)
            changed = True
            result_msg = "Successfully configured global IPFIX services"

        elif operation == 'deconfigure_ipfix_services':
            edge.global_config.deconfigure_ipfix_services(config_file)
            changed = True
            result_msg = "Successfully deconfigured global IPFIX services"

        elif operation == 'configure_vpn_profiles':
            edge.global_config.configure_vpn_profiles(config_file)
            changed = True
            result_msg = "Successfully configured global VPN profiles"

        elif operation == 'deconfigure_vpn_profiles':
            edge.global_config.deconfigure_vpn_profiles(config_file)
            changed = True
            result_msg = "Successfully deconfigured global VPN profiles"

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
