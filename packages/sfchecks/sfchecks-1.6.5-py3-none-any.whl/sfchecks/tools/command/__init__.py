from subprocess import CompletedProcess
import subprocess


def run(command: str, **kwargs) -> CompletedProcess:
    """
    Dumb wrapper around subprocess.run that just adds `shell=True` and `capture_output=True`.

    Additional keyword arguments are passed to `subprocess.run`, and it is possible to overwrite
    the default values of `shell` and `capture_output`.

    Args:
        command: command to run
        **kwargs: additional kwargs to pass to `subprocess.run`

    Returns:
        CompletedProcess from the `subprocess` lib
    """
    args = {"capture_output": True, "shell": True, **kwargs}
    return subprocess.run(command, **args)
