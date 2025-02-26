
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

class GraphiantDeviceLifecycleState(object):

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
        self.device_id = self.module.params['device_id']
        self.action = self.module.params['action']
        self.device = PortalUtils(parameters['base_url'], parameters['username'], parameters['password'])


def run_module():
    class_object = GraphiantDeviceLifecycleState()
    status = class_object.device.update_device_bringup_status(device_id=class_object.device_id, status=class_object.action)
    if status:
        class_object.module.exit_json(msg=f"Passed : {class_object.__class__.__name__} {class_object.action}", changed=True)
    else:
        class_object.module.exit_json(msg=f"Failed : {class_object.__class__.__name__} {class_object.action}", changed=False)

def main():
    run_module()


if __name__ == '__main__':
    main()

