
# regular import
import psutil
import os


def get_terminal_pid():
    """
    Retrieves the PID (Process ID) of the terminal window that launched this script.

    Returns:
        int: The PID of the terminal process or None if not found.
    """
    current_process = psutil.Process(os.getpid())
    parent_pid = current_process.ppid()

    while parent_pid:
        parent_process = psutil.Process(parent_pid)
        if 'cmd.exe' in parent_process.name().lower():
            return parent_pid
        parent_pid = parent_process.ppid()

    return None

