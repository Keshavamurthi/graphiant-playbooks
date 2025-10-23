"""
Refactored Edge class for Graphiant Playbooks.

This module provides a clean, maintainable interface for managing
Graphiant network configurations using composition and proper separation of concerns.
"""

from typing import Optional, Dict
from libs.edge_utils import EdgeUtils
from libs.interface_manager import InterfaceManager
from libs.bgp_manager import BGPManager
from libs.global_config_manager import GlobalConfigManager
from libs.site_manager import SiteManager
from libs.logger import setup_logger
from libs.exceptions import GraphiantPlaybookError

LOG = setup_logger()


class Edge:
    """
    Main interface for Graphiant Playbooks.

    This class provides a clean, maintainable interface for managing
    Graphiant network configurations. It uses composition to delegate
    specific responsibilities to specialized manager classes.

    The class follows the Single Responsibility Principle by delegating
    different types of configurations to appropriate managers:
    - InterfaceManager: Interface and circuit configurations
    - BGPManager: BGP peering configurations
    - GlobalConfigManager: Global configuration objects
    - SiteManager: Site management operations
    """

    def __init__(self, base_url: Optional[str] = None, username: Optional[str] = None,
                 password: Optional[str] = None, **kwargs):
        """
        Initialize the Edge class with connection parameters.

        Args:
            base_url: Base URL for the Graphiant API
            username: Username for authentication
            password: Password for authentication
            **kwargs: Additional parameters passed to EdgeUtils
        """
        try:
            # Initialize the base utilities
            self.edge_utils = EdgeUtils(
                base_url=base_url,
                username=username,
                password=password,
                **kwargs
            )

            # Initialize specialized managers
            self.interfaces = InterfaceManager(self.edge_utils)
            self.bgp = BGPManager(self.edge_utils)
            self.global_config = GlobalConfigManager(self.edge_utils)
            self.sites = SiteManager(self.edge_utils)

            LOG.info("Edge class initialized successfully with all managers")

        except Exception as e:
            LOG.error(f"Failed to initialize Edge class: {str(e)}")
            raise GraphiantPlaybookError(f"Edge initialization failed: {str(e)}")

    def get_manager_status(self) -> Dict[str, bool]:
        """
        Get the status of all managers.

        Returns:
            Dictionary indicating which managers are properly initialized
        """
        return {
            'interfaces': hasattr(self, 'interfaces') and self.interfaces is not None,
            'bgp': hasattr(self, 'bgp') and self.bgp is not None,
            'global_config': hasattr(self, 'global_config') and self.global_config is not None,
            'sites': hasattr(self, 'sites') and self.sites is not None,
            'edge_utils': hasattr(self, 'edge_utils') and self.edge_utils is not None
        }
