# bulkllm 

## Development

### Quick Commands
 - `make init` create the environment and install dependencies
 - `make help` see available commands
 - `make af` format code
 - `make lint` run linter
- `make typecheck` run type checker
- `make test` run tests
- `make coverage` run tests with coverage report
- `make check` run all checks (format, lint, typecheck, test)
 - `make checku` run all checks with unsafe autoformatting

### Code Conventions

#### Testing
- Use **pytest** (no test classes).
- Always set `match=` in `pytest.raises`.
- Prefer `monkeypatch` over other mocks.
- Mirror the source-tree layout in `tests/`.
- Always run `make checku` after making changes.

#### Exceptions
- Catch only specific exceptions—never blanket `except:` blocks.
- Don’t raise bare `Exception`.

#### Python
- Manage env/deps with **uv** (`uv add|remove`, `uv run -- …`).
- No logging config or side-effects at import time.
- Keep interfaces (CLI, web, etc.) thin; put logic elsewhere.
- Use `typer` for CLI interfaces, `fastapi` for web interfaces, 
 and `pydantic` for data models.
