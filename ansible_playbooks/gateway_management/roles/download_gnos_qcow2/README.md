# download_gnos_qcow2

Download the GNOS qcow2 image to the hypervisor

## Requirements

- Ansible 2.17 or later
- No collections beyond `ansible.builtin`

## Role Variables

Required (the role fails fast if unset):

- `gitlab_api_key`
- `software_download_url`
- `software_version`

Facts set by this role:

- `gnos_qcow2_path`

## Dependencies

None.

## Example Playbook

```yaml
- name: Download the GNOS qcow2 image to the hypervisor
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Download the GNOS qcow2 image to the hypervisor
      ansible.builtin.include_role:
        name: download_gnos_qcow2
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
