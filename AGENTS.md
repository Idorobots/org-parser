# AGENTS.md
Guidance for coding agents working in `org-mode-parser`.

## Scope
- Repository provides a Python Org-mode parser wrapper around tree-sitter.
- Primary package: `src/org_parser/`
- Tests: `tests/`
- Examples/fixtures: `examples/`
- CI workflow: `.github/workflows/parser-checks.yml`

## Repository Map
- Public package entrypoint: `src/org_parser/__init__.py`
- Tree-sitter language/parser singleton: `src/org_parser/_lang.py`
- Shared node helpers/constants:
  - `src/org_parser/_node.py`
  - `src/org_parser/_nodes.py`
- Strict parse helpers: `src/org_parser/_from_source.py`
- Document APIs:
  - `src/org_parser/document/__init__.py`
  - `src/org_parser/document/_document.py`
  - `src/org_parser/document/_heading.py`
  - `src/org_parser/document/_loader.py` (`load_raw`)
- Semantic element modules: `src/org_parser/element/*.py`
- Text/time modules:
  - `src/org_parser/text/*.py`
  - `src/org_parser/time/*.py`
- Utility script: `format.py`

## External Grammar Note
- This repository does **not** contain a local tree-sitter grammar source directory.
- Grammar runtime comes from dependency `tree-sitter-org` (see `pyproject.toml`).
- Do not add instructions that assume local grammar regeneration unless such files are added in the future.

## Cursor / Copilot Rules
- No Cursor rules were found (`.cursor/rules/` and `.cursorrules` absent).
- No Copilot instructions were found (`.github/copilot-instructions.md` absent).
- If any of these files are added later, treat them as authoritative and merge their requirements here.

## Toolchain (CI-aligned)
- Python: `3.12`
- Poetry: `2.3.2` (CI)
- Node.js: `22` in CI (used for tree-sitter CLI install)
- Tree-sitter CLI: `0.26.6` in CI
- QA tools: `ruff`, `mypy`, `pyright`, `pytest`, `pytest-cov`, `taskipy`

## Setup
```bash
poetry install
```

## Build / Lint / Type / Test Commands
Run from repository root unless noted otherwise.

### Primary quality gate
```bash
poetry run task check
```
- Executes: format-check + lint + mypy + tests.

### Individual tasks
```bash
poetry run task format-check
poetry run task format
poetry run task lint
poetry run task lint-fix
poetry run task type
poetry run task test
```

### Direct tool commands
```bash
poetry run ruff check src/ tests/
poetry run ruff format --check src/ tests/
poetry run mypy src/ tests
poetry run pyright
poetry run pytest
```

### Run a single test (important)
```bash
poetry run pytest tests/test_document.py::TestLoadRaw::test_simple_org_returns_tree
poetry run pytest tests/test_document.py::TestLoadRaw
poetry run pytest tests/test_document.py
poetry run pytest -k "from_source and not recovery"
poetry run pytest -m integration
```

### Useful pytest options
```bash
poetry run pytest -x
poetry run pytest --maxfail=1
poetry run pytest --tb=short
poetry run pytest -q
```

## Test Suite Notes
- Pytest config is in `pyproject.toml` under `[tool.pytest.ini_options]`.
- `testpaths = ["tests"]`
- Default options include `--tb=short --strict-markers -q`.
- Marker available:
  - `integration`: tests that require compiled `org.so` shared library.

## Formatting, Linting, and Types
- Ruff line length: `88`
- Ruff target version: `py312`
- Ruff formatter uses:
  - double quotes
  - spaces for indentation
- isort behavior is handled by Ruff (`I` rules enabled).
- mypy is `strict = true`.
- pyright uses `typeCheckingMode: "strict"` (see `pyrightconfig.json`).

## Python Code Style
- Keep imports sorted and grouped consistently (stdlib, third-party, first-party).
- Prefer explicit imports over wildcard imports.
- Use `TYPE_CHECKING` blocks for type-only imports to avoid runtime cycles/cost.
- Use type annotations on public APIs and internal helpers where practical.
- Prefer precise types (`Path`, `Sequence[T]`, `list[str]`, `tuple[...]`) over broad types.
- Use `Any` only when unavoidable (interop boundaries, dynamic APIs).
- Use Google-style docstrings in library modules.
- Keep module-level `__all__` in public-facing modules.
- Internal/private modules and helpers should use leading underscore naming (`_module.py`, `_helper`).

## Naming Conventions
- Modules/functions/variables: `snake_case`
- Classes/dataclasses: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private/internal attrs/methods: leading underscore
- Test files and tests:
  - files: `tests/test_*.py`
  - test classes: `Test...`
  - test functions: `test_...`

## Error Handling Conventions
- Raise clear built-in exceptions for API misuse and missing resources:
  - `FileNotFoundError` for missing paths
  - `ValueError` for invalid parse state / invalid arguments
- Preserve parser recovery behavior; do not aggressively hard-fail where graceful parsing is intended.
- Let low-level exceptions propagate unless translating them improves API clarity.
- Keep error messages actionable and specific.
- In strict parse helpers, fail fast when parse errors are detected (`document.errors`).

## Working in This Repo
- Keep diffs focused; avoid unrelated refactors.
- Preserve public API compatibility unless change is intentional and tested.
- Add or update tests with behavior changes.
- Run the narrowest relevant test first, then broaden to `poetry run task check`.
- Prefer modifying existing modules over introducing new abstractions unless necessary.
- Avoid committing generated cache files (`__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`).

## Agent Workflow Checklist
1. Read relevant module(s) and nearby tests first.
2. Implement minimal targeted change.
3. Run a single focused test (`pytest <nodeid>`).
4. Run broader suite (`poetry run task test` or `poetry run task check`).
5. Ensure formatting/lint/type checks pass before finalizing.
6. Document behavioral changes in tests and docstrings when applicable.

## If Repository Layout Changes
- Re-check for:
  - local grammar directories
  - Cursor/Copilot rule files
  - new CI commands
- Update this file to keep agent instructions aligned with the current repository.
