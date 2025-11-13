# Graphiant Playbooks Ansible Collection

This Ansible collection provides modules for automating Graphiant NaaS (Network as a Service) configurations. It allows you to manage network infrastructure, interfaces, circuits, BGP peering, global configurations, and Data Exchange workflows through Ansible playbooks.

## Prerequisites

- Ansible >= 2.15
- Python >= 3.12
- Graphiant SDK >= 25.11.1
- Access to Graphiant NaaS platform

## Installation

### From Source (Recommended Method)

#### Method 1: Direct Directory Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/graphiant/graphiant-playbooks.git
cd graphiant-playbooks

# Set PYTHONPATH to include the project directory
export PYTHONPATH=$(pwd):$PYTHONPATH

# Install the collection directly from source directory
ansible-galaxy collection install ansible_collections/graphiant/graphiant_playbooks/ --force
```

#### Method 2: Build and Install from Archive
```bash
# Clone the repository
git clone https://github.com/graphiant/graphiant-playbooks.git
cd graphiant-playbooks

# Build the collection
python ansible_collections/graphiant/graphiant_playbooks/build_collection.py

# Install from built archive
ansible-galaxy collection install build/graphiant-graphiant_playbooks-1.0.0.tar.gz --force
```

### Verification
After installation, verify the collection is properly installed:

```bash
# Check installed collections
ansible-galaxy collection list | grep graphiant

# Expected output:
# graphiant.graphiant_playbooks            1.0.0
```

### Understanding Collection Paths
To understand where Ansible looks for collections:

```bash
# Check Ansible collection search paths
ansible-config dump | grep COLLECTIONS_PATHS

# Typical output:
# COLLECTIONS_PATHS(default) = ['/Users/username/.ansible/collections', '/usr/share/ansible/collections']
```

**Collection Search Order:**
1. **User collections**: `~/.ansible/collections/` (highest priority)
2. **System collections**: `/usr/share/ansible/collections/` (fallback)
3. **Custom paths**: Any additional paths configured in `ansible.cfg`

**Path Resolution Priority (for config files):**
1. **GRAPHIANT_PLAYBOOKS_PATH**: User-configured environment variable (highest priority)
2. **PYTHONPATH**: Check paths in PYTHONPATH for graphiant-playbooks directory
3. **Current working directory**: Check if running from project root
4. **Git repository root**: Find .git directory and look for configs/libs there
5. **File location walk-up**: Walk up from current file location (fallback)

### Testing the Installation
Test the collection with a simple playbook:

```bash
# Set PYTHONPATH (required for library access)
export PYTHONPATH=$(pwd):$PYTHONPATH

# Optional: Enable debug output callback for better log formatting
# This makes detailed_logs output more readable (removes \n characters)
export ANSIBLE_STDOUT_CALLBACK=debug

# Set Graphiant portal client parameters
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="username"
export GRAPHIANT_PASSWORD="password"

# Optional: Set custom path to graphiant-playbooks directory
# This is useful when running from different working directories
export GRAPHIANT_PLAYBOOKS_PATH="/path/to/your/graphiant-playbooks"

# Run a test playbook in check mode
ansible-playbook --check ansible_collections/graphiant/graphiant_playbooks/playbooks/final_test.yml
```

**Note:** Setting `ANSIBLE_STDOUT_CALLBACK=debug` is recommended when using `detailed_logs: true` as it formats multi-line log output properly, making it easier to read detailed operation logs.

## Uninstallation

To remove the Graphiant Ansible collection from your system:

### Method 1: Manual Removal (Recommended)
```bash
# Remove the collection directory
rm -rf ~/.ansible/collections/ansible_collections/graphiant/graphiant_playbooks

# Verify removal
ansible-galaxy collection list | grep graphiant
```

### Method 2: Using Ansible Galaxy (if supported)
```bash
# Note: This method may not be available in all Ansible versions
ansible-galaxy collection remove graphiant.graphiant_playbooks
```

### Verification
After uninstallation, verify the collection has been removed:

```bash
# Check installed collections
ansible-galaxy collection list | grep graphiant

# Expected output: Only other graphiant collections (if any) should remain
# graphiant.portal                         1.0.0  (if installed)
```

### Clean Up (Optional)
If you want to completely remove all Graphiant collections:

```bash
# Remove the entire graphiant namespace
rm -rf ~/.ansible/collections/ansible_collections/graphiant/

# Verify complete removal
ansible-galaxy collection list | grep graphiant
# Expected output: (empty)
```

## Parameter Behavior

All modules support flexible parameter usage with `operation` and `state` parameters:

### **Parameter Rules**
- **`operation` parameter**: Optional - specifies the exact operation to perform
- **`state` parameter**: Optional - provides a fallback when operation is not specified
- **Validation**: At least one of `operation` or `state` must be provided
- **Precedence**: If both are provided, `operation` takes precedence over `state`

### **State-to-Operation Mapping**

When `operation` is not specified, `state` determines the operation:

- **`state: present`** → Maps to:
  - `configure` (global_config, bgp, sites)
  - `configure_interfaces` (interfaces)

- **`state: absent`** → Maps to:
  - `deconfigure` (global_config, bgp, sites)
  - `deconfigure_interfaces` (interfaces)

### **Usage Examples**

```yaml
# Using operation parameter (explicit)
- name: Configure interfaces
  graphiant.graphiant_playbooks.graphiant_interfaces:
    operation: "configure_interfaces"
    state: present

# Using state parameter only (fallback)
- name: Configure interfaces
  graphiant.graphiant_playbooks.graphiant_interfaces:
    state: present  # operation will be "configure_interfaces"

# Using both (operation takes precedence)
- name: Configure specific interfaces
  graphiant.graphiant_playbooks.graphiant_interfaces:
    operation: "configure_lan_interfaces"  # This takes precedence
    state: absent  # This is ignored

# Error handling
- name: Invalid task (will fail)
  graphiant.graphiant_playbooks.graphiant_interfaces:
    # No operation or state specified - will show supported operations
