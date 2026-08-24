# read_vms_yml_file

Load the per-site gateway VM config file

## Requirements

- Ansible 2.17 or later
- No collections beyond `ansible.builtin`

## Role Variables

Defaults (`defaults/main.yml`):

| Variable | Default | Description |
|---|---|---|
| `gateway_configs_dir` | `{{ playbook_dir }}/configs` | See `defaults/main.yml`. |

Required (the role fails fast if unset):

- `device_hostname`

Facts set by this role:

- `vms_file_name`
- `vms_dict`

## Dependencies

None.

## Example Playbook

```yaml
- name: Load the per-site gateway VM config file
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Load the per-site gateway VM config file
      ansible.builtin.include_role:
        name: read_vms_yml_file
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
