#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Graphiant Team <support@graphiant.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Ansible module for invoking individual Graphiant portal API calls.
"""

DOCUMENTATION = r"""
---
module: graphiant_api
short_description: Invoke a single Graphiant portal API call
description:
  - >-
    Calls one Graphiant portal API method by name and returns its response, for
    procedural workflows that need individual API calls rather than declarative
    configuration management.
  - >-
    Used by the gateway VM lifecycle playbooks, where each step (obtain a token, look up a
    device, poll status) is a distinct call whose result feeds the next task.
  - >-
    Prefer the resource-specific modules such as M(graphiant.naas.graphiant_interfaces) or
    M(graphiant.naas.graphiant_sites) for ordinary configuration management. They are
    idempotent and config-file driven; this module is a lower-level escape hatch.
  - Only the methods listed under O(method) may be called.
version_added: "26.7.0"
extends_documentation_fragment:
  - graphiant.naas.graphiant_portal_auth
options:
  method:
    description:
      - Name of the portal API method to call.
      - >-
        Read-only methods (C(get_)/C(post_troubleshooting_device_by_device_id)) report
        RV(ignore:changed) as false; the remaining methods report it as true.
    type: str
    required: true
    choices:
      - get_all_enterprises
      - get_bearer_token
      - get_device_info
      - get_edges_summary
      - get_software_download_url
      - get_software_releases_summary
      - post_device_bringup_token
      - post_troubleshooting_device_by_device_id
      - put_device_config
      - put_devices_bringup
  kwargs:
    description:
      - Keyword arguments for the selected O(method).
      - Omit for methods that take no arguments, such as C(get_bearer_token).
    type: dict
    required: false
  detailed_logs:
    description: Enable detailed logging in the task result message.
    type: bool
    default: false
attributes:
  check_mode:
    description: Supports check mode with partial support.
    support: partial
    details: >
      Read-only methods (the C(get_) methods and
      C(post_troubleshooting_device_by_device_id)) execute normally in check mode and return
      their real response. The state-modifying methods (C(post_device_bringup_token),
      C(put_device_config), C(put_devices_bringup)) are not called at all; the module
      returns V(changed=True) without a RV(ignore:response_data) value, since the result
      cannot be known without performing the call.
requirements:
  - python >= 3.7
  - graphiant-sdk >= 26.7.0
seealso:
  - module: graphiant.naas.graphiant_device_config
    description: Declarative device configuration management.
author:
  - Graphiant Team (@graphiant)
"""

EXAMPLES = r"""
- name: Get a bearer token
  graphiant.naas.graphiant_api:
    method: get_bearer_token
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
  register: token_response

- name: Look up a device by hostname
  graphiant.naas.graphiant_api:
    method: get_edges_summary
    kwargs:
      hostname: "gateway-1-sdktest"
    host: "{{ graphiant_host }}"
    access_token: "{{ token_response.response_data }}"
  register: edge_summary_response

- name: Wait for the device to report Ready
  graphiant.naas.graphiant_api:
    method: get_edges_summary
    kwargs:
      device_id: "{{ device_id }}"
    host: "{{ graphiant_host }}"
    access_token: "{{ token_response.response_data }}"
  register: portal_status_response
  retries: 10
  delay: 30
  until: >
    portal_status_response is succeeded
    and portal_status_response.get('response_data') is not none
    and portal_status_response['response_data'].get('portal_status', '') == 'Ready'

- name: Generate a device onboarding token
  graphiant.naas.graphiant_api:
    method: post_device_bringup_token
    kwargs:
      role: Gateway
      validity_sec: 3600
    host: "{{ graphiant_host }}"
    access_token: "{{ token_response.response_data }}"
  register: onboarding_token_response
"""

RETURN = r"""
msg:
  description: Human-readable result (includes detailed logs when enabled).
  type: str
  returned: always
method:
  description: The API method that was called.
  type: str
  returned: always
response_data:
  description:
    - The API response, converted to plain serializable data.
    - >-
      Omitted when the call fails, so tasks can poll on
      C(response_data is not none) without matching a failed call.
  type: raw
  returned: on success
"""

from typing import Any  # noqa: E402

from ansible.module_utils.basic import AnsibleModule  # noqa: E402

from ansible_collections.graphiant.naas.plugins.module_utils.graphiant_utils import (  # noqa: E402
    graphiant_portal_auth_argument_spec,
    get_graphiant_connection,
    handle_graphiant_exception,
)
from ansible_collections.graphiant.naas.plugins.module_utils.logging_decorator import (  # noqa: E402
    capture_library_logs,
)

# Methods callable through this module. Dispatch is restricted to this allowlist rather
# than resolving any attribute on the client, so a playbook cannot reach arbitrary
# internals. The value records whether the call modifies portal state.
SUPPORTED_METHODS = {
    "get_all_enterprises": False,
    "get_bearer_token": False,
    "get_device_info": False,
    "get_edges_summary": False,
    "get_software_download_url": False,
    "get_software_releases_summary": False,
    # Reads troubleshooting counters; POST only because it takes a time-window body.
    "post_troubleshooting_device_by_device_id": False,
    "post_device_bringup_token": True,
    "put_device_config": True,
    "put_devices_bringup": True,
}


def convert_to_serializable(module, obj: Any) -> Any:
    """
    Convert SDK response objects into structures Ansible can return.

    The SDK returns Pydantic models, which are not JSON-serializable as-is.
    """
    try:
        if hasattr(obj, "model_dump"):  # Pydantic v2
            return obj.model_dump()
        if hasattr(obj, "dict"):  # Pydantic v1
            return obj.dict()
        if isinstance(obj, dict):
            return {key: convert_to_serializable(module, value) for key, value in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [convert_to_serializable(module, item) for item in obj]
        if hasattr(obj, "__dict__"):
            return {
                name: convert_to_serializable(module, value)
                for name, value in obj.__dict__.items()
                if not name.startswith("_")
            }
        return obj
    except Exception as e:  # noqa: BLE001
        module.warn(f"Failed to convert response of type {type(obj)}: {e}")
        return str(obj)


@capture_library_logs
def execute_with_logging(module, func, *args, **kwargs):
    success_msg = kwargs.pop("success_msg", "API call completed successfully")
    result = func(*args, **kwargs)
    return {"result_msg": success_msg, "details": result}


def main():
    argument_spec = dict(
        **graphiant_portal_auth_argument_spec(),
        method=dict(type="str", required=True, choices=sorted(SUPPORTED_METHODS)),
        kwargs=dict(type="dict", required=False, default=None),
        detailed_logs=dict(type="bool", required=False, default=False),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    params = module.params
    method_name = params["method"]
    method_kwargs = params.get("kwargs") or {}
    modifies_state = SUPPORTED_METHODS[method_name]

    if modifies_state and module.check_mode:
        module.exit_json(
            changed=True,
            msg=f"Check mode: skipped {method_name}",
            method=method_name,
        )
        return

    try:
        connection = get_graphiant_connection(params, check_mode=module.check_mode)
        client = connection.graphiant_config.config_utils.gsdk

        result = execute_with_logging(
            module,
            getattr(client, method_name),
            success_msg=f"Completed {method_name}",
            **method_kwargs,
        )
        module.exit_json(
            changed=modifies_state,
            msg=result["result_msg"],
            method=method_name,
            response_data=convert_to_serializable(module, result.get("details")),
        )

    except Exception as e:
        error_msg = handle_graphiant_exception(e, method_name)
        # response_data is deliberately omitted so callers can poll on its absence.
        module.fail_json(msg=error_msg, method=method_name)


if __name__ == "__main__":
    main()
