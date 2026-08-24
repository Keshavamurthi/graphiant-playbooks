# get_enterprise_info

Resolve enterprise and parent enterprise details

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Facts set by this role:

- `enterprise_name`
- `parent_enterprise_name`
- `parent_enterprise_id`

## Dependencies

None.

## Example Playbook

```yaml
- name: Resolve enterprise and parent enterprise details
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Resolve enterprise and parent enterprise details
      ansible.builtin.include_role:
        name: get_enterprise_info
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
