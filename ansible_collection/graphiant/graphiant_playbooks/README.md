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

## Modules

### graphiant_interfaces

Manages Graphiant interfaces and circuits.

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `interface_config_file` (required): Path to interface configuration YAML file
- `circuit_config_file` (optional): Path to circuit configuration YAML file
- `operation` (required): Operation to perform
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
```

### graphiant_bgp

Manages Graphiant BGP peering and routing policies.

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `bgp_config_file` (required): Path to BGP configuration YAML file
- `operation` (required): Operation to perform
  - `configure`: Configure BGP peering and attach policies
  - `deconfigure`: Deconfigure BGP peering
  - `detach_policies`: Detach policies from BGP peers
- `state` (optional): Desired state (present/absent, default: present)

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
```

### graphiant_global_config

Manages Graphiant global configuration objects.

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `config_file` (required): Path to global configuration YAML file
- `operation` (required): Operation to perform
  - `configure`: Configure all global objects
  - `deconfigure`: Deconfigure all global objects
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
```

### graphiant_sites

Manages Graphiant site attachments and detachments.

**Parameters:**
- `host` (required): Graphiant API host URL
- `username` (required): Username for authentication
- `password` (required): Password for authentication
- `site_config_file` (required): Path to site configuration YAML file
- `operation` (required): Operation to perform
  - `configure` or `attach`: Attach global objects to sites
  - `deconfigure` or `detach`: Detach global objects from sites
- `state` (optional): Desired state (present/absent, default: present)

**Example:**
```yaml
- name: Attach global objects to sites
  graphiant.graphiant_playbooks.graphiant_sites:
    host: "https://api.graphiant.com"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    site_config_file: "configs/sample_site_attachments.yaml"
    operation: "attach"
    state: present
```

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

### Option 5: Environment Variables
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
        config_file: "configs/sample_global_prefix_lists.yaml"
        operation: "configure"
        state: present
    
    - name: Configure global BGP filters
      graphiant.graphiant_playbooks.graphiant_global_config:
        <<: *graphiant_client_params
        config_file: "configs/sample_global_bgp_filters.yaml"
        operation: "configure"
        state: present
    
    - name: Configure BGP peering
      graphiant.graphiant_playbooks.graphiant_bgp:
        <<: *graphiant_client_params
        bgp_config_file: "configs/sample_bgp_peering.yaml"
        operation: "configure"
        state: present
    
    - name: Configure interfaces and circuits
      graphiant.graphiant_playbooks.graphiant_interfaces:
        <<: *graphiant_client_params
        interface_config_file: "configs/sample_interface_config.yaml"
        circuit_config_file: "configs/sample_circuit_config.yaml"
        operation: "configure_interfaces"
        state: present
    
    - name: Attach global objects to sites
      graphiant.graphiant_playbooks.graphiant_sites:
        <<: *graphiant_client_params
        site_config_file: "configs/sample_site_attachments.yaml"
        operation: "attach"
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

## Error Handling

The collection provides comprehensive error handling with user-friendly error messages for:
- Configuration errors
- API errors
- Device not found errors
- Authentication errors
- File not found errors

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


