# Graphiant Playbooks

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Ansible](https://img.shields.io/badge/ansible--core-2.17+-green.svg)](https://docs.ansible.com/)

Automated network infrastructure management for Graphiant NaaS (Network as a Service).

## Components

| Component | Description | Documentation |
|-----------|-------------|---------------|
| **Ansible Collection** | Ansible modules for Graphiant NaaS automation | [📖 Documentation](ansible_collections/graphiant/graphiant_playbooks/README.md) |
| **Terraform Modules** | Infrastructure as Code for cloud connectivity | [📖 Documentation](terraform/README.md) |
| **CI/CD Pipelines** | Automation pipelines | [📖 Documentation](pipelines/README.md) |
| **Cloud-Init Generator** | Device onboarding scripts | [📖 Documentation](scripts/cloud-init-generator/README.md) |
| **Docker Support** | Containerized execution | [📖 Documentation](Docker.md) |

## Quick Start

### Ansible Collection (Recommended)

```bash
# Clone the repo and install dependencies in a virtual env

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r ansible_collections/graphiant/graphiant_playbooks/requirements.txt

# Install collection from source
ansible-galaxy collection install ansible_collections/graphiant/graphiant_playbooks/ --force

# Or Install collection from Ansible Galaxy
ansible-galaxy collection install graphiant.graphiant_playbooks

# Use in playbooks
```

```yaml
- name: Configure Graphiant interfaces
  graphiant.graphiant_playbooks.graphiant_interfaces:
    host: "{{ graphiant_host }}"
    username: "{{ graphiant_username }}"
    password: "{{ graphiant_password }}"
    interface_config_file: "interface_config.yaml"
    operation: "configure_lan_interfaces"
```

**See the [Ansible Collection README](ansible_collections/graphiant/graphiant_playbooks/README.md) for complete documentation.**

### Python Library

The collection can also be used as a Python library:

```bash
# Set PYTHONPATH for direct Python usage
export PYTHONPATH=$(pwd)/ansible_collections/graphiant/graphiant_playbooks/plugins/module_utils:$PYTHONPATH
```

```python
from libs.graphiant_config import GraphiantConfig

config = GraphiantConfig(
    base_url="https://api.graphiant.com",
    username="user",
    password="pass"
)
config.interfaces.configure_lan_interfaces("interface_config.yaml")
```

## Project Structure

```
graphiant-playbooks/
├── ansible_collections/graphiant/graphiant_playbooks/  # Ansible collection
├── terraform/                                          # Terraform modules
├── pipelines/                                          # CI/CD pipelines
├── scripts/                                            # Utility scripts
└── README.md                                           # This file
```

## Support

- **Documentation**: See component-specific README files above
- **Issues**: [GitHub Issues](https://github.com/Graphiant-Inc/graphiant-playbooks/issues)
- **Email**: [support@graphiant.com](mailto:support@graphiant.com)

## License

MIT License - see [LICENSE](LICENSE) for details.
