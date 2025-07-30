# 🪵 Chronilog

**Chronilog** is a clean, configurable, and developer-friendly logging package for Python. It provides rich terminal output, rotating file logging, diagnostics, and full environment-based customization — all in a zero-hassle API.

> Designed for real-world projects that need stability, structure, and style in their logs.

---

## 🚀 Features

- ✅ `ChroniLog(name)` — powerful, configurable logger instance
- 🎨 Rich console output with emoji support
- 📁 Rotating file logs (configurable via `.env` or `.toml`)
- ⚙️ Environment + TOML-based configuration layering
- 🧪 Built-in diagnostics system (`print_diagnostics()`)
- 🔄 Optional JSON logging
- 🧰 Developer-first: testable, extensible, and production-ready

---

## 📦 Installation

```bash
pip install -e .
```

> Clone this repo and install it locally in editable mode during development.

## 🧠 Basic Usage
``` python
from chronilog import ChroniLog

log = ChroniLog("my_app")

log.info("🚀 App started")
log.warning("⚠️ Something might be wrong...")
log.error("❌ An error occurred!")
```
---

## ⚙️ Configuration Options

Chronilog supports config from 3 layers:

`.env` file

`.chronilog.toml` file

Built-in defaults

### 🔧 Example .env
``` ini
CHRONILOG_LOG_PATH=logs/my_app.log
CHRONILOG_LOG_LEVEL=DEBUG
CHRONILOG_LOG_MAX_MB=5
CHRONILOG_LOG_BACKUP_COUNT=3
CHRONILOG_JSON=0
```

---

### 🧪 Diagnostic Mode
```python
from chronilog.diagnostics import print_diagnostics

print_diagnostics()
```

You’ll get a Rich-powered terminal table showing logger status and any setup issues.

---

## ✨ Customizing ChroniLog
You can override behavior with optional arguments:

``` python
from chronilog import ChroniLog
from chronilog.core.formatter import PlainFormatter

log = ChroniLog(
    name="myapp",
    level=logging.INFO,
    file_formatter=PlainFormatter(),
    use_cache=False
)
```

---

### 🔎 Parameters
| Argument           | Type            | Description                                        |
|--------------------|-----------------|----------------------------------------------------|
| `name`             | `str`           | Logger name (typically `__name__`)                 |
| `level`            | `int` *(optional)* | Custom log level (`logging.DEBUG`, etc)         |
| `console_formatter`| `Formatter`     | Optional override for console formatter            |
| `file_formatter`   | `Formatter`     | Optional override for file formatter               |
| `use_cache`        | `bool`          | Whether to reuse existing logger by name           |


## 📁 Default Log Paths
Automatically chooses safe OS-specific defaults:

* 🪟 Windows → `%LOCALAPPDATA%/chronilog/logs/`

* 🍎 macOS → `~/Library/Logs/chronilog/`

* 🐧 Linux → `~/.local/share/chronilog/logs/`

### 🧪 Example Project Structure
```bash
myapp/
├── main.py
├── .env
├── logs/
│   └── chronilog.log
└── requirements.txt
```

---

## 🧪 Example: `test_app.py`
``` python
from chronilog import ChroniLog

log = ChroniLog("test_app")

log.info("🚀 Startup")
log.debug("🔧 Debugging")
log.warning("⚠️ Warning issued")
log.error("❌ Error occurred")
log.critical("🔥 Critical failure")
```

---

## 🧪 Testing
```bash
pytest tests/
```
Or run the built-in usage script:

```bash
python examples/usage.py
```

---

## 📜 License
MIT License — free to use, modify, and contribute.

## 💡 Coming Soon
`chronilog diagnostics` CLI tool

JSON log viewer + filter

Async logging support

Release to PyPI (`pip install chronilog`)

---

## 🙌 Credits
Built with ❤️ by [Brandon McKinney]

Inspired by clean logging practices at scale.