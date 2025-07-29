import logging
import importlib.util
import os
import sys
import json
import traceback
from types import ModuleType
from loguru import logger
from typing import Callable, List, TypeVar, Union, Any
from functools import wraps
from contextlib import redirect_stdout
from sfchecks.logger import InterceptHandler
from sfchecks.types import CheckResult


def check(func: Callable[[], CheckResult | None]) -> Callable[..., CheckResult]:
    """
    Decorator for the root level `check()` method in a `flag.py`.

    - Replaces normal logging calls with loguru logs.
    - Redirects stdout to stderr
    - Prints results/status when `flag.py` is run directly

    Args:
        func: A function taking no parameters that returns either a `CheckResult` or `None`.

    Returns:
        If a `CheckResult` is returned from `func`, then it returns that.
        On Exceptions or if None is returned, broken-functionality is returned.
    """
    _configure_logging()

    def wrapper() -> CheckResult:
        try:
            was_ran_directly = _was_ran_directly()

            with redirect_stdout(sys.stderr):
                result = func()
            if result is None:
                logging.debug("No status returned, defaulting to broken-functionality")
                result = "broken-functionality"
            if was_ran_directly:
                print_results(result)
            return result
        except Exception as e:
            logger.error(
                "Check raised an Exception, defaulting to broken-functionality"
            )
            logging.exception(e)
            return "broken-functionality"

    return wrapper


def run_checks(
    checks: List[Callable[..., CheckResult | None]],
) -> CheckResult | None:
    """
    Executes a list of `Callable[..., CheckResult | None]`, returning the
    status of the first not to return None.

    Args:
        checks: checks to run

    Returns:
        The status of the first check to return True, else
        None
    """
    results = map(lambda f: f(), checks)
    result = next((result for result in results if result is not None), None)
    if result is not None:
        return result

    logger.debug("No check resolved True, returning None")
    return None


def check_for(
    status: str, function: Callable[..., bool], on_exit: Union[Callable, None] = None
) -> Callable[..., CheckResult | None]:
    """
    Creates a wrapper around a `Callable[..., bool]` to associate it with a status,
    returning that status if the function returns `True`.

    Adds some logging to tell you when the check is running, and what the
    result was.

    Args:
        status: status the `function` checks for
        function: function that checks for a given status
        on_exit: a function run at the end, no matter what

    Returns:
        A function that returns a `CheckResult | None`
    """

    def run_check() -> CheckResult | None:
        logger.debug(f"Running check for {status}")
        try:
            result = function()
        finally:
            if on_exit is not None:
                logger.debug(f"Running on_exit for {status}")
                on_exit()

        logger.debug(f"{status}? {result}")
        if result is True:
            return status
        else:
            return None

    return run_check


def on_exit(exit_function: Callable[..., Any]) -> Callable[..., Callable[..., Any]]:
    """
    Decorator. Runs the `exit_function` at the end, no matter what

    Args:
        exit_function: The method to run at the end

    Example:
        ```python
        def print_stuff():
            print("stuff")

        @sfchecks.utils.check
        @sfchecks.utils.on_exit(print_stuff)
        def check():
            return 'fixed'

        @sfchecks.utils.on_exit(print_stuff)
        def something_else():
            print("hi")
        ```
    """

    T = TypeVar("T")

    def decorator(function: Callable[..., T]) -> Callable[..., T]:
        """
        Runs an predefined method at the end, no matter what
        """

        @wraps(function)
        def wrapper():
            try:
                return function()
            finally:
                exit_function()

        return wrapper

    return decorator


def print_results(status: CheckResult | None):
    """
    Print the status out in a format originally from SF/bin/check
    """
    flag_name = []
    try:
        with open("/home/sf/.sf/flag-names.txt") as fs:
            flag_name = fs.read().strip()
        print(json.dumps({"results": [{flag_name: status}], "errors": []}, indent=2))
    except FileNotFoundError:
        print("/home/sf/.sf/flag-names.txt not found")


def _configure_logging():
    """
    Sets logging level, configures loguru, and intercepts `logging` calls to
    loguru
    """
    if os.getenv("DEBUG") is not None and os.getenv("DEBUG") != "":
        logurulevel = "DEBUG"
    else:
        logurulevel = "INFO"

    logger.remove()
    logger.add(
        sys.stderr,
        level=logurulevel,
        format="<yellow>{time:HH:mm:ss.SSS}</yellow> <lvl>{level}</lvl> <green>{name}:{function}:{line}</green> | {message}",
    )
    # Redirect ordinary logging calls to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def _was_ran_directly() -> bool:
    """
    Returns:
        True if the top level caller is /SF/bin/check, else False
    """
    if os.path.exists("/SF/conf/flag.py"):
        stack = traceback.extract_stack()
        return stack[0].filename == "/SF/conf/flag.py"
    else:
        return False


def import_from_templates(filename: str) -> ModuleType:
    """
    Import a file from the `/SF/conf/templates.d` directory. The module name is assumed to be the same as the filename
    without the file extension.

    Example:

    ```python
    shared = sfchecks.utils.import_from_templates("shared.py")
    ```
    """
    module_name = filename.replace(".py", "")
    file_path = f"/SF/conf/templates.d/{filename}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        if spec.loader:
            spec.loader.exec_module(module)
            return module
    raise Exception(f"Could not import /SF/conf/templates.d/{filename}")
