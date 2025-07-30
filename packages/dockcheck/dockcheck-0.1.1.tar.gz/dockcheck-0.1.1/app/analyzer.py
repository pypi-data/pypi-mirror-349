import re
from typing import Any

SEVERITY = {"info": 1, "warn": 2, "error": 3}


def analyze_from(instruction: dict[str, Any]) -> list[dict[str, Any]]:
    issues = []
    line = instruction["line"]
    lineno = instruction["line_number"]

    if "@sha256:" in line:
        issues.append(
            {"line": lineno, "instruction": "FROM", "message": "✅ Image is pinned by digest.", "severity": "info"}
        )
    else:
        issues.append(
            {
                "line": lineno,
                "instruction": "FROM",
                "message": "Image is not pinned by digest. Use `@sha256:` for reproducibility.",
                "severity": "warn",
            }
        )

    if ":" not in line:
        issues.append(
            {
                "line": lineno,
                "instruction": "FROM",
                "message": "Missing tag in base image. Pin to a specific version.",
                "severity": "error",
            }
        )
    elif re.search(r":latest\b", line):
        issues.append(
            {
                "line": lineno,
                "instruction": "FROM",
                "message": "Avoid `latest` tag. Use an explicit version.",
                "severity": "warn",
            }
        )

    if any(x in line for x in ["ubuntu", "debian", "centos"]) and "slim" not in line:
        issues.append(
            {
                "line": lineno,
                "instruction": "FROM",
                "message": "Consider using lightweight images (e.g. `slim`, `alpine`).",
                "severity": "warn",
            }
        )

    return issues


def analyze_run(instruction: dict[str, Any]) -> list[dict[str, Any]]:
    issues = []
    line = instruction["line"]
    lineno = instruction["line_number"]

    if "apt-get" in line:
        if not re.search(r"apt-get\s+update.*&&.*apt-get\s+install", line):
            issues.append(
                {
                    "line": lineno,
                    "instruction": "RUN",
                    "message": "Combine `apt-get update` and `install` in one RUN layer.",
                    "severity": "warn",
                }
            )
        if "rm -rf /var/lib/apt/lists" not in line:
            issues.append(
                {
                    "line": lineno,
                    "instruction": "RUN",
                    "message": "Clean apt cache (`rm -rf /var/lib/apt/lists/*`) to reduce image size.",
                    "severity": "info",
                }
            )

    if "pip install" in line and "--no-cache-dir" not in line:
        issues.append(
            {
                "line": lineno,
                "instruction": "RUN",
                "message": "Use `--no-cache-dir` with pip to reduce image size.",
                "severity": "warn",
            }
        )

    return issues


def analyze_copy(instruction: dict[str, Any]) -> list[dict[str, Any]]:
    issues = []
    line = instruction["line"]
    lineno = instruction["line_number"]

    if "." in line and not re.search(r"\s+\.", line):  # heuristic: COPY . .
        issues.append(
            {
                "line": lineno,
                "instruction": "COPY",
                "message": "Avoid using `COPY . .` — use `.dockerignore` and copy only needed files.",
                "severity": "warn",
            }
        )

    return issues


def analyze_env(instruction: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "line": instruction["line_number"],
            "instruction": "ENV",
            "message": "Make sure environment variables don’t include secrets.",
            "severity": "warn",
        }
    ]


def analyze_workdir(instruction: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "line": instruction["line_number"],
            "instruction": "WORKDIR",
            "message": "Set WORKDIR early and avoid hardcoding absolute paths.",
            "severity": "info",
        }
    ]


def analyze_cmd(instruction: dict[str, Any]) -> list[dict[str, Any]]:
    line = instruction["line"]
    lineno = instruction["line_number"]
    issues = []

    if not line.startswith("CMD ["):
        issues.append(
            {
                "line": lineno,
                "instruction": "CMD",
                "message": 'Use exec form (`CMD ["executable", "arg"]`) instead of shell form.',
                "severity": "warn",
            }
        )

    return issues


INSTRUCTION_ANALYZERS = {
    "FROM": analyze_from,
    "RUN": analyze_run,
    "COPY": analyze_copy,
    "ENV": analyze_env,
    "WORKDIR": analyze_workdir,
    "CMD": analyze_cmd,
}


def analyze_instructions(instructions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_issues = []
    for inst in instructions:
        analyzer = INSTRUCTION_ANALYZERS.get(inst["instruction"])
        if analyzer:
            issues = analyzer(inst)
            all_issues.extend(issues)
    return all_issues
