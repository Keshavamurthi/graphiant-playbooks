
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''

'''

EXAMPLES = r'''

'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.graphiant.portal.plugins.module_utils.portal_utils import PortalUtils
import csv

class ReadInputCsv(object):

    def __init__(self):
        self.argument_spec = {}
        self.argument_spec.update(dict(
            json=dict(required=False, type='dict'),
            base_url=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            input_csv_file=dict(required=True, type='str')
        ))
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        parameters = self.module.params
        self.json = parameters['json']
        self.input_csv_file = self.module.params['input_csv_file']
        self.portal_utils = PortalUtils(parameters['base_url'], parameters['username'], parameters['password'])
    
    def get_wan_interface_config(self):
        templates_path = "ansible_collections/graphiant/portal/playbooks/templates/"
        input_csv_file = templates_path + self.input_csv_file
        interface_data_dict = {}
        try:        
            with open(input_csv_file, "r") as file:
                input_data = csv.DictReader(file)
                for each_row in input_data:
                    interface_data_dict[each_row['id']] = each_row
                return interface_data_dict
        except FileNotFoundError as e:
            assert False, f"Exception while reading {self.input_csv_file} : {e}"

def run_module():
    read_input_csv = ReadInputCsv()
    interface_config = read_input_csv.get_wan_interface_config()
    if interface_config:
        pass
        # Need to return the interface config to the playbook
        # graphiant_wan_interface.module.exit_json(msg=[status, uri, device_interface_config, response.json()], changed=False)


def main():
    run_module()


if __name__ == '__main__':
    main()

