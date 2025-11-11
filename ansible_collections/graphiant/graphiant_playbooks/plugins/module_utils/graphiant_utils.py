#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Graphiant Ansible Collection - Module Utilities

This module provides common utilities for Graphiant Ansible modules.
"""

import sys
import os
from typing import Dict, Any


def _find_project_directory(directory_name: str) -> str:
    """
    Find a specific directory in the project structure using a systematic approach.

    This method uses a systematic approach to locate any directory with the following priority:
    1. Check user-configured GRAPHIANT_PLAYBOOKS_PATH environment variable (highest priority)
    2. Check PYTHONPATH for graphiant-playbooks directory
    3. Check current working directory
    4. Find Git repository root and look for the directory there
    5. Walk up from the current file location to find the directory (fallback)

    Args:
        directory_name: Name of the directory to find (e.g., 'libs', 'configs', 'templates')

    Returns:
        str: Path to the directory, or None if not found
    """
    # Method 1: Check user-configured GRAPHIANT_PLAYBOOKS_PATH environment variable (highest priority)
    # This allows users to specify the path to their graphiant-playbooks directory
    user_playbooks_path = os.environ.get('GRAPHIANT_PLAYBOOKS_PATH')
    if user_playbooks_path and os.path.exists(user_playbooks_path):
        target_path = os.path.join(user_playbooks_path, directory_name)
        if os.path.exists(target_path):
            return target_path

    # Method 2: Check PYTHONPATH for graphiant-playbooks directory
    pythonpath = os.environ.get('PYTHONPATH', '')
    for path in pythonpath.split(os.pathsep):
        if path and os.path.exists(path):
            # Check if this path contains the graphiant-playbooks directory
            if 'graphiant-playbooks' in path:
                target_path = os.path.join(path, directory_name)
                if os.path.exists(target_path):
                    return target_path
            # Also check if the directory exists directly in this path
            target_path = os.path.join(path, directory_name)
            if os.path.exists(target_path):
                return target_path

    # Method 3: Check current working directory
    target_path = os.path.join(os.getcwd(), directory_name)
    if os.path.exists(target_path):
        return target_path

    # Method 4: Find Git repository root and look for the directory there
    current_dir = os.path.dirname(__file__)
    for _ in range(10):  # Walk up to 10 levels
        git_path = os.path.join(current_dir, '.git')
        if os.path.exists(git_path):
            target_path = os.path.join(current_dir, directory_name)
            if os.path.exists(target_path):
                return target_path
        current_dir = os.path.dirname(current_dir)

    # Method 5: Walk up from the current file location (fallback)
    current_dir = os.path.dirname(__file__)
    for _ in range(10):  # Walk up to 10 levels
        target_path = os.path.join(current_dir, directory_name)
        if os.path.exists(target_path):
            return target_path
        current_dir = os.path.dirname(current_dir)

    return None


def _find_libs_directory() -> str:
    """
    Find the libs directory by looking for it in the project structure.

    Returns:
        str: Path to the libs directory, or None if not found
    """
    return _find_project_directory('libs')


def _find_configs_directory() -> str:
    """
    Find the configs directory by looking for it in the project structure.

    Returns:
        str: Path to the configs directory, or None if not found
    """
    return _find_project_directory('configs')


def _import_graphiant_libs():
    """
    Import Graphiant library modules with robust path resolution.

    Returns:
        tuple: (GraphiantConfig, GraphiantPlaybookError, ConfigurationError, APIError, DeviceNotFoundError)
    """
    # Find the libs directory
    libs_path = _find_libs_directory()

    if libs_path:
        # Add libs directory to Python path
        sys.path.insert(0, libs_path)
        try:
            from libs.graphiant_config import GraphiantConfig
            from libs.exceptions import GraphiantPlaybookError, ConfigurationError, APIError, DeviceNotFoundError
            return GraphiantConfig, GraphiantPlaybookError, ConfigurationError, APIError, DeviceNotFoundError
        except ImportError:
            # Remove the path we just added to avoid conflicts
            if libs_path in sys.path:
                sys.path.remove(libs_path)

    # Fallback: Try direct imports (for when libs is in current directory)
    try:
        from graphiant_config import GraphiantConfig
        from exceptions import GraphiantPlaybookError, ConfigurationError, APIError, DeviceNotFoundError
        return GraphiantConfig, GraphiantPlaybookError, ConfigurationError, APIError, DeviceNotFoundError
    except ImportError:
        pass

    # Final fallback: Create mock classes for testing/development
    class MockGraphiantConfig:
        def __init__(self, *args, **kwargs):
            raise ImportError("Graphiant SDK not available. Please install graphiant-sdk package.")

    class MockException(Exception):
        pass

    return MockGraphiantConfig, MockException, MockException, MockException, MockException


# Import the Graphiant library modules
GraphiantConfig, GraphiantPlaybookError, ConfigurationError, APIError, DeviceNotFoundError = _import_graphiant_libs()


class GraphiantConnection:
    """
    Manages connection to Graphiant API and provides common functionality.
    """

    def __init__(self, host: str, username: str, password: str):
        """
        Initialize Graphiant connection.

        Args:
            host: Graphiant API host URL
            username: Username for authentication
            password: Password for authentication
        """
        self.host = host
        self.username = username
        self.password = password
        self._graphiant_config = None

    @property
    def graphiant_config(self) -> GraphiantConfig:
        """
        Get or create GraphiantConfig instance.

        Returns:
            GraphiantConfig: Graphiant configuration instance
        """
        if self._graphiant_config is None:
            try:
                self._graphiant_config = GraphiantConfig(
                    base_url=self.host,
                    username=self.username,
                    password=self.password
                )
            except Exception as e:
                raise GraphiantPlaybookError(f"Failed to initialize Graphiant connection: {str(e)}")

        return self._graphiant_config

    def test_connection(self) -> bool:
        """
        Test the connection to Graphiant API.

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            # Try to get manager status to test connection
            status = self.graphiant_config.get_manager_status()
            return all(status.values())
        except Exception:
            return False


