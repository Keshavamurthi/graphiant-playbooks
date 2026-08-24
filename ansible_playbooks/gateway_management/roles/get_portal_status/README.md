# get_portal_status

Wait for a device to report Ready portal status

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Required (the role fails fast if unset):

- `api_base_url`
- `bearer_token`
- `device_id`

Facts set by this role:

- `device_portal_status`
- `device_status`

## Dependencies

None.

## Example Playbook

```yaml
- name: Wait for a device to report Ready portal status
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Wait for a device to report Ready portal status
      ansible.builtin.include_role:
        name: get_portal_status
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
