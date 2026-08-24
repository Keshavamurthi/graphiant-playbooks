# compute_interface_config_payload

Build the interface and circuit payload for a gateway VM

## Requirements

- Ansible 2.17 or later
- No collections beyond `ansible.builtin`

## Role Variables

Required (the role fails fast if unset):

- `device_hostname`
- `vm_index`

Facts set by this role:

- `hypervisor_hostname`
- `region_name`
- `interface_configs`
- `static_routes`
- `GigabitEthernet3_0_0`
- `VirtualFunctionEthernet6_0_0`
- `VirtualFunctionEthernet7_0_0`
- `pf_sub_interfaces`
- `interfaces`
- `rendered_template`
- `circuit_payload`
- `interface_payload`
- `final_config_payload`

## Dependencies

- `read_vms_yml_file`

## Example Playbook

```yaml
- name: Build the interface and circuit payload for a gateway VM
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Build the interface and circuit payload for a gateway VM
      ansible.builtin.include_role:
        name: compute_interface_config_payload
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
