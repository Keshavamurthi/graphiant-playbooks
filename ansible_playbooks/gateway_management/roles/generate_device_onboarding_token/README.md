# generate_device_onboarding_token

Create a device onboarding token in the Graphiant portal

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Required (the role fails fast if unset):

- `api_base_url`
- `bearer_token`
- `device_type`

Facts set by this role:

- `onboarding_token`

## Dependencies

None.

## Example Playbook

```yaml
- name: Create a device onboarding token in the Graphiant portal
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Create a device onboarding token in the Graphiant portal
      ansible.builtin.include_role:
        name: generate_device_onboarding_token
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
