# install_dependencies

Install the hypervisor packages and Python virtualenv the gateway automation needs.

The role detects the target's OS family and installs the matching package list. Hosts whose
family has no package list fail immediately with a message naming the files to add, rather
than attempting a package manager that will not work.

## Requirements

- Ansible 2.17 or later
- Privilege escalation (`become: true`) on the target
- A supported OS family (see below)
- `/usr/bin/python3` present on the target — used to bootstrap before `/venv` exists

## Supported operating systems

| OS family | Package list | Status |
|---|---|---|
| `Debian` (Debian, Ubuntu) | `vars/Debian.yml` | Supported |

To add another family:

1. Create `vars/<os_family>.yml` defining `install_dependencies_packages`.
2. Add `<os_family>` to `install_dependencies_supported_os_families` in `vars/main.yml`.
3. If its package manager needs a cache refresh, add a task guarded on that family
   alongside the existing `Update the apt cache` step.

Use the family name exactly as Ansible reports it in `ansible_facts.os_family`
(`RedHat`, `Suse`, `Archlinux`, ...) — the file name is looked up from that fact.

## Role Variables

Defined in `vars/`, so they are not intended to be overridden per play:

| Variable | Where | Description |
|---|---|---|
| `install_dependencies_supported_os_families` | `vars/main.yml` | Families with a package list |
| `install_dependencies_packages` | `vars/<os_family>.yml` | Packages for the detected family |

Python packages for the virtualenv are pinned in `files/requirements.txt`, matching
`ansible_collections/graphiant/naas/_version.py`.

## Facts set by this role

- `ansible_python_interpreter` — `/usr/bin/python3` while bootstrapping, then `/venv/bin/python`
- `dependencies_installed` — `true`, so callers can guard with
  `when: dependencies_installed is not defined`

## Interpreter bootstrap

The inventories set `ansible_python_interpreter: /venv/bin/python`, but creating `/venv` is
this role's job — on a fresh host that interpreter does not exist. The first task therefore
switches to the system Python. It is a `set_fact`, which runs on the controller and needs no
remote interpreter, so it works even when the pinned one is missing. Fact gathering and
every package task then run under `/usr/bin/python3`. No extra-var override is needed.

## Example Playbook

```yaml
- name: Install dependencies
  hosts: gateway_hypervisors
  become: true
  gather_facts: false

  tasks:
    - name: Install required packages
      when: dependencies_installed is not defined
      ansible.builtin.include_role:
        name: install_dependencies
```

The role gathers the distribution facts it needs itself, so callers may leave
`gather_facts: false`.

## Note on idempotence

The pip step runs with `--upgrade --force-reinstall`, so Python packages are reinstalled on
every run and the task always reports `changed`. Package installs and the venv creation are
idempotent.

## License

GPL-3.0-or-later

## Author Information

Graphiant (https://www.graphiant.com)
