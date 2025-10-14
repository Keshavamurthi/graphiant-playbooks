"""
Logging decorator for Ansible modules to capture detailed library logs
"""
import logging
import io
import functools


def capture_library_logs(func):
    """
    Decorator to capture and return detailed library logs for Ansible modules.

    This decorator:
    1. Captures all INFO level logs from the library
    2. Appends them to the result message if detailed logging is enabled
    3. Can be controlled via module parameter 'detailed_logs'

    Usage:
        @capture_library_logs
        def some_operation(module, *args, **kwargs):
            # Your operation code here
            pass
    """
    @functools.wraps(func)
    def wrapper(module, *args, **kwargs):
        # Check if detailed logging is enabled
        detailed_logs = module.params.get('detailed_logs', False)

        if not detailed_logs:
            # If detailed logging is disabled, just run the function normally
            return func(module, *args, **kwargs)

        # Note: For best output formatting with detailed_logs, set:
        # export ANSIBLE_STDOUT_CALLBACK=debug
        # This ensures clean output without literal \n characters

        # Set up logging capture
        log_capture = io.StringIO()

        # Custom handler that writes to our buffer
        class LogCaptureHandler(logging.Handler):
            def __init__(self, buffer):
                super().__init__()
                self.buffer = buffer

            def emit(self, record):
                self.buffer.write(self.format(record) + '\n')

        # Create and configure the handler
        log_handler = LogCaptureHandler(log_capture)
        log_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler.setFormatter(formatter)

        # Get the library logger and add our handler
        try:
            from libs.logger import setup_logger
            LOG = setup_logger()
            LOG.addHandler(log_handler)
        except ImportError:
            # If logger import fails, continue without logging
            log_handler = None

        try:
            # Execute the original function
            result = func(module, *args, **kwargs)

            # Capture the logs
            if log_handler:
                captured_logs = log_capture.getvalue()
                if captured_logs and 'result_msg' in result:
                    result['result_msg'] += f"\n\nDetailed logs:\n{captured_logs}"

            return result

        except Exception as e:
            # Capture logs even when exception occurs
            if log_handler:
                captured_logs = log_capture.getvalue()
                if captured_logs:
                    # Add logs to the exception message for better debugging
                    import traceback
                    full_traceback = traceback.format_exc()
                    enhanced_message = f"{str(e)}\n\nDetailed logs before exception:\n{captured_logs}"
                    # Create a new exception with enhanced message (without full traceback to avoid duplication)
                    new_exception = type(e)(enhanced_message)
                    new_exception.__cause__ = e
                    raise new_exception
            raise

        finally:
            # Clean up the handler
            if log_handler:
                try:
                    LOG.removeHandler(log_handler)
                except Exception:
                    pass
                log_capture.close()

    return wrapper
