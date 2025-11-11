#!/usr/bin/env python3
"""
Build script for Graphiant Ansible Collection
"""

import os
import shutil
import tarfile
import tempfile
import json
import hashlib
from pathlib import Path


def calculate_file_checksum(file_path):
    """Calculate SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def generate_files_manifest(collection_dir):
    """Generate FILES.json manifest for the collection."""
    files_manifest = {
        "format": 1,
        "files": []
    }

    # Walk through all files in the collection
    for root, dirs, files in os.walk(collection_dir):
        for file in files:
            if file in ['FILES.json', 'MANIFEST.json']:
                continue  # Skip manifest files themselves

            file_path = Path(root) / file
            relative_path = file_path.relative_to(collection_dir)

            # Calculate checksum
            checksum = calculate_file_checksum(file_path)

            files_manifest["files"].append({
                "name": str(relative_path),
                "ftype": "file",
                "chksum_type": "sha256",
                "chksum_sha256": checksum,
                "format": 1
            })

    return files_manifest


def build_collection():
    """Build the Ansible collection."""
    print("🚀 Building Graphiant Ansible Collection")
    print("=" * 50)

    # Get the collection directory
    collection_dir = Path(__file__).parent
    collection_name = "graphiant-graphiant_playbooks-1.0.0"

    # Create build directory
    build_dir = collection_dir.parent.parent.parent / "build"
    build_dir.mkdir(exist_ok=True)

    # Create temporary directory for collection
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_collection_dir = Path(temp_dir) / collection_name
        temp_collection_dir.mkdir()

        # Copy collection files
        print("Copying collection files...")
        for item in collection_dir.iterdir():
            if item.name not in ['build_collection.py', 'test_collection.py', 'validate_collection.py']:
                if item.is_dir():
                    shutil.copytree(item, temp_collection_dir / item.name)
                else:
                    shutil.copy2(item, temp_collection_dir / item.name)

        # Generate FILES.json manifest
        print("Generating FILES.json manifest...")
        files_manifest = generate_files_manifest(temp_collection_dir)
        files_json_path = temp_collection_dir / "FILES.json"
        with open(files_json_path, 'w') as f:
            json.dump(files_manifest, f, indent=2)

        # Update MANIFEST.json with correct checksum
        print("Updating MANIFEST.json...")
        manifest_path = temp_collection_dir / "MANIFEST.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Calculate checksum for FILES.json
        files_checksum = calculate_file_checksum(files_json_path)
        manifest["file_manifest_file"]["chksum_sha256"] = files_checksum

        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Create tar.gz file
        output_file = build_dir / f"{collection_name}.tar.gz"
        print(f"Creating collection archive: {output_file}")

        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(temp_collection_dir, arcname=collection_name)

        print(f"✅ Collection built successfully: {output_file}")
        print(f"📦 Collection size: {output_file.stat().st_size / 1024:.1f} KB")
        print(f"📄 Files included: {len(files_manifest['files'])}")

        return output_file


if __name__ == '__main__':
    build_collection()
