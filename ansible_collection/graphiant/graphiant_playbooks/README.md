# Graphiant Playbooks Ansible Collection

This Ansible collection provides modules for automating Graphiant NaaS (Network as a Service) configurations. It allows you to manage network infrastructure, interfaces, circuits, BGP peering, and global configurations through Ansible playbooks.

## Installation

### Prerequisites
Before installing the collection, ensure you have the following requirements:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify Ansible installation
ansible --version

# Set PYTHONPATH to include the project directory (required for library access)
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### From Ansible Galaxy (when published)
```bash
ansible-galaxy collection install graphiant.graphiant_playbooks
```

### From Source (Recommended Method)

#### Method 1: Direct Directory Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/graphiant/graphiant-playbooks.git
cd graphiant-playbooks

# Set PYTHONPATH to include the project directory
export PYTHONPATH=$(pwd):$PYTHONPATH

# Install the collection directly from source directory
ansible-galaxy collection install ansible_collection/graphiant/graphiant_playbooks/ --force
```

#### Method 2: Build and Install from Archive
```bash
# Clone the repository
git clone https://github.com/graphiant/graphiant-playbooks.git
cd graphiant-playbooks

# Build the collection
python ansible_collection/graphiant/graphiant_playbooks/build_collection.py

# Install from built archive (Note: This method may have issues with MANIFEST.json)
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

**Troubleshooting Collection Issues:**
- If collections aren't found, check the `COLLECTIONS_PATHS` configuration
- Ensure the collection is installed in the correct directory
- Verify file permissions on the collection directory

### Testing the Installation
Test the collection with a simple playbook:

```bash
# Set PYTHONPATH (required for library access)
export PYTHONPATH=$(pwd):$PYTHONPATH

# Set Graphiant portal client parameters
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="username"
export GRAPHIANT_PASSWORD="password"

# Optional: Set custom path to graphiant-playbooks directory
# This is useful when running from different working directories
export GRAPHIANT_PLAYBOOKS_PATH="/path/to/your/graphiant-playbooks"

# Run a test playbook in check mode
ansible-playbook --check ansible_collection/graphiant/graphiant_playbooks/playbooks/final_test.yml
```

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

**Troubleshooting Collection Issues:**
- If collections aren't found, check the `COLLECTIONS_PATHS` configuration
- Ensure the collection is installed in the correct directory
- Verify file permissions on the collection directory

### Clean Up (Optional)
If you want to completely remove all Graphiant collections:

```bash
# Remove the entire graphiant namespace
rm -rf ~/.ansible/collections/ansible_collections/graphiant/

# Verify complete removal
ansible-galaxy collection list | grep graphiant
# Expected output: (empty)
```

## Requirements

- Ansible >= 2.15
- Python >= 3.12
- Graphiant SDK >= 25.6.2
- Access to Graphiant NaaS platform

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
    interface_config_file: "configs/sample_interface_config.yaml"
    circuit_config_file: "configs/sample_circuit_config.yaml"
    operation: "configure_interfaces"
    state: present

- name: Configure LAN interfaces with detailed logging
  graphiant.graphiant_playbooks.graphiant_interfaces:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    interface_config_file: "configs/sample_interface_config.yaml"
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
    bgp_config_file: "configs/sample_bgp_peering.yaml"
    operation: "configure"
    state: present

- name: Configure BGP peering with detailed logging
  graphiant.graphiant_playbooks.graphiant_bgp:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    bgp_config_file: "configs/sample_bgp_peering.yaml"
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
    config_file: "configs/sample_global_prefix_lists.yaml"
    operation: "configure_prefix_sets"
    state: present

- name: Configure global LAN segments (using specific operation)
  graphiant.graphiant_playbooks.graphiant_global_config:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    config_file: "configs/sample_lan_segments.yaml"
    operation: "configure_lan_segments"
    state: present