```

## Manager Template Usage

The Graphiant Playbooks collection includes different managers that use different approaches for configuration payload generation:

| Manager | Operations | Template Usage | Notes |
|---------|------------|----------------|--------|
| **InterfaceManager** | `configure_interfaces`, `configure_lan_interfaces`, `configure_wan_circuits_interfaces`, `configure_circuits` | ✅ **Uses Templates** | Uses Jinja2 templates for interface and circuit configurations |
| **BGPManager** | `configure`, `detach_policies`, `deconfigure` | ✅ **Uses Templates** | Uses Jinja2 templates for BGP peering configurations |
| **GlobalConfigManager** | `configure`, `deconfigure`, `configure_*`, `deconfigure_*` | ✅ **Uses Templates** | Uses Jinja2 templates for global object configurations |
| **SiteManager** | `configure`, `deconfigure`, `configure_sites`, `attach_objects` | ✅ **Uses Templates** | Uses Jinja2 templates for site and attachment configurations |
| **DataExchangeManager** | `create_services`, `create_customers`, `match_service_to_customers`, `delete_services`, `delete_customers`, `accept_invitation` | ❌ **Direct API Calls** | Uses direct API calls without template rendering |

### Template-Based Managers
- **InterfaceManager**: Uses `interface_template.yaml` and `circuit_template.yaml`
- **BGPManager**: Uses `bgp_peering_template.yaml`
- **GlobalConfigManager**: Uses various global templates (`global_*_template.yaml`)
- **SiteManager**: Uses site and attachment templates

### Direct API Managers
- **DataExchangeManager**: Processes YAML configuration directly and makes API calls without template rendering

**Note**: The Data Exchange manager was designed to work directly with the existing YAML configuration structure, avoiding the complexity of template rendering for Data Exchange operations.

## Modules

### graphiant_interfaces

Manages Graphiant interfaces and circuits.

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `interface_config_file` (required): Path to interface configuration YAML file
- `circuit_config_file` (optional): Path to circuit configuration YAML file
- `operation` (optional): Operation to perform (at least one of operation or state required)
  - `configure_interfaces`: Configure all interfaces
  - `deconfigure_interfaces`: Deconfigure all interfaces
  - `configure_lan_interfaces`: Configure LAN interfaces only
  - `deconfigure_lan_interfaces`: Deconfigure LAN interfaces only
  - `configure_wan_circuits_interfaces`: Configure WAN circuits and interfaces
  - `deconfigure_wan_circuits_interfaces`: Deconfigure WAN circuits and interfaces
  - `configure_circuits`: Configure circuits only
  - `deconfigure_circuits`: Deconfigure circuits only
- `circuits_only` (optional): If true, only circuits are affected (default: false)
- `state` (optional): Desired state (present/absent, default: present)
  - `present`: Maps to `configure_interfaces` when operation not specified
  - `absent`: Maps to `deconfigure_interfaces` when operation not specified
- `detailed_logs` (optional): Enable detailed logging output from library operations (default: false)
  - `true`: Show detailed library logs in the task output
  - `false`: Show only basic success/error messages

**Example:**
```yaml
- name: Configure all interfaces
  graphiant.graphiant_playbooks.graphiant_interfaces:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    interface_config_file: "sample_interface_config.yaml"
    circuit_config_file: "sample_circuit_config.yaml"
    operation: "configure_interfaces"
    state: present

- name: Configure LAN interfaces with detailed logging
  graphiant.graphiant_playbooks.graphiant_interfaces:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    interface_config_file: "sample_interface_config.yaml"
    operation: "configure_lan_interfaces"
    detailed_logs: true
    state: present
```

### graphiant_bgp

Manages Graphiant BGP peering and routing policies.

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `bgp_config_file` (required): Path to BGP configuration YAML file
- `operation` (optional): Operation to perform (at least one of operation or state required)
  - `configure`: Configure BGP peering and attach policies
  - `deconfigure`: Deconfigure BGP peering
  - `detach_policies`: Detach policies from BGP peers
- `state` (optional): Desired state (present/absent, default: present)
  - `present`: Maps to `configure` when operation not specified
  - `absent`: Maps to `deconfigure` when operation not specified
- `detailed_logs` (optional): Enable detailed logging output from library operations (default: false)
  - `true`: Show detailed library logs in the task output
  - `false`: Show only basic success/error messages

**Example:**
```yaml
- name: Configure BGP peering
  graphiant.graphiant_playbooks.graphiant_bgp:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    bgp_config_file: "sample_bgp_peering.yaml"
    operation: "configure"
    state: present

- name: Configure BGP peering with detailed logging
  graphiant.graphiant_playbooks.graphiant_bgp:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    bgp_config_file: "sample_bgp_peering.yaml"
    operation: "configure"
    detailed_logs: true
    state: present
```

### graphiant_global_config

Manages Graphiant global configuration objects.

**Note:** Global configurations can be managed using either:
- **General operations**: `configure` and `deconfigure` - automatically detects and processes all configuration types in the YAML file
- **Specific operations**: `configure_*` and `deconfigure_*` - processes only the specific configuration type

**Detailed Logging:**
The `detailed_logs` parameter enables comprehensive logging output from the underlying Graphiant library operations. When enabled, you'll see:
- API call details and responses
- Configuration processing steps
- Success/failure messages for each operation
- Debugging information for troubleshooting

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `config_file` (required): Path to global configuration YAML file
- `operation` (optional): Operation to perform (at least one of operation or state required)
  - `configure`: Configure all global objects
  - `deconfigure`: Deconfigure all global objects
  - `configure_lan_segments`: Configure LAN segments only
  - `deconfigure_lan_segments`: Deconfigure LAN segments only
  - `configure_prefix_sets`: Configure prefix sets only
  - `deconfigure_prefix_sets`: Deconfigure prefix sets only
  - `configure_bgp_filters`: Configure BGP filters only
  - `deconfigure_bgp_filters`: Deconfigure BGP filters only
  - `configure_snmp_services`: Configure SNMP services only
  - `deconfigure_snmp_services`: Deconfigure SNMP services only
  - `configure_syslog_services`: Configure syslog services only
  - `deconfigure_syslog_services`: Deconfigure syslog services only
  - `configure_ipfix_services`: Configure IPFIX services only
  - `deconfigure_ipfix_services`: Deconfigure IPFIX services only
  - `configure_vpn_profiles`: Configure VPN profiles only
  - `deconfigure_vpn_profiles`: Deconfigure VPN profiles only
- `state` (optional): Desired state (present/absent, default: present)
  - `present`: Maps to `configure` when operation not specified
  - `absent`: Maps to `deconfigure` when operation not specified
- `detailed_logs` (optional): Enable detailed logging output from library operations (default: false)
  - `true`: Show detailed library logs in the task output
  - `false`: Show only basic success/error messages

**Example:**
```yaml
- name: Configure global prefix sets
  graphiant.graphiant_playbooks.graphiant_global_config:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    config_file: "sample_global_prefix_lists.yaml"
    operation: "configure_prefix_sets"
    state: present

