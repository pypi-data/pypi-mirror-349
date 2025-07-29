from pathlib import Path

import pytest

from app.parser import parse_dockerfile


@pytest.fixture
def simple_dockerfile(tmp_path: Path) -> Path:
    content = """
FROM python:3.11
RUN pip install --no-cache-dir flask
CMD ["python", "app.py"]
"""
    file = tmp_path / "Dockerfile"
    file.write_text(content)
    return file


@pytest.fixture
def multiline_dockerfile(tmp_path: Path) -> Path:
    content = """
FROM ubuntu:20.04 \
    AS base
# This is a comment
RUN apt-get update && \
    apt-get install -y python3 \
    python3-pip

COPY . /app
"""
    file = tmp_path / "Dockerfile"
    file.write_text(content)
    return file


@pytest.fixture
def multi_stage_dockerfile(tmp_path: Path) -> Path:
    content = """
FROM node:18 AS build
RUN npm install
FROM nginx:alpine
COPY --from=build /dist /usr/share/nginx/html
"""
    file = tmp_path / "Dockerfile"
    file.write_text(content)
    return file


def test_parse_simple_dockerfile(simple_dockerfile: Path):
    result = parse_dockerfile(simple_dockerfile)
    assert len(result) == 3
    assert result[0]["instruction"] == "FROM"
    assert result[1]["instruction"] == "RUN"
    assert result[2]["instruction"] == "CMD"
    assert result[0]["stage"] == 0
    assert result[1]["stage"] == 0
    assert result[2]["stage"] == 0


def test_parse_multiline_dockerfile(multiline_dockerfile: Path):
    result = parse_dockerfile(multiline_dockerfile)
    assert len(result) == 3
    assert result[0]["instruction"] == "FROM"
    # Normalize whitespace for robust comparison
    from_line = " ".join(result[0]["line"].split())
    assert from_line.startswith("FROM ubuntu:20.04 AS base")
    assert result[1]["instruction"] == "RUN"
    run_line = " ".join(result[1]["line"].split())
    assert "apt-get install -y python3 python3-pip" in run_line
    assert result[2]["instruction"] == "COPY"
    assert result[2]["line"].startswith("COPY . /app")
    # Comments and blank lines are skipped


def test_parse_multi_stage_dockerfile(multi_stage_dockerfile: Path):
    result = parse_dockerfile(multi_stage_dockerfile)
    assert len(result) == 4
    assert result[0]["instruction"] == "FROM"
    assert result[0]["stage"] == 0
    assert result[1]["instruction"] == "RUN"
    assert result[1]["stage"] == 0
    assert result[2]["instruction"] == "FROM"
    assert result[2]["stage"] == 1
    assert result[3]["instruction"] == "COPY"
    assert result[3]["stage"] == 1


def test_parse_skips_comments_and_blank_lines(tmp_path: Path):
    content = """
# Comment line

FROM alpine

# Another comment
RUN echo 'hello' # Inline comment
"""
    file = tmp_path / "Dockerfile"
    file.write_text(content)
    result = parse_dockerfile(file)
    assert len(result) == 2
    assert result[0]["instruction"] == "FROM"
    assert result[1]["instruction"] == "RUN"


def test_parse_trailing_multiline(tmp_path: Path):
    content = """
FROM busybox
RUN echo 'foo' && \
    echo 'bar' && \
    echo 'baz' \
"""
    file = tmp_path / "Dockerfile"
    file.write_text(content)
    result = parse_dockerfile(file)
    assert len(result) == 2
    assert result[1]["instruction"] == "RUN"
    assert "echo 'baz'" in result[1]["line"]
