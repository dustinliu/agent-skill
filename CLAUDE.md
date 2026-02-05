# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Skill Linker** — a Python CLI tool that copies AI agent skills from source directories to multiple IDE skill directories (Claude Code, Cursor, Antigravity/Gemini). It reads `skills_config.toml` to determine which skills to copy, where to find them, and which IDE targets to deploy to.

## Common Commands

```bash
# Install dependencies
uv sync

# Run all tests (with coverage report, minimum 85% required)
uv run pytest

# Run a specific test class
uv run pytest test_deploy.py::TestFindSkillInSources

# Run a specific test
uv run pytest test_deploy.py::TestFindSkillInSources::test_finds_skill_in_first_source

# Lint
uv run ruff check .

# Format check
uv run ruff format --check .

# Full CI pipeline (test + lint + format + deploy)
make push

# Deploy skills to IDE directories
uv run deploy            # or: python deploy.py
uv run deploy --dry-run  # preview only
uv run deploy -v         # verbose output
```

## Architecture

Single-module Python project using `uv` for dependency management:

- `deploy.py` — entire application logic: config parsing (TOML), skill discovery across multiple source directories, and copying skill directories to IDE targets. Entry point is `main()`, core logic in `link_skills()`.
- `test_deploy.py` — pytest test suite (37 tests) organized by test classes per function (`TestFindSkillInSources`, `TestExpandPath`, `TestLoadConfig`, `TestCopySkill`, `TestLinkSkills`).
- `skills_config.toml` — configuration: skill names list, source directory paths, and target IDE directories with enable/disable flags.
- `skills/` — local skill definitions. Each skill is a directory with `SKILL.md` and optional `assets/` and `references/` subdirectories.

### Key Data Flow

1. `load_config()` reads `skills_config.toml`
2. `expand_path()` resolves `~` and relative paths (relative to config file directory)
3. `find_skill_in_sources()` searches skill names across multiple source directories (first match wins)
4. For each enabled target IDE: clean stale skills not in config, then `shutil.copytree()` each skill

## Conventions

- Python >=3.11 required (uses `tomllib` from stdlib)
- Linting: ruff with rules F, E, W, I, N, UP, B, C4, SIM
- Formatting: ruff format (double quotes, spaces, unix line endings)
- Coverage threshold: 85% (configured in `pyproject.toml`)
- Source code and comments in English
