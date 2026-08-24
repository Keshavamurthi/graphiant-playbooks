# get_device_troubleshooting_status

Verify device data, control and system plane health

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Required (the role fails fast if unset):

- `api_base_url`
- `bearer_token`
- `device_id`

Facts set by this role:

- `dataplane_status`
- `controlplane_status`
- `systemplane_status`

## Dependencies

None.

## Example Playbook

```yaml
- name: Verify device data, control and system plane health
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Verify device data, control and system plane health
      ansible.builtin.include_role:
        name: get_device_troubleshooting_status
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
