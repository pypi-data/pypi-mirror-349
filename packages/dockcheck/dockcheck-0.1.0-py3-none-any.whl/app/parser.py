import re
from pathlib import Path
from typing import Any


def parse_dockerfile(path: Path) -> list[dict[str, Any]]:
    """
    Read a Dockerfile and return its logical instructions as a list of dictionaries.
    Each dictionary contains:
        - 'line': full instruction string
        - 'line_number': starting line number in the original Dockerfile
        - 'instruction': Dockerfile keyword (e.g., FROM, RUN)
        - 'stage': integer index of the stage (0-based)
    Multi-line instructions are joined into a single logical line.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    instructions: list[dict[str, Any]] = []
    current: list[str] = []
    start_line: int = 0
    stage_index: int = -1

    for idx, raw in enumerate(lines):
        stripped = raw.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        if not current:
            start_line = idx + 1

        if stripped.endswith("\\"):
            segment = stripped[:-1].strip()
            if segment:
                current.append(segment)
        else:
            segment = stripped.strip()
            if segment:
                current.append(segment)
            joined = " ".join(current)
            instruction_type = re.split(r"\s+", joined, maxsplit=1)[0].upper()

            if instruction_type == "FROM":
                stage_index += 1

            instructions.append(
                {"line": joined, "line_number": start_line, "instruction": instruction_type, "stage": stage_index}
            )
            current = []

    if current:
        joined = " ".join(current)
        instruction_type = re.split(r"\s+", joined, maxsplit=1)[0].upper()
        if instruction_type == "FROM":
            stage_index += 1
        instructions.append(
            {"line_number": start_line, "instruction": instruction_type, "line": joined, "stage": stage_index}
        )

    return instructions
