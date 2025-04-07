
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''

'''

EXAMPLES = r'''

'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.graphiant.portal.plugins.module_utils.edge_utils import Edge
from ansible_collections.graphiant.portal.plugins.module_utils.core_utils import Core

class GraphiantInterfaces(object):

    def __init__(self):
        self.argument_spec = {}
        self.argument_spec.update(dict(
            input_config_yaml=dict(required=False, type='str'),
            portal_url=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            action=dict(required=True, type='str'),
            device_type=dict(required=True, type='str')
        ))
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        parameters = self.module.params
        self.input_config_yaml = parameters['input_config_yaml']
        self.action = parameters['action']
        self.portal_url = parameters.get('portal_url', None)
        self.portal_username = parameters.get('username', None)
        self.portal_password = parameters.get('password', None)
        match parameters['device_type']:
            case "edge":
                self.device = Edge(self.portal_url, self.portal_username, self.portal_password)


def run_module():
    class_object = GraphiantInterfaces()
    if class_object.action.lower() in ["deconfig", "deconfigure", "delete"]:
        status = class_object.device.delete_multiple_interfaces_from_yaml(yaml_file=class_object.input_config_yaml)
    else:
        status = class_object.device.add_multiple_interfaces_from_yaml(yaml_file=class_object.input_config_yaml)
    if status:
        class_object.module.exit_json(msg=f"Passed : {class_object.__class__.__name__} {class_object.action}", changed=True)
    else:
        class_object.module.exit_json(msg=f"Failed : {class_object.__class__.__name__} {class_object.action}", changed=False)

def main():
    run_module()


if __name__ == '__main__':
    main()

