# pathlib-ng — Enhanced Path implementation

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/pathlib-ng.svg)](https://pypi.org/project/pathlib-ng)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff)

A lightweight, drop-in replacement for `pathlib.Path` with enhanced features, better error messages, and zero external dependencies.

---

## 📑 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [📖 Usage Examples](#-usage-examples)
- [📚 API Reference](#-api-reference)
  - [Creating Paths](#creating-paths)
  - [Path Properties](#path-properties)
  - [File I/O](#file-io)
  - [Directory Operations](#directory-operations)
  - [File Management](#file-management)
  - [Path Resolution](#path-resolution)
  - [Glob Patterns](#glob-patterns)
- [🔄 Migration from pathlib](#-migration-from-pathlib)
- [📁 Project Structure](#-project-structure)
- [⚙️ Requirements](#-requirements)
- [📄 License](#-license)

---

## 🚀 Quick Start

```bash
pip install pathlib-ng
```

```python
from pathlib_ng import Path

# Create paths with intuitive syntax
p = Path("projects") / "docs" / "readme.md"

# Read file content
if p.exists() and p.is_file():
    content = p.read_text()
    print(f"Content length: {len(content)} characters")
    print(f"File size: {p.stat().st_size} bytes")

# Work with path components
print(f"Name: {p.name}")           # readme.md
print(f"Stem: {p.stem}")           # readme
print(f"Suffix: {p.suffix}")       # .md
print(f"Parent: {p.parent}")       # projects/docs
```

---

## ✨ Features

- **Complete API** — All standard `pathlib.Path` methods implemented
- **Path concatenation** — Overloaded `/` operator for intuitive path building
- **File I/O** — `read_text()`, `write_text()`, `read_bytes()`, `write_bytes()`
- **Directory operations** — `mkdir()`, `rmdir()`, `iterdir()`
- **Glob patterns** — `glob()` and `rglob()` for file matching
- **Path resolution** — `resolve()`, `absolute()`, `expanduser()`
- **File metadata** — `stat()`, `exists()`, `is_file()`, `is_dir()`
- **File management** — `rename()`, `unlink()`, `touch()`
- **Cross-platform** — Works on Linux, macOS, and Windows
- **Zero dependencies** — Pure Python with standard library only
- **Type hints** — Full typing support for better IDE integration

---

## 📖 Usage Examples

### Creating Paths

```python
from pathlib_ng import Path

# Various ways to create paths
p1 = Path("docs/readme.md")
p2 = Path("projects", "src", "main.py")
p3 = Path("/usr", "local", "bin")
p4 = Path.home() / "Documents" / "file.txt"
p5 = Path.cwd() / "data" / "output.json"

# Path concatenation with / operator
p = Path("projects") / "src" / "utils"
```

### Path Properties

```python
p = Path("projects/docs/readme.md")

print(p.parent)      # projects/docs
print(p.name)        # readme.md
print(p.stem)        # readme
print(p.suffix)      # .md
print(p.anchor)      # (empty string for relative path)
```

### File I/O

```python
p = Path("data.txt")

# Write and read text
p.write_text("Hello, World!", encoding="utf-8")
content = p.read_text()  # "Hello, World!"

# Write and read bytes
p.write_bytes(b"Binary data")
data = p.read_bytes()    # b"Binary data"

# Append to file
with open(p, "a") as f:
    f.write("Appended text")
```

### Directory Operations

```python
# Create directories
p = Path("projects/my_app/data")
p.mkdir(parents=True, exist_ok=True)  # Creates all parent directories

# Iterate directory contents
for item in p.parent.iterdir():
    if item.is_file():
        print(f"File: {item.name}")
    elif item.is_dir():
        print(f"Directory: {item.name}")

# Remove empty directory
p.rmdir()

# Get working directories
cwd = Path.cwd()
home = Path.home()
```

### File Management

```python
p = Path("file.txt")

# Create empty file
p.touch()
p.touch(exist_ok=False)  # Raises FileExistsError if exists

# Check existence
p.exists()      # True/False
p.is_file()     # True/False
p.is_dir()      # True/False

# Rename
p.rename("renamed.txt")

# Delete
p.unlink()
p.unlink(missing_ok=True)  # No error if file doesn't exist

# Get file stats
stat = p.stat()
print(f"Size: {stat.st_size} bytes")
print(f"Modified: {stat.st_mtime}")
```

### Path Resolution

```python
# Resolve to absolute path (with symlinks resolved)
p = Path("docs/../src/main.py")
resolved = p.resolve()  # /absolute/path/src/main.py

# Get absolute path without resolving symlinks
absolute = p.absolute()  # /current/working/dir/docs/../src/main.py

# Expand user home directory
p = Path("~/Documents/file.txt")
expanded = p.expanduser()  # /home/username/Documents/file.txt
```

### Glob Patterns

```python
# Find all Python files
for py_file in Path.cwd().glob("*.py"):
    print(py_file)

# Find all .txt files recursively
for txt_file in Path.cwd().rglob("*.txt"):
    print(txt_file)

# Find all directories
for dir in Path.cwd().glob("*/"):
    print(dir.name)

# Complex pattern matching
Path.cwd().glob("src/**/*.py")  # All Python files in src/ and subdirectories
```

---

## 🔄 Migration from pathlib

**pathlib-ng** is designed as a drop-in replacement. Most code works with minimal changes:

```python
# Standard pathlib
from pathlib import Path

# pathlib-ng
from pathlib_ng import Path

# Everything else remains the same!
p = Path("/tmp/test")
p.mkdir(exist_ok=True)
p.write_text("Hello")
```

---

## 🆕 Additional Features

pathlib-ng includes several enhancements over standard `pathlib`:

### Enhanced Error Messages
```python
try:
    Path("/nonexistent/file.txt").read_text()
except FileNotFoundError as e:
    print(e)  # Clear, descriptive error message
```

### Additional Utility Methods
```python
# Get absolute path as string
path_str = Path("file.txt").absolute_path()

# Create all parents automatically with touch()
Path("deep/nested/file.txt").touch()  # Creates parent directories
```

### Better Cross-Platform Support
- Handles path separators consistently across platforms
- Properly normalizes paths for Windows and Unix

---

## 📁 Project Structure

```
pathlib-ng/
├── pathlib_ng/
│   ├── __init__.py      # Package exports
│   └── path.py          # Path class implementation
├── LICENSE              # MIT License
├── pyproject.toml       # Project metadata
└── README.md            # This file
```

---

## 💡 Real-World Examples

### Recursive File Search
```python
from pathlib_ng import Path

def find_files(directory, extension):
    """Find all files with given extension recursively."""
    return list(Path(directory).rglob(f"*.{extension}"))

txt_files = find_files(".", "txt")
for f in txt_files:
    print(f"Found: {f}")
```

### Project Structure Validation
```python
from pathlib_ng import Path

project = Path("my_project")
required_dirs = ["src", "tests", "docs"]
required_files = ["README.md", "pyproject.toml"]

# Check directories
for dir_name in required_dirs:
    dir_path = project / dir_name
    if not dir_path.exists():
        print(f"Missing directory: {dir_name}")
        dir_path.mkdir(parents=True)

# Check files
for file_name in required_files:
    file_path = project / file_name
    if not file_path.exists():
        print(f"Missing file: {file_name}")
        file_path.touch()
```

### Batch File Processing
```python
from pathlib_ng import Path

def process_logs(log_dir):
    """Process all log files in a directory."""
    log_dir = Path(log_dir)
    
    for log_file in log_dir.glob("*.log"):
        # Read and process
        content = log_file.read_text()
        processed = content.upper()
        
        # Write processed version
        processed_file = log_file.with_suffix(".processed.log")
        processed_file.write_text(processed)
        
        # Archive original
        archive_dir = log_dir / "archive"
        archive_dir.mkdir(exist_ok=True)
        log_file.rename(archive_dir / log_file.name)
```

---

## ⚙️ Requirements

- **Python 3.10+** — Uses modern Python features
- **No external dependencies** — Pure Python with standard library only

---

## 📄 License

MIT License — Use freely in open source and commercial projects.

**Author:** [Fkernel653](https://github.com/Fkernel653)

**Links:** [GitHub](https://github.com/Fkernel653/pathlib-ng) • [PyPI](https://pypi.org/project/pathlib-ng)
