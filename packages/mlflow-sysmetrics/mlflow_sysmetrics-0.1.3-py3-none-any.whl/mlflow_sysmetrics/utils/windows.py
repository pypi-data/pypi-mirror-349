"""Windows system utilities for mlflow-sysmetrics.

This module provides platform-specific helpers to extract system metadata
used by the MLflow SysMetrics plugin. Currently, it supports retrieving
the GPU name on Windows systems using PowerShell via the `Get-CimInstance` cmdlet.

Functions:
    - get_windows_gpu_name: Parses GPU name from PowerShell output on Windows.

Note:
    This module is Windows-specific. It is safe to import cross-platform, but
    the included methods should only be executed when `platform.system() == "Windows"`.

Dependencies:
    - subprocess

"""

import subprocess

from mlflow_sysmetrics.utils.constants import (
    WINDOWS_GPU_COMMAND,
    DEFAULT_SUBPROCESS_TIMEOUT,
)


def get_windows_gpu_name() -> str:
    """Return the GPU name on Windows using PowerShell.

    Returns:
        str: The name of the first GPU detected, or "None" on failure.

    """
    try:
        output = subprocess.check_output(
            WINDOWS_GPU_COMMAND,
            stderr=subprocess.DEVNULL,
            timeout=DEFAULT_SUBPROCESS_TIMEOUT,
            text=True,
        )
        lines = [line.strip() for line in output.strip().splitlines() if line.strip()]
        return lines[0] if lines else "None"
    except Exception:
        return "None"
