# get_device_hostname_from_device_id

Look up a device hostname by portal device ID

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Required (the role fails fast if unset):

- `api_base_url`
- `bearer_token`
- `device_id`

Facts set by this role:

- `device_not_found`
- `device_hostname`

## Dependencies

None.

## Example Playbook

```yaml
- name: Look up a device hostname by portal device ID
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Look up a device hostname by portal device ID
      ansible.builtin.include_role:
        name: get_device_hostname_from_device_id
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
