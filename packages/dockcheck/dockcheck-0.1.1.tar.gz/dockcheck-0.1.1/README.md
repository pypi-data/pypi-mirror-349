# 🚢 DockCheck

A lightweight CLI tool for analyzing Dockerfiles.
Ensure your containers follow best practices, remain reproducible, and stay small & secure — in seconds.

## ✨ Features

- ✅ **Parse** Dockerfiles into structured JSON or YAML
- 🔍 **Analyze** each instruction and get actionable best-practice suggestions
- 📦 Recommendations for:
  - `FROM` (digest pinning, image size)
  - `RUN` (layer optimization, cache clearing)
  - `COPY` (overuse of `.` or missing `.dockerignore`)
  - `ENV`, `CMD`, `WORKDIR`, and more
- 💡 Designed to be readable, minimal, and CI/CD-friendly

## 📦 Installation

You can install DockCheck via pip or use uvx to run it without worrying about virtual environment creation.

```bash
pip install dockcheck
```

Or run locally from source:

```bash
git clone https://github.com/yourusername/DockCheck.git
cd DockCheck
uv venv && uv pip install -e .
```

### Using uvx (Fastest Way to Run Without Installing)

You can use [uv](https://github.com/astral-sh/uv) to run DockCheck directly, without needing to install dependencies globally. First, install `uv` if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then run DockCheck with `uvx`:

```bash
uvx dockcheck path/to/Dockerfile --analyze
```

This will automatically handle dependencies and run the CLI tool in a single step.

## 🚀 Usage

### Analyze a Dockerfile

```bash
dockcheck path/to/Dockerfile --analyze
```

### Parse a Dockerfile as JSON or YAML

```bash
dockcheck path/to/Dockerfile --parse --output json
```

You can also do both at once:

```bash
dockcheck path/to/Dockerfile -a -p -o yaml
```

## 🛠 Example

Dockerfile

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Run the application
CMD ["python", "main.py"]
```

### Output

```bash
dockcheck examples/Dockerfile.1 -a
Running analysis on: examples/Dockerfile.1
[
  {
    "line": 2,
    "instruction": "FROM",
    "message": "Image is not pinned by digest. Use `@sha256:` for reproducibility.",
    "severity": "warn"
  },
  {
    "line": 5,
    "instruction": "ENV",
    "message": "Make sure environment variables don\u2019t include secrets.",
    "severity": "warn"
  },
  {
    "line": 6,
    "instruction": "ENV",
    "message": "Make sure environment variables don\u2019t include secrets.",
    "severity": "warn"
  },
  {
    "line": 9,
    "instruction": "WORKDIR",
    "message": "Set WORKDIR early and avoid hardcoding absolute paths.",
    "severity": "info"
  }
]
```

## 📚 Why This Exists

Dockerfiles are deceptively simple — but it's easy to overlook best practices.
This tool helps you:

- Write **secure**, **reproducible** builds
- Catch common **Docker anti-patterns**
- Optimize image **size** and **layering**

Ideal for local devs, teams, and CI pipelines alike.

## 💖 Support This Project

Maintaining open-source tools takes time and care.
If you find DockCheck helpful, please consider supporting it with a small donation.
It helps keep the project alive and encourages continued development.

<a href="https://www.buymeacoffee.com/hyperoot" target="_blank">
<img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" >
</a>

## 📢 Contribute

PRs are very welcome! See [`CONTRIBUTING.md`](./CONTRIBUTING.md) to get started.

- Have a rule idea? Open an issue!
- Want to build a GitHub Action or VS Code plugin? Let’s collaborate!

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
