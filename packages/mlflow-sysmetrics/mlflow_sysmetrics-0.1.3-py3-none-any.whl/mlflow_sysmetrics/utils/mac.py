"""macOS system utilities for mlflow-sysmetrics.

This module provides platform-specific helpers to extract system metadata
used by the MLflow SysMetrics plugin. Currently, it supports retrieving
the Apple GPU chipset name on macOS systems using the `system_profiler` command.

Functions:
    - get_macos_gpu_chipset: Parses `Chipset Model` from SPDisplaysDataType output.

Note:
    This module is macOS-specific. It is safe to import cross-platform, but
    the included methods should only be executed when `platform.system() == "Darwin"`.

Dependencies:
    - subprocess
    - re

"""
import subprocess
import re

from mlflow_sysmetrics.utils.constants import SYSTEM_PROFILER_COMMAND, DEFAULT_SUBPROCESS_TIMEOUT


def get_macos_gpu_chipset() -> str:
    """Return the Apple GPU chipset name from system_profiler on macOS."""
    try:
        output = subprocess.check_output(
            SYSTEM_PROFILER_COMMAND,
            stderr=subprocess.DEVNULL,
            timeout=DEFAULT_SUBPROCESS_TIMEOUT,
            text=True,
        )
        match = re.search(r"Chipset Model:\s+(.+)", output)
        return match.group(1) if match else "None"
    except Exception:
        return "None"
