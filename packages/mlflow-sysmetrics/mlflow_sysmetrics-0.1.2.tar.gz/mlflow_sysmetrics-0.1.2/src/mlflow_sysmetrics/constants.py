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
