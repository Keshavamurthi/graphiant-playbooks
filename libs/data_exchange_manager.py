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

            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

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

                if 'policy' in service_config:
                    # Resolve LAN segment ID if provided by name
                    if 'serviceLanSegment' in service_config['policy']:
                        lan_segment_name = service_config['policy']['serviceLanSegment']
                        if isinstance(lan_segment_name, str):
                            lan_segment_id = self.gsdk.get_lan_segment_id(lan_segment_name)
                            if lan_segment_id:
                                service_config['policy']['serviceLanSegment'] = lan_segment_id
                            else:
                                raise ConfigurationError(
                                    f"LAN segment '{lan_segment_name}' not found for service '{service_name}'.")

                    # Resolve site or site list IDs if provided by names
                    self._resolve_site_ids(service_config['policy'], service_name)
                    self._resolve_site_list_ids(service_config['policy'], service_name)

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

    def _resolve_site_list_ids(self, policy_config: dict, service_name: str) -> None:
        """
        Resolve site list names to site list IDs in the policy configuration.

        Args:
            policy_config (dict): Policy configuration to update
            service_name (str): Service name for error reporting
        """
        if 'site' in policy_config and isinstance(policy_config['site'], list):
            for site_entry in policy_config['site']:
                if 'siteLists' in site_entry and isinstance(site_entry['siteLists'], list):
                    resolved_site_list_ids = []
                    for site_list_name in site_entry['siteLists']:
                        if isinstance(site_list_name, str):
                            site_list_id = self.gsdk.get_site_list_id(site_list_name)
                            if site_list_id:
                                resolved_site_list_ids.append(site_list_id)
                            else:
                                raise ConfigurationError(f"Site list '{site_list_name}' not found "
                                                         f"for service '{service_name}'.")
                        else:
                            resolved_site_list_ids.append(site_list_name)  # Already an ID
                    site_entry['siteLists'] = resolved_site_list_ids

    def get_services_summary(self) -> Dict[str, Any]:
        """
        Get summary of all Data Exchange services.

        Returns:
            dict: Services summary response
        """
        try:
            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

            LOG.info("Retrieving Data Exchange services summary")
            response = self.gsdk.get_data_exchange_services_summary()

            # Display services in a nice table format
            if response.info:
                service_table = []
                for service in response.info:
                    # Get publisher/subscriber role
                    role = "Publisher" if getattr(service, 'is_publisher', False) else "Subscriber"

                    # Get matched customers count
                    matched_customers = getattr(service, 'matched_customers', 0)

                    service_table.append([
                        service.id,
                        service.name,
                        service.status,
                        role,
                        matched_customers
                    ])

                LOG.info(
                    f"Services Summary:\n"
                    f"""{tabulate(service_table,
                                  headers=['ID', 'Service Name', 'Status', 'Role', 'Matched Customers'],
                                  tablefmt='grid')}""")

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

            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

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
            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

            LOG.info("Retrieving Data Exchange customers summary")
            response = self.gsdk.get_data_exchange_customers_summary()

            # Display customers in a nice table format
            if response.customers:
                customer_table = []
                for customer in response.customers:
                    # Get customer type (Non-Graphiant or Graphiant)
                    customer_type = "Non-Graphiant" if customer.type == "non_graphiant_peer" else "Graphiant"

                    # Get matched services count
                    matched_services = getattr(customer, 'matched_services', 0)

                    customer_table.append([
                        customer.id,
                        customer.name,
                        customer_type,
                        customer.status,
                        matched_services
                    ])

                LOG.info(f"Customers Summary:\n"
                         f"""{tabulate(customer_table,
                                       headers=['ID', 'Customer Name', 'Customer Type', 'Status', 'Matched Services'],
                                       tablefmt='grid')}""")

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

            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

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

            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

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

    def _save_match_service_to_customer_responses(self, match_responses: list, config_yaml_file: str) -> None:
        """
        Save match service to customer responses to JSON files.
        Updates existing entries if they match (customer_name, service_name), otherwise appends new entries.

        Args:
            match_responses (list): List of match response dictionaries
            config_yaml_file (str): Path to the YAML configuration file to determine output directory
        """
        if not match_responses:
            return

        import json
        from datetime import datetime

        # Resolve config file path using the same logic as render_config_file
        # Handle absolute paths
        if os.path.isabs(config_yaml_file):
            resolved_config_file = config_yaml_file
        else:
            # Handle relative paths by concatenating with config_path
            # Security: Normalize path to prevent path traversal attacks
            resolved_config_file = os.path.normpath(os.path.join(self.config_utils.config_path, config_yaml_file))
            # Security: Validate that resolved path is within config_path to prevent path traversal
            config_path_real = os.path.realpath(self.config_utils.config_path)
            resolved_config_file_real = os.path.realpath(resolved_config_file)
            if not resolved_config_file_real.startswith(config_path_real):
                raise ConfigurationError(
                    f"Security: Path traversal detected. Config file path '{config_yaml_file}' "
                    f"resolves outside config directory."
                )

        # Create output directory near the config file (same logic as render_config_file)
        output_dir = os.path.join(os.path.dirname(resolved_config_file), "output")
        os.makedirs(output_dir, exist_ok=True)

        # Generate output filenames based on input config
        base_name = os.path.splitext(os.path.basename(resolved_config_file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create two files: one with timestamp, one with _latest suffix
        timestamped_file = os.path.join(output_dir, f"{base_name}_responses_{timestamp}.json")
        latest_file = os.path.join(output_dir, f"{base_name}_responses_latest.json")

        # Read existing latest file if it exists
        existing_responses = []
        if os.path.exists(latest_file):
            try:
                with open(latest_file, 'r') as f:
                    existing_responses = json.load(f)
                LOG.info(f"Loaded {len(existing_responses)} existing entries from {latest_file}")
            except (json.JSONDecodeError, IOError) as e:
                LOG.warning(f"Could not read existing latest file {latest_file}: {e}. Starting fresh.")

        # Create a dictionary for efficient lookup: key = (customer_name, service_name)
        # This allows us to update existing entries or add new ones
        response_dict = {}
        for entry in existing_responses:
            key = (entry.get('customer_name'), entry.get('service_name'))
            if key[0] and key[1]:  # Only add if both keys are present
                response_dict[key] = entry

        # Update or add new match responses
        updated_count = 0
        added_count = 0
        for new_response in match_responses:
            key = (new_response.get('customer_name'), new_response.get('service_name'))
            if key[0] and key[1]:
                if key in response_dict:
                    # Update existing entry
                    response_dict[key].update(new_response)
                    updated_count += 1
                    LOG.debug(f"Updated entry for customer '{key[0]}' and service '{key[1]}'")
                else:
                    # Add new entry
                    response_dict[key] = new_response
                    added_count += 1
                    LOG.debug(f"Added new entry for customer '{key[0]}' and service '{key[1]}'")

        # Convert back to list for JSON serialization
        merged_responses = list(response_dict.values())

        # Save responses to both JSON files
        with open(timestamped_file, 'w') as f:
            json.dump(merged_responses, f, indent=2)

        with open(latest_file, 'w') as f:
            json.dump(merged_responses, f, indent=2)

        LOG.info(f"Match responses saved to matches_file_with_timestamp: {timestamped_file}")
        LOG.info(f"Latest match responses saved to matches_file: {latest_file}")
        LOG.info(f"Updated {updated_count} existing entries, added {added_count} new entries. "
                 f"Total entries in matches_file: {len(merged_responses)}")

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
                raise ConfigurationError("Configuration error: 'data_exchange_matches' key not found in YAML file.")

            matches = config_data['data_exchange_matches']
            if not isinstance(matches, list):
                raise ConfigurationError("Configuration error: 'data_exchange_matches' must be a list.")

            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

            matched_count = 0
            skipped_count = 0
            failed_count = 0
            match_responses = []

            for match_config in matches:
                customer_name = match_config.get('customerName')
                service_name = match_config.get('serviceName')

                if not customer_name or not service_name:
                    LOG.error("Configuration error: Each match must have 'customerName' and 'serviceName' fields.")
                    failed_count += 1
                    continue

                # Get customer ID
                customer = self.gsdk.get_data_exchange_customer_by_name(customer_name)
                if not customer:
                    LOG.error(f"Customer '{customer_name}' not found in the enterprise.")
                    failed_count += 1
                    continue

                # Get service ID
                service = self.gsdk.get_data_exchange_service_by_name(service_name)
                if not service:
                    LOG.error(f"Service '{service_name}' not found in the enterprise.")
                    failed_count += 1
                    continue

                '''
                TODO: Uncomment. Remove this once latest sdk version 25.11.1 is released.
                # Check if service is already matched to this customer
                matched_services = self.gsdk.get_matched_services_for_customer(customer.id)
                if matched_services is not None:
                    # Check if this service is already in the matched services list
                    already_matched = False
                    for matched_service in matched_services:
                        if matched_service.name == service_name:
                            LOG.warning(
                                f"Service '{service_name}' is already matched to customer '{customer_name}'. "
                                f"Match ID: {matched_service.id}, Status: {matched_service.status}. "
                                f"Skipping to avoid 'match already exists' error.")
                            already_matched = True
                            skipped_count += 1
                            break

                    if already_matched:
                        continue
                '''
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

                try:
                    # Perform the match and capture response
                    LOG.info(f"match_service_to_customer: Matching service '{service_name}' to "
                             f"customer '{customer_name}'")
                    response = self.gsdk.match_service_to_customer(match_payload)
                except Exception as e:
                    error_msg = str(e)
                    # Handle "match already exists" errors gracefully till new sdk version 25.11.1 is released.
                    if "match already exists" in error_msg.lower():
                        LOG.info(f"Service '{service_name}' is already matched to customer '{customer_name}', "
                                 f"skipping match as it already exists.")
                        skipped_count += 1
                        continue
                    else:
                        LOG.error(f"Failed to match service '{service_name}' to customer '{customer_name}': "
                                  f"{error_msg}")
                        failed_count += 1
                        continue

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
            self._save_match_service_to_customer_responses(match_responses, config_yaml_file)

            LOG.info(f"Data Exchange service matching completed: {matched_count} matched, "
                     f"{skipped_count} skipped, {failed_count} failed")
            if failed_count > 0:
                raise ConfigurationError(f"Data Exchange service to customer matching had {failed_count} failures "
                                         f"out of {matched_count + skipped_count + failed_count} total")
        except Exception as e:
            LOG.error(f"Failed to match Data Exchange services to customers: {e}")
            raise ConfigurationError(f"Data Exchange service to customer matching failed: {e}")

    def accept_invitation(self, config_yaml_file: str, matches_file: str = None, dry_run: bool = False) -> None:
        """
        Accept Data Exchange service invitation (Workflow 4).

        Args:
            config_yaml_file (str): Path to YAML configuration file containing acceptance details
            matches_file (str, optional): Path to matches responses JSON file for match ID lookup
            dry_run (bool, optional): If True, skip the actual API call (validation only). Defaults to False.
        """
        try:
            LOG.info(f"accept_invitation: Loading configuration from {config_yaml_file}")
            config_data = self.render_config_file(config_yaml_file)

            # All configurations are under 'data_exchange_acceptances' key
            if 'data_exchange_acceptances' not in config_data:
                raise ConfigurationError("Configuration file must contain 'data_exchange_acceptances' key")

            acceptances = config_data['data_exchange_acceptances']

            # Ensure it's always a list
            if not isinstance(acceptances, list):
                raise ConfigurationError("data_exchange_acceptances must be a list of acceptance configurations")

            # Print current enterprise info
            LOG.info(f"DataExchangeManager: Current enterprise info: {self.gsdk.enterprise_info}")

            # Log dry-run mode if enabled
            if dry_run:
                LOG.info("accept_invitation: DRY-RUN MODE ENABLED - API calls will be skipped")

            # Validate gateway requirements before processing acceptances
            self._validate_gateway_requirements_for_acceptances(acceptances)

            # Process acceptances and log results
            result = self._process_multiple_acceptances(acceptances, matches_file, dry_run)

            # Log summary like other operations
            total_processed = result.get('total_processed', 0)
            total_successful = result.get('total_successful', 0)
            total_failed = total_processed - total_successful

            LOG.info(f"Data Exchange invitation acceptance completed: {total_successful} accepted, "
                     f"{total_failed} failed")

            # Check if there were any failures
            if total_failed > 0:
                LOG.warning(f"accept_invitation: {total_failed} "
                            f"out of {total_processed} invitation acceptances failed")
                # TODO:Optionally raise an exception for partial failures
                # raise ConfigurationError(f"Data Exchange invitation acceptance had {total_failed} failures "
                #                         f"out of {total_processed} total")
            return result
        except ConfigurationError:
            raise
        except Exception as e:
            LOG.error(f"Failed to accept Data Exchange service invitation: {e}")
            raise ConfigurationError(f"Data Exchange service acceptance failed: {e}")

    def _validate_gateway_requirements_for_acceptances(self, acceptances, min_gateways=2):
        """
        Validate gateway requirements for all acceptances.

        Args:
            acceptances (list): List of acceptance configurations
            min_gateways (int): Minimum number of gateways required per region
        """
        try:
            LOG.info(f"_validate_gateway_requirements_for_acceptances: Validating gateway requirements for "
                     f"{len(acceptances)} acceptances")

            # Collect unique regions from acceptances
            regions_to_validate = set()
            for acceptance in acceptances:
                if 'siteToSiteVpn' in acceptance and 'region' in acceptance['siteToSiteVpn']:
                    region_name = acceptance['siteToSiteVpn']['region']
                    regions_to_validate.add(region_name)

            # Validate each region
            for region_name in regions_to_validate:
                edges_summary = self.gsdk.get_edges_summary_filter(region=region_name, role='gateway', status='active')
                if not edges_summary:
                    LOG.error(f"_validate_gateway_requirements_for_acceptances: "
                              f"No active gateways found in region {region_name}")
                    raise ConfigurationError(f"No active gateways found in region {region_name}")
                else:
                    LOG.info(f"_validate_gateway_requirements_for_acceptances: Region {region_name} has "
                             f"{len(edges_summary)} active gateways")
                if len(edges_summary) < min_gateways:
                    LOG.error(f"_validate_gateway_requirements_for_acceptances: Region {region_name} has only "
                              f"{len(edges_summary)} gateways, minimum {min_gateways} required")
                    raise ConfigurationError(f"Region {region_name} has only {len(edges_summary)} gateways,"
                                             f"minimum {min_gateways} required")
                else:
                    LOG.info(f"_validate_gateway_requirements_for_acceptances: Region {region_name} meets "
                             f"minimum gateway requirements")
                # Validate tunnel terminator connection count for each gateway
                for edge_summary in edges_summary:
                    LOG.info(f"_validate_gateway_requirements_for_acceptances: Validating tunnel terminator "
                             f"connection count for gateway {edge_summary.hostname}")
                    if hasattr(edge_summary, 'tt_conn_count') and edge_summary.tt_conn_count:
                        if edge_summary.tt_conn_count < 2:
                            LOG.error(f"_validate_gateway_requirements_for_acceptances: Gateway "
                                      f"{edge_summary.hostname} has only {edge_summary.tt_conn_count} "
                                      f"tunnel terminators, minimum 2 required")
                            raise ConfigurationError(f"Gateway {edge_summary.hostname} has only "
                                                     f"{edge_summary.tt_conn_count} tunnel terminators, "
                                                     f"minimum 2 required")
                    else:
                        LOG.error(f"_validate_gateway_requirements_for_acceptances: Gateway {edge_summary.hostname} "
                                  f"does not have any tunnel terminators connected, minimum 2 required")
                        raise ConfigurationError(f"Gateway {edge_summary.hostname} does not have any "
                                                 f"tunnel terminators connected, minimum 2 required")
        except Exception as e:
            LOG.warning(f"_validate_gateway_requirements_for_acceptances: Gateway validation failed: {e}")
            raise
            # TODO: Don't fail the entire operation for validation issues ?

    def _process_multiple_acceptances(self, acceptances_config, matches_file=None, dry_run=False):
        """
        Process multiple invitation acceptances from configuration.

        Args:
            acceptances_config (list): List of acceptance configurations
            matches_file (str, optional): Path to matches responses JSON file for match ID lookup
            dry_run (bool, optional): If True, skip the actual API call (validation only). Defaults to False.

        Returns:
            dict: Combined results from all acceptances
        """
        try:
            results = []
            total_processed = 0
            total_successful = 0

            LOG.info(f"_process_multiple_acceptances: Processing {len(acceptances_config)} invitation acceptances")

            for i, acceptance_config in enumerate(acceptances_config):
                try:
                    LOG.info(f"_process_multiple_acceptances: Processing acceptance {i+1}/{len(acceptances_config)}")

                    # Resolve names to IDs (returns direct API payload structure)
                    resolved_config = self._resolve_acceptance_names_to_ids(acceptance_config, matches_file)

                    # Extract service ID and match ID from resolved configuration
                    service_id = resolved_config['id']  # Service ID is 'id' in API payload
                    match_id = resolved_config['matchId']  # Match ID is 'matchId' in API payload

                    # Validate required fields in resolved configuration
                    required_fields = ['id', 'siteInformation', 'policy', 'siteToSiteVpn', 'nat']
                    for field in required_fields:
                        if field not in resolved_config or resolved_config[field] is None:
                            raise ConfigurationError(f"Missing required field '{field}' in resolved configuration")

                    # Use the resolved configuration directly as the API payload
                    acceptance_payload = resolved_config

                    LOG.info(f"_process_multiple_acceptances: Acceptance payload for "
                             f"'{acceptance_config.get('customerName')}' and '{acceptance_config.get('serviceName')}'"
                             f": {acceptance_payload}")

                    # Check for dry-run mode
                    if dry_run:
                        LOG.info(f"_process_multiple_acceptances: DRY-RUN - Skipping API call for "
                                 f"'{acceptance_config.get('customerName')}' and "
                                 f"'{acceptance_config.get('serviceName')}' "
                                 f" with match_id: {match_id} and service_id: {service_id}")
                        result = {
                            'dry_run': True,
                            'message': 'API call skipped in dry-run mode',
                            'payload_validated': True,
                            'match_id': match_id,
                            'service_id': service_id
                        }
                    else:
                        # Call the acceptance API with match_id as path parameter
                        response = self.gsdk.accept_data_exchange_service(match_id, acceptance_payload)
                        result = response.to_dict()

                    results.append({
                        'customer_name': acceptance_config.get('customerName'),
                        'service_name': acceptance_config.get('serviceName'),
                        'result': result,
                        'status': 'success' if not dry_run else 'dry-run'
                    })
                    total_successful += 1

                except Exception as e:
                    LOG.error(f"_process_multiple_acceptances: Failed to process acceptance {i+1}: {e}")
                    results.append({
                        'customer_name': acceptance_config.get('customerName'),
                        'service_name': acceptance_config.get('serviceName'),
                        'error': str(e),
                        'status': 'failed'
                    })

                total_processed += 1

            LOG.info(f"_process_multiple_acceptances: Completed {total_successful}/{total_processed} "
                     f"acceptances successfully")

            return {
                'total_processed': total_processed,
                'total_successful': total_successful,
                'results': results
            }

        except Exception as e:
            LOG.error(f"Failed to process multiple acceptances: {e}")
            raise ConfigurationError(f"Multiple acceptance processing failed: {e}")

    def _fill_missing_tunnel_values(self, acceptance_config, region_id, lan_segment_id):
        """
        Fill in missing tunnel configuration values using Graphiant portal APIs.

        Args:
            acceptance_config (dict): The acceptance configuration
            region_id (int): The region ID for subnet allocation
            lan_segment_id (int): The LAN segment ID for subnet allocation

        Returns:
            dict: Updated acceptance configuration with filled values
        """
        try:
            site_to_site_vpn = acceptance_config.get('siteToSiteVpn', {})
            ipsec_gateway_details = site_to_site_vpn.get('ipsecGatewayDetails', {})

            # Fill in missing tunnel1 values
            tunnel1 = ipsec_gateway_details.get('tunnel1', {})
            if tunnel1.get('insideIpv4Cidr') is None:
                ipv4_subnet = self.gsdk.get_ipsec_inside_subnet(region_id, lan_segment_id, 'ipv4')
                if ipv4_subnet:
                    tunnel1['insideIpv4Cidr'] = ipv4_subnet
                    LOG.info(f"_fill_missing_tunnel_values: Filled tunnel1 insideIpv4Cidr: {ipv4_subnet}")

            if tunnel1.get('insideIpv6Cidr') is None:
                ipv6_subnet = self.gsdk.get_ipsec_inside_subnet(region_id, lan_segment_id, 'ipv6')
                if ipv6_subnet:
                    tunnel1['insideIpv6Cidr'] = ipv6_subnet
                    LOG.info(f"_fill_missing_tunnel_values: Filled tunnel1 insideIpv6Cidr: {ipv6_subnet}")

            if tunnel1.get('psk') is None:
                psk = self.gsdk.get_preshared_key()
                if psk:
                    tunnel1['psk'] = psk
                    LOG.info(f"_fill_missing_tunnel_values: Filled tunnel1 psk: {psk}")

            # Fill in missing tunnel2 values
            tunnel2 = ipsec_gateway_details.get('tunnel2', {})
            if tunnel2.get('insideIpv4Cidr') is None:
                ipv4_subnet = self.gsdk.get_ipsec_inside_subnet(region_id, lan_segment_id, 'ipv4')
                if ipv4_subnet:
                    tunnel2['insideIpv4Cidr'] = ipv4_subnet
                    LOG.info(f"_fill_missing_tunnel_values: Filled tunnel2 insideIpv4Cidr: {ipv4_subnet}")

            if tunnel2.get('insideIpv6Cidr') is None:
                ipv6_subnet = self.gsdk.get_ipsec_inside_subnet(region_id, lan_segment_id, 'ipv6')
                if ipv6_subnet:
                    tunnel2['insideIpv6Cidr'] = ipv6_subnet
                    LOG.info(f"_fill_missing_tunnel_values: Filled tunnel2 insideIpv6Cidr: {ipv6_subnet}")

            if tunnel2.get('psk') is None:
                psk = self.gsdk.get_preshared_key()
                if psk:
                    tunnel2['psk'] = psk
                    LOG.info(f"_fill_missing_tunnel_values: Filled tunnel2 psk: {psk}")

            return acceptance_config

        except Exception as e:
            LOG.error(f"_fill_missing_tunnel_values: Error filling tunnel values: {e}")
            return acceptance_config

    def _resolve_acceptance_names_to_ids(self, acceptance_config, matches_file=None):
        """
        Resolve names to IDs for acceptance configuration.

        Args:
            acceptance_config (dict): Acceptance configuration with names
            matches_file (str, optional): Path to matches responses JSON file for match ID lookup

        Returns:
            dict: Resolved configuration with IDs
        """
        try:
            customer_name = acceptance_config.get('customerName')
            service_name = acceptance_config.get('serviceName')

            if not customer_name or not service_name:
                raise ConfigurationError("customer_name and service_name are required in acceptance configuration")

            LOG.info(f"_resolve_acceptance_names_to_ids: Resolving names for customer "
                     f"'{customer_name}' and service '{service_name}'")

            # Get match ID and service ID from customer name and service name combination
            # This is important because a customer can be matched to multiple services
            match_data = self._get_match_id_from_customer_service(customer_name, service_name, matches_file)

            if not match_data:
                raise ConfigurationError(f"No match found for customer '{customer_name}' and service '{service_name}'")

            match_id = match_data.get('match_id')
            service_id = match_data.get('service_id')

            if not match_id or not service_id:
                raise ConfigurationError(f"Invalid match data for customer "
                                         f"'{customer_name}' and service '{service_name}'")

            # Resolve site names to IDs
            site_names = acceptance_config.get('siteInformation', [{}])[0].get('sites', [])
            site_ids = []
            for site_name in site_names:
                site_id = self.gsdk.get_site_id(site_name)
                if site_id:
                    site_ids.append(site_id)
                else:
                    raise ConfigurationError(f"Site '{site_name}' not found")

            # Resolve site list names to IDs
            site_list_names = acceptance_config.get('siteInformation', [{}])[0].get('siteLists', [])
            site_list_ids = []
            for site_list_name in site_list_names:
                site_list_id = self.gsdk.get_site_list_id(site_list_name)
                if site_list_id:
                    site_list_ids.append(site_list_id)
                else:
                    raise ConfigurationError(f"Site list '{site_list_name}' not found")

            # Resolve LAN segment name to ID
            lan_segment_name = acceptance_config.get('policy', [{}])[0].get('lanSegment')
            lan_segment_id = None
            if lan_segment_name:
                lan_segment_id = self.gsdk.get_lan_segment_id(lan_segment_name)
                if not lan_segment_id:
                    raise ConfigurationError(f"LAN segment '{lan_segment_name}' not found")

            # Resolve region name to ID
            region_name = acceptance_config.get('siteToSiteVpn', {}).get('region')
            region_id = None
            if region_name:
                region_id = self._get_region_id_from_name(region_name)
                if not region_id:
                    raise ConfigurationError(f"Region '{region_name}' not found")

            # Build resolved acceptance configuration in API payload format
            # Update siteToSiteVpn to include resolved regionId and emails
            site_to_site_vpn = acceptance_config.get('siteToSiteVpn', {}).copy()
            if region_id:
                site_to_site_vpn['regionId'] = region_id
            # Ensure emails are included in siteToSiteVpn
            if 'emails' in acceptance_config.get('siteToSiteVpn', {}):
                site_to_site_vpn['emails'] = acceptance_config.get('siteToSiteVpn', {}).get('emails', [])

            resolved_config = {
                'id': service_id,  # Service ID for API payload
                'siteInformation': [{
                    'sites': site_ids,
                    'siteLists': site_list_ids
                }],
                'nat': acceptance_config.get('nat', []),
                'policy': [{
                    'lanSegment': lan_segment_id,
                    'consumerPrefixes': acceptance_config.get('policy', [{}])[0].get('consumerPrefixes', [])
                }],
                'siteToSiteVpn': site_to_site_vpn,
                'globalObjectOps': acceptance_config.get('globalObjectOps', {}),
                'routingPolicyTable': acceptance_config.get('routingPolicyTable', []),
                'matchId': match_id
            }

            # Fill in missing tunnel values using Graphiant portal APIs
            resolved_config = self._fill_missing_tunnel_values(resolved_config, region_id, lan_segment_id)

            LOG.info(f"_resolve_acceptance_names_to_ids: Resolved service_id={service_id}, match_id={match_id}, "
                     f"region_id={region_id}")
            return resolved_config

        except Exception as e:
            LOG.error(f"Failed to resolve names to IDs: {e}")
            raise ConfigurationError(f"Name resolution failed: {e}")

    def _get_match_id_from_customer_service(self, customer_name, service_name, matches_file=None):
        """
        Get match ID and service ID from customer name and service name.
        Reads from the matches responses JSON file.

        Args:
            customer_name (str): Customer name
            service_name (str): Service name
            matches_file (str, optional): Path to matches responses JSON file

        Returns:
            dict: Dictionary containing match_id and service_id, or None if not found
        """
        try:
            import json
            import os

            # Use provided matches file or default
            if not matches_file:
                # Use the same path resolution logic as render_config_file
                # Use config_path for relative path resolution
                matches_file = os.path.join(
                    self.config_utils.config_path,
                    "de_workflows_configs/output/sample_data_exchange_matches_responses_latest.json"
                )
            else:
                # Apply the same path resolution logic as render_config_file for provided path
                if os.path.isabs(matches_file):
                    # Absolute path - use as is
                    pass
                else:
                    # Relative path - resolve using config_path (same as render_config_file)
                    # Security: Normalize path to prevent path traversal attacks
                    matches_file = os.path.normpath(os.path.join(self.config_utils.config_path, matches_file))
                    # Security: Validate that resolved path is within config_path to prevent path traversal
                    config_path_real = os.path.realpath(self.config_utils.config_path)
                    matches_file_real = os.path.realpath(matches_file)
                    if not matches_file_real.startswith(config_path_real):
                        raise ConfigurationError(
                            "Security: Path traversal detected. Matches file path resolves outside config directory."
                        )

            if os.path.exists(matches_file):
                LOG.info(f"_get_match_id_from_customer_service: Reading matches from {matches_file}")
                with open(matches_file, 'r') as f:
                    matches_data = json.load(f)

                # Find matching customer and service
                for match in matches_data:
                    if (match.get('customer_name') == customer_name and
                            match.get('service_name') == service_name):
                        match_id = match.get('match_id')
                        service_id = match.get('service_id')
                        LOG.info(f"_get_match_id_from_customer_service: Found match_id {match_id} "
                                 f"and service_id {service_id} for customer "
                                 f"'{customer_name}' and service '{service_name}'")
                        return {
                            'match_id': match_id,
                            'service_id': service_id
                        }

                LOG.warning(f"_get_match_id_from_customer_service: No match found for customer "
                            f"'{customer_name}' and service '{service_name}'")
                return None
            else:
                LOG.error(f"_get_match_id_from_customer_service: Matches file not found at {matches_file}")
                return None

        except Exception as e:
            LOG.error(f"_get_match_id_from_customer_service: Error reading matches file: {e}")
            return None

    def _get_region_id_from_name(self, region_name):
        """
        Get region ID from region name using the API.

        Args:
            region_name (str): Region name

        Returns:
            int: Region ID if found, None otherwise
        """
        try:
            LOG.info(f"_get_region_id_from_name: Looking up region ID for '{region_name}'")
            region_id = self.gsdk.get_region_id_by_name(region_name)

            if region_id is None:
                LOG.warning(f"_get_region_id_from_name: Region '{region_name}' not found")
            else:
                LOG.info(f"_get_region_id_from_name: Found region '{region_name}' with ID {region_id}")

            return region_id
        except Exception as e:
            LOG.error(f"_get_region_id_from_name: Failed to get region ID for '{region_name}': {e}")
            return None

    def get_service_health(self, service_name, is_provider=False):
        """
        Get service health monitoring information.

        Args:
            service_name (str): The service name
            is_provider (bool): Whether this is a provider view

        Returns:
            dict: Service health data
        """
        try:
            LOG.info(f"get_service_health: Retrieving health for service {service_name}")

            # Get service ID from service name
            service_id = self.gsdk.get_data_exchange_service_id_by_name(service_name)
            if not service_id:
                raise ConfigurationError(f"Service '{service_name}' not found")

            LOG.info(f"get_service_health: Found service ID {service_id} for service '{service_name}'")
            response = self.gsdk.get_service_health(service_id, is_provider)

            if response and hasattr(response, 'service_health'):
                health_table = []
                for health in response.service_health:
                    health_table.append([
                        health.customer_name,
                        health.overall_health,
                        health.producer_prefix_health.health,
                        health.customer_prefix_health.health
                    ])

                LOG.info(
                    f"Service Health:\n"
                    f"""{tabulate(health_table,
                                  headers=['Customer', 'Overall', 'Producer Prefixes', 'Customer Prefixes'],
                                  tablefmt='grid')}""")

            return response.to_dict() if response else {}

        except Exception as e:
            LOG.error(f"Failed to retrieve service health: {e}")
            raise ConfigurationError(f"Service health retrieval failed: {e}")
