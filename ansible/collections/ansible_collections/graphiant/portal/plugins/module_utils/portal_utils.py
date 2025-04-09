import os
import yaml
from concurrent.futures import Future, wait
from concurrent.futures.thread import ThreadPoolExecutor
from .logger import setup_logger
from .gcsdk_client import GcsdkClient
from typing import Sequence

LOG = setup_logger()

class PortalUtils(object):

    def __init__(self, base_url=None, username=None, password=None):
        cwd = os.getcwd()
        self.ansible_playbook_path = cwd
        self.config_path = self.ansible_playbook_path + "/configs/"
        self.artefacts_path = self.ansible_playbook_path + "/artefacts/"
        self.config_templates_path = self.ansible_playbook_path + "/../../plugins/module_utils/config_templates/"
        self.logs_path = self.ansible_playbook_path + "/logs/"
        LOG.info(f"PortalUtils : templates_path : {self.config_path}")
        LOG.info(f"PortalUtils : artefacts_path : {self.artefacts_path}")
        LOG.info(f"PortalUtils : config_templates : {self.config_templates_path}")
        LOG.info(f"PortalUtils : logs_path : {self.logs_path}")
        self.gcsdk = GcsdkClient(base_url=base_url, username=username, password=password)

    def concurrent_task_execution(self, function, config_dict):
        output_dict = {}
        with ThreadPoolExecutor(max_workers=150) as executor:
            for device_id, device_config in config_dict.items():
                output_dict[device_id] = executor.submit(function, **device_config)
            self.wait_checked(list(future for future in output_dict.values()))
        return output_dict

    @staticmethod
    def wait_checked(posible_futures: Sequence[Future | None]) -> None:
        """ Wait for a set of futures to complete, and log an error for
        each future that failed """
        # Remove None from list. It got None in list due to ssh failures.
        futures = [item for item in posible_futures if item is not None]
        print(f"Waiting for futures {futures} to complete")
        (_done, not_done) = wait(futures)
        # If called with default arguments, `wait` should only return when
        # all the futures completed
        if not_done:
            LOG.warning(f"{len(not_done)} futures did not finish running")

        for future in futures:
            try:
                if future:
                    future.result(timeout=0)
            except Exception as e:
                LOG.error(f"future failed: {e}")

    def update_device_bringup_status(self, device_id, status):
        result = self.gcsdk.put_devices_bringup(device_ids=[device_id], status=status)
        return result

    def update_multiple_devices_bringup_status(self, yaml_file):
        input_file_path = self.config_path + yaml_file
        input_dict = {}
        with open(input_file_path, "r") as file:
            config_data = yaml.safe_load(file)
            for device_name, config in config_data.items():
                device_id = self.get_device_id(device_name=device_name)
                input_dict[device_id] = {"device_id": device_id, "status": config["status"]}
            self.concurrent_task_execution(self.update_device_bringup_status, input_dict)

    def get_device_id(self, device_name):
        output = self.gcsdk.get_edges_summary()
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
        output = self.gcsdk.get_edges_summary()
        for device_info in output:
            LOG.debug(f"get_enterprise_id : {device_info.enterprise_id}")
            return device_info.enterprise_id
