# mlflow-sysmetrics

🧠 A lightweight [MLflow Run Context Provider](https://mlflow.org/docs/latest/tracking.html#context-providers) that automatically logs system-level metrics (CPU, memory, disk, GPU, OS) as run tags.

> ✅ Cross-platform · 🔌 Plugin-ready · 🧪 Tested · ⚙️ Minimal dependencies

---

## 📦 What it does

This plugin automatically adds system environment metadata to each MLflow run. It enables lightweight observability for experiment tracking — useful in both local development and remote execution contexts.

### ✅ Captured Tags

| Tag Key            | Description                               |
| ------------------ | ----------------------------------------- |
| `sys.cpu`          | CPU model or architecture                 |
| `sys.cpu_cores`    | Logical CPU core count                    |
| `sys.memory_gb`    | Total system memory (GB)                  |
| `sys.disk_free_gb` | Free disk space in current directory (GB) |
| `sys.platform`     | OS and kernel version                     |
| `sys.gpu`          | GPU name via `nvidia-smi` or "None"       |
| `sysmetrics.error` | Captures any exception during tagging     |

---

## 🚀 Installation

```bash
poetry add mlflow-sysmetrics
```

> Requires: Python ≥ 3.9 · `mlflow` ≥ 2.0 · `psutil` (automatically included)

---

## 🛠️ Usage

Set the environment variable to activate the plugin:

```bash
export MLFLOW_RUN_CONTEXT_PROVIDER=sysmetrics
```

Then run any MLflow experiment:

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("foo", "bar")
    # Plugin will automatically add sys.* tags
```

---

## 🧪 Testing

Run both unit and integration tests:

```bash
poetry run pytest -m unit
poetry run pytest -m integration
```

To manually verify plugin behavior:

```bash
export MLFLOW_RUN_CONTEXT_PROVIDER=sysmetrics
poetry run python scripts/debug_run.py
```

### 📷 Example: Debug Script Output

You can verify system metrics manually with the debug script. Below is a sample output:

![Example terminal output of sysmetrics plugin](assets/debug_run.png)

---

## 🔍 Project Structure

```text
mlflow-sysmetrics/
├── src/mlflow_sysmetrics/
│   ├── __init__.py
│   ├── constants.py
│   └── system_context.py         # Plugin implementation
├── tests/
│   ├── unit/                     # Logic-only tests
│   └── integration/              # MLflow integration tests
├── scripts/
│   └── debug_run.py              # Manual testing script
├── assets/                       # Image and media assets
│   └── debug_run.png             # Screenshot of debug script
├── pyproject.toml
└── README.md
```

---

## 📩 Plugin Registration

This plugin is exposed to MLflow via entry points:

```toml
[tool.poetry.plugins."mlflow.run_context_provider"]
sysmetrics = "mlflow_sysmetrics:SysMetricsRunContextProvider"
```

---

## 🤝 Contributing

Pull requests, bug reports, and suggestions are welcome!

1. Fork the repo
2. Create a virtual environment: `poetry install`
3. Write or update tests
4. Run tests with `poetry run pytest`
5. Submit your PR 🚀

---

## 📄 License

Apache License 2.0. See [`LICENSE`](./LICENSE) for full terms.

---

## 💬 Questions?

Feel free to open an issue or reach out via GitHub Discussions.