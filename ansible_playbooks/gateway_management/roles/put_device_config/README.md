# put_device_config

Apply device configuration through the Graphiant portal

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Required (the role fails fast if unset):

- `api_base_url`
- `bearer_token`
- `device_id`

## Dependencies

- `get_portal_status`

## Example Playbook

```yaml
- name: Apply device configuration through the Graphiant portal
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Apply device configuration through the Graphiant portal
      ansible.builtin.include_role:
        name: put_device_config
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
