# update_device_bringup_status

Set the bringup status of a device in the portal

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Required (the role fails fast if unset):

- `api_base_url`
- `bearer_token`
- `device_id`

## Dependencies

None.

## Example Playbook

```yaml
- name: Set the bringup status of a device in the portal
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Set the bringup status of a device in the portal
      ansible.builtin.include_role:
        name: update_device_bringup_status
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
