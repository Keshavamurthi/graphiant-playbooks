# Documentation for Graphiant Playbooks Ansible Collection

This directory contains documentation and docsite configuration for the Graphiant Playbooks Ansible Collection.

## Directory Structure

```
docs/
├── README.md              # This file
├── DOCSITE_SETUP.md       # Comprehensive setup guide
├── QUICK_START.md         # Quick reference guide
├── build_docsite.sh       # Custom automated build script
├── build.sh               # Auto-generated build script (from sphinx-init)
├── conf.py                # Sphinx configuration (auto-generated)
├── requirements.txt      # Python dependencies (auto-generated)
├── antsibull-docs.cfg     # antsibull-docs configuration (auto-generated)
├── rst/                   # Generated RST files (auto-generated)
│   ├── index.rst
│   └── *_module.rst
└── build/                 # Built HTML files (after Sphinx build)
    └── html/              # Final HTML documentation
```

## Quick Start

### Using the Build Script (Recommended)

```bash
# From collection root
cd ansible_collections/graphiant/graphiant_playbooks
./docs/build_docsite.sh
```

### Manual Build

See [QUICK_START.md](QUICK_START.md) for step-by-step instructions.

## Documentation Files

- **DOCSITE_SETUP.md**: Comprehensive guide with all options and troubleshooting
- **QUICK_START.md**: Quick reference for common tasks
- **build_docsite.sh**: Automated build script

## Building the Docusite

The docsite is built in two steps:

1. **Generate RST files** using `antsibull-docs collection`
   - Extracts documentation from module `DOCUMENTATION` strings
   - Creates RST files for Sphinx

2. **Build HTML** using `sphinx-build`
   - Converts RST files to HTML
   - Creates a navigable documentation site

## Publishing

See [DOCSITE_SETUP.md](DOCSITE_SETUP.md) for publishing options:
- GitHub Pages
- Your existing documentation site
- Other hosting options

## Validation

Before building, validate your documentation:

```bash
cd ansible_collections/graphiant/graphiant_playbooks
antsibull-docs lint-collection-docs --plugin-docs --skip-rstcheck --validate-collection-refs=self .
```

## Resources

- [antsibull-docs Documentation](https://ansible.readthedocs.io/projects/antsibull-docs/collection-docs/)
- [Ansible Collection Development Guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)

