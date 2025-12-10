# Contributing to Graphiant Playbooks Collection

Thank you for your interest in contributing!

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/Graphiant-Inc/graphiant-playbooks.git
   cd graphiant-playbooks
   ```
3. **Set up development environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r ansible_collections/graphiant/graphiant_playbooks/requirements.txt
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Validate collection structure:**
   ```bash
   python ansible_collections/graphiant/graphiant_playbooks/validate_collection.py
   ```

3. **Build and install collection:**
   ```bash
   ansible-galaxy collection install ansible_collections/graphiant/graphiant_playbooks/ --force
   ```

4. **Run linting (before commit):**
   ```bash
   # Python linting with flake8
   flake8 ansible_collections/graphiant/graphiant_playbooks/plugins/module_utils/libs

   # Python linting with pylint (errors only)
   export PYTHONPATH=$PYTHONPATH:$(pwd)/ansible_collections/graphiant/graphiant_playbooks/plugins/module_utils/libs
   pylint --errors-only ansible_collections/graphiant/graphiant_playbooks/plugins/module_utils/libs

   # Ansible playbook linting (requires collection to be installed - step 3)
   ansible-lint --config-file ~/.ansible/collections/ansible_collections/graphiant/graphiant_playbooks/.ansible-lint ~/.ansible/collections/ansible_collections/graphiant/graphiant_playbooks/playbooks/

   # YAML/Jinja template linting with djlint
   djlint ansible_collections/graphiant/graphiant_playbooks/configs -e yaml
   djlint ansible_collections/graphiant/graphiant_playbooks/templates -e yaml
   ```

5. **Run test playbook:**
   ```bash
   # Set credentials
   export GRAPHIANT_HOST="https://api.graphiant.com"
   export GRAPHIANT_USERNAME="your_username"
   export GRAPHIANT_PASSWORD="your_password"

   # Optional: Enable pretty output for detailed_logs
   export ANSIBLE_STDOUT_CALLBACK=debug
   
   # Run hello_test.yml to verify collection works
   ansible-playbook ~/.ansible/collections/ansible_collections/graphiant/graphiant_playbooks/playbooks/hello_test.yml
   ```

6. **Commit with clear messages:**
   ```bash
   git commit -m "Add: description of changes"
   ```

7. **Push and create a pull request**

## Linting Tools

The project uses multiple linting tools to ensure code quality:

| Tool | Purpose | Target |
|------|---------|--------|
| `flake8` | Python style guide (PEP 8) | `plugins/module_utils/libs/`, `tests/` |
| `pylint` | Python code analysis | `plugins/module_utils/libs/` |
| `ansible-lint` | Ansible playbook best practices | `playbooks/` |
| `djlint` | Jinja2/YAML template linting | `configs/`, `templates/` |

Configuration files:
- `.ansible-lint` - Ansible lint rules
- `setup.cfg` (root) - flake8/pylint configuration

## Code Standards

### Python Code
- Follow PEP 8 style guidelines
- Include docstrings for functions and classes
- Use type hints where appropriate

### Ansible Modules
- Include `DOCUMENTATION`, `EXAMPLES`, and `RETURN` strings
- Ensure idempotency
- Handle errors gracefully
- Support check mode

### Example Module Structure

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: your_module
short_description: Brief description
description:
  - Detailed description
options:
  option_name:
    description: Option description
    required: true
    type: str
'''

EXAMPLES = r'''
- name: Example task
  graphiant.graphiant_playbooks.your_module:
    option_name: value
'''

RETURN = r'''
result:
  description: Result description
  returned: always
  type: dict
'''

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            option_name=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )
    module.exit_json(changed=False, result={})

if __name__ == '__main__':
    main()
```

## Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] Commit messages are clear

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Graphiant-Inc/graphiant-playbooks/issues)
- **Email**: support@graphiant.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
