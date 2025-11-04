#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ansible module for managing Graphiant Data Exchange services, customers, and matches.

This module provides Data Exchange management capabilities including:
- Data Exchange services creation and deletion
- Data Exchange customers creation and deletion
- Service-to-customer matching operations
- Summary and query operations for services and customers
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.graphiant.graphiant_playbooks.plugins.module_utils.graphiant_utils import (
    get_graphiant_connection,
    handle_graphiant_exception
    )
from ansible_collections.graphiant.graphiant_playbooks.plugins.module_utils.logging_decorator import (
    capture_library_logs
)

DOCUMENTATION = r'''
---
module: graphiant_data_exchange
short_description: Manage Graphiant Data Exchange services, customers, and matches
description:
  - This module provides comprehensive Data Exchange management capabilities for Graphiant's B2B peering platform.
  - Supports creating, deleting, and querying Data Exchange services and customers.
  - Enables service-to-customer matching operations for Data Exchange workflows.
  - Provides detailed logging and summary operations for monitoring and management.
  - Supports tabulated output for better readability of summaries and operations.
version_added: "1.0.0"
options:
  operation:
    description:
      - The specific Data Exchange operation to perform.
      - create_services: Create Data Exchange services from YAML configuration
      - delete_services: Delete Data Exchange services from YAML configuration
      - get_services_summary: Get summary of all Data Exchange services with tabulated output
      - create_customers: Create Data Exchange customers from YAML configuration
      - delete_customers: Delete Data Exchange customers from YAML configuration
      - get_customers_summary: Get summary of all Data Exchange customers with tabulated output
      - match_service_to_customers: Match services to customers from YAML configuration with status validation
      - accept_invitation: Accept Data Exchange service invitation (Workflow 4) - requires config_file
      - get_service_health: Get service health monitoring information
    type: str
    choices:
      - create_services
      - delete_services
      - get_services_summary
      - create_customers
      - delete_customers
      - get_customers_summary
      - match_service_to_customers
      - accept_invitation
      - get_service_health
    required: true
  state:
    description:
      - The desired state of the Data Exchange resources.
      - present: Create/configure Data Exchange resources
      - absent: Delete/deconfigure Data Exchange resources
      - query: Get information about Data Exchange resources
    type: str
    choices:
      - present
      - absent
      - query
    default: present
  config_file:
    description:
      - Path to the YAML configuration file for the operation.
      - Required for create_services, delete_services, create_customers, delete_customers,
        match_service_to_customers, and accept_invitation operations.
      - The configuration file should contain the appropriate Data Exchange resource definitions.
      - For accept_invitation operation, the file should contain data_exchange_acceptances list with acceptance details.
    type: str
  matches_file:
    description:
      - Path to the matches responses JSON file for match ID lookup.
      - Optional for accept_invitation operation.
      - If not provided, uses default matches file.
    type: str
  dry_run:
    description:
      - Enable dry-run mode for accept_invitation operation.
      - When enabled, validates configuration without making actual API calls.
      - Useful for testing and validation before actual execution.
    type: bool
    default: false
  detailed_logs:
    description:
      - Enable detailed logging output for troubleshooting and monitoring.
      - When enabled, provides comprehensive logs of all Data Exchange operations.
      - Logs are captured and included in the result_msg for display using debug module.
    type: bool
    default: false
  host:
    description:
      - Graphiant portal host URL for API connectivity.
      - Example: "https://api.graphiant.com"
    type: str
    required: true
  username:
    description:
      - Graphiant portal username for authentication.
    type: str
    required: true
  password:
    description:
      - Graphiant portal password for authentication.
    type: str
    required: true
    no_log: true
  service_name:
    description:
      - Service name for health monitoring operations.
      - Required for get_service_health operations.
    type: str
  is_provider:
    description:
      - Whether to get provider view for service health monitoring.
      - Used with get_service_health operation.
    type: bool
    default: false

requirements:
  - python >= 3.6
  - graphiant-sdk
  - tabulate

author:
  - Graphiant Team

'''

