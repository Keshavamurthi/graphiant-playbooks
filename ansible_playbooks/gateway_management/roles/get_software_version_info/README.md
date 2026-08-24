# get_software_version_info

Resolve the GNOS software version and download URL

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
- `bearer_token`
- `gnos_mode`

Facts set by this role:

- `software_version`
- `software_release`
- `software_download_url` — resolved from the portal
  (`get_software_download_url`) when `gnos_mode` is `production`, and built from
  the GitLab package registry path otherwise. The production URL is issued by the
  portal per request, so re-use a saved value promptly.

## Dependencies

None.

## Example Playbook

```yaml
- name: Resolve the GNOS software version and download URL
  hosts: gateway_hypervisors
  gather_facts: false
  vars_files:
    - vars/gateway_vm_vars.yml
  tasks:
    - name: Resolve the GNOS software version and download URL
      ansible.builtin.include_role:
        name: get_software_version_info
```

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
