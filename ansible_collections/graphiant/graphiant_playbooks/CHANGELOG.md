# Changelog

All notable changes to the Graphiant Playbooks collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-08

### Added
- Initial release of Graphiant Playbooks Ansible Collection
- **Modules:**
  - `graphiant_interfaces` - Manage interfaces and circuits (LAN/WAN)
  - `graphiant_bgp` - Manage BGP peering and routing policies
  - `graphiant_global_config` - Manage global configuration objects
  - `graphiant_sites` - Manage sites and site attachments
  - `graphiant_data_exchange` - Manage Data Exchange workflows
- Self-contained collection with embedded Python libraries
- Sample playbooks and configuration files
- Jinja2 templates for configuration generation
- Comprehensive documentation

### Notes
- Requires ansible-core >= 2.17.0
- Requires Python >= 3.12
- Requires Graphiant SDK >= 25.11.1

## [Unreleased]

### Planned
- Additional modules for advanced features
- Enhanced error handling
- Performance optimizations

## Support

- GitHub Issues: https://github.com/Graphiant-Inc/graphiant-playbooks/issues
- Documentation: https://docs.graphiant.com/
- Email: support@graphiant.com
