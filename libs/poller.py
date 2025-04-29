import functools
import sys
import time
import traceback
from future.utils import raise_
from .logger import setup_logger

LOG = setup_logger()


def poller(timeout=60, wait=0.1, retries=None):
    """
    Returns a decorator that adds polling to the decorated function or method

    e.g.
    @poller(timeout=1, wait=0.2)
    def random_number_picker_max_timeout(number, numbers):
        assert number == random.choice(numbers)

    2022-09-13 14:48:30,799.799 - test.lib.poller - INFO: Poller attempt: 1
    2022-09-13 14:48:30,799.799 - test.lib.poller - INFO: Poller time remaining: 0.9998311996459961 seconds
    2022-09-13 14:48:30,800.800 - test.lib.poller - INFO: Calling method random_number_picker_max_timeout()...
    2022-09-13 14:48:30,800.800 - test.lib.poller - INFO: Exception caught while calling method
    2022-09-13 14:48:30,800.800 - test.lib.poller - INFO: Sleeping for 0.2 seconds before poller re-attempt...
    2022-09-13 14:48:31,005.005 - test.lib.poller - INFO: Poller attempt: 2
    2022-09-13 14:48:31,005.005 - test.lib.poller - INFO: Poller time remaining: 0.7942500114440918 seconds
    2022-09-13 14:48:31,005.005 - test.lib.poller - INFO: Calling method random_number_picker_max_timeout()...



    @poller(retries=5, wait=0.2)
    def random_number_picker_max_reties(number, numbers):
        assert number == random.choice(numbers)

    test.random_number_picker_max_reties()
    2022-09-13 14:46:30,981.981 - test.lib.poller - INFO: Poller attempt: 1/5
    2022-09-13 14:46:30,981.981 - test.lib.poller - INFO: Calling method random_number_picker_max_reties()...
    2022-09-13 14:46:30,981.981 - test.lib.poller - INFO: Exception caught while calling method
    2022-09-13 14:46:30,982.982 - test.lib.poller - INFO: Sleeping for 0.2 seconds before retry...
    2022-09-13 14:46:31,185.185 - test.lib.poller - INFO: Poller attempt: 2/5
    2022-09-13 14:46:31,186.186 - test.lib.poller - INFO: Calling method random_number_picker_max_reties()...
    2022-09-13 14:46:31,186.186 - test.lib.poller - INFO: Exception caught while calling method
    2022-09-13 14:46:31,186.186 - test.lib.poller - INFO: Sleeping for 0.2 seconds before retry...
    2022-09-13 14:46:31,387.387 - test.lib.poller - INFO: Poller attempt: 3/5
    2022-09-13 14:46:31,388.388 - test.lib.poller - INFO: Calling method random_number_picker_max_reties()...
    2022-09-13 14:46:31,388.388 - test.lib.poller - INFO: Exception caught while calling method
    2022-09-13 14:46:31,388.388 - test.lib.poller - INFO: Sleeping for 0.2 seconds before retry...
    2022-09-13 14:46:31,592.592 - test.lib.poller - INFO: Poller attempt: 4/5
    2022-09-13 14:46:31,592.592 - test.lib.poller - INFO: Calling method random_number_picker_max_reties()...
    2022-09-13 14:46:31,592.592 - test.lib.poller - INFO: Exception caught while calling method
    2022-09-13 14:46:31,592.592 - test.lib.poller - INFO: Sleeping for 0.2 seconds before retry...
    2022-09-13 14:46:31,796.796 - test.lib.poller - INFO: Poller attempt: 5/5
    2022-09-13 14:46:31,796.796 - test.lib.poller - INFO: Calling method random_number_picker_max_reties()...
    """

    def poller_decorator(fun):
        """
        Decorator that adds polling to the decorated function or method
        """

        @functools.wraps(fun)
        def timeout_poller(fun, timeout, wait, *fun_args, **fun_kwargs):
            """
            Wraps a function inside a timeout polling loop
            """
            start_time = time.time()
            attempt = 0
            exc = None
            while (time.time() - start_time) < timeout:
                remain = timeout - (time.time() - start_time)
                LOG.info(f'{fun.__module__}.{fun.__name__}(): attempt {attempt+1}, time remaining {remain:.2f}s')
                try:
                    return fun(*fun_args, **fun_kwargs)
                except Exception as e:
                    exc = sys.exc_info()
                    LOG.info(f'Exception caught while calling method {fun.__name__}(): {e!r}')
                LOG.info(f'Sleeping for {wait} seconds before poller re-attempt...')
                time.sleep(wait)
                attempt += 1
            if exc:
                LOG.warning(''.join(traceback.format_exception(*exc)))
                raise_(exc[0], exc[1], exc[2])
            return False

        @functools.wraps(fun)
        def retry_poller(fun, retries, wait, *fun_args, **fun_kwargs):
            """
            Wraps a function inside a retry polling loop
            """
            exc = None
            for attempt in range(0, retries):
                LOG.info(f'Poller attempt: {attempt + 1}/{retries}')
                LOG.info(f'Calling method {fun.__name__}()...')
                try:
                    return fun(*fun_args, **fun_kwargs)
                except Exception as e:
                    exc = sys.exc_info()
                    LOG.info(f'Exception caught while calling method {fun.__name__}(): {e}')
                LOG.info(f'Sleeping for {wait} seconds before retry...')
                time.sleep(wait)
            if exc:
                LOG.warning(''.join(traceback.format_exception(*exc)))
                raise_(exc[0], exc[1], exc[2])
            return False

        def pick_a_poller(*args, **kwargs):
            if retries is not None:
                return retry_poller(fun, retries, wait, *args, **kwargs)
            else:
                return timeout_poller(fun, timeout, wait, *args, **kwargs)

        # Return decorated function
        return pick_a_poller

    # Return decorator
    return poller_decorator