EXAMPLES = r'''
# Create Data Exchange services with detailed logging
- name: Create Data Exchange services
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: create_services
    config_file: "sample_data_exchange_services.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: create_result

- name: Display detailed logs
  debug:
    msg: "{{ create_result.result_msg }}"

# Delete Data Exchange services
- name: Delete Data Exchange services
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: delete_services
    config_file: "sample_data_exchange_services.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"

# Get services summary with tabulated output
- name: Get Data Exchange services summary
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: get_services_summary
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
  register: services_summary

- name: Display services summary
  debug:
    msg: "{{ services_summary.result_msg }}"

# Create Data Exchange customers
- name: Create Data Exchange customers
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: create_customers
    config_file: "sample_data_exchange_customers.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"

# Delete Data Exchange customers
- name: Delete Data Exchange customers
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: delete_customers
    config_file: "sample_data_exchange_customers.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"

# Get customers summary with tabulated output
- name: Get Data Exchange customers summary
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: get_customers_summary
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
  register: customers_summary

- name: Display customers summary
  debug:
    msg: "{{ customers_summary.result_msg }}"

# Match services to customers with intelligent status checking
- name: Match Data Exchange services to customers
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: match_service_to_customers
    config_file: "sample_data_exchange_matches.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: match_result

- name: Display match operation details
  debug:
    msg: "{{ match_result.result_msg }}"

# Using state parameter for cleaner syntax
- name: Create services using state parameter
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    state: present
    operation: create_services
    config_file: "sample_data_exchange_services.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"

- name: Delete services using state parameter
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    state: absent
    operation: delete_services
    config_file: "sample_data_exchange_services.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"

- name: Query services using state parameter
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    state: query
    operation: get_services_summary
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"

# Complete Data Exchange workflow
- name: Complete Data Exchange workflow
  block:
    - name: Create services
      graphiant.graphiant_playbooks.graphiant_data_exchange:
        operation: create_services
        config_file: "sample_data_exchange_services.yaml"
        host: "{{ graphiant_host }}"
        username: "{{ graphiant_username }}"
        password: "{{ graphiant_password }}"
        detailed_logs: true
      register: create_services_result

    - name: Create customers
      graphiant.graphiant_playbooks.graphiant_data_exchange:
        operation: create_customers
        config_file: "sample_data_exchange_customers.yaml"
        host: "{{ graphiant_host }}"
        username: "{{ graphiant_username }}"
        password: "{{ graphiant_password }}"
        detailed_logs: true
      register: create_customers_result

    - name: Match services to customers
      graphiant.graphiant_playbooks.graphiant_data_exchange:
        operation: match_service_to_customers
        config_file: "sample_data_exchange_matches.yaml"
        host: "{{ graphiant_host }}"
        username: "{{ graphiant_username }}"
        password: "{{ graphiant_password }}"
        detailed_logs: true
      register: match_result

    - name: Display workflow results
      debug:
        msg: "{{ item.result_msg }}"
      loop:
        - "{{ create_services_result }}"
        - "{{ create_customers_result }}"
        - "{{ match_result }}"

# Accept Data Exchange service invitation (Workflow 4)
- name: Accept Data Exchange service invitation
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: accept_invitation
    config_file: "sample_data_exchange_acceptance.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: accept_result

- name: Display acceptance result
  debug:
    msg: "{{ accept_result.result_msg }}"

# Get service health
- name: Get service health
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: get_service_health
    service_name: "de-service-1"
    is_provider: false
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: service_health
'''

