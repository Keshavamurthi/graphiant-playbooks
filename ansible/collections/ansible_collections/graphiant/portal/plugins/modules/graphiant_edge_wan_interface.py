
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

class GraphiantEdgeWanInterface(object):

    def __init__(self):
        self.argument_spec = {}
        self.argument_spec.update(dict(
            json=dict(required=False, type='dict'),
            base_url=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            device_id=dict(required=True, type='str'),
            interface_data=dict(required=True, type='str'),
            action=dict(required=True, type='str')
        ))
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        parameters = self.module.params
        self.json = parameters['json']
        self.interface_data = self.module.params['interface_data']
        self.device_id = self.module.params['device_id']
        self.action = self.module.params['action']
        self.edge = Edge(parameters['base_url'], parameters['username'], parameters['password'])


def run_module():
    class_object = GraphiantEdgeWanInterface()
    if class_object.action.lower() in ["deconfig", "deconfigure", "delete"]:
        status = class_object.edge.delete_interface(**class_object.interface_data)
    else:
        status = class_object.edge.add_wan_interface(**class_object.interface_data)
    if status:
        class_object.module.exit_json(msg=f"Passed : {class_object.__class__.__name__} {class_object.action}", changed=True)
    else:
        class_object.module.exit_json(msg=f"Failed : {class_object.__class__.__name__} {class_object.action}", changed=False)

def main():
    run_module()


if __name__ == '__main__':
    main()

