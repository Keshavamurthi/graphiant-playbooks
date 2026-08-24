# Gateway VM Automation Playbooks

Ansible playbooks for the lifecycle of Graphiant gateway VMs on libvirt hypervisors:
provisioning, configuration through the Graphiant portal, health verification and teardown.

These playbooks are **operational automation** — they drive a procedural workflow against
real hypervisors. For declarative Graphiant network configuration (interfaces, BGP, sites,
policies), use the `graphiant.naas` collection's own playbooks under
`ansible_collections/graphiant/naas/playbooks/`.

## Layout

```
ansible_playbooks/gateway_management/
├── NN_<playbook>.yml  9 top-level playbooks, numbered in run order
├── roles/             19 roles, each with tasks/, meta/, README.md
├── vars/              gateway_vm_vars.yml (defaults); runtime_vars*.yml generated at run time
├── configs/           per-environment gateway VM configs: <env>/<site>-hypervisor.yml
├── inventory/         inventory, plus per-site and per-hypervisor variables
│   ├── inventory.yaml
│   ├── group_vars/    SKU table and fleet/site defaults
│   └── host_vars/     per-hypervisor overrides
└── requirements.yml   collection dependencies
```

`configs/` and `inventory/` hold environment-specific data and are **not** committed — see
the note at the end of this file.

## Setup

To manually test,

