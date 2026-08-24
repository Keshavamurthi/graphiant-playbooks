# get_bearer_token

Obtain a Graphiant portal bearer token and impersonate an enterprise

## Requirements

- Ansible 2.17 or later
- The `graphiant.naas` collection (module `graphiant.naas.graphiant_api`)

## Role Variables

Defaults (`defaults/main.yml`):

| Variable | Default | Description |
|---|---|---|
| `playbook_vars_dir` | `{{ playbook_dir }}/vars` | See `defaults/main.yml`. |

Required (the role fails fast if unset):

- `api_base_url`
- `api_password`
- `api_username`

Facts set by this role:

- `bearer_token`

## Dependencies

- `get_enterprise_info`

## Example Playbook

```yaml
- name: Obtain a Graphiant portal bearer token and impersonate an enterprise
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Obtain a Graphiant portal bearer token and impersonate an enterprise
      ansible.builtin.include_role:
        name: get_bearer_token
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
