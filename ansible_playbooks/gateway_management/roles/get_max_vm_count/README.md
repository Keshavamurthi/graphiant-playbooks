# get_max_vm_count

Resolve the configured gateway VM capacity for a hypervisor

## Requirements

- Ansible 2.17 or later

## Role Variables

Required (supplied by the calling play or inventory):

- `gcs_env`

Facts set by this role:

- `max_vm_count` — number of VM entries declared under
  `<inventory_hostname>.vms` in `configs/<gcs_env>/<site>-hypervisor.yml`

Also sets `vms_dict` and `vms_file_name` via `read_vms_yml_file`, which it includes
only when `vms_dict` is not already defined.

## Dependencies

- `read_vms_yml_file`

## Example Playbook

```yaml
- name: Resolve the configured gateway VM capacity for a hypervisor
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Resolve the configured gateway VM capacity for a hypervisor
      ansible.builtin.include_role:
        name: get_max_vm_count
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
