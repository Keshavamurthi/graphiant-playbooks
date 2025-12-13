#!/usr/bin/env python3
"""
Generate requirements.txt from _version.py

This script reads dependency versions from _version.py and generates
requirements.txt to ensure consistency.
"""

import sys
from pathlib import Path

# Get the collection directory (scripts/ is at repo root, collection is in ansible_collections/graphiant/graphiant_playbooks)
script_dir = Path(__file__).parent
repo_root = script_dir.parent
collection_dir = repo_root / "ansible_collections" / "graphiant" / "graphiant_playbooks"

# Import version information from collection directory
sys.path.insert(0, str(collection_dir))
from _version import DEPENDENCIES


def generate_requirements_txt():
    """Generate requirements.txt from _version.py"""
    output_lines = [
        "# Base Packages",
        f"PyYAML=={DEPENDENCIES['PyYAML']}",
        f"Jinja2=={DEPENDENCIES['Jinja2']}",
        f"future=={DEPENDENCIES['future']}",
        f"tabulate=={DEPENDENCIES['tabulate']}",
        "",
        "# Graphiant SDK Package",
        f"graphiant-sdk=={DEPENDENCIES['graphiant-sdk']}",
        "",
        "# Ansible Collection Dependencies",
        f"ansible-core{DEPENDENCIES['ansible-core']}",
        "",
        "# Linter Checks Packages",
        f"flake8=={DEPENDENCIES['flake8']}",
        f"pylint=={DEPENDENCIES['pylint']}",
        f"djlint=={DEPENDENCIES['djlint']}",
        f"ansible-lint{DEPENDENCIES['ansible-lint']}",
        f"pre-commit=={DEPENDENCIES['pre-commit']}",
        "",
        "# Documentation Build Packages (for Ansible collection docsite)",
        f"antsibull-docs{DEPENDENCIES['antsibull-docs']}",
        "ansible-pygments",
        "sphinx",
        f"sphinx-ansible-theme{DEPENDENCIES['sphinx-ansible-theme']}",
        "",
    ]

    # Write requirements.txt to the collection directory
    requirements_file = collection_dir / "requirements.txt"
    with open(requirements_file, 'w') as f:
        f.write('\n'.join(output_lines))

    print("✅ Generated requirements.txt from _version.py")
    print(f"   Location: {requirements_file}")


if __name__ == '__main__':
    generate_requirements_txt()
