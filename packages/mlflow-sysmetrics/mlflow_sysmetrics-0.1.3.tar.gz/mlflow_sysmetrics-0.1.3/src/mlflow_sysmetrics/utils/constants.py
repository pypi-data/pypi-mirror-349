"""Shared constants for the mlflow-sysmetrics plugin."""

# Tag keys
TAG_CPU = "sys.cpu"
TAG_CPU_CORES = "sys.cpu_cores"
TAG_MEMORY_GB = "sys.memory_gb"
TAG_DISK_FREE_GB = "sys.disk_free_gb"
TAG_PLATFORM = "sys.platform"
TAG_GPU = "sys.gpu"
TAG_ERROR = "sysmetrics.error"

# Environment variable
ENV_MLFLOW_CONTEXT = "MLFLOW_RUN_CONTEXT_PROVIDER"

# External command
NVIDIA_SMI_COMMAND = [
    "nvidia-smi",
    "--query-gpu=name",
    "--format=csv,noheader",
]

SYSTEM_PROFILER_COMMAND = ["system_profiler", "SPDisplaysDataType"]

# PowerShell GPU detection on Windows
WINDOWS_GPU_COMMAND = [
    "powershell",
    "-Command",
    "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name",
]

# Timeout for subprocess calls
DEFAULT_SUBPROCESS_TIMEOUT = 3

# Regex for parsing macOS GPU name
SYSTEM_PROFILER_GPU_REGEX = r"Chipset Model:\s+(.+)"

# OS names
OS_NAME_MAC = "Darwin"
OS_NAME_WINDOWS = "Windows"

# Bytes per GB
BYTES_PER_GB = 1e9