- name: Configure global LAN segments (using specific operation)
  graphiant.graphiant_playbooks.graphiant_global_config:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    config_file: "sample_global_lan_segments.yaml"
    operation: "configure_lan_segments"
    state: present

# Alternative: Configure global LAN segments (using general configure operation)
# - name: Configure global LAN segments
#   graphiant.graphiant_playbooks.graphiant_global_config:
#     host: "https://api.graphiant.com"
#     username: "{{ graphiant_username }}"
#     password: "{{ graphiant_password }}"
#     config_file: "sample_global_lan_segments.yaml"
#     operation: "configure"
#     state: present

# Configure with detailed logging enabled
- name: Configure global LAN segments (with detailed logs)
  graphiant.graphiant_playbooks.graphiant_global_config:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    config_file: "sample_global_lan_segments.yaml"
    operation: "configure_lan_segments"
    state: present
    detailed_logs: true

- name: Configure global site lists
  graphiant.graphiant_playbooks.graphiant_global_config:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    config_file: "sample_global_site_lists.yaml"
    operation: "configure_site_lists"
    state: present

- name: Deconfigure global site lists
  graphiant.graphiant_playbooks.graphiant_global_config:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    config_file: "sample_global_site_lists.yaml"
    operation: "deconfigure_site_lists"
    state: absent
```

### graphiant_sites

Manages Graphiant site creation, deletion, and object attachments/detachments.

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `site_config_file` (required): Path to site configuration YAML file
- `operation` (optional): Operation to perform (at least one of operation or state required)
  - `configure`: Create sites and attach global objects (default for state: present)
  - `deconfigure`: Detach global objects and delete sites (default for state: absent)
  - `configure_sites`: Create sites only
  - `deconfigure_sites`: Delete sites only
  - `attach_objects`: Attach global objects to existing sites
  - `detach_objects`: Detach global objects from sites
- `state` (optional): Desired state (present/absent, default: present)
  - `present`: Maps to `configure` when operation not specified
  - `absent`: Maps to `deconfigure` when operation not specified
- `detailed_logs` (optional): Enable detailed logging output from library operations (default: false)
  - `true`: Show detailed library logs in the task output
  - `false`: Show only basic success/error messages

**Examples:**
```yaml
# Configure sites (create sites and attach objects)
- name: Configure sites
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "sample_sites.yaml"
    operation: "configure"
    state: present

# Create sites only
- name: Create sites
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "sample_sites.yaml"
    operation: "configure_sites"
    state: present

# Attach objects to existing sites
- name: Attach objects to sites
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "sample_sites.yaml"
    operation: "attach_objects"
    state: present

- name: Attach global objects to sites with detailed logging
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "sample_site_attachments.yaml"
    operation: "attach_objects"
    detailed_logs: true
    state: present
```

### graphiant_data_exchange

Manages Graphiant Data Exchange services, customers, service-to-customer matches, and invitation acceptance workflows.

**Overview of Data Exchange Workflows:**

The Data Exchange module supports four main workflows:
- **Workflow 1: Create New Service** - Create Data Exchange services that can be shared with customers
- **Workflow 2: Create New Customer** - Create Data Exchange customers (non Graphiant peers)
- **Workflow 3: Match Services to Customer** - Match services to customers and establish peering relationships
- **Workflow 4: Accept Invitation** - Accept service invitations for non Graphiant customers with gateway service deployment

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `config_file` (required for create/delete/match/accept operations): Path to Data Exchange configuration YAML file
- `matches_file` (optional for accept_invitation): Path to matches responses JSON file for match ID lookup. If not provided, uses default path.
- `dry_run` (optional for accept_invitation): Enable dry-run mode for accept_invitation operation (default: false)
- `operation` (optional): Operation to perform (at least one of operation or state required)
  - `create_services`: Create Data Exchange services from YAML configuration (Workflow 1)
  - `delete_services`: Delete Data Exchange services from YAML configuration
  - `get_services_summary`: Get summary of all Data Exchange services with tabulated output
  - `create_customers`: Create Data Exchange customers from YAML configuration (Workflow 2)
  - `delete_customers`: Delete Data Exchange customers from YAML configuration
  - `get_customers_summary`: Get summary of all Data Exchange customers with tabulated output
  - `match_service_to_customers`: Match services to customers from YAML configuration (Workflow 3)
  - `accept_invitation`: Accept Data Exchange service invitation (Workflow 4) - requires config_file
  - `get_service_health`: Get service health monitoring information
- `state` (optional): Desired state (present/absent/query, default: present)
  - `present`: Maps to `create_services` when operation not specified
  - `absent`: Maps to `delete_services` when operation not specified
  - `query`: Maps to `get_services_summary` when operation not specified
- `detailed_logs` (optional): Enable detailed logging output from library operations (default: false)
  - `true`: Show detailed library logs in the task output
  - `false`: Show only basic success/error messages
- `service_name` (optional): Service name for health monitoring operations (required for get_service_health)
- `is_provider` (optional): Whether to get provider view for service health monitoring (default: false)

**Workflow 1: Create Data Exchange Services**

```yaml
- name: Create Data Exchange services
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: create_services
    config_file: "de_workflows_configs/sample_data_exchange_services.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: create_services_result

- name: Display services creation result
  debug:
    msg: "{{ create_services_result.msg }}"
```

**Configuration File Structure:**
```yaml
data_exchange_services:
  - serviceName: "de-service-1"
    type: "peering_service"
    policy:
      serviceLanSegment: "lan-segment-3"  # Resolved to ID automatically
      type: "peering_service"
      site:
        - sites: ["Wales-sdktest"]  # Site names resolved to IDs
          siteLists: []
      description: "de_service_1_description"
      prefixTags:
        - prefix: "10.1.1.0/24"
          tag: "s-1-prefix1"
```

**Workflow 2: Create Data Exchange Customers**

```yaml
- name: Create Data Exchange customers
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: create_customers
    config_file: "de_workflows_configs/sample_data_exchange_customers.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: create_customers_result

- name: Display customers creation result
  debug:
    msg: "{{ create_customers_result.msg }}"
```

**Configuration File Structure:**
```yaml
data_exchange_customers:
  - name: "FinanceInc"
    type: "non_graphiant_peer"
    invite:
      adminEmail: 
        - "finance@financeinc.com"
      maximumNumberOfSites: 2
```

**Note:** Configuration files support Jinja2 templates for scale testing. See `sample_data_exchange_customers_scale2.yaml` for examples.

**Workflow 3: Match Services to Customers**

```yaml
- name: Match Data Exchange services to customers
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: match_service_to_customers
    config_file: "de_workflows_configs/sample_data_exchange_matches.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: match_result

