import json
import time
import graphiant_sdk
from graphiant_sdk.exceptions import (
    ApiException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    ServiceException,
)

from libs.logger import setup_logger
from libs.poller import poller

LOG = setup_logger()


class GraphiantPortalClient():
    def __init__(self, base_url=None, username=None, password=None):
        self.config = graphiant_sdk.Configuration(host=base_url,
                                                  username=username, password=password)
        self.api_client = graphiant_sdk.ApiClient(self.config)
        self.api = graphiant_sdk.DefaultApi(self.api_client)
        self.bearer_token = None

    def set_bearer_token(self):
        v1_auth_login_post_request = \
            graphiant_sdk.V1AuthLoginPostRequest(username=self.config.username,
                                                 password=self.config.password)
        v1_auth_login_post_response = None
        try:
            v1_auth_login_post_response = self.api.v1_auth_login_post(
                v1_auth_login_post_request=v1_auth_login_post_request)
        except BadRequestException as e:
            LOG.error(f"v1_auth_login_post: Got BadRequestException. "
                      f"Please verify payload is correct. {e}")
        except (UnauthorizedException, ServiceException) as e:
            LOG.error(f"v1_auth_login_post: Got Exception. "
                      f"Please verify crendentials are correct. {e}")
        assert v1_auth_login_post_response, 'v1_auth_login_post_response is None'
        assert v1_auth_login_post_response.token, 'bearer_token is not retrieved'
        LOG.debug(f"GraphiantPortalClient Bearer token : {v1_auth_login_post_response.token}")
        LOG.info("Graphiant Portal Bearer token retrieved successfully !!! ")
        self.bearer_token = f'Bearer {v1_auth_login_post_response.token}'

    def _log_api_error(self, method_name: str, api_url: str,
                       path_params: dict = None, query_params: dict = None,
                       request_body: dict = None, exception: Exception = None):
        """
        Helper method to log API errors with comprehensive parameter information.

        Args:
            method_name (str): Name of the API method
            api_url (str): Full API URL
            path_params (dict): Path parameters
            query_params (dict): Query parameters
            request_body (dict): Request body for POST/PUT requests
            exception (Exception): The exception that occurred
        """
        LOG.error(f"{method_name}: API Error - URL: {api_url}")

        if path_params:
            LOG.error(f"{method_name}: Path Parameters - {path_params}")

        if query_params:
            query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
            LOG.error(f"{method_name}: Query Parameters - {query_string}")
        else:
            LOG.error(f"{method_name}: Query Parameters - None")

        if request_body:
            LOG.error(f"{method_name}: Request Body - {request_body}")

        if exception:
            LOG.error(f"{method_name}: Got Exception: {exception}")

    def get_all_enterprises(self):
        """
        Get all enterprises on GCS.

        Returns:
            list: A list of enterprise information if successful, otherwise an empty list.
        """
        enterprises = self.api.v1_enterprises_get(authorization=self.bearer_token)
        LOG.debug(f"get_all_enterprises : {enterprises}")
        return enterprises

    def get_edges_summary(self, device_id=None):
        """
        Get all edges summary from GCS.

        Args:
            device_id (int, optional): The device ID to filter edges.
            If not provided, returns all edges.

        Returns:
            list or dict: A list of all edges info if no device_id is provided,
            or a single edge's information if a device_id is provided.
        """
        response = self.api.v1_edges_summary_get(authorization=self.bearer_token)
        if device_id:
            for edge_info in response.edges_summary:
                if edge_info.device_id == device_id:
                    return edge_info
        return response.edges_summary

    def get_device_id(self, device_name):
        """
        Retrieve the device ID(s) based on the device name.

        If a single match is found, returns the device ID.
        If multiple matches are found, returns a dictionary of {hostname: device_id}.
        If no match is found, returns an empty dict.
        """
        output = self.get_edges_summary()
        output_dict = {}
        for device_info in output:
            if device_name in device_info.hostname:
                output_dict[device_info.hostname] = device_info.device_id
        LOG.debug(f"get_device_id : {output_dict}")
        if len(output_dict) == 1:
            for device_id in output_dict.values():
                return device_id
        return output_dict

    def get_enterprise_id(self):
        """
        Retrieve the enterprise ID from the first available device in the edges summary.

        Returns:
            str or None: The enterprise ID, or None if no devices are found.
        """
        output = self.get_edges_summary()
        if not output:
            return None
        for device_info in output:
            LOG.debug(f"get_enterprise_id : {device_info.enterprise_id}")
            return device_info.enterprise_id

    @poller(timeout=90, wait=5)
    def verify_device_portal_status(self, device_id: int):
        """
        Verifies device portal sync Ready status (InSync) and
         also verifies device connections to tunnel terminators status.
        """
        edge_summary = self.get_edges_summary(device_id=device_id)
        if edge_summary.portal_status == "Ready":
            if edge_summary.tt_conn_count and edge_summary.tt_conn_count == 2:
                return
            else:
                LOG.info(f"verify_device_portal_status: {device_id} tunnel terminitor conn count: "
                         f"{edge_summary.tt_conn_count} Expected: tt_conn_count=2. Retrying..")
                assert False, (f"verify_device_portal_status: "
                               f"{device_id} tunnel terminitor conn count: "
                               f"{edge_summary.tt_conn_count} Expected: tt_conn_count=2. Retry")

        else:
            LOG.info(f"verify_device_portal_status: {device_id} Portal Status: "
                     f"{edge_summary.portal_status} Expected: Ready. Retrying..")
            assert False, (f"verify_device_portal_status: {device_id} Portal Status: "
                           f"{edge_summary.portal_status} Expected: Ready. Retrying..")

    def put_device_config(self, device_id: int, core=None, edge=None):
        """
        Put Devices Config on GCS for Core or Edge

        Args:
            device_id (int): The device ID to push the config.
            core (dict, V1DevicesDeviceIdConfigPutRequestCore, optional): Core configuration data.
            edge (dict, V1DevicesDeviceIdConfigPutRequestEdge, optional): Edge configuration data.

        Returns:
            response (V1DevicesDeviceIdConfigPut202Response):
            The response from the API call to push the device config.

        Raises:
            AssertionError: If the device portal status is not 'Ready' after retries
            ApiException/AssertionError: If there is an API exception during the
            config push after retries
        """
        device_config_put_request = \
            graphiant_sdk.V1DevicesDeviceIdConfigPutRequest(core=core, edge=edge)
        try:
            # Verify device portal status and connection status.
            self.verify_device_portal_status(device_id=device_id)
            LOG.info(f"put_device_config : config to be pushed for {device_id}: \
                     \n{json.dumps(device_config_put_request.to_dict(), indent=2)}")
            response = self.api.v1_devices_device_id_config_put(
                authorization=self.bearer_token, device_id=device_id,
                v1_devices_device_id_config_put_request=device_config_put_request)
            # Verify device portal status and connection status.
            self.verify_device_portal_status(device_id=device_id)
            return response
        except ForbiddenException as e:
            LOG.error(f"put_device_config: Got ForbiddenException while config push {e}")
            assert False, (f"put_device_config : Retrying, Got ForbiddenException "
                           f"while config push to {device_id}. "
                           f"User {self.config.username} does not have permissions "
                           f"to perform the requested operation "
                           f"(v1_devices_device_id_config_put).")
        except ApiException as e:
            LOG.warning(f"put_device_config : Exception while config push {e}")
            assert False, (f"put_device_config : Retrying, Exception while config push to {device_id}. "
                           f"Exception: {e}")

    def post_devices_bringup(self, device_ids):
        """
        Post Devices Bringup On GCS

        Args:
            device_ids (list): List of device IDs to bring up.

        Returns:
            response: The response from the API call to bring up the devices.
        """
        data = {'deviceIds': device_ids}
        LOG.debug(f"post_devices_bringup : {data}")
        response = self.api.v1_devices_bringup_post(authorization=self.bearer_token,
                                                    v1_devices_bringup_post_request=data)
        return response

    def put_devices_bringup(self, device_ids, status):
        """
        Update the bringup status of the devices specified by their device IDs.

        Args:
            device_ids (list): A list of device IDs whose status needs to be updated.
            status (str): The desired status to be set for the devices:
                        - 'allowed', 'active', 'activate' → 'Allowed'
                        - 'denied', 'deactivate' → 'Denied'
                        - 'removed', 'decommission' → 'Removed'
                        - 'pending', 'staging', 'stage' → 'Pending'
                        - 'maintenance' → 'Maintenance'

        Returns:
            bool: True if the status update was successful, False if ApiException occurs.
        """
        data = {'deviceIds': device_ids, 'status': ''}
        data['status'] = status
        if status.lower() in ['allowed', 'active', 'activate']:
            data['status'] = 'Allowed'
        if status.lower() == ['denied', 'deactivate']:
            data['status'] = 'Denied'
        if status.lower() == ['removed', 'decommission']:
            data['status'] = 'Removed'
        if status.lower() in ['pending', 'staging', 'stage']:
            data['status'] = 'Pending'
        if status.lower() == 'maintenance':
            data['status'] = 'Maintenance'
        try:
            LOG.debug(f"put_devices_bringup : {data}")
            self.api.v1_devices_bringup_put(authorization=self.bearer_token,
                                            v1_devices_bringup_put_request=data)
            time.sleep(15)
            return True
        except ApiException:
            return False

    def patch_global_config(self, **kwargs):
        """
        Patch the global configuration on the system.

        Args:
            **kwargs: The global configuration parameters to be patched.

        Returns:
            The response from the API

        Raises:
            ApiException: If the API call fails.

        """
        try:
            patch_global_config_request = graphiant_sdk.V1GlobalConfigPatchRequest(
                global_prefix_sets=kwargs.get('global_prefix_sets'),
                ipfix_exporters=kwargs.get('ipfix_exporters'),
                prefix_sets=kwargs.get('prefix_sets'),
                routing_policies=kwargs.get('routing_policies'),
                snmps=kwargs.get('snmps'),
                syslog_servers=kwargs.get('syslog_servers'),
                traffic_policies=kwargs.get('traffic_policies'),
                vpn_profiles=kwargs.get('vpn_profiles'))
            LOG.info(f"patch_global_config : config to be pushed : \
                     \n{json.dumps(patch_global_config_request.to_dict(), indent=2)}")
            response = self.api.v1_global_config_patch(
                authorization=self.bearer_token,
                v1_global_config_patch_request=patch_global_config_request
            )
            return response
        except (NotFoundException, ServiceException) as e:
            LOG.error("patch_global_config: Got Exception while v1_global_config_patch request. "
                      "Global object(s) might not exist.")
            assert False, (f"patch_global_config : Got Exception {e} while "
                           f"v1_global_config_patch request. "
                           f"Global object(s) in the request might not exist.")
        except ApiException as e:
            LOG.warning(f"patch_global_config : Exception While Global config patch {e}")
            assert False, "patch_global_config : Retrying, Exception while Global config patch"

    @poller(retries=3, wait=10)
    def post_global_summary(self, **kwargs):
        """
        Posts global summary configuration to the system.
        Args:
            **kwargs: The global summary configuration parameters to be posted.

        Returns:
            The response from the API

        Raises:
            ApiException: If the API call fails.
        """
        body = graphiant_sdk.V1GlobalSummaryPostRequest(**kwargs)
        try:
            LOG.info(f"post_global_summary : config to be pushed : \n{body}")
            response = self.api.v1_global_summary_post(authorization=self.bearer_token,
                                                       v1_global_summary_post_request=body)
            return response
        except ApiException as e:
            LOG.warning(f"post_global_summary : Exception While Global config patch {e}")
            assert False, "post_global_summary : Retrying, Exception while Global config patch"

    def get_global_routing_policy_id(self, policy_name):
        """
        Retrieve the global routing policy ID based on the policy name.

        Args:
            policy_name (str): The name of the routing policy.

        Returns:
            str or None: The ID of the routing policy if found, otherwise None.
        """
        result = self.post_global_summary(routing_policy_type=True)
        for key, value in result.to_dict().items():
            for config in value:
                if config['name'] == policy_name:
                    return config['id']
        return None

    # Site API methods
    def create_site(self, site_data: dict):
        """
        Create a new site.

        Args:
            site_data (dict): The site data containing name, location, etc.

        Returns:
            dict: The created site information

        Raises:
            ApiException: If the API call fails.
        """
        try:
            LOG.info(f"create_site: Creating site with data: {json.dumps(site_data, indent=2)}")
            response = self.api.v1_sites_post(
                authorization=self.bearer_token,
                v1_sites_post_request=site_data
            )
            LOG.info(f"create_site: Successfully created site with ID: {response.site.id}")
            return response.site
        except ApiException as e:
            api_url = f"{self.api.api_client.configuration.host}/v1/sites"
            self._log_api_error(
                method_name="create_site",
                api_url=api_url,
                request_body=site_data,
                exception=e
            )
            raise e

    def delete_site(self, site_id: int):
        """
        Delete a site.

        Args:
            site_id (int): The ID of the site to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            LOG.info(f"delete_site: Deleting site with ID: {site_id}")
            self.api.v1_sites_site_id_delete(
                authorization=self.bearer_token,
                site_id=site_id
            )
            LOG.info(f"delete_site: Successfully deleted site with ID: {site_id}")
            return True
        except ApiException as e:
            api_url = f"{self.api.api_client.configuration.host}/v1/sites/{site_id}"
            self._log_api_error(
                method_name="delete_site",
                api_url=api_url,
                path_params={"site_id": site_id},
                exception=e
            )
            return False

    def get_sites_details(self):
        """
        Get detailed information about all sites using v1/sites/details API.

        Returns:
            list: List of site details
        """
        try:
            response = self.api.v1_sites_details_get(authorization=self.bearer_token)
            LOG.debug(f"get_sites_details: Retrieved {len(response.sites)} sites using v1/sites/details")
            return response.sites
        except ApiException as e:
            api_url = f"{self.api.api_client.configuration.host}/v1/sites/details"
            self._log_api_error(
                method_name="get_sites_details",
                api_url=api_url,
                exception=e
            )
            return []

    def site_exists(self, site_name: str) -> bool:
        """
        Check if a site exists using v1/sites/details API.

        Args:
            site_name (str): The name of the site to check.

        Returns:
            bool: True if site exists, False otherwise.
        """
        try:
            site_id = self.get_site_id(site_name)
            return site_id is not None
        except Exception as e:
            LOG.error(f"site_exists: Got Exception while checking if site '{site_name}' exists: {e}")
            return False

    def post_site_config(self, site_id: int, site_config: dict):
        """
        Update site configuration for global system object attachments.

        Args:
            site_id (int): The site ID to update the configuration for.
            site_config (dict): The site configuration payload containing global object operations.

        Returns:
            The response from the API

        Raises:
            ApiException: If the API call fails.
        """
        try:
            LOG.info(f"post_site_config : config to be pushed for site {site_id}: \
                     \n{json.dumps(site_config, indent=2)}")
            response = self.api.v1_sites_site_id_post(
                authorization=self.bearer_token,
                site_id=site_id,
                v1_sites_site_id_post_request=site_config
            )
            return response
        except ApiException as e:
            LOG.error(f"post_site_config: Got Exception while updating site {site_id} config: {e}")
            raise e

    def get_site_id(self, site_name: str):
        """
        Get site ID by site name using v1/sites/details API.

        Args:
            site_name (str): The name of the site.

        Returns:
            int or None: The site ID if found, None otherwise.
        """
        try:
            # Get detailed site information using v1/sites/details
            response = self.api.v1_sites_details_get(authorization=self.bearer_token)
            sites = response.sites
            LOG.debug(f"get_site_id: Looking for site '{site_name}' in {len(sites)} sites using v1/sites/details")
            for site in sites:
                if site.name == site_name:
                    LOG.debug(f"get_site_id: Found site '{site_name}' with ID {site.id}")
                    return site.id
            LOG.debug(f"get_site_id: Site '{site_name}' not found")
            return None
        except ApiException as e:
            api_url = f"{self.api.api_client.configuration.host}/v1/sites"
            self._log_api_error(
                method_name="get_site_id",
                api_url=api_url,
                query_params={"name": site_name},
                exception=e
            )
            return None

    # Global LAN Segments API methods
    def post_global_lan_segments(self, name: str, description: str = ""):
        """
        Create a global LAN segment.

        Args:
            name (str): Name of the LAN segment
            description (str): Description of the LAN segment

        Returns:
            dict: Response containing the created LAN segment ID
        """
        try:
            post_lan_segments_request = graphiant_sdk.V1GlobalLanSegmentsPostRequest(
                name=name,
                description=description
            )
            LOG.info(f"post_global_lan_segments: Creating LAN segment '{name}' with description '{description}'")
            response = self.api.v1_global_lan_segments_post(
                authorization=self.bearer_token,
                v1_global_lan_segments_post_request=post_lan_segments_request
            )
            LOG.info(f"post_global_lan_segments: Successfully created LAN segment '{name}' with ID: {response.id}")
            return response
        except ApiException as e:
            api_url = f"{self.api.api_client.configuration.host}/v1/global/lan-segments"
            self._log_api_error(
                method_name="post_global_lan_segments",
                api_url=api_url,
                request_body={"name": name, "description": description},
                exception=e
            )
            raise

    def delete_global_lan_segments(self, lan_segment_id: int):
        """
        Delete a global LAN segment.

        Args:
            lan_segment_id (int): ID of the LAN segment to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            LOG.info(f"delete_global_lan_segments: Deleting LAN segment with ID: {lan_segment_id}")
            # Use the correct method name from the SDK
            self.api.v1_global_lan_segments_id_delete(
                authorization=self.bearer_token,
                id=lan_segment_id
            )
            # DELETE operations typically return 204 (No Content) or empty response
            # We consider any successful call (no exception) as success
            LOG.info(f"delete_global_lan_segments: Successfully deleted LAN segment with ID: {lan_segment_id}")
            return True
        except Exception as e:
            # Check if it's a validation error that we can ignore
            if "validation error" in str(e) and "V1GlobalLanSegmentsPost200Response" in str(e):
                LOG.info(f"delete_global_lan_segments: Delete operation completed "
                         f"(validation error can be ignored): {lan_segment_id}")
                return True
            else:
                LOG.error(f"delete_global_lan_segments: Got Exception while deleting LAN segment {lan_segment_id}: {e}")
                return False

    def get_global_lan_segments(self):
        """
        Get all global LAN segments.

        Returns:
            list: List of global LAN segments
        """
        try:
            response = self.api.v1_global_lan_segments_get(authorization=self.bearer_token)
            LOG.debug(f"get_global_lan_segments: {response}")
            # Ensure we always return a list, even if entries is None
            if hasattr(response, 'entries') and response.entries is not None:
                return response.entries
            else:
                LOG.info("get_global_lan_segments: No LAN segments found or entries is None")
                return []
        except ApiException as e:
            api_url = f"{self.api.api_client.configuration.host}/v1/global/lan-segments"
            self._log_api_error(
                method_name="get_global_lan_segments",
                api_url=api_url,
                exception=e
            )
            return []

    def get_lan_segment_id(self, lan_segment_name):
        """
        Retrieve the lan segment ID based on the lan segment name.

        Args:
            lan_segment_name (str): The name of the lan segment (e.g., 'lan-7-test')

        Returns:
            int or None: The ID of the lan segment if found, None otherwise.
        """
        output = self.get_global_lan_segments()
        for lan_segment_obj in output:
            if lan_segment_obj.name == lan_segment_name:
                return lan_segment_obj.id
        return None

    def get_lan_segments_dict(self):
        """
        Retrieve all lan segments as a dictionary mapping names to IDs.

        Returns:
            dict: A dictionary mapping lan segment names to their IDs.
        """
        output = self.get_global_lan_segments()
        lan_segments = {}
        for lan_segment_obj in output:
            lan_segments[lan_segment_obj.name] = lan_segment_obj.id
        return lan_segments

    # Site Lists API methods

    def create_global_site_list(self, site_list_config: dict):
        """
        Create a global site list.
        """
        try:
            LOG.info(f"create_global_site_list: Creating site list '{site_list_config.get('name')}'")
            response = self.api.v1_global_site_lists_post(
                authorization=self.bearer_token,
                v1_global_site_lists_post_request=site_list_config
            )
            LOG.info(f"create_global_site_list: Successfully created site list with ID: {response.id}")
            return response
        except ApiException as e:
            LOG.error(f"create_global_site_list: Got Exception while creating site list: {e}")
            raise e

    def delete_global_site_list(self, site_list_id: int):
        """
        Delete a global site list.
        """
        try:
            LOG.info(f"delete_global_site_list: Deleting site list with ID: {site_list_id}")
            self.api.v1_global_site_lists_id_delete(
                authorization=self.bearer_token,
                id=site_list_id
            )
            LOG.info(f"delete_global_site_list: Successfully deleted site list with ID: {site_list_id}")
            return True
        except Exception as e:
            # Handle validation errors for DELETE operations (often return empty responses)
            if "validation error" in str(e) and "V1GlobalLanSegmentsPost200Response" in str(e):
                LOG.info(f"delete_global_site_list: "
                         f"Delete operation completed (validation error can be ignored): {site_list_id}")
                return True
            LOG.error(f"delete_global_site_list: Got Exception while deleting site list {site_list_id}: {e}")
            return False

    def get_global_site_lists(self):
        """
        Get all global site lists.
        """
        try:
            LOG.info("get_global_site_lists: Retrieving all global site lists")
            response = self.api.v1_global_site_lists_get(
                authorization=self.bearer_token
            )
            if response and hasattr(response, 'entries') and response.entries:
                LOG.info(f"get_global_site_lists: Successfully retrieved {len(response.entries)} site lists")
                return response.entries
            else:
                LOG.info("get_global_site_lists: No site lists found")
                return []
        except ApiException as e:
            LOG.error(f"get_global_site_lists: Got Exception while retrieving site lists: {e}")
            return []

    def get_global_site_list(self, site_list_id: int):
        """
        Get a specific global site list by ID.
        """
        try:
            LOG.info(f"get_global_site_list: Retrieving site list with ID: {site_list_id}")
            response = self.api.v1_global_site_lists_id_get(
                authorization=self.bearer_token,
                id=site_list_id
            )
            LOG.info("get_global_site_list: Successfully retrieved site list")
            return response
        except ApiException as e:
            LOG.error(f"get_global_site_list: Got Exception while retrieving site list {site_list_id}: {e}")
            raise e

    def get_site_list_id(self, site_list_name: str):
        """
        Get site list ID by name.
        """
        try:
            site_lists = self.get_global_site_lists()
            for site_list in site_lists:
                if site_list.name == site_list_name:
                    return site_list.id
            return None
        except Exception as e:
            LOG.error(f"get_site_list_id: Error finding site list '{site_list_name}': {e}")
            return None

    # Data Exchange API Methods

    def create_data_exchange_services(self, service_config: dict):
        """
        Create a new Data Exchange service.

        Args:
            service_config (dict): Service configuration containing:
                - serviceName: Service name
                - type: Service type (e.g., "peering_service")
                - policy: Service policy configuration

        Returns:
            dict: Created service response
        """
        try:
            LOG.info(f"create_data_exchange_services: Creating service '{service_config.get('serviceName')}'")
            response = self.api.v1_extranets_b2b_peering_producer_post(
                authorization=self.bearer_token,
                v1_extranets_b2b_peering_producer_post_request=service_config
            )
            LOG.info(f"create_data_exchange_services: Successfully created service with ID: {response.id}")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL and request body for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b-peering/producer"
            self._log_api_error(
                method_name="create_data_exchange_services",
                api_url=api_url,
                request_body=service_config,
                exception=e
            )
            raise e

    def get_data_exchange_services_summary(self):
        """
        Get summary of all Data Exchange services.

        Returns:
            dict: Services summary response
        """
        try:
            LOG.info("get_data_exchange_services_summary: Retrieving services summary")
            response = self.api.v1_extranets_b2b_general_services_summary_get(
                authorization=self.bearer_token
            )
            services_count = len(response.info) if response.info else 0
            LOG.info(f"get_data_exchange_services_summary: Successfully retrieved {services_count} services")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b-general/services-summary"
            self._log_api_error(
                method_name="get_data_exchange_services_summary",
                api_url=api_url,
                exception=e
            )
            raise e

    def get_data_exchange_service_by_name(self, service_name: str):
        """
        Get a specific Data Exchange service by name.

        Args:
            service_name (str): Name of the service to retrieve

        Returns:
            dict: Service details or None if not found
        """
        try:
            LOG.info(f"get_data_exchange_service_by_name: Looking for service '{service_name}'")
            services_summary = self.get_data_exchange_services_summary()

            # Handle case where services list is None
            if not services_summary.info:
                LOG.info("get_data_exchange_service_by_name: No services found")
                return None

            for service in services_summary.info:
                if service.name == service_name:
                    LOG.info(f"get_data_exchange_service_by_name: Found service '{service_name}' with ID: {service.id}")
                    return service

            LOG.info(f"get_data_exchange_service_by_name: Service '{service_name}' not found")
            return None
        except Exception as e:
            LOG.error(f"get_data_exchange_service_by_name: Error finding service '{service_name}': {e}")
            return None

    def create_data_exchange_customers(self, customer_config: dict):
        """
        Create a new Data Exchange customer.

        Args:
            customer_config (dict): Customer configuration containing:
                - name: Customer name
                - type: Customer type (e.g., "non_graphiant_peer")
                - invite: Customer invite configuration

        Returns:
            dict: Created customer response
        """
        try:
            LOG.info(f"create_data_exchange_customers: Creating customer '{customer_config.get('name')}'")
            response = self.api.v1_extranets_b2b_peering_customer_post(
                authorization=self.bearer_token,
                v1_extranets_b2b_peering_customer_post_request=customer_config
            )
            LOG.info(f"create_data_exchange_customers: Successfully created customer with ID: {response.id}")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL and request body for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b-peering/customer"
            self._log_api_error(
                method_name="create_data_exchange_customers",
                api_url=api_url,
                request_body=customer_config,
                exception=e
            )
            raise e

    def get_data_exchange_customers_summary(self):
        """
        Get summary of all Data Exchange customers.

        Returns:
            dict: Customers summary response
        """
        try:
            LOG.info("get_data_exchange_customers_summary: Retrieving customers summary")
            response = self.api.v1_extranets_b2b_general_customers_summary_get(
                authorization=self.bearer_token
            )
            customers_count = len(response.customers) if response.customers else 0
            LOG.info(f"get_data_exchange_customers_summary: Successfully retrieved {customers_count} customers")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b-general/customers-summary"
            self._log_api_error(
                method_name="get_data_exchange_customers_summary",
                api_url=api_url,
                exception=e
            )
            raise e

    def get_data_exchange_customer_by_name(self, customer_name: str):
        """
        Get a specific Data Exchange customer by name.

        Args:
            customer_name (str): Name of the customer to retrieve

        Returns:
            dict: Customer details or None if not found
        """
        try:
            LOG.info(f"get_data_exchange_customer_by_name: Looking for customer '{customer_name}'")
            customers_summary = self.get_data_exchange_customers_summary()

            # Handle case where customers list is None
            if not customers_summary.customers:
                LOG.info("get_data_exchange_customer_by_name: No customers found")
                return None

            for customer in customers_summary.customers:
                if customer.name == customer_name:
                    LOG.info(f"get_data_exchange_customer_by_name: Found customer '{customer_name}' "
                             f"with ID: {customer.id}")
                    return customer

            LOG.info(f"get_data_exchange_customer_by_name: Customer '{customer_name}' not found")
            return None
        except Exception as e:
            LOG.error(f"get_data_exchange_customer_by_name: Error finding customer '{customer_name}': {e}")
            return None

    def delete_data_exchange_customer(self, customer_id: int):
        """
        Delete a Data Exchange customer.

        Args:
            customer_id (int): ID of the customer to delete

        Returns:
            dict: Delete response
        """
        try:
            LOG.info(f"delete_data_exchange_customer: Deleting customer with ID: {customer_id}")
            response = self.api.v1_extranets_b2b_peering_customer_id_delete(
                authorization=self.bearer_token,
                id=customer_id
            )
            LOG.info(f"delete_data_exchange_customer: Successfully deleted customer with ID: {customer_id}")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b-peering/customer/{customer_id}"
            self._log_api_error(
                method_name="delete_data_exchange_customer",
                api_url=api_url,
                path_params={"customer_id": customer_id},
                exception=e
            )
            raise e

    def get_data_exchange_service_details(self, service_id: int, type: str = "peering_service"):
        """
        Get detailed information about a specific Data Exchange service.

        Args:
            service_id (int): ID of the service to retrieve
            type (str): Type of service to retrieve (default: "peering_service")

        Returns:
            dict: Service details response
        """
        try:
            LOG.info(f"get_data_exchange_service_details: Retrieving service details for ID: {service_id}")
            response = self.api.v1_extranets_b2b_id_producer_get(
                authorization=self.bearer_token,
                id=service_id,
                type=type
            )
            LOG.info(f"get_data_exchange_service_details: Successfully retrieved service details for ID: {service_id}")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL with path and query parameters for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b/{service_id}/producer"
            self._log_api_error(
                method_name="get_data_exchange_service_details",
                api_url=api_url,
                path_params={"service_id": service_id},
                query_params={"type": type},
                exception=e
            )
            raise e

    def match_service_to_customer(self, match_config: dict):
        """
        Match a service to a customer with specific prefix configurations.

        Args:
            match_config (dict): Match configuration containing:
                - id: Customer ID
                - service: Service configuration with prefixes and NAT settings

        Returns:
            dict: Match response with matchId
        """
        try:
            LOG.info("match_service_to_customer: Matching service to customer")
            response = self.api.v1_extranets_b2b_peering_match_service_to_customer_post(
                authorization=self.bearer_token,
                v1_extranets_b2b_peering_match_service_to_customer_post_request=match_config
            )
            LOG.info(
                f"match_service_to_customer: "
                f"Successfully matched service to customer with matchId: {response.match_id}")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL and request body for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b-peering/match/service-to-customer"
            self._log_api_error(
                method_name="match_service_to_customer",
                api_url=api_url,
                request_body=match_config,
                exception=e
            )
            raise e

    def delete_data_exchange_service(self, service_id: int):
        """
        Delete a Data Exchange service.

        Args:
            service_id (int): ID of the service to delete

        Returns:
            dict: Delete response
        """
        try:
            LOG.info(f"delete_data_exchange_service: Deleting service with ID: {service_id}")
            response = self.api.v1_extranets_b2b_id_delete(
                authorization=self.bearer_token,
                id=service_id
            )
            LOG.info(f"delete_data_exchange_service: Successfully deleted service with ID: {service_id}")
            return response
        except ApiException as e:
            # Log the actual API endpoint URL for debugging
            api_url = f"{self.api.api_client.configuration.host}/v1/extranets-b2b/{service_id}"
            self._log_api_error(
                method_name="delete_data_exchange_service",
                api_url=api_url,
                path_params={"service_id": service_id},
                exception=e
            )
            raise e
