#!/usr/bin/python

# Copyright: (c) 2025, Graphiant Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: graphiant_api_requests

short_description: Graphiant Portal Rest API requests generic module.

version_added: "1.0.0"

description: Graphiant Portal Rest API requests generic module.

options:
    method:
        description: Method for the Request object: GET, POST,PUT,PATCH, or DELETE.
        required: false
        default: GET
        type: str
    uri:
        description: Graphiant Portal API Endpoint.
        required: true
        type: str
    json:
        description: A JSON serializable Python object to send in the body of the Request.
        required: false
        type: json
    base_url:
        description: Graphiant Portal API Base URL.
        required: true
        type: str
    username:
        description: Graphiant Portal API Username.
        required: true
        type: str
    password:
        description: Graphiant Portal API User Password. (Can be passed during runtime using --extra-var)
        required: true
        type: str 

requirements:

'''

EXAMPLES = r'''
# Pass case

---
- name: Graphiant Portal Client Examples
  hosts: localhost
  gather_facts: false

  vars:
    # portal_api_url: 
    # portal_username: 
    # portal_password: 

    gcs_client_params: &gcs_client_params
      base_url: "{{ portal_api_url }}"
      username: "{{ portal_username }}"
      password: "{{ portal_password }}"

  tasks:
    - name: Sending REST API request to Graphiant Portal
      graphiant.portal.graphiant_api_requests:
        <<: *gcs_client_params
        method: GET
        uri: v1/devices
      register: request_results
    - name: Display request_results
      ansible.builtin.debug:
        var: request_results

'''

RETURN = r'''

% ansible-playbook tasks/graphiant_portal_rest_client_example.yml --check -e=@vars/credentials.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Graphiant Portal Client Examples] ****************************************************************************************************************************************************************************

TASK [Sending REST API request to Graphiant Portal] ****************************************************************************************************************************************************************
[WARNING]: Module did not set no_log for password
ok: [localhost]

TASK [Display request_results] *************************************************************************************************************************************************************************************
ok: [localhost] => {
    "request_results": {
        "changed": false,
        "failed": false,
        "msg": {
            "devices": [
                {
                    "bgpEnabled": true,
                    "configUpdatedAt": {
                        "nanos": 183290000,
                        "seconds": 1703888554
                    },
                    "createdAt": {
                        "nanos": 185775000,
                        "seconds": 1703888554
                    },
                    "dhcpServerEnabled": true,
                    "hostname": "tunnel-terminator-30000000xyz",
                    "id": 30000000xyz,
                    "ipfixEnabled": true,
                    "lastBootedAt": {
                        "nanos": 567666000,
                        "seconds": 1739392902
                    },
                    "operStaledAt": {
                        "nanos": 230835000,
                        "seconds": 1739668756
                    },
                    "ospfv2Enabled": true,
                    "ospfv3Enabled": true,
                    "rebootReason": "User requested reboot",
                    "role": "tunnel_terminator",
                    "serialNumber": "xyz82c77-62d4-4126-9a88-cdbe1d637831",
                    "staticRoutesEnabled": true,
                    "status": "active",
                    "uptime": {
                        "nanos": 938792032,
                        "seconds": 426410
                    }
                },
                {
                .
                .
                <snip>
            ],
            "pageInfo": {
                "currentPage": 1,
                "endCursor": "eyJjb2wiOiJcImlkXCIiLCJhc2MiOnRydWUsInZhbCI6IjMwMDAwMDE4OTI5In0=",
                "startCursor": "eyJjb2wiOiJcImlkXCIiLCJhc2MiOnRydWUsInZhbCI6IjMwMDAwMDAwMDE1In0=",
                "totalPages": 1,
                "totalRecords": 13
            }
        },
        "warnings": [
            "Module did not set no_log for password"
        ]
    }
}

PLAY RECAP *********************************************************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.graphiant.portal.plugins.module_utils.gcsdk_client import GcsdkClient
# TODO move light weight client to modules_utils instead of picking from test infra ?
# from ansible_collections.graphiant.portal.plugins.modules_utils.gcs_client import GcsClient

class GraphiantAPIRequests(object):
    ''' 
    Module GraphiantAPIRequests Class
        Login to Graphiant portal as Rest User.
        Send API Requests to portal.
    '''

    def __init__(self):
        # TODO use modules_utils util file methods to pre-process received arargument_spec if needed.
        # ansible_collections.graphiant.portal.plugins.modules_utils.<util file>
        self.argument_spec = {}
        self.argument_spec.update(dict(
            method=dict(required=False, type='str', default='GET'),
            uri=dict(required=True, type='str'),
            json=dict(required=False, type='dict'),
            base_url=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str')
        ))
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        parameters = self.module.params
        self.method = parameters['method']
        self.uri = str(parameters['uri'])
        self.json = parameters['json']

        self.gcs_client = GcsdkClient(parameters['base_url'], parameters['username'], parameters['password'])

def run_module():
    graphiant_api_request = GraphiantAPIRequests()
    if graphiant_api_request.method == 'GET':
        response = graphiant_api_request.gcs_client.get(graphiant_api_request.uri)
        if graphiant_api_request.module.check_mode:
             graphiant_api_request.module.exit_json(msg=response.json(), changed=False)
        if 200 <= response.status_code < 300:
             graphiant_api_request.module.exit_json(msg=response.json(), changed=True)
        else:
            graphiant_api_request.module.fail_json(msg=response.json(), changed=False)
    elif graphiant_api_request.method == 'PUT':
        response = graphiant_api_request.gcs_client.put(graphiant_api_request.uri, json=graphiant_api_request.json)
        if graphiant_api_request.module.check_mode:
             graphiant_api_request.module.exit_json(msg=response.json(), changed=False)
        if 200 <= response.status_code < 300:
             graphiant_api_request.module.exit_json(msg=response.json(), changed=True)
        else:
            graphiant_api_request.module.fail_json(msg=response.json(), changed=False)   


def main():
    run_module()


if __name__ == '__main__':
    main()

