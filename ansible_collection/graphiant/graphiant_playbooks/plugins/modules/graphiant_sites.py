#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ansible module for managing Graphiant site attachments and detachments.

This module provides site management capabilities including:
- Attaching global system objects to sites
- Detaching global system objects from sites
- Managing site-level configurations
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.graphiant.graphiant_playbooks.plugins.module_utils.graphiant_utils import (
    get_graphiant_connection,
    handle_graphiant_exception,
    validate_config_file
)


def main():
    """
    Main function for the Graphiant sites module.
    """

    # Define module arguments
    argument_spec = dict(
        host=dict(type='str', required=True, aliases=['base_url']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        site_config_file=dict(type='str', required=True),
        operation=dict(
            type='str',
            required=True,
            choices=[
                'configure',
                'deconfigure',
                'attach',
                'detach'
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
    site_config_file = params['site_config_file']

    # Validate configuration file
    if not validate_config_file(site_config_file):
        module.fail_json(
            msg=f"Site configuration file not found or not readable: {site_config_file}"
        )

    # Handle check mode
    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f"Check mode: Would execute {operation}",
            operation=operation,
            site_config_file=site_config_file
        )

    try:
        # Get Graphiant connection
        connection = get_graphiant_connection(params)
        edge = connection.edge

        # Execute the requested operation
        changed = False
        result_msg = ""

        if operation in ['configure', 'attach']:
            edge.sites.configure(site_config_file)
            changed = True
            result_msg = "Successfully attached global system objects to sites"

        elif operation in ['deconfigure', 'detach']:
            edge.sites.deconfigure(site_config_file)
            changed = True
            result_msg = "Successfully detached global system objects from sites"

        # Return success
        module.exit_json(
            changed=changed,
            msg=result_msg,
            operation=operation,
            site_config_file=site_config_file
        )

    except Exception as e:
        error_msg = handle_graphiant_exception(e, operation)
        module.fail_json(msg=error_msg, operation=operation)


if __name__ == '__main__':
    main()
