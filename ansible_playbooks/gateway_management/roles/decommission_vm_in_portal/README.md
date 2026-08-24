# decommission_vm_in_portal

Deactivate and decommission a gateway VM in the Graphiant portal

## Requirements

- Ansible 2.17 or later
- No collections beyond `ansible.builtin`

## Role Variables

This role takes no variables.

## Dependencies

- `update_device_bringup_status`

## Example Playbook

```yaml
- name: Deactivate and decommission a gateway VM in the Graphiant portal
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Deactivate and decommission a gateway VM in the Graphiant portal
      ansible.builtin.include_role:
        name: decommission_vm_in_portal
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