# Alternative: Configure global LAN segments (using general configure operation)
# - name: Configure global LAN segments
#   graphiant.graphiant_playbooks.graphiant_global_config:
#     host: "https://api.graphiant.com"
#     username: "{{ graphiant_username }}"
#     password: "{{ graphiant_password }}"
#     config_file: "configs/sample_lan_segments.yaml"
#     operation: "configure"
#     state: present

# Configure with detailed logging enabled
- name: Configure global LAN segments (with detailed logs)
  graphiant.graphiant_playbooks.graphiant_global_config:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    config_file: "configs/sample_lan_segments.yaml"
    operation: "configure_lan_segments"
    state: present
    detailed_logs: true
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
    site_config_file: "configs/sample_sites.yaml"
    operation: "configure"
    state: present

# Create sites only
- name: Create sites
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "configs/sample_sites.yaml"
    operation: "configure_sites"
    state: present

# Attach objects to existing sites
- name: Attach objects to sites
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "configs/sample_sites.yaml"
    operation: "attach_objects"
    state: present

- name: Attach global objects to sites with detailed logging
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "configs/sample_site_attachments.yaml"
    operation: "attach_objects"
    detailed_logs: true
    state: present
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
    interface_config_file: "configs/sample_interface_config.yaml"
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
        config_file: "configs/sample_global_prefix_lists.yaml"
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
    host: "{{ lookup('ini', 'url file=test/test.ini section=host') }}"
    username: "{{ lookup('ini', 'username file=test/test.ini section=credentials') }}"
    password: "{{ lookup('ini', 'password file=test/test.ini section=credentials') }}"
    interface_config_file: "configs/sample_interface_config.yaml"
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
    host: "{{ lookup('ini', 'url file=test/test.ini section=host') }}"
    username: "{{ lookup('ini', 'username file=test/test.ini section=credentials') }}"
    password: "{{ lookup('ini', 'password file=test/test.ini section=credentials') }}"
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
        site_config_file: "configs/sample_site_attachments.yaml"
        operation: "attach_object"
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
        interface_config_file: "configs/sample_interface_config.yaml"
        circuit_config_file: "configs/sample_circuit_config.yaml"
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
- `sample_site_attachments.yaml`: Site attachment configurations
- `sample_sites.yaml`: Site creation and object attachment configurations

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
Supported operations: configure, deconfigure, configure_prefix_sets, deconfigure_prefix_sets, configure_bgp_filters, deconfigure_bgp_filters, configure_snmp_services, deconfigure_snmp_services, configure_syslog_services, deconfigure_syslog_services, configure_ipfix_services, deconfigure_ipfix_services, configure_vpn_profiles, deconfigure_vpn_profiles, configure_lan_segments, deconfigure_lan_segments
```

**Module-Specific Supported Operations:**
- **graphiant_global_config**: configure, deconfigure, configure_prefix_sets, deconfigure_prefix_sets, configure_bgp_filters, deconfigure_bgp_filters, configure_snmp_services, deconfigure_snmp_services, configure_syslog_services, deconfigure_syslog_services, configure_ipfix_services, deconfigure_ipfix_services, configure_vpn_profiles, deconfigure_vpn_profiles, configure_lan_segments, deconfigure_lan_segments
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
ansible-galaxy collection install ansible_collection/graphiant/graphiant_playbooks/ --force
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
ansible-galaxy collection install ansible_collection/graphiant/graphiant_playbooks/ --force
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

### Virtual Environment Setup
For isolated installation, use a virtual environment:

```bash
# Create virtual environment
python -m venv ~/venv_pb
source ~/venv_pb/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install collection
ansible-galaxy collection install ansible_collection/graphiant/graphiant_playbooks/ --force
```

### Collection Validation
Validate the collection structure:

```bash
# Run validation script
python ansible_collection/graphiant/graphiant_playbooks/validate_collection.py

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
ansible-galaxy collection install ansible_collection/graphiant/graphiant_playbooks/ --force

# Uninstall collection
rm -rf ~/.ansible/collections/ansible_collections/graphiant/graphiant_playbooks

# Test collection
ansible-playbook --check ansible_collection/graphiant/graphiant_playbooks/playbooks/final_test.yml
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