- name: Display match result
  debug:
    msg: "{{ match_result.msg }}"
```

**Configuration File Structure:**
```yaml
data_exchange_matches:
  - customerName: "FinanceInc"
    serviceName: "de-service-1"
    servicePrefixes:  # Select specific service prefixes to include
      - prefix: "10.1.1.0/24" 
        tag: "s-1-prefix1"
    nat:  # Optional NAT configuration
      - prefix: "10.101.1.0/24"
        outsideNatPrefix: "170.101.1.0/24"
```

**Important:** After successful matching, responses are automatically saved to:
- `de_workflows_configs/output/sample_data_exchange_matches_responses_<timestamp>.json`
- `de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json`

The response file contains match details (`customer_id`, `service_id`, `match_id`, `status`) required for Workflow 4.

**Workflow 4: Accept Invitation (Non-Graphiant Customer)**

```yaml
- name: Accept Data Exchange service invitation (Dry Run)
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: accept_invitation
    config_file: "de_workflows_configs/sample_data_exchange_acceptance.yaml"
    matches_file: "de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json"
    dry_run: true
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: accept_result_dry_run

- name: Display dry run result
  debug:
    msg: "{{ accept_result_dry_run.msg }}"

- name: Accept Data Exchange service invitation
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: accept_invitation
    config_file: "de_workflows_configs/sample_data_exchange_acceptance.yaml"
    matches_file: "de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json"
    dry_run: false
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: accept_result

- name: Display acceptance result
  debug:
    msg: "{{ accept_result.msg }}"
```

**Configuration File Structure:**
```yaml
data_exchange_acceptances:
  - customerName: "FinanceInc"
    serviceName: "de-service-1"
    siteInformation:
      - sites: ["site-sjc-sdktest"]
        siteLists: []
    nat:
      - prefix: "10.1.1.0/24"
        tag: "s-1-prefix1"
    policy:
      - lanSegment: "customer-1-segment"
        consumerPrefixes:
          - "10.101.0.0/24"
    siteToSiteVpn:
      ipsecGatewayDetails:
        name: "s2s-FinanceInc"
        destinationAddress: "204.137.1.1"
        ikeInitiator: false
        tunnel1: {}
        tunnel2: {}
        routing:
          static:
            destinationPrefix:
              - "10.101.0.0/24"
        vpnProfile: "GlobalVpnProfile-joule-smoke"
      region: "us-central-1 (Chicago)"
      emails: ["finance@financeinc.com"]
```

**Prerequisites for Data Exchange Workflows:**

Before running Data Exchange workflows, ensure prerequisites are met:

1. **Prerequisite Playbooks** (run in order):
   ```bash
   # 1. Configure LAN segments (required for services)
   ansible-playbook ansible_collections/graphiant/graphiant_playbooks/playbooks/de_workflows/00_dataex_lan_segments_prerequisites.yml
   
   # 2. Configure LAN interfaces (required for services)
   ansible-playbook ansible_collections/graphiant/graphiant_playbooks/playbooks/de_workflows/00_dataex_lan_interface_prerequisites.yml
   
   # 3. Configure VPN profiles (required for Workflow 4 - accept invitation)
   ansible-playbook ansible_collections/graphiant/graphiant_playbooks/playbooks/de_workflows/00_dataex_vpn_profile_prerequisites.yml
   ```

2. **Workflow 4 Specific Prerequisites:**
   - Workflow 3 must be completed first (match services to customers)
   - Matches response file must exist with valid match IDs
   - Required global objects (LAN segments, VPN profiles) must exist
   - Minimum 2 gateways required per region for redundancy

**Complete Data Exchange Workflow Example:**

```yaml
---
- name: Complete Data Exchange Workflow
  hosts: localhost
  gather_facts: false
  vars:
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  
  tasks:
    # Workflow 1: Create services
    - name: Create Data Exchange services
      graphiant.graphiant_playbooks.graphiant_data_exchange:
        <<: *graphiant_client_params
        operation: create_services
        config_file: "de_workflows_configs/sample_data_exchange_services.yaml"
        detailed_logs: true
    
    # Workflow 2: Create customers
    - name: Create Data Exchange customers
      graphiant.graphiant_playbooks.graphiant_data_exchange:
        <<: *graphiant_client_params
        operation: create_customers
        config_file: "de_workflows_configs/sample_data_exchange_customers.yaml"
        detailed_logs: true
    
    # Workflow 3: Match services to customers
    - name: Match Data Exchange services to customers
      graphiant.graphiant_playbooks.graphiant_data_exchange:
        <<: *graphiant_client_params
        operation: match_service_to_customers
        config_file: "de_workflows_configs/sample_data_exchange_matches.yaml"
        detailed_logs: true
    
    # Workflow 4: Accept invitations
    - name: Accept Data Exchange service invitation
      graphiant.graphiant_playbooks.graphiant_data_exchange:
        <<: *graphiant_client_params
        operation: accept_invitation
        config_file: "de_workflows_configs/sample_data_exchange_acceptance.yaml"
        matches_file: "de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json"
        dry_run: false
        detailed_logs: true
```

**Query Operations:**

```yaml
# Get services summary
- name: Get Data Exchange services summary
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: get_services_summary
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
  register: services_summary

- name: Display services summary
  debug:
    msg: "{{ services_summary.msg }}"

# Get customers summary
- name: Get Data Exchange customers summary
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: get_customers_summary
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
  register: customers_summary

- name: Display customers summary
  debug:
    msg: "{{ customers_summary.msg }}"
```

**Delete Operations:**

```yaml
# Delete customers (must be deleted before services)
- name: Delete Data Exchange customers
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: delete_customers
    config_file: "de_workflows_configs/sample_data_exchange_customers.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"

# Delete services
- name: Delete Data Exchange services
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: delete_services
    config_file: "de_workflows_configs/sample_data_exchange_services.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
```

**Service Health Monitoring:**

```yaml
# Get service health (consumer view)
- name: Get Data Exchange service health
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: get_service_health
    service_name: "de-service-1"
    is_provider: false
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: service_health

- name: Display service health
  debug:
    msg: "{{ service_health.msg }}"

# Get service health (provider view)
- name: Get Data Exchange service health (provider view)
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: get_service_health
    service_name: "de-service-1"
    is_provider: true
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
  register: service_health_provider

- name: Display service health (provider view)
  debug:
    msg: "{{ service_health_provider.msg }}"
