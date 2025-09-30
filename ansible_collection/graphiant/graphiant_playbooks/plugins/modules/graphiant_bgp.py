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
            required=True,
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
    bgp_config_file = params['bgp_config_file']
    
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
            edge.bgp.configure(bgp_config_file)
            changed = True
            result_msg = "Successfully configured BGP peering and attached policies"
            
        elif operation == 'detach_policies':
            edge.bgp.detach_policies(bgp_config_file)
            changed = True
            result_msg = "Successfully detached policies from BGP peers"
            
        elif operation == 'deconfigure':
            edge.bgp.deconfigure(bgp_config_file)
            changed = True
            result_msg = "Successfully deconfigured BGP peering"
        
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