RETURN = r'''
result_msg:
  description: Result message from the operation, including detailed logs when detailed_logs is enabled
  type: str
  returned: always
  sample: "Successfully created 3 Data Exchange services\n\nDetailed logs:
          \n2025-10-19 23:08:05,315 - Graphiant_playbook - INFO - Creating service 'de-service-1'..."
result_data:
  description: Result data from the operation, including structured data for summary operations
  type: dict
  returned: when applicable
  sample: {"services": [{"name": "de-service-1", "status": "ACTIVE", "id": 123}], "summary": {"total": 3, "created": 3}}
changed:
  description: Whether the operation made changes to the system
  type: bool
  returned: always
  sample: true
operation:
  description: The operation that was performed
  type: str
  returned: always
  sample: "create_services"
config_file:
  description: The configuration file used for the operation
  type: str
  returned: when applicable
  sample: "sample_data_exchange_services.yaml"
'''


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
    """Main function for the Data Exchange module."""

    # Define module arguments
    argument_spec = dict(
        host=dict(type='str', required=True, aliases=['base_url']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        operation=dict(
            type='str',
            required=False,
            choices=[
                'create_services',
                'delete_services',
                'get_services_summary',
                'create_customers',
                'delete_customers',
                'get_customers_summary',
                'match_service_to_customers',
                'accept_invitation',
                'get_service_health'
            ]
        ),
        state=dict(
            type='str',
            choices=['present', 'absent', 'query'],
            default='present'
        ),
        config_file=dict(type='str', required=False),
        matches_file=dict(type='str', required=False),
        detailed_logs=dict(type='bool', default=False),
        dry_run=dict(type='bool', default=False),
        service_name=dict(type='str', required=False),
        is_provider=dict(type='bool', default=False)
    )

    # Create module instance
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        mutually_exclusive=[
            ('operation', 'state')
        ],
        required_one_of=[
            ('operation', 'state')
        ]
    )

    # Get parameters
    params = module.params
    operation = params.get('operation')
    state = params.get('state')
    config_file = params.get('config_file')

    # Determine operation based on state if operation not provided
    if not operation:
        if state == 'present':
            # Default to create_services for present state
            operation = 'create_services'
        elif state == 'absent':
            # Default to delete_services for absent state
            operation = 'delete_services'
        elif state == 'query':
            # Default to get_services_summary for query state
            operation = 'get_services_summary'

    # Validate required parameters
    if operation in ['create_services', 'delete_services', 'create_customers', 'delete_customers',
                     'match_service_to_customers']:
        if not config_file:
            module.fail_json(
                msg=f"config_file parameter is required for operation '{operation}'"
            )

    try:
        # Get Graphiant connection
        connection = get_graphiant_connection(params)
        graphiant_config = connection.graphiant_config

        # Execute the requested operation
        changed = False
        result_msg = ""
        result_data = {}

        if operation == 'create_services':
            result = execute_with_logging(module, graphiant_config.data_exchange.create_services,
                                          config_file,
                                          success_msg=f"Successfully created Data Exchange services from {config_file}")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'delete_services':
            result = execute_with_logging(module, graphiant_config.data_exchange.delete_services,
                                          config_file,
                                          success_msg=f"Successfully deleted Data Exchange services from {config_file}")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'get_services_summary':
            result = execute_with_logging(module, graphiant_config.data_exchange.get_services_summary,
                                          success_msg="Successfully retrieved Data Exchange services summary")
            result_msg = result['result_msg']
            result_data = result.get('result_data', {})

        elif operation == 'create_customers':
            result = execute_with_logging(module, graphiant_config.data_exchange.create_customers,
                                          config_file,
                                          success_msg=f"Successfully created Data Exchange customers {config_file}")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'delete_customers':
            result = execute_with_logging(module, graphiant_config.data_exchange.delete_customers,
                                          config_file,
                                          success_msg=f"Successfully deleted Data Exchange customers {config_file}")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'get_customers_summary':
            result = execute_with_logging(module, graphiant_config.data_exchange.get_customers_summary,
                                          success_msg="Successfully retrieved Data Exchange customers summary")
            result_msg = result['result_msg']
            result_data = result.get('result_data', {})

        elif operation == 'match_service_to_customers':
            result = execute_with_logging(module, graphiant_config.data_exchange.match_service_to_customers,
                                          config_file,
                                          success_msg="Successfully matched Data Exchange services to customers")
            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'accept_invitation':
            # accept_invitation operation supports config_file and optional matches_file, dry_run
            if not config_file:
                module.fail_json(msg="accept_invitation operation requires config_file parameter")

            matches_file = params.get('matches_file')
            dry_run = params.get('dry_run', False)

            success_msg = f"Successfully accepted Data Exchange service invitation from {config_file}"
            if dry_run:
                success_msg = f"DRY-RUN: Validated Data Exchange service invitation from {config_file} " \
                              "(API calls skipped)"

            result = execute_with_logging(module, graphiant_config.data_exchange.accept_invitation,
                                          config_file, matches_file, dry_run,
                                          success_msg=success_msg)

            changed = result['changed']
            result_msg = result['result_msg']

        elif operation == 'get_service_health':
            service_name = params.get('service_name')
            is_provider = params.get('is_provider', False)

            if not service_name:
                module.fail_json(msg="get_service_health operation requires service_name parameter")

            result = execute_with_logging(
              module, graphiant_config.data_exchange.get_service_health, service_name, is_provider,
              success_msg=f"Successfully retrieved service health for service {service_name}")
            result_msg = result['result_msg']
            result_data = result.get('result_data', {})

        else:
            module.fail_json(
                msg=f"Unsupported operation: {operation}. "
                    f"Supported operations are: create_services, delete_services, get_services_summary, "
                    f"create_customers, delete_customers, get_customers_summary, match_service_to_customers, "
                    f"accept_invitation, get_service_health"
            )

        # Return success
        module.exit_json(
            changed=changed,
            result_msg=result_msg,
            result_data=result_data
        )

    except Exception as e:
        error_msg = handle_graphiant_exception(e, operation or 'unknown')
        module.fail_json(msg=error_msg, operation=operation or 'unknown')


if __name__ == '__main__':
    main()
