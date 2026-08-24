# update_audit_log

Append a gateway VM entry to the hypervisor audit log

## Requirements

- Ansible 2.17 or later
- No collections beyond `ansible.builtin`

## Role Variables

This role takes no variables.

## Dependencies

- `get_device_id_from_device_name`

## Example Playbook

```yaml
- name: Append a gateway VM entry to the hypervisor audit log
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Append a gateway VM entry to the hypervisor audit log
      ansible.builtin.include_role:
        name: update_audit_log
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
