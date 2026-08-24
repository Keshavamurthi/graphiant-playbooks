# get_device_id_from_device_name

Look up a portal device ID by device hostname

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Required (the role fails fast if unset):

- `api_base_url`
- `bearer_token`

Facts set by this role:

- `device_id`

## Dependencies

None.

## Example Playbook

```yaml
- name: Look up a portal device ID by device hostname
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Look up a portal device ID by device hostname
      ansible.builtin.include_role:
        name: get_device_id_from_device_name
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