def get_graphiant_connection(module_params: Dict[str, Any]) -> GraphiantConnection:
    """
    Create and return a Graphiant connection from module parameters.

    Args:
        module_params: Ansible module parameters

    Returns:
        GraphiantConnection: Initialized connection object
    """
    required_params = ['host', 'username', 'password']
    for param in required_params:
        if param not in module_params:
            raise ValueError(f"Missing required parameter: {param}")

    return GraphiantConnection(
        host=module_params['host'],
        username=module_params['username'],
        password=module_params['password']
    )


def handle_graphiant_exception(exception: Exception, operation: str) -> str:
    """
    Handle Graphiant exceptions and return user-friendly error messages.

    Args:
        exception: The exception that occurred
        operation: Description of the operation that failed

    Returns:
        str: User-friendly error message
    """
    if isinstance(exception, ConfigurationError):
        return f"Configuration error during {operation}: {str(exception)}"
    elif isinstance(exception, APIError):
        return f"API error during {operation}: {str(exception)}"
    elif isinstance(exception, DeviceNotFoundError):
        return f"Device not found during {operation}: {str(exception)}"
    elif isinstance(exception, GraphiantPlaybookError):
        return f"Graphiant playbook error during {operation}: {str(exception)}"
    else:
        return f"Unexpected error during {operation}: {str(exception)}"


def validate_config_file(config_file: str) -> bool:
    """
    Validate that a configuration file exists and is readable.

    This function handles the Graphiant library's path resolution logic:
    - If config_file is an absolute path, check if it exists
    - If config_file is a relative path, check if it exists in the project's configs directory

    Args:
        config_file: Path to the configuration file

    Returns:
        bool: True if file is valid, False otherwise
    """
    # If it's an absolute path, check directly
    if os.path.isabs(config_file):
        return os.path.exists(config_file) and os.access(config_file, os.R_OK)

    # If it's a relative path, check in the project's configs directory
    configs_path = _find_configs_directory()
    if configs_path:
        full_path = os.path.join(configs_path, config_file)
        if os.path.exists(full_path) and os.access(full_path, os.R_OK):
            return True

    # Fallback: Check relative to current working directory (for backward compatibility)
    if os.path.exists(config_file) and os.access(config_file, os.R_OK):
        return True

    return False
