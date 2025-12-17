# Credential Management Guide

This guide covers various approaches for managing Graphiant credentials in Ansible playbooks.

## Recommended: YAML Anchors

Use YAML anchors to define credentials once and reuse them:

```yaml
---
- name: Graphiant Configuration
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
      graphiant.naas.graphiant_interfaces:
        <<: *graphiant_client_params
        interface_config_file: "interface_config.yaml"
        operation: "configure_lan_interfaces"
    
    - name: Configure BGP
      graphiant.naas.graphiant_bgp:
        <<: *graphiant_client_params
        bgp_config_file: "bgp_config.yaml"
        operation: "configure"
```

## Other Options

### Environment Variables

```bash
export GRAPHIANT_HOST="https://api.graphiant.com"
export GRAPHIANT_USERNAME="myuser"
export GRAPHIANT_PASSWORD="mypass"
```

```yaml
vars:
  graphiant_host: "{{ ansible_env.GRAPHIANT_HOST }}"
  graphiant_username: "{{ ansible_env.GRAPHIANT_USERNAME }}"
  graphiant_password: "{{ ansible_env.GRAPHIANT_PASSWORD }}"
```

### Variable Files

```yaml
# vars/credentials.yml
graphiant_host: "https://api.graphiant.com"
graphiant_username: "{{ vault_graphiant_username }}"
graphiant_password: "{{ vault_graphiant_password }}"
```

```yaml
# playbook.yml
- name: Configuration
  hosts: localhost
  vars_files:
    - vars/credentials.yml
```

### Runtime Variables

```bash
ansible-playbook playbook.yml -e "graphiant_username=user" -e "graphiant_password=pass"
ansible-playbook playbook.yml -e "@vars/credentials.yml"
```

## Security Best Practices

### Ansible Vault

Encrypt sensitive credentials:

```bash
# Create encrypted file
ansible-vault create vars/secrets.yml

# Run with vault
ansible-playbook playbook.yml --ask-vault-pass
```

### Recommendations

1. **Never commit plaintext passwords** to version control
2. **Use Ansible Vault** for sensitive data
3. **Use service accounts** with minimal permissions
4. **Environment-specific credentials** for different environments

## Additional Resources

- [Ansible Vault Documentation](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [Ansible Variable Precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)
