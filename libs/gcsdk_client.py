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

    def get_global_lan_segments(self):
        """
        Get all edges summary from GCS.

        Args:
            device_id (int, optional): The device ID to filter edges.
            If not provided, returns all edges.

        Returns:
            list or dict: A list of all edges info if no device_id is provided,
            or a single edge's information if a device_id is provided.
        """
        response = self.api.v1_global_lan_segments_get(authorization=self.bearer_token)
        return response.entries

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
        Get site ID by site name.

        Args:
            site_name (str): The name of the site.

        Returns:
            int or None: The site ID if found, None otherwise.
        """
        try:
            # Get all sites
            response = self.api.v1_sites_get(authorization=self.bearer_token)
            sites = response.sites
            LOG.debug(f"get_site_id: Looking for site '{site_name}' in {len(sites)} sites")
            for site in sites:
                if site.name == site_name:
                    LOG.debug(f"get_site_id: Found site '{site_name}' with ID {site.id}")
                    return site.id
            LOG.debug(f"get_site_id: Site '{site_name}' not found")
            return None
        except ApiException as e:
            LOG.error(f"get_site_id: Got Exception while getting site ID for {site_name}: {e}")
            return None
