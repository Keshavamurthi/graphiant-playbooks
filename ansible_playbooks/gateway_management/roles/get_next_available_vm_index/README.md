# get_next_available_vm_index

Find the next free gateway VM index on a hypervisor

## Requirements

- Ansible 2.17 or later
- The `community.libvirt` collection (module `community.libvirt.virt`)

## Role Variables

Optional inputs:

- `max_vm_count` — highest gateway VM index to consider. Defaults to `10`; set it
  from config with the `get_max_vm_count` role.

Facts set by this role:

- `deployed_vm_indices`
- `vm_count`
- `next_available_vm_index`
- `vm_index`

## Dependencies

None. Pair with `get_max_vm_count` to take the capacity from config instead of the
default.

## Example Playbook

```yaml
- name: Find the next free gateway VM index on a hypervisor
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Find the next free gateway VM index on a hypervisor
      ansible.builtin.include_role:
        name: get_next_available_vm_index
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
