"""SysMetricsRunContextProvider.

This MLflow Run Context Provider automatically adds system metadata as tags to MLflow runs.
It provides lightweight insights into the environment where a run is executed.

Captured tags include:
- sys.cpu: CPU model or architecture
- sys.cpu_cores: Logical CPU core count
- sys.memory_gb: Total system memory in gigabytes
- sys.disk_free_gb: Available disk space at current working directory
- sys.platform: OS + kernel description
- sys.gpu: GPU name (via nvidia-smi) or "None" if unavailable

This plugin is cross-platform and requires only `psutil` for system metrics.
"""

import os
import platform
import shutil
import psutil
import subprocess

from mlflow.tracking.context.abstract_context import RunContextProvider
from mlflow_sysmetrics.constants import (
    TAG_CPU,
    TAG_CPU_CORES,
    TAG_MEMORY_GB,
    TAG_DISK_FREE_GB,
    TAG_PLATFORM,
    TAG_GPU,
    TAG_ERROR,
    NVIDIA_SMI_COMMAND,
)


class SysMetricsRunContextProvider(RunContextProvider):
    """MLflow context provider for logging basic system resource information as run tags."""

    def in_context(self) -> bool:
        """Determine whether this context provider is applicable.

        Returns:
            bool: Always returns True, enabling this provider for all runs.

        """
        return True

    def tags(self) -> dict[str, str]:
        """Collect and return system-related tags to attach to the MLflow run.

        Returns:
            dict[str, str]: A dictionary of system metadata tags to log with the run.

        """
        tags: dict[str, str] = {}

        try:
            # CPU and platform
            tags[TAG_CPU] = platform.processor() or platform.machine() or "unknown"
            tags[TAG_CPU_CORES] = str(os.cpu_count())
            tags[TAG_PLATFORM] = platform.platform()

            # Memory
            memory_bytes = psutil.virtual_memory().total
            tags[TAG_MEMORY_GB] = str(round(memory_bytes / 1e9, 2))

            # Disk
            disk = shutil.disk_usage(os.getcwd())
            tags[TAG_DISK_FREE_GB] = str(round(disk.free / 1e9, 2))

            # GPU
            try:
                output = subprocess.check_output(
                    NVIDIA_SMI_COMMAND,
                    stderr=subprocess.DEVNULL,
                    timeout=2,
                )
                tags[TAG_GPU] = output.decode("utf-8").strip()
            except (FileNotFoundError, subprocess.SubprocessError):
                tags[TAG_GPU] = "None"

        except Exception as e:
            # Catch any unexpected failure and log the error
            tags[TAG_ERROR] = str(e)

        return tags