```

## Detailed Logging

All Graphiant Ansible modules support detailed logging through the `detailed_logs` parameter. When enabled, you'll see comprehensive output from the underlying Graphiant library operations, including:

- **API Call Details**: Full request/response information for Graphiant API calls
- **Configuration Processing**: Step-by-step processing of configuration files
- **Operation Progress**: Real-time updates on what the library is doing
- **Debugging Information**: Detailed error messages and troubleshooting data
- **Success/Failure Details**: Specific information about what succeeded or failed

### When to Use Detailed Logging

- **Development and Testing**: When developing new playbooks or troubleshooting issues
- **Debugging**: When operations fail and you need to understand why
- **Monitoring**: When you want to see exactly what changes are being made
- **Auditing**: When you need detailed records of what operations were performed

### Output Formatting

When using `detailed_logs: true`, you may see output with literal `\n` characters. For clean, readable output, use one of these methods:

#### Method 1: Environment Variable (Recommended)
```bash
export ANSIBLE_STDOUT_CALLBACK=debug
ansible-playbook your_playbook.yml
```

#### Method 2: Command Line
```bash
ANSIBLE_STDOUT_CALLBACK=debug ansible-playbook your_playbook.yml
```

### Example Usage

```yaml
- name: Configure interfaces with detailed logging
  graphiant.graphiant_playbooks.graphiant_interfaces:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    interface_config_file: "sample_interface_config.yaml"
    operation: "configure_lan_interfaces"
    detailed_logs: true  # Enable detailed logging
    state: present
```

**Note**: Detailed logging is disabled by default (`detailed_logs: false`) to keep output clean during normal operations. Enable it only when you need the additional information.

## Credential Management

The Graphiant Ansible Collection supports multiple ways to manage credentials securely. Here are the recommended approaches:

### Option 1: YAML Anchors (Recommended)
Use YAML anchors to avoid repetition and keep playbooks clean:

```yaml
---
- name: Graphiant Configuration with YAML Anchors
  hosts: localhost
  gather_facts: false
  vars:
    graphiant_host: "https://api.graphiant.com"
    graphiant_username: "{{ vault_graphiant_username }}"
    graphiant_password: "{{ vault_graphiant_password }}"
    
    # Use YAML anchors to avoid repetition
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  
  tasks:
    - name: Configure global prefix sets
      graphiant.graphiant_playbooks.graphiant_global_config:
        <<: *graphiant_client_params
        config_file: "sample_global_prefix_lists.yaml"
        operation: "configure"
        state: present
```

### Option 2: Inventory Variables
Store credentials in inventory files for different environments:

```yaml
# inventory/production.yml
[graphiant_prod:vars]
graphiant_host = "https://api.graphiant.com"
graphiant_username = "{{ vault_prod_graphiant_username }}"
graphiant_password = "{{ vault_prod_graphiant_password }}"
```

### Option 3: Variable Files
Use external variable files for credential management:

```yaml
# vars/credentials.yml
graphiant_host: "https://api.graphiant.com"
graphiant_username: "{{ vault_graphiant_username }}"
graphiant_password: "{{ vault_graphiant_password }}"
```

```yaml
# playbook.yml
- name: Graphiant Configuration
  hosts: localhost
  vars_files:
    - vars/credentials.yml
  tasks:
    - name: Configure interfaces
      graphiant.graphiant_playbooks.graphiant_interfaces:
        host: "{{ graphiant_host }}"
        username: "{{ graphiant_username }}"
        password: "{{ graphiant_password }}"
        # ... other parameters
```

### Option 4: Runtime Variables
Pass credentials at runtime using `--extra-vars`:

```bash
# Key-value format
ansible-playbook playbook.yml -e "graphiant_username=myuser" -e "graphiant_password=mypass"

# JSON format
ansible-playbook playbook.yml -e '{"graphiant_username":"myuser","graphiant_password":"mypass"}'

# YAML file format
ansible-playbook playbook.yml -e "@vars/credentials.yml"
```

### Option 5: INI File with Lookup (Development/Testing)
Use INI files for local development and testing with the `lookup` function:

```ini
# test/test.ini
[credentials]
username = your_username@graphiant.com
password = your_password
[host]
url = https://api.test.graphiant.io
```

```yaml
# In playbook
- name: Configure interfaces using INI file credentials
  graphiant.graphiant_playbooks.graphiant_interfaces:
    host: "{{ lookup('ini', 'url file=/absolute/path/test/test.ini section=host') }}"
    username: "{{ lookup('ini', 'username file=/absolute/path/test/test.ini section=credentials') }}"
    password: "{{ lookup('ini', 'password file=/absolute/path/test/test.ini section=credentials') }}"
    interface_config_file: "sample_interface_config.yaml"
    operation: "configure_lan_interfaces"
    state: present
```

**Benefits:**
- Keep credentials separate from playbooks
- Easy to switch between different environments
- Secure for local development (add to `.gitignore`)
- Works well with the project's existing `test.ini` structure

**Example with existing project structure:**
```yaml
# Using the project's test.ini file
- name: Configure LAN interfaces using project credentials
  graphiant.graphiant_playbooks.graphiant_interfaces:
    host: "{{ lookup('ini', 'url file=/absolute/path/test/test.ini section=host') }}"
    username: "{{ lookup('ini', 'username file=/absolute/path/test/test.ini section=credentials') }}"
    password: "{{ lookup('ini', 'password file=/absolute/path/test/test.ini section=credentials') }}"
    interface_config_file: "sample_interface_config.yaml"
    operation: "configure_lan_interfaces"
    detailed_logs: true
    state: present
```

### Option 6: Environment Variables
Use environment variables for CI/CD pipelines:

```bash
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="myuser"
export GRAPHIANT_PASSWORD="mypass"
ansible-playbook playbook.yml
```

```yaml
# In playbook
vars:
  graphiant_host: "{{ ansible_env.GRAPHIANT_HOST }}"
  graphiant_username: "{{ ansible_env.GRAPHIANT_USERNAME }}"
  graphiant_password: "{{ ansible_env.GRAPHIANT_PASSWORD }}"
```

#### Path Configuration
For advanced use cases, you can specify the path to your graphiant-playbooks directory:

```bash
# Set the path to your graphiant-playbooks directory
export GRAPHIANT_PLAYBOOKS_PATH="/path/to/your/graphiant-playbooks"

