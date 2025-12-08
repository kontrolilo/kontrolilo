# AGENTS.md

## Build/Lint/Test Commands
- **Setup**: `make local-setup` (uses pipenv)
- **Lint**: `make lint` (runs pre-commit hooks)
- **Unit tests**: `make unit-test` (pytest with coverage)
- **Integration tests**: `make integration-test`
- **Single test**: `pipenv run pytest path/to/test.py::test_function`
- **All tests**: `make test` (combines unit + integration)

## Code Style Guidelines
- **Python version**: 3.x (uses pipenv)
- **Encoding**: UTF-8 with `# -*- coding: utf-8 -*-` header
- **Imports**: Group standard library, third-party, then local imports
- **Type hints**: Use `typing` module (List, Dict, etc.)
- **Classes**: PascalCase, inherit from abstract base classes where appropriate
- **Functions**: snake_case, include type hints for parameters and return
- **Error handling**: Use subprocess.run with check=True, capture_output=True
- **Logging**: Use getLogger(__name__) for module-level logging
- **Testing**: pytest with fixtures in conftest.py, coverage required