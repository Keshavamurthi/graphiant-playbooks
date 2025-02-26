import os
from concurrent.futures import Future, wait
from concurrent.futures.thread import ThreadPoolExecutor
from gcsdk_client import GcsdkClient
from typing import Sequence

class PortalUtils(object):

    def __init__(self, base_url=None, username=None, password=None):
        cwd = os.getcwd()
        self.ansible_playbook_path = cwd + \
        "/graphiant-playbooks/ansible/collections/ansible_collections/graphiant/portal/playbooks"
        self.templates_path = self.ansible_playbook_path + "/templates/"
        self.artefacts_path = self.ansible_playbook_path + "/artefacts/"
        #self.templates_path = cwd + "/../templates/"
        #self.artefacts_path = cwd + "/../artefacts/"
        self.gcsdk = GcsdkClient(base_url=base_url, username=username, password=password)

    def update_device_bringup_status(self, device_id, status):
        result = self.gcsdk.put_devices_bringup(device_ids=[device_id], status=status)
        return result

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
            print(f"{len(not_done)} futures did not finish running")

        for future in futures:
            try:
                if future:
                    future.result(timeout=0)
            except Exception as e:
                print(f"future failed: {e}")