# This is useful when:
# - Running playbooks from different working directories
# - Using the collection in CI/CD pipelines
# - Deploying from non-standard locations
ansible-playbook playbook.yml
```

### Security Best Practices

1. **Use Ansible Vault** for sensitive credentials:
   ```bash
   ansible-vault create vars/credentials.yml
   ansible-playbook playbook.yml --ask-vault-pass
   ```

2. **Environment-specific credentials**:
   ```yaml
   # vars/production.yml
   graphiant_host: "https://api.graphiant.com"
   graphiant_username: "{{ vault_prod_username }}"
   graphiant_password: "{{ vault_prod_password }}"
   ```

3. **Never commit plaintext passwords** to version control

4. **Use least privilege** - create dedicated service accounts for automation

## Example Playbooks

### Complete Network Setup
```yaml
---
- name: Deploy complete Graphiant network configuration
  hosts: localhost
  gather_facts: false
  vars:
    graphiant_host: "https://api.graphiant.com"
    graphiant_username: "{{ vault_graphiant_username }}"
    graphiant_password: "{{ vault_graphiant_password }}"
    
    # Use YAML anchors to avoid repetition
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  
  tasks:
    - name: Configure global prefix sets
      graphiant.graphiant_playbooks.graphiant_global_config:
        <<: *graphiant_client_params
        config_file: "sample_global_prefix_lists.yaml"
        operation: "configure"
        state: present
    
    - name: Configure global BGP filters
      graphiant.graphiant_playbooks.graphiant_global_config:
        <<: *graphiant_client_params
        config_file: "sample_global_bgp_filters.yaml"
        operation: "configure"
        state: present
    
    - name: Configure BGP peering
      graphiant.graphiant_playbooks.graphiant_bgp:
        <<: *graphiant_client_params
        bgp_config_file: "sample_bgp_peering.yaml"
        operation: "configure"
        state: present
    
    - name: Configure interfaces and circuits
      graphiant.graphiant_playbooks.graphiant_interfaces:
        <<: *graphiant_client_params
        interface_config_file: "sample_interface_config.yaml"
        circuit_config_file: "sample_circuit_config.yaml"
        operation: "configure_interfaces"
        state: present
    
    - name: Attach global objects to sites
      graphiant.graphiant_playbooks.graphiant_sites:
        <<: *graphiant_client_params
        site_config_file: "sample_site_attachments.yaml"
        operation: "attach_objects"
        state: present
```

### Circuit-Only Operations
```yaml
---
- name: Update circuit configurations with static routes
  hosts: localhost
  gather_facts: false
  vars:
    graphiant_host: "https://api.graphiant.com"
    graphiant_username: "{{ vault_graphiant_username }}"
    graphiant_password: "{{ vault_graphiant_password }}"
    
    # Use YAML anchors to avoid repetition
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  
  tasks:
    - name: Configure circuits only (for static routes)
      graphiant.graphiant_playbooks.graphiant_interfaces:
        <<: *graphiant_client_params
        interface_config_file: "sample_interface_config.yaml"
        circuit_config_file: "sample_circuit_config.yaml"
        operation: "configure_circuits"
        state: present
```

## Configuration Files

The collection uses the same YAML configuration files as the standalone Graphiant Playbooks library:

- `sample_interface_config.yaml`: Interface configurations
- `sample_circuit_config.yaml`: Circuit configurations with static routes
- `sample_bgp_peering.yaml`: BGP peering configurations
- `sample_global_prefix_lists.yaml`: Global prefix set configurations
- `sample_global_bgp_filters.yaml`: Global BGP filter configurations
- `sample_global_snmp_services.yaml`: Global SNMP service configurations
- `sample_global_syslog_servers.yaml`: Global syslog service configurations
- `sample_global_ipfix_exporters.yaml`: Global IPFIX service configurations
- `sample_global_vpn_profiles.yaml`: Global VPN profile configurations
- `sample_global_lan_segments.yaml`: Global LAN segment configurations
- `sample_global_site_lists.yaml`: Global site list configurations
- `sample_site_attachments.yaml`: Site attachment configurations
- `sample_sites.yaml`: Site creation and object attachment configurations
- `sample_data_exchange_services.yaml`: Data Exchange service configurations (Workflow 1)
- `sample_data_exchange_customers.yaml`: Data Exchange customer configurations (Workflow 2)
- `sample_data_exchange_matches.yaml`: Data Exchange service-to-customer match configurations (Workflow 3)
- `sample_data_exchange_acceptance.yaml`: Data Exchange invitation acceptance configurations (Workflow 4)
- `sample_data_exchange_services_scale.yaml`: Scale test configuration for services
- `sample_data_exchange_customers_scale.yaml`: Scale test configuration for customers
- `sample_data_exchange_customers_scale2.yaml`: Scale test configuration with Jinja2 templates for customers
- `sample_data_exchange_matches_scale.yaml`: Scale test configuration for matches
- `sample_data_exchange_acceptance_scale.yaml`: Scale test configuration for invitation acceptance

### Jinja2 Template Support in Configuration Files

**All configuration files support Jinja2 templating syntax**, allowing dynamic generation of configurations. This feature is automatically enabled - simply use Jinja2 syntax in your YAML files.

**Key Features:**
- **Automatic Rendering**: Jinja2 templates are automatically detected and rendered before YAML parsing
- **Works with All Managers**: Supported by all operations that use configuration files
- **Scale Testing**: Perfect for generating multiple similar configurations
- **Backward Compatible**: Regular YAML files (without Jinja2) continue to work as before

**Example: Scale Testing with Jinja2**

```yaml
# sample_data_exchange_customers_scale2.yaml
data_exchange_customers:
  {% for i in range(1, 51) %}
  - name: "FinanceBank-{{ 100 + i }}"
    type: "non_graphiant_peer"
    invite:
      adminEmail: 
        - "admin{{ 100 + i }}@financebank.com"
        - "support{{ 100 + i }}@financebank.com"
      maximumNumberOfSites: 4
  {% endfor %}
```

This generates 50 customer configurations automatically (FinanceBank-101 through FinanceBank-150).

**Supported Jinja2 Features:**
- **Loops**: `{% for item in list %}...{% endfor %}`
- **Conditionals**: `{% if condition %}...{% endif %}`
- **Variables**: `{{ variable_name }}`
- **Expressions**: `{{ 100 + i }}`, `{{ item.name }}`
- **Filters**: `{{ value | upper }}`, `{{ value | default('default') }}`

**Usage in Ansible Playbooks:**

```yaml
- name: Create Data Exchange customers with Jinja2 template
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: create_customers
    config_file: "de_workflows_configs/sample_data_exchange_customers_scale2.yaml"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    detailed_logs: true
