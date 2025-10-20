"""
Data Exchange Manager for Graphiant Playbooks

This module provides functionality for managing Data Exchange workflows including:
- Create New Services
- Create New Customers
- Match Services to Customers
"""

import os
from typing import Dict, Any, Optional
from libs.base_manager import BaseManager
from libs.logger import setup_logger
from libs.exceptions import ConfigurationError

from tabulate import tabulate

LOG = setup_logger()


class DataExchangeManager(BaseManager):
    """
    Manager for Data Exchange workflows and operations.
    """

    def configure(self, config_yaml_file: str) -> None:
        """
        Configure Data Exchange resources based on the provided YAML file.
        This is the main entry point for Data Exchange configuration.

        Args:
            config_yaml_file: Path to the YAML configuration file
        """
        LOG.info(f"Configuring Data Exchange resources from {config_yaml_file}")

        # Create services first
        self.create_services(config_yaml_file)

        # Create customers
        self.create_customers(config_yaml_file)

        # Match services to customers
        self.match_service_to_customers(config_yaml_file)

        LOG.info("Data Exchange configuration completed successfully")

    def deconfigure(self, config_yaml_file: str) -> None:
        """
        Deconfigure Data Exchange resources based on the provided YAML file.
        This is the main entry point for Data Exchange deconfiguration.

        Args:
            config_yaml_file: Path to the YAML configuration file
        """
        LOG.info(f"Deconfiguring Data Exchange resources from {config_yaml_file}")

        # Delete customers first (they depend on services)
        self.delete_customers(config_yaml_file)

        # Delete services
        self.delete_services(config_yaml_file)

        LOG.info("Data Exchange deconfiguration completed successfully")

    def create_services(self, config_yaml_file: str) -> None:
        """
        Create new Data Exchange services from YAML configuration.

        Args:
            config_yaml_file (str): Path to the YAML configuration file
        """
        try:
            LOG.info(f"Creating Data Exchange service from {config_yaml_file}")
            config_data = self.render_config_file(config_yaml_file)

            if not config_data or 'data_exchange_services' not in config_data:
                LOG.info("No data_exchange_services configuration found in YAML file")
                return

            services = config_data['data_exchange_services']
            if not isinstance(services, list):
                raise ConfigurationError("Configuration error: 'data_exchange_services' must be a list.")

            created_count = 0
            skipped_count = 0

            for service_config in services:
                service_name = service_config.get('serviceName')
                if not service_name:
                    raise ConfigurationError("Configuration error: Each service must have a 'serviceName' field.")

                # Check if service already exists
                existing_service = self.gsdk.get_data_exchange_service_by_name(service_name)
                if existing_service:
                    LOG.info(f"Service '{service_name}' already exists (ID: {existing_service.id}), skipping creation")
                    skipped_count += 1
                    continue

                # Resolve LAN segment ID if provided by name
                if 'policy' in service_config and 'serviceLanSegment' in service_config['policy']:
                    lan_segment_name = service_config['policy']['serviceLanSegment']
                    if isinstance(lan_segment_name, str):
                        lan_segment_id = self.gsdk.get_lan_segment_id(lan_segment_name)
                        if lan_segment_id:
                            service_config['policy']['serviceLanSegment'] = lan_segment_id
                        else:
                            raise ConfigurationError(
                                f"LAN segment '{lan_segment_name}' not found for service '{service_name}'.")

                # Resolve site IDs if provided by names
                if 'policy' in service_config and 'site' in service_config['policy']:
                    self._resolve_site_ids(service_config['policy'], service_name)

                # Create service directly
                LOG.info(f"Service configuration: {service_config}")
                LOG.info(f"create_data_exchange_services: Creating service '{service_name}'")
                self.gsdk.create_data_exchange_services(service_config)
                LOG.info(f"Successfully created service '{service_name}'")
                created_count += 1

            LOG.info(f"Data Exchange service creation completed: {created_count} created, {skipped_count} skipped")

        except ConfigurationError:
            raise
        except Exception as e:
            LOG.error(f"Failed to create Data Exchange service: {e}")
            raise ConfigurationError(f"Data Exchange service creation failed: {e}")

    def _resolve_site_ids(self, policy_config: dict, service_name: str) -> None:
        """
        Resolve site names to site IDs in the policy configuration.

        Args:
            policy_config (dict): Policy configuration to update
            service_name (str): Service name for error reporting
        """
        if 'site' in policy_config and isinstance(policy_config['site'], list):
            for site_entry in policy_config['site']:
                if 'sites' in site_entry and isinstance(site_entry['sites'], list):
                    resolved_site_ids = []
                    for site_name in site_entry['sites']:
                        if isinstance(site_name, str):
                            site_id = self.gsdk.get_site_id(site_name)
                            if site_id:
                                resolved_site_ids.append(site_id)
                            else:
                                raise ConfigurationError(f"Site '{site_name}' not found for service '{service_name}'.")
                        else:
                            resolved_site_ids.append(site_name)  # Already an ID
                    site_entry['sites'] = resolved_site_ids

    def get_services_summary(self) -> Dict[str, Any]:
        """
        Get summary of all Data Exchange services.

        Returns:
            dict: Services summary response
        """
        try:
            LOG.info("Retrieving Data Exchange services summary")
            response = self.gsdk.get_data_exchange_services_summary()

            # Display services in a nice table format
            if response.info:
                service_table = []
                for service in response.info:
                    service_table.append([
                        service.name,
                        service.status,
                        service.id
                    ])

                LOG.info(
                    f"Services Summary:\n"
                    f"{tabulate(service_table, headers=['Service Name', 'Status', 'ID'], tablefmt='grid')}")

            return response.to_dict()
        except Exception as e:
            LOG.error(f"Failed to retrieve services summary: {e}")
            raise ConfigurationError(f"Failed to retrieve services summary: {e}")

    def get_service_by_name(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific Data Exchange service by name.

        Args:
            service_name (str): Name of the service to retrieve

        Returns:
            dict or None: Service details if found, None otherwise
        """
        try:
            LOG.info(f"Retrieving Data Exchange service '{service_name}'")
            service = self.gsdk.get_data_exchange_service_by_name(service_name)
            return service
        except Exception as e:
            LOG.error(f"Failed to retrieve service '{service_name}': {e}")
            raise ConfigurationError(f"Failed to retrieve service '{service_name}': {e}")

    def create_customers(self, config_yaml_file: str) -> None:
        """
        Create a new Data Exchange customer from YAML configuration.

        Args:
            config_yaml_file (str): Path to the YAML configuration file
        """
        try:
            LOG.info(f"Creating Data Exchange customer from {config_yaml_file}")
            config_data = self.render_config_file(config_yaml_file)

            if not config_data or 'data_exchange_customers' not in config_data:
                LOG.info("No data_exchange_customers configuration found in YAML file")
                return

            customers = config_data['data_exchange_customers']
            if not isinstance(customers, list):
                raise ConfigurationError("Configuration error: 'data_exchange_customers' must be a list.")

            created_count = 0
            skipped_count = 0

            for customer_config in customers:
                customer_name = customer_config.get('name')
                if not customer_name:
                    raise ConfigurationError("Configuration error: Each customer must have a 'name' field.")

                # Check if customer already exists
                existing_customer = self.gsdk.get_data_exchange_customer_by_name(customer_name)
                if existing_customer:
                    LOG.info(f"Customer '{customer_name}' already exists "
                             f"(ID: {existing_customer.id}), skipping creation")
                    skipped_count += 1
                    continue

                # Create customer directly
                LOG.info(f"Customer configuration: {customer_config}")
                LOG.info(f"create_data_exchange_customers: Creating customer '{customer_name}'")
                self.gsdk.create_data_exchange_customers(customer_config)
                LOG.info(f"Successfully created customer '{customer_name}'")
                created_count += 1

            LOG.info(f"Data Exchange customer creation completed: {created_count} created, {skipped_count} skipped")

        except ConfigurationError:
            raise
        except Exception as e:
            LOG.error(f"Failed to create Data Exchange customer: {e}")
            raise ConfigurationError(f"Data Exchange customer creation failed: {e}")

    def get_customers_summary(self) -> Dict[str, Any]:
        """
        Get summary of all Data Exchange customers.

        Returns:
            dict: Customers summary response
        """
        try:
            LOG.info("Retrieving Data Exchange customers summary")
            response = self.gsdk.get_data_exchange_customers_summary()

            # Display customers in a nice table format
            if response.customers:
                customer_table = []
                for customer in response.customers:
                    customer_table.append([
                        customer.name,
                        customer.type,
                        customer.status,
                        customer.id
                    ])

                LOG.info(f"Customers Summary:\n"
                         f"{tabulate(customer_table, headers=['Name', 'Type', 'Status', 'ID'], tablefmt='grid')}")

            return response.to_dict()
        except Exception as e:
            LOG.error(f"Failed to retrieve customers summary: {e}")
            raise ConfigurationError(f"Failed to retrieve customers summary: {e}")

    def get_customer_by_name(self, customer_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific Data Exchange customer by name.

        Args:
            customer_name (str): Name of the customer to retrieve

        Returns:
            dict or None: Customer details if found, None otherwise
        """
        try:
            LOG.info(f"Retrieving Data Exchange customer '{customer_name}'")
            customer = self.gsdk.get_data_exchange_customer_by_name(customer_name)
            return customer
        except Exception as e:
            LOG.error(f"Failed to retrieve customer '{customer_name}': {e}")
            raise ConfigurationError(f"Failed to retrieve customer '{customer_name}': {e}")

    def delete_customers(self, config_yaml_file: str) -> None:
        """
        Delete Data Exchange customers from YAML configuration.

        Args:
            config_yaml_file (str): Path to the YAML configuration file
        """
        try:
            LOG.info(f"Deleting Data Exchange customers from {config_yaml_file}")
            config_data = self.render_config_file(config_yaml_file)

            if not config_data or 'data_exchange_customers' not in config_data:
                LOG.info("No data_exchange_customers configuration found in YAML file")
                return

            customers = config_data['data_exchange_customers']
            if not isinstance(customers, list):
                raise ConfigurationError("Configuration error: 'data_exchange_customers' must be a list.")

            deleted_count = 0
            skipped_count = 0

            for customer_config in customers:
                customer_name = customer_config.get('name')
                if not customer_name:
                    raise ConfigurationError("Configuration error: Each customer must have a 'name' field.")

                # Get customer ID
                customer = self.gsdk.get_data_exchange_customer_by_name(customer_name)
                if not customer:
                    LOG.info(f"Customer '{customer_name}' not found, skipping deletion")
                    skipped_count += 1
                    continue

                # Delete customer directly
                LOG.info(f"delete_data_exchange_customer: Deleting customer '{customer_name}'")
                self.gsdk.delete_data_exchange_customer(customer.id)
                LOG.info(f"Successfully deleted customer '{customer_name}' (ID: {customer.id})")
                deleted_count += 1

            LOG.info(f"Data Exchange customer deletion completed: {deleted_count} deleted, {skipped_count} skipped")

        except ConfigurationError:
            raise
        except Exception as e:
            LOG.error(f"Failed to delete Data Exchange customers: {e}")
            raise ConfigurationError(f"Data Exchange customer deletion failed: {e}")

    def delete_services(self, config_yaml_file: str) -> None:
        """
        Delete Data Exchange services from YAML configuration.

        Args:
            config_yaml_file (str): Path to the YAML configuration file
        """
        try:
            LOG.info(f"Deleting Data Exchange services from {config_yaml_file}")
            config_data = self.render_config_file(config_yaml_file)

            if not config_data or 'data_exchange_services' not in config_data:
                LOG.info("No data_exchange_services configuration found in YAML file")
                return

            services = config_data['data_exchange_services']
            if not isinstance(services, list):
                raise ConfigurationError("Configuration error: 'data_exchange_services' must be a list.")

            deleted_count = 0
            skipped_count = 0

            for service_config in services:
                service_name = service_config.get('serviceName')
                if not service_name:
                    raise ConfigurationError("Configuration error: Each service must have a 'serviceName' field.")

                # Get service ID
                service = self.gsdk.get_data_exchange_service_by_name(service_name)
                if not service:
                    LOG.info(f"Service '{service_name}' not found, skipping deletion")
                    skipped_count += 1
                    continue

                # Delete service directly
                LOG.info(f"delete_data_exchange_service: Deleting service '{service_name}'")
                self.gsdk.delete_data_exchange_service(service.id)
                LOG.info(f"Successfully deleted service '{service_name}' (ID: {service.id})")
                deleted_count += 1

            LOG.info(f"Data Exchange service deletion completed: {deleted_count} deleted, {skipped_count} skipped")

        except ConfigurationError:
            raise
        except Exception as e:
            LOG.error(f"Failed to delete Data Exchange services: {e}")
            raise ConfigurationError(f"Data Exchange service deletion failed: {e}")

    def get_service_details(self, service_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific Data Exchange service.

        Args:
            service_id (int): ID of the service to retrieve

        Returns:
            dict: Service details response
        """
        try:
            LOG.info(f"Retrieving Data Exchange service details for ID: {service_id}")
            response = self.gsdk.get_data_exchange_service_details(service_id)
            return response
        except Exception as e:
            LOG.error(f"Failed to retrieve service details for ID {service_id}: {e}")
            raise ConfigurationError(f"Failed to retrieve service details for ID {service_id}: {e}")

    def match_service_to_customers(self, config_yaml_file: str) -> None:
        """
        Match Data Exchange services to customers from YAML configuration.

        Args:
            config_yaml_file (str): Path to the YAML configuration file
        """
        try:
            LOG.info(f"Matching Data Exchange services to customers from {config_yaml_file}")
            config_data = self.render_config_file(config_yaml_file)

            if not config_data or 'data_exchange_matches' not in config_data:
                LOG.info("No data_exchange_matches configuration found in YAML file")
                return

            matches = config_data['data_exchange_matches']
            if not isinstance(matches, list):
                raise ConfigurationError("Configuration error: 'data_exchange_matches' must be a list.")

            matched_count = 0
            skipped_count = 0
            match_responses = []

            for match_config in matches:
                customer_name = match_config.get('customerName')
                service_name = match_config.get('serviceName')

                if not customer_name or not service_name:
                    raise ConfigurationError(
                        "Configuration error: Each match must have 'customerName' and 'serviceName' fields.")

                # Get customer ID
                customer = self.gsdk.get_data_exchange_customer_by_name(customer_name)
                if not customer:
                    raise ConfigurationError(f"Customer '{customer_name}' not found.")

                # Check customer status before attempting match
                if customer.status != "B2B_PEERING_SERVICE_STATUS_INACTIVE":
                    LOG.warning(
                        f"Customer '{customer_name}' status is '{customer.status}', "
                        f"not 'B2B_PEERING_SERVICE_STATUS_INACTIVE'. "
                        f"Skipping match to avoid 'match already exists' error.")
                    LOG.info(
                        f"To resolve this issue, please delete the customer "
                        f"'{customer_name}' and run the match operation again.")
                    skipped_count += 1
                    continue

                # Get service ID
                service = self.gsdk.get_data_exchange_service_by_name(service_name)
                if not service:
                    raise ConfigurationError(f"Service '{service_name}' not found.")

                # Use configured service prefixes (user-selected)
                service_prefixes = match_config.get('servicePrefixes', [])
                if not service_prefixes:
                    raise ConfigurationError(
                        f"Configuration error: 'servicePrefixes' must be specified "
                        f"for matching service '{service_name}' to customer '{customer_name}'.")

                # Build match configuration for API call
                match_payload = {
                    "id": customer.id,
                    "service": {
                        "id": service.id,
                        "servicePrefixes": service_prefixes,
                        "nat": match_config.get('nat', [])
                    }
                }

                # Perform the match and capture response
                LOG.info(f"match_service_to_customer: Matching service '{service_name}' to customer '{customer_name}'")
                response = self.gsdk.match_service_to_customer(match_payload)

                # Store response data for next workflow
                match_response_data = {
                    "customer_name": customer_name,
                    "service_name": service_name,
                    "customer_id": customer.id,
                    "service_id": service.id,
                    "match_id": response.match_id,
                    "timestamp": response.timestamp if hasattr(response, 'timestamp') else None,
                    "status": "matched"
                }
                match_responses.append(match_response_data)
                LOG.info(f"Successfully matched service '{service_name}' to customer '{customer_name}' "
                         f"with match_id: {response.match_id}")
                matched_count += 1

            # Save match responses to file for next workflow
            if match_responses:
                import json
                from datetime import datetime

                # Create output directory if it doesn't exist
                output_dir = os.path.join(os.path.dirname(config_yaml_file), "output")
                os.makedirs(output_dir, exist_ok=True)

                # Generate output filenames based on input config
                base_name = os.path.splitext(os.path.basename(config_yaml_file))[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Create two files: one with timestamp, one with _latest suffix
                timestamped_file = os.path.join(output_dir, f"{base_name}_responses_{timestamp}.json")
                latest_file = os.path.join(output_dir, f"{base_name}_responses_latest.json")

                # Save responses to both JSON files
                with open(timestamped_file, 'w') as f:
                    json.dump(match_responses, f, indent=2)

                with open(latest_file, 'w') as f:
                    json.dump(match_responses, f, indent=2)

                LOG.info(f"Match responses saved to: {timestamped_file}")
                LOG.info(f"Latest match responses saved to: {latest_file}")

            LOG.info(f"Data Exchange service matching completed: {matched_count} matched, {skipped_count} skipped")

        except ConfigurationError:
            raise
        except Exception as e:
            LOG.error(f"Failed to match Data Exchange services to customers: {e}")
            raise ConfigurationError(f"Data Exchange service matching failed: {e}")
