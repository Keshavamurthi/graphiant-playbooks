import os
import yaml
from concurrent.futures import wait
from concurrent.futures.thread import ThreadPoolExecutor
from libs.logger import setup_logger
from libs.gcsdk_client import GraphiantPortalClient
from libs.exceptions import ConfigurationError

LOG = setup_logger()


class PortalUtils(object):

    def __init__(self, base_url=None, username=None, password=None):
        # Find the project root directory by looking for the libs directory
        project_root = self._find_project_root()

        self.config_path = os.path.join(project_root, "configs") + "/"
        self.templates = os.path.join(project_root, "templates") + "/"
        self.logs_path = os.path.join(project_root, "logs") + "/"

        LOG.info(f"PortalUtils : project_root : {project_root}")
        LOG.info(f"PortalUtils : templates_path : {self.config_path}")
        LOG.info(f"PortalUtils : config_templates : {self.templates}")
        LOG.info(f"PortalUtils : logs_path : {self.logs_path}")
        self.gsdk = GraphiantPortalClient(base_url=base_url, username=username, password=password)
        self.gsdk.set_bearer_token()

    def _find_project_root(self) -> str:
        """
        Find the project root directory using a systematic approach with the following priority:
        1. Check user-configured GRAPHIANT_PLAYBOOKS_PATH environment variable (highest priority)
        2. Check PYTHONPATH for graphiant-playbooks directory
        3. Check current working directory
        4. Find Git repository root and look for the directory there
        5. Walk up from the current file location to find the directory (fallback)

        Returns:
            str: Path to the project root directory
        """
        # Method 1: Check user-configured GRAPHIANT_PLAYBOOKS_PATH environment variable (highest priority)
        user_playbooks_path = os.environ.get('GRAPHIANT_PLAYBOOKS_PATH')
        if user_playbooks_path and os.path.exists(user_playbooks_path):
            LOG.debug(f"Found project root via GRAPHIANT_PLAYBOOKS_PATH: {user_playbooks_path}")
            return user_playbooks_path

        # Method 2: Check PYTHONPATH for graphiant-playbooks directory
        pythonpath = os.environ.get('PYTHONPATH', '')
        for path in pythonpath.split(os.pathsep):
            if path and os.path.exists(path):
                # Check if this path contains the graphiant-playbooks directory
                if 'graphiant-playbooks' in path:
                    LOG.debug(f"Found project root via PYTHONPATH: {path}")
                    return path
                # Also check if this path is the project root (contains libs, configs, etc.)
                if (os.path.exists(os.path.join(path, 'libs')) and os.path.exists(os.path.join(path, 'configs'))):
                    LOG.debug(f"Found project root via PYTHONPATH (contains libs/configs): {path}")
                    return path

        # Method 3: Check current working directory
        if (os.path.exists(os.path.join(os.getcwd(), 'libs')) and os.path.exists(os.path.join(os.getcwd(), 'configs'))):
            LOG.debug(f"Found project root in current working directory: {os.getcwd()}")
            return os.getcwd()

        # Method 4: Find Git repository root and look for the directory there
        current_dir = os.getcwd()
        for _ in range(10):  # Walk up to 10 levels
            git_path = os.path.join(current_dir, '.git')
            if os.path.exists(git_path):
                LOG.debug(f"Found project root at Git repository: {current_dir}")
                return current_dir
            current_dir = os.path.dirname(current_dir)

        # Method 5: Walk up from the current file location (fallback)
        current_dir = os.path.dirname(__file__)
        for _ in range(10):  # Walk up to 10 levels
            if (os.path.exists(os.path.join(current_dir, 'libs')) and os.path.exists(os.path.join(current_dir,
                                                                                                  'configs'))):
                LOG.debug(f"Found project root by walking up from file location: {current_dir}")
                return current_dir
            current_dir = os.path.dirname(current_dir)

        # Final fallback to current working directory if nothing else works
        LOG.warning("Could not find project root using any method, using current working directory")
        return os.getcwd()

    def concurrent_task_execution(self, function, config_dict):
        """
        Executes a function concurrently using ThreadPoolExecutor for each key-value in config_dict.
        The value must be a dict of kwargs to pass to the function.

        :param function: Callable function to be executed concurrently
        :param config_dict: Dict with keys as identifiers and values as kwargs for the function
        :return: Dict with keys as original keys and values as Future objects
        """
        output_dict = {}
        with ThreadPoolExecutor(max_workers=150) as executor:
            for key, value in config_dict.items():
                output_dict[key] = executor.submit(function, **value)
            self.wait_checked(list(future for future in output_dict.values()))
        return output_dict

    @staticmethod
    def wait_checked(posible_futures):
        """
        Waits for a set of futures to complete, logging errors for those that fail.

        :param possible_futures: List of futures (may include None)
        """
        futures = [item for item in posible_futures if item is not None]
        LOG.debug(f"Waiting for futures {futures} to complete")
        (_done, not_done) = wait(futures)

        if not_done:
            LOG.warning(f"{len(not_done)} futures did not finish running")
        failures = []
        for future in futures:
            try:
                if future:
                    future.result(timeout=0)
            except Exception as e:
                failures.append(e)
        if failures:
            raise Exception(f"futures failed: {failures}")

    def update_device_bringup_status(self, device_id, status):
        """
        Update the device bringup status via GCSDK APIs.

        :param device_id: str - The ID of the device to update
        :param status: str - New status to set
        :return: Response from GCSDK
        """
        result = self.gsdk.put_devices_bringup(device_ids=[device_id], status=status)
        return result

    def update_multiple_devices_bringup_status(self, yaml_file):
        """
        Update the multiple device bringup status concurrently via GCSDK APIs.

        :param yaml_file: Contains list of devices and expected device status
        :return: None
        """
        input_file_path = self.config_path + yaml_file
        input_dict = {}
        with open(input_file_path, "r") as file:
            config_data = yaml.safe_load(file)
            for device_name, config in config_data.items():
                device_id = self.gsdk.get_device_id(device_name=device_name)
                input_dict[device_id] = {"device_id": device_id, "status": config["status"]}
            self.concurrent_task_execution(self.update_device_bringup_status, input_dict)

    def render_config_file(self, yaml_file):
        """
        Load a YAML configuration file from the config path.

        Args:
            yaml_file (str): The filename of the YAML config (can be absolute or relative).

        Returns:
            dict: Parsed configuration data.

        Logs Warning:
            FileNotFoundError: If the file doesn't exist.
        """
        # Handle absolute paths
        if os.path.isabs(yaml_file):
            input_file_path = yaml_file
        else:
            # Handle relative paths by concatenating with config_path
            input_file_path = self.config_path + yaml_file

        try:
            with open(input_file_path, "r") as file:
                config_data = yaml.safe_load(file)
            return config_data
        except FileNotFoundError:
            LOG.warning(f"File not found : {input_file_path}")
        except yaml.YAMLError as e:
            # Provide user-friendly YAML error messages
            if hasattr(e, 'problem_mark'):
                line_num = e.problem_mark.line + 1
                col_num = e.problem_mark.column + 1
                error_msg = f"YAML syntax error in '{input_file_path}' at line {line_num}, column {col_num}:\n"
                error_msg += f"  {str(e)}\n"
                error_msg += f"Please check the YAML syntax around line {line_num} " \
                             "and fix any indentation or formatting issues."
                raise ConfigurationError(error_msg)
            else:
                raise ConfigurationError(f"YAML parsing error in '{input_file_path}': {str(e)}")
        except Exception as e:
            raise ConfigurationError(f"Error reading configuration file '{input_file_path}': {str(e)}")
