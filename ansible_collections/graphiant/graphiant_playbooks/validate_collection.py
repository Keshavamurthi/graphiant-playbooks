#!/usr/bin/env python3
"""
Simple validation script for Graphiant Ansible Collection
"""

import sys
import os


def main():
    print("🚀 Validating Graphiant Ansible Collection Structure")
    print("=" * 60)

    # Check collection structure
    required_files = [
        'meta/galaxy.yml',
        'meta/runtime.yml',
        'plugins/modules/graphiant_interfaces.py',
        'plugins/modules/graphiant_bgp.py',
        'plugins/modules/graphiant_global_config.py',
        'plugins/modules/graphiant_sites.py',
        'plugins/module_utils/graphiant_utils.py',
        'README.md'
    ]

    required_dirs = [
        'meta',
        'plugins',
        'plugins/modules',
        'plugins/module_utils',
        'playbooks'
    ]

    base_path = os.path.dirname(__file__)

    print("Checking required directories...")
    for dir_path in required_dirs:
        full_path = os.path.join(base_path, dir_path)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")
            return 1

    print("\nChecking required files...")
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            return 1

    print("\nChecking playbook files...")
    playbooks_dir = os.path.join(base_path, 'playbooks')
    if os.path.exists(playbooks_dir):
        playbooks = [f for f in os.listdir(playbooks_dir) if f.endswith('.yml')]
        for playbook in playbooks:
            print(f"✅ playbooks/{playbook}")

    print("\n" + "=" * 60)
    print("🎉 Collection structure validation passed!")
    print("\nCollection is ready for:")
    print("- Building with: ansible-galaxy collection build")
    print("- Testing with: ansible-playbook --check")
    print("- Publishing to Ansible Galaxy")

    return 0


if __name__ == '__main__':
    sys.exit(main())
