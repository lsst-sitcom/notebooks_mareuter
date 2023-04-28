import os
import subprocess as sp


def run_cmd(command: list[str], as_lines: bool = False) -> str | list[str]:
    """Run a command via subprocess::run.

    Parameters
    ----------
    command : `list`
        The command to run.
    as_lines : `bool`, optional
        Return the output as a list instead of a string.

    Returns
    -------
    `str` or `list`
        The output from the command.
    """
    output = sp.run(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    decoded_output = output.stdout.decode("utf-8")
    if as_lines:
        return decoded_output.split(os.linesep)
    else:
        return decoded_output[:-1]
