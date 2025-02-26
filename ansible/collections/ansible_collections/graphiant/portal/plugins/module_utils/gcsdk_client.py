import swagger_client
from json import loads
from poller import poller
import time

class GcsdkClient():

    def __init__(self, base_url=None, username=None, password=None):
        self.swagger_client = swagger_client
        self.config = self.swagger_client.Configuration()
        if base_url and username and password:
            self.config.host = base_url
            self.config.username = username
            self.config.password = password
        self.api = self.swagger_client.DefaultApi(swagger_client.ApiClient(self.config))
        #print(self.config.username, self.config.password)
        auth_login_body = self.swagger_client.AuthLoginBody(username=self.config.username, password=self.config.password)
        response = self.api.v1_auth_login_post(body=auth_login_body, _preload_content=False)
        self.token = loads(response.data).get("token")
        self.bearer_token = 'Bearer ' + self.token

    def get_all_enterprises(self):
        """
        Get All Enterprises On GCS
        Class Object EnterpriseMembers has a List of Individual Objects EnterpriseMember
        """
        enterprises = self.api.v1_enterprises_get(authorization=self.bearer_token)
        return enterprises

    def get_edges_summary(self, device_id=None):
        response = self.api.v1_edges_summary_get(authorization=self.bearer_token)
        if device_id:
            for edge_info in response.edges_summary:
                if edge_info.device_id == str(device_id):
                    return edge_info
        return response.edges_summary

    @poller(retries=12, wait=10)
    def put_device_config(self, device_id: int, core=None, edge=None):
        """
        Put Devices Config
        """
        body = swagger_client.DeviceIdConfigBody(core=core, edge=edge)
        try:
            edge_summary = self.get_edges_summary(device_id=device_id)
            if edge_summary.portal_status == "Ready":
                print(f"config to be pushed : {body}")
                response = self.api.v1_devices_device_id_config_put(authorization=self.bearer_token, 
                                                                    device_id=device_id, body=body)
                return response
            else:
                print(f"Retrying,  {device_id} Portal Status: {edge_summary.portal_status} (Expected Ready)")
                assert False, f"Retrying,  {device_id} Portal Status: {edge_summary.portal_status} (Expected Ready)"
        except self.swagger_client.rest.ApiException as e:
            print(f"Exception While config push {e}")
            assert False, f"Retrying, Exception while config push to {device_id}"
    
    def post_devices_bringup(self, device_ids):
        data = {'deviceIds': device_ids}
        response = self.api.v1_devices_bringup_post(authorization=self.bearer_token, body=data)
        return response

    def put_devices_bringup(self, device_ids, status):
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
            self.api.v1_devices_bringup_put(authorization=self.bearer_token, body=data)
            time.sleep(15)
            return True
        except self.swagger_client.rest.ApiException:
            return False
