"""
Base manager class for Graphiant Playbooks.

This module provides a base class that contains common functionality
for all configuration managers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from libs.edge_utils import EdgeUtils
from libs.logger import setup_logger
from libs.exceptions import ConfigurationError, APIError, DeviceNotFoundError, SiteNotFoundError

LOG = setup_logger()


class BaseManager(ABC):
    """
    Base class for all configuration managers.

    Provides common functionality for configuration processing,
    template rendering, and API communication.
    """

    def __init__(self, edge_utils: EdgeUtils):
        """
        Initialize the base manager.

        Args:
            edge_utils: Instance of EdgeUtils containing common utilities
        """
        self.edge_utils = edge_utils
        self.gsdk = edge_utils.gsdk
        self.template = edge_utils.template

    @abstractmethod
    def configure(self, config_yaml_file: str) -> None:
        """
        Configure resources based on the provided YAML file.

        Args:
            config_yaml_file: Path to the YAML configuration file
        """
        pass

    @abstractmethod
    def deconfigure(self, config_yaml_file: str) -> None:
        """
        Deconfigure resources based on the provided YAML file.

        Args:
            config_yaml_file: Path to the YAML configuration file
        """
        pass

    def render_config_file(self, yaml_file: str) -> Dict[str, Any]:
        """
        Load and parse a YAML configuration file.

        Args:
            yaml_file: Path to the YAML configuration file

        Returns:
            Parsed configuration data

        Raises:
            ConfigurationError: If the file cannot be loaded or parsed
        """
        try:
            config_data = self.edge_utils.render_config_file(yaml_file)
            if config_data is None:
                raise ConfigurationError(f"Failed to load configuration file: {yaml_file}")
            return config_data
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration file {yaml_file}: {str(e)}")

    def execute_concurrent_tasks(self, function, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function concurrently for each item in the config dictionary.

        Args:
            function: The function to execute
            config_dict: Dictionary with configuration data

        Returns:
            Dictionary with execution results
        """
        try:
            return self.edge_utils.concurrent_task_execution(function, config_dict)
        except Exception as e:
            raise APIError(f"Error executing concurrent tasks: {str(e)}")

    def get_device_id(self, device_name: str) -> Optional[int]:
        """
        Get device ID by device name.

        Args:
            device_name: Name of the device

        Returns:
            Device ID if found, None otherwise

        Raises:
            DeviceNotFoundError: If device cannot be found
        """
        device_id = self.edge_utils.get_device_id(device_name)
        if not device_id:
            raise DeviceNotFoundError(f"Device '{device_name}' not found")
        return device_id

    def get_site_id(self, site_name: str) -> Optional[int]:
        """
        Get site ID by site name.

        Args:
            site_name: Name of the site

        Returns:
            Site ID if found, None otherwise

        Raises:
            SiteNotFoundError: If site cannot be found
        """
        site_id = self.edge_utils.get_site_id(site_name)
        if not site_id:
            raise SiteNotFoundError(f"Site '{site_name}' not found")
        return site_id