```

**Error Handling:**
- Jinja2 syntax errors are caught and reported with file location
- YAML parsing errors after rendering include line numbers for debugging
- Both templated and non-templated files are handled seamlessly

**Best Practices:**
- Use Jinja2 for repetitive configurations (scale testing, bulk operations)
- Test templates with small ranges first (e.g., `range(1, 6)` for 5 items)
- Keep template logic simple and readable
- Use comments to document template purpose and logic
- Verify rendered output before scaling to large numbers

## Configuration Format Examples

### Global Site Lists Configuration

The `sample_global_site_lists.yaml` file demonstrates how to configure global site lists:

```yaml
# Sample Global Site Lists Configuration
# This file demonstrates how to configure global site lists
#
# The system will:
# 1. Read site names from the 'sites' list
# 2. Look up site IDs using v1/sites/details API
# 3. Generate the correct API payload with site IDs
# 4. POST to v1/global/site-lists with the payload

site_lists:
  - name: "Site-list1"
    description: "Site-list1 desc"
    sites:
      - "UAT-Site1"
      - "UAT-Site2"
      - "UAT-Site3"
      - "Liverpool-sdktest"
      - "Wales-sdktest"

  - name: "Site-list2"
    description: "Site-list2 desc"
    sites:
      - "UAT-Site3"
      - "Liverpool-sdktest"
      - "Wales-sdktest"
```

**Key Features:**
- **Site Name Resolution**: The system automatically converts site names to site IDs
- **Fail-Fast Approach**: If any site name is not found, the entire operation fails
- **Idempotent Operations**: Configure only creates if not exists, deconfigure only deletes if exists
- **Reference Checking**: Deconfigure fails if site lists have active references

## Error Handling

The collection provides comprehensive error handling with user-friendly error messages for:
- Configuration errors
- API errors
- Device not found errors
- Authentication errors
- File not found errors

### **Parameter Validation Errors**

When neither `operation` nor `state` parameters are provided, modules return helpful error messages with the list of supported operations:

**Example Error Messages:**
```
Either 'operation' or 'state' parameter must be provided. 
Supported operations: configure, deconfigure, configure_prefix_sets, deconfigure_prefix_sets, configure_bgp_filters, deconfigure_bgp_filters, configure_snmp_services, deconfigure_snmp_services, configure_syslog_services, deconfigure_syslog_services, configure_ipfix_services, deconfigure_ipfix_services, configure_vpn_profiles, deconfigure_vpn_profiles, configure_lan_segments, deconfigure_lan_segments, configure_site_lists, deconfigure_site_lists
```

**Module-Specific Supported Operations:**
- **graphiant_global_config**: configure, deconfigure, configure_prefix_sets, deconfigure_prefix_sets, configure_bgp_filters, deconfigure_bgp_filters, configure_snmp_services, deconfigure_snmp_services, configure_syslog_services, deconfigure_syslog_services, configure_ipfix_services, deconfigure_ipfix_services, configure_vpn_profiles, deconfigure_vpn_profiles, configure_lan_segments, deconfigure_lan_segments, configure_site_lists, deconfigure_site_lists
- **graphiant_interfaces**: configure_interfaces, deconfigure_interfaces, configure_lan_interfaces, deconfigure_lan_interfaces, configure_wan_circuits_interfaces, deconfigure_wan_circuits_interfaces, configure_circuits, deconfigure_circuits
- **graphiant_sites**: configure, deconfigure, attach, detach
- **graphiant_bgp**: configure, deconfigure, detach_policies

## Check Mode

All modules support Ansible's check mode (`--check`), which allows you to see what changes would be made without actually executing them.

## Troubleshooting

### Common Installation Issues

#### Issue: "Collection does not contain the required file MANIFEST.json"
**Solution**: Use Method 1 (Direct Directory Installation) instead of the tar.gz archive:
```bash
ansible-galaxy collection install ansible_collections/graphiant/graphiant_playbooks/ --force
```

#### Issue: "Could not import Graphiant library: No module named 'libs'"
**Solution**: Set the PYTHONPATH environment variable to include the project directory:
```bash
export PYTHONPATH=$(pwd):$PYTHONPATH
```
This allows the collection to access the Graphiant library from the `libs` directory.

#### Issue: "Collection not found" or "Module not found"
**Solution**: Check your Ansible collection paths and installation:
```bash
# Check where Ansible looks for collections
ansible-config dump | grep COLLECTIONS_PATHS

# Verify the collection is installed
ansible-galaxy collection list | grep graphiant

# Reinstall if necessary
ansible-galaxy collection install ansible_collections/graphiant/graphiant_playbooks/ --force
```

#### Issue: "Module failed: Configuration file not found"
**Solution**: Ensure your configuration files exist and are accessible:
```bash
# Check if config files exist
ls -la configs/sample_*.yaml

# Use absolute paths if needed
config_file: "/full/path/to/your/config.yaml"
```

#### Issue: "Task failed: Finalization of task args failed"
**Solution**: Check that all required parameters are provided and variables are defined:
```bash
# Use --check mode to validate without executing
ansible-playbook --check your_playbook.yml

# Check variable definitions
ansible-playbook --check your_playbook.yml -e "graphiant_username=test" -e "graphiant_password=test"
```

### Common Runtime Errors

#### Issue: "Graphiant SDK not available. Please install graphiant-sdk package"
**Error Message:**
```
Module failed: Configuration error during get_services_summary: Failed to initialize Graphiant connection: Graphiant SDK not available. Please install graphiant-sdk package.
```

**Solution**: Install the Graphiant SDK package:
```bash
# Activate your virtual environment (if using one)
source venv/bin/activate  # or source venv_pb/bin/activate
```

**Prevention**: Always install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

#### Issue: "No host specified"
**Error Message:**
```
Module failed: Graphiant playbook error during get_services_summary: Failed to initialize Graphiant connection: GraphiantConfig initialization failed: No host specified.
```

**Solution**: Set the `GRAPHIANT_HOST` environment variable or provide `host` parameter in the playbook:
```bash
# Option 1: Set environment variable
export GRAPHIANT_HOST="https://api.graphiant.com"
# or for test environment
export GRAPHIANT_HOST="https://api.test.graphiant.io"

# Option 2: Provide in playbook
- name: Get services summary
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    host: "https://api.graphiant.com"
    operation: get_services_summary
```

**Note**: The `host` parameter in the playbook takes precedence over the environment variable.

#### Issue: "v1_auth_login_post_response is None"
**Error Message:**
```
Module failed: Graphiant playbook error during get_services_summary: Failed to initialize Graphiant connection: GraphiantConfig initialization failed: v1_auth_login_post_response is None
```

**Solution**: Provide authentication credentials:
```bash
# Set environment variables
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="your_username@graphiant.com"
export GRAPHIANT_PASSWORD="your_password"

