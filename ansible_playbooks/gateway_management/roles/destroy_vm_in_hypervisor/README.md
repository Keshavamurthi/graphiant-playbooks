# destroy_vm_in_hypervisor

Destroy and undefine a gateway VM and its storage pools

## Requirements

- Ansible 2.17 or later
- The `community.libvirt` collection (module `community.libvirt.virt`)

## Role Variables

Required (the role fails fast if unset):

- `vm_name`

## Dependencies

None.

## Example Playbook

```yaml
- name: Destroy and undefine a gateway VM and its storage pools
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Destroy and undefine a gateway VM and its storage pools
      ansible.builtin.include_role:
        name: destroy_vm_in_hypervisor
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
