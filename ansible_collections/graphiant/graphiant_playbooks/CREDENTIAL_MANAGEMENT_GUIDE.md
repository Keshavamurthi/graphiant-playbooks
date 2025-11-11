# Graphiant Ansible Collection - Credential Management Guide

This guide demonstrates various approaches for managing Graphiant credentials in Ansible playbooks, from simple to enterprise-grade solutions.

## 🎯 Recommended Approach: YAML Anchors

**Best Practice**: Use YAML anchors to avoid repetition and keep playbooks clean and maintainable.

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

## 🔐 Credential Management Options

### Option 1: Inventory Variables
Store credentials in inventory files for different environments.

**File**: `inventory/production.yml`
```yaml
[graphiant_prod:vars]
graphiant_host = "https://api.graphiant.com"
graphiant_username = "{{ vault_prod_graphiant_username }}"
graphiant_password = "{{ vault_prod_graphiant_password }}"
```

**Usage**:
```bash
ansible-playbook -i inventory/production.yml playbook.yml
```

### Option 2: Variable Files
Use external variable files for credential management.

**File**: `vars/credentials.yml`
```yaml
graphiant_host: "https://api.graphiant.com"
graphiant_username: "{{ vault_graphiant_username }}"
graphiant_password: "{{ vault_graphiant_password }}"
```

**Playbook**:
```yaml
---
- name: Graphiant Configuration
  hosts: localhost
  vars_files:
    - vars/credentials.yml
  vars:
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  tasks:
    - name: Configure interfaces
      graphiant.graphiant_playbooks.graphiant_interfaces:
        <<: *graphiant_client_params
        interface_config_file: "configs/sample_interface_config.yaml"
        operation: "configure_interfaces"
        state: present
```

### Option 3: Runtime Variables
Pass credentials at runtime using `--extra-vars`.

**Key-value format**:
```bash
ansible-playbook playbook.yml \
  -e "graphiant_username=myuser" \
  -e "graphiant_password=mypass"
```

**JSON format**:
```bash
ansible-playbook playbook.yml \
  -e '{"graphiant_username":"myuser","graphiant_password":"mypass"}'
```

**YAML file format**:
```bash
ansible-playbook playbook.yml -e "@vars/credentials.yml"
```

### Option 4: Environment Variables
Use environment variables for CI/CD pipelines.

**Set environment variables**:
```bash
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="myuser"
export GRAPHIANT_PASSWORD="mypass"
```

**Playbook**:
```yaml
---
- name: Graphiant Configuration
  hosts: localhost
  vars:
    graphiant_host: "{{ ansible_env.GRAPHIANT_HOST }}"
    graphiant_username: "{{ ansible_env.GRAPHIANT_USERNAME }}"
    graphiant_password: "{{ ansible_env.GRAPHIANT_PASSWORD }}"
    
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  tasks:
    - name: Configure BGP peering
      graphiant.graphiant_playbooks.graphiant_bgp:
        <<: *graphiant_client_params
        bgp_config_file: "configs/sample_bgp_peering.yaml"
        operation: "configure"
        state: present
```

## 🔒 Security Best Practices

### 1. Ansible Vault
Encrypt sensitive credentials using Ansible Vault.

**Create encrypted file**:
```bash
ansible-vault create vars/credentials.yml
```

**Edit encrypted file**:
```bash
ansible-vault edit vars/credentials.yml
```

**Run playbook with vault**:
```bash
ansible-playbook playbook.yml --ask-vault-pass
```

**Or use vault password file**:
```bash
ansible-playbook playbook.yml --vault-password-file .vault_pass
```

### 2. Environment-Specific Credentials
Use different credentials for different environments.

**File**: `vars/production.yml`
```yaml
graphiant_host: "https://api.graphiant.com"
graphiant_username: "{{ vault_prod_username }}"
graphiant_password: "{{ vault_prod_password }}"
```

**File**: `vars/development.yml`
```yaml
graphiant_host: "https://api-dev.graphiant.com"
graphiant_username: "{{ vault_dev_username }}"
graphiant_password: "{{ vault_dev_password }}"
```

### 3. Service Accounts
Create dedicated service accounts for automation with minimal required permissions.

### 4. Never Commit Plaintext Passwords
Always use encrypted files or environment variables for sensitive data.

## 📁 Example File Structure

```
project/
├── inventory/
│   ├── production.yml
│   ├── development.yml
│   └── staging.yml
├── vars/
│   ├── credentials.yml          # Encrypted with ansible-vault
│   ├── production.yml
│   ├── development.yml
│   └── staging.yml
├── playbooks/
│   ├── complete_network_setup.yml
│   ├── circuit_management.yml
│   └── interface_management.yml
└── configs/
    ├── sample_interface_config.yaml
    ├── sample_circuit_config.yaml
    └── sample_bgp_peering.yaml
```

## 🚀 Quick Start Examples

### Basic Setup with YAML Anchors
```yaml
---
- name: Basic Graphiant Configuration
  hosts: localhost
  gather_facts: false
  vars:
    graphiant_host: "https://api.graphiant.com"
    graphiant_username: "{{ vault_graphiant_username }}"
    graphiant_password: "{{ vault_graphiant_password }}"
    
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  
  tasks:
    - name: Configure interfaces
      graphiant.graphiant_playbooks.graphiant_interfaces:
        <<: *graphiant_client_params
        interface_config_file: "configs/sample_interface_config.yaml"
        operation: "configure_interfaces"
        state: present
```

### CI/CD Pipeline Example
```yaml
---
- name: CI/CD Graphiant Configuration
  hosts: localhost
  gather_facts: false
  vars:
    graphiant_host: "{{ ansible_env.GRAPHIANT_HOST }}"
    graphiant_username: "{{ ansible_env.GRAPHIANT_USERNAME }}"
    graphiant_password: "{{ ansible_env.GRAPHIANT_PASSWORD }}"
    
    graphiant_client_params: &graphiant_client_params
      host: "{{ graphiant_host }}"
      username: "{{ graphiant_username }}"
      password: "{{ graphiant_password }}"
  
  tasks:
    - name: Deploy network configuration
      graphiant.graphiant_playbooks.graphiant_global_config:
        <<: *graphiant_client_params
        config_file: "configs/{{ environment }}/global_config.yaml"
        operation: "configure"
        state: present
```

## 📚 Additional Resources

- [Ansible Variable Precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence)
- [Ansible Vault Documentation](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [YAML Anchors and Aliases](https://yaml.org/spec/1.2/spec.html#id2765878)

## 🎉 Benefits of This Approach

1. **DRY Principle**: Don't Repeat Yourself - credentials defined once
2. **Maintainability**: Easy to update credentials in one place
3. **Security**: Support for encrypted credential storage
4. **Flexibility**: Multiple credential management options
5. **CI/CD Ready**: Environment variable support for automation
6. **Clean Code**: Readable and maintainable playbooks