# Or provide in playbook
- name: Get services summary
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    host: "https://api.graphiant.com"
    username: "{{ vault_graphiant_username }}"
    password: "{{ vault_graphiant_password }}"
    operation: get_services_summary
```

**Common Causes:**
- Missing `GRAPHIANT_USERNAME` or `GRAPHIANT_PASSWORD` environment variables
- Incorrect credentials
- Network connectivity issues to Graphiant API

#### Issue: "Matches file not found" (Data Exchange Workflow 4)
**Error Message:**
```
WARNING - _get_match_id_from_customer_service: Matches file not found at /path/to/de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json
ERROR - Failed to resolve names to IDs: No match found for customer 'FinanceInc' and service 'de-service-1'
```

**Solution**: Ensure Workflow 3 (Match Services to Customers) has been completed first:
```bash
# Step 1: Run Workflow 3 to create matches
ansible-playbook ansible_collections/graphiant/graphiant_playbooks/playbooks/de_workflows/03_dataex_match_services_to_customers.yml

# Step 2: Verify matches file was created
ls -la configs/de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json

# Step 3: Then run Workflow 4
ansible-playbook ansible_collections/graphiant/graphiant_playbooks/playbooks/de_workflows/06_dataex_accept_invitation_dry_run.yml
```

**Alternative Solution**: If matches file exists in a different location, specify it explicitly:
```yaml
- name: Accept Data Exchange service invitation
  graphiant.graphiant_playbooks.graphiant_data_exchange:
    operation: accept_invitation
    config_file: "de_workflows_configs/sample_data_exchange_acceptance.yaml"
    matches_file: "/custom/path/to/matches_responses_latest.json"
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
```

**Note**: The matches file is automatically created by Workflow 3 and contains the `match_id` required for Workflow 4.

### Environment Setup Checklist

Before running Ansible playbooks, ensure all required environment variables are set:

```bash
# Required: Python path for library access
export PYTHONPATH=$(pwd):$PYTHONPATH

# Required: Graphiant API credentials
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="your_username@graphiant.com"
export GRAPHIANT_PASSWORD="your_password"

# Optional: Better log formatting
export ANSIBLE_STDOUT_CALLBACK=debug

# Optional: Custom playbooks path (if not running from project root)
export GRAPHIANT_PLAYBOOKS_PATH="/path/to/your/graphiant-playbooks"
```

**Quick Verification:**
```bash
# Check environment variables
echo "PYTHONPATH: $PYTHONPATH"
echo "GRAPHIANT_HOST: $GRAPHIANT_HOST"
echo "GRAPHIANT_USERNAME: $GRAPHIANT_USERNAME"

# Test connection with a simple query
ansible-playbook --check ansible_collections/graphiant/graphiant_playbooks/playbooks/de_workflows/01_dataex_create_services.yml
```

### Data Exchange Workflow Troubleshooting

#### Workflow 4 Fails: "No match found for customer and service"
**Symptoms:**
- Workflow 4 (accept invitation) fails with "No match found"
- Matches file not found error

**Solution Steps:**
1. **Verify Workflow 3 completed successfully:**
   ```bash
   # Check if matches file exists
   ls -la configs/de_workflows_configs/output/*matches*latest.json
   ```

2. **Verify match exists in the file:**
   ```bash
   # Check match entries
   cat configs/de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json | jq '.[] | select(.customer_name=="FinanceInc" and .service_name=="de-service-1")'
   ```

3. **Verify customer and service names match exactly:**
   - Customer name in acceptance config must match customer name in matches file
   - Service name in acceptance config must match service name in matches file
   - Names are case-sensitive

4. **Re-run Workflow 3 if needed:**
   ```bash
   ansible-playbook ansible_collections/graphiant/graphiant_playbooks/playbooks/de_workflows/03_dataex_match_services_to_customers.yml
   ```

#### Workflow 4 Fails: "Region does not meet minimum gateway requirements"
**Error Message:**
```
ERROR - Region us-central-1 (Chicago) does not meet minimum gateway requirements (found 1, required 2)
```

**Solution**: Ensure at least 2 active gateways exist in the specified region:
```bash
# Check gateway status (requires Graphiant API access)
# Or configure additional gateways in the Graphiant portal
```

**Note**: Gateway requirements are validated during dry-run mode, so you'll see this error even in validation.

### Virtual Environment Setup
For isolated installation, use a virtual environment:

```bash
# Create virtual environment
python -m venv ~/venv_pb
source ~/venv_pb/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install collection
ansible-galaxy collection install ansible_collections/graphiant/graphiant_playbooks/ --force
```

### Collection Validation
Validate the collection structure:

```bash
# Run validation script
python ansible_collections/graphiant/graphiant_playbooks/validate_collection.py

# Expected output: "Collection structure validation passed!"
```

## Quick Reference

### Essential Commands
```bash
# Check Ansible collection paths
ansible-config dump | grep COLLECTIONS_PATHS

# List installed collections
ansible-galaxy collection list | grep graphiant

# Install collection
ansible-galaxy collection install ansible_collections/graphiant/graphiant_playbooks/ --force

# Uninstall collection
rm -rf ~/.ansible/collections/ansible_collections/graphiant/graphiant_playbooks

# Test collection
ansible-playbook --check ansible_collections/graphiant/graphiant_playbooks/playbooks/final_test.yml
```

### Environment Variables
```bash
# Required for library access
export PYTHONPATH=$(pwd):$PYTHONPATH

# Graphiant API credentials
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="username"
export GRAPHIANT_PASSWORD="password"

# Optional: Custom playbooks path
export GRAPHIANT_PLAYBOOKS_PATH="/path/to/your/graphiant-playbooks"
```

## License

This collection is licensed under the same license as the Graphiant Playbooks project.

## Additional Resources

- **Credential Management Guide**: See `CREDENTIAL_MANAGEMENT_GUIDE.md` for comprehensive credential management examples
- **Example Files**: Check the `examples/` directory for various credential management approaches
- **Test Playbooks**: Use `playbooks/credential_examples.yml` to test different credential methods

## Support

For support and documentation, visit:
- [Graphiant Documentation](https://docs.graphiant.com/)
- [Graphiant Playbooks User Guide](https://docs.graphiant.com/docs/graphiant-playbooks)
- [GitHub Repository](https://github.com/graphiant/graphiant-playbooks)