Create the virtual environment and install the `graphiant.naas` dependencies as
described under [Ansible Collection (Recommended)](../../README.md#ansible-collection-recommended)
in the repository README, then install the collections these playbooks need:

```bash
ansible-galaxy collection install -r requirements.yml
```

Python dependencies are installed on each hypervisor into `/venv` by the
`install_dependencies` role, which every playbook runs as a pre-task when needed.

## Credentials

Supply portal credentials as extra vars or through your vault — never commit them:

| Variable | Purpose |
|---|---|
| `api_base_url` | Portal API URL, e.g. `https://api.graphiant.com` |
| `api_username` / `api_password` | Portal login |
| `ansible_enterprise_id` | Enterprise to impersonate |
| `gcs_env` | Environment name; selects `configs/<gcs_env>/` |
| `gateway_hypervisor_ssh_password` | Hypervisor SSH password (referenced by the inventories) |

## Playbooks

| Playbook | Purpose |
|---|---|
| `00_hypervisor_resource_availability.yml` | Report free gateway VM slots on a hypervisor (read-only) |
| `01_install_dependencies.yml` | Install hypervisor packages and the `/venv` virtualenv |
| `02_download_gnos_image.yml` | Resolve and download the GNOS qcow2 image |
| `03_deploy_gateway_vm.yml` | Provision a gateway VM and onboard it to the portal |
| `04_configure_gateway_vm.yml` | Push interface and circuit configuration to the device |
| `05_verify_gateway_status.yml` | Verify portal status and data/control/system plane health |
| `06_delete_gateway_vm.yml` | Decommission a VM in the portal and destroy it on the hypervisor |
| `07_cleanup_vm_in_hypervisor.yml` | Destroy hypervisor-side resources only |
| `08_restart_gateway_vm.yml` | Restart a gateway VM |

Typical order for a new gateway:

```bash
ENV=production
INV=inventory/inventory.yaml
ANSIBLE_USER=<> # Gateway Hypervisor Username
ANSIBLE_SSH_PASS=<> # Gateway Hypervisor Password

Note: Preview any playbook first with `--check --diff`.

ansible-playbook -i $INV 00_hypervisor_resource_availability.yml -e gcs_env=$ENV -e ansible_user=$ANSIBLE_USER -e ansible_ssh_pass=$ANSIBLE_SSH_PASS
ansible-playbook -i $INV 03_deploy_gateway_vm.yml -e gcs_env=$ENV -e ansible_user=$ANSIBLE_USER -e ansible_ssh_pass=$ANSIBLE_SSH_PASS
ansible-playbook -i $INV 04_configure_gateway_vm.yml -e gcs_env=$ENV -e ansible_user=$ANSIBLE_USER -e ansible_ssh_pass=$ANSIBLE_SSH_PASS
ansible-playbook -i $INV 05_verify_gateway_status.yml -e gcs_env=$ENV -e ansible_user=$ANSIBLE_USER -e ansible_ssh_pass=$ANSIBLE_SSH_PASS
```

## How the roles fit together

The roles are a pipeline: each publishes facts that later roles and the calling play
consume (`bearer_token` → `max_vm_count` → `vm_index` → `device_hostname` →
`final_config_payload`). They are included with `ansible.builtin.include_role` so `when:`
guards and per-call `vars:` work, and most begin by asserting their required variables so
they can be run individually. Each role's `README.md` lists what it requires and what facts
it sets.

Two steps read from `configs/` rather than from a constant:

- `get_max_vm_count` publishes `max_vm_count` from the hypervisor's `vms:` block, which
  bounds the slot search in `get_next_available_vm_index`.
- `get_software_version_info` resolves `software_download_url` from the portal when
  `gnos_mode` is `production`, and from the GitLab package registry otherwise. The
  production URL is issued per request, so a saved value should be used promptly.

Portal calls go through `graphiant.naas.graphiant_api`, which invokes one portal API method
per task.

## Per-hypervisor configuration

VM sizing and host NIC names are per-hypervisor, resolved through Ansible's inventory
precedence: fleet defaults in `group_vars/gateway_hypervisors.yml`, site overrides in
`group_vars/<site>.yml`, per-box overrides in `host_vars/<hostname>.yml`.

### VM SKUs

Sizes are named profiles, defined once in `inventory/group_vars/gateway_hypervisors.yml`:

```yaml
gateway_vm_skus:
  standard:
    vcpus: 4
    memory: 4096
    cpu_pin_start: 16
  large:
    vcpus: 8
    memory: 8192
    cpu_pin_start: 32

gateway_vm_sku: standard      # fleet default
```

A hypervisor picks one by name in its `host_vars` file:

```yaml
# inventory/host_vars/sanjose-hypervisor-1.yml
gateway_vm_sku: large
```

To add a size, add an entry to `gateway_vm_skus`. Keep `cpu_pin_start` an unquoted int —
`03_deploy_gateway_vm.yml` does arithmetic on it to build the CPU pin set.

### Host NIC names

`towards_packetfabric`, `towards_core0` and `towards_core1` are the hypervisor's physical
NIC names. They build the SR-IOV lookup keys (`<nic>v<vm_index>`) that index
`sr_iov_mappings`, which is read off the host at deploy time. A box whose NICs are named
differently must override them, or `virt-install` fails on an unknown key:

```yaml
# inventory/host_vars/sanjose-hypervisor-1.yml
towards_packetfabric: "ens1f0"
towards_core0: "ens1f2"
towards_core1: "ens1f3"
```

### Checking what a host resolves to

```bash
ansible -i inventory/inventory.yaml gateway_hypervisors --connection=local \
  -m debug -a "msg='{{ gateway_vm_sku }} {{ gateway_vm_skus[gateway_vm_sku] }} {{ towards_packetfabric }}'"
```

> **Do not define these in `vars/gateway_vm_vars.yml`.** A play's `vars_files` outranks
> inventory host and group vars, so a value there silently overrides every per-hypervisor
> setting. That file carries only genuinely fleet-wide values.

## Configuration data

`configs/<env>/<site>-hypervisor.yml` maps each hypervisor to its region, static routes
and per-VM interface addressing. The file name is the first two dash-separated fields of
the hypervisor's inventory hostname — `sanjose-hypervisor-1` resolves to
`sanjose-hypervisor.yml` — which is how `read_vms_yml_file` locates it. One file can hold
several hypervisors:

```yaml
---
<hypervisor-hostname>:                        # e.g. sanjose-hypervisor-1
  RegionName: "us_west_2"
  static_routes:
    - destination_prefix: 0.0.0.0/0
      next_hop: 192.0.2.1
      description: dia_default_route
  vms:
    gw-1-vm:                                  # libvirt domain name: gw-<index>-vm
      hostname: sanjose-hypervisor-1-vm-1     # device hostname as registered in the portal
      GigabitEthernet3_0_0: 192.0.2.10/27
      VirtualFunctionEthernet6_0_0: 198.51.100.10/24
      VirtualFunctionEthernet7_0_0: 198.51.100.110/24
```

Each key is the VM's libvirt domain name, `gw-<index>-vm` — the same name
`get_next_available_vm_index` scans the hypervisor for and that `vm_name` is built from,
so the config states outright what the VM will be called. Those keys are the slots the
index search allocates from, and the number of entries becomes `max_vm_count` via
`get_max_vm_count`, so a hypervisor's capacity is declared here rather than hardcoded.

`hostname` is the portal-side device name and is free-form: the roles look a device up by
this value and never rebuild it from the key, so keep it unique across the file.

`inventory/whitelisted_data.yml` lists the enterprise IDs each environment may target.

> **Note:** `configs/` and `inventory/` are excluded by `.gitignore`. They describe real
> deployments — hypervisor addresses, gateway addresses, site hostnames and enterprise IDs
> — and this is a public repository. Keep them in your own private configuration
> management and copy them in at run time. The snippet above shows the expected schema
> using documentation-range addresses.
