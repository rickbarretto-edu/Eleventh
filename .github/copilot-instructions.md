### Quick orientation — Eleventh (Python)

This repo implements a small distributed card-game backend (FastAPI services) split into small per-service modules under `eleventh/services/`.

Keep guidance concise and specific to the codebase so a coding agent can be productive immediately.

1) Big-picture architecture
- Each service lives at `eleventh/services/<name>/` and commonly exposes:
  - `api.py` — FastAPI router (APIRouter) with endpoints and Pydantic models.
  - `repo.py` — in-process implementation of a storage interface (Protocols used for tests and DI).
  - `__main__.py` — local runnable FastAPI app that includes the router. Start services using Uvicorn via the `__main__` module.

  Example: `eleventh/services/accounts/__main__.py` includes `route` and documents how to run the service:
  `poetry run uvicorn eleventh.services.accounts.__main__:app --host 127.0.0.1 --port 8001 --reload`

2) Common patterns and conventions
- Dependency injection: services expose Protocol types in `repo.py` and provide an in-memory implementation (e.g. `InMemoryAccounts`, `InMemoryLogs`). Tests frequently override dependencies using FastAPI's `app.dependency_overrides`.
- Small, focused modules: business logic lives in `repo.py` and typed models in `model.py` (attrs-based immutable dataclasses are used, e.g. `attrs.frozen`).
- Routers: `api.py` creates an `APIRouter` named `route` and endpoints are `async def` functions returning Pydantic models.
- Type aliases and Protocols: prefer Protocols for interface definitions; use explicit Enum status results (e.g. `Creation` in `accounts/repo.py`) rather than exceptions for common state.

3) Tests and runtime
- Tests run under pytest with `pytest` (pyproject includes pytest config). Async tests use `pytest-asyncio`.
- To run a single service for manual testing use the documented uvicorn command in that service's `__main__.py`. Example commands are present in file docstrings — prefer those.

Poetry (project-specific)
- This project uses Poetry for dependency management and packaging. The project's `pyproject.toml` declares Python >=3.12 and the runtime/test deps.
- Use `poetry run` to execute commands inside the project virtualenv. Examples below are provided for PowerShell (Windows) which is the common development shell used in this environment.

  Install dependencies and create a venv (recommended):

```powershell
poetry install
```

  Run tests:

```powershell
poetry run pytest -q
```

  Run an individual service (example from `eleventh/services/accounts/__main__.py`):

```powershell
poetry run uvicorn eleventh.services.accounts.__main__:app --host 127.0.0.1 --port 8001 --reload
```

  Spawn a shell inside the project's virtualenv (optional):

```powershell
poetry shell
# then run uvicorn or pytest directly
```

- Tips / gotchas:
  - Ensure Python 3.12+ is available. If Poetry complains about the interpreter, run `poetry env use <path-to-python3.12>`.
  - Tests and many quick-start docstrings assume `poetry run` usage. Prefer `poetry run` to avoid accidental use of a wrong Python environment.
  - If you want in-project venv (easier for some editors): `poetry config virtualenvs.in-project true` then `poetry install`.

4) Integration and communication
- Services are HTTP-based (FastAPI), and the logging service exposes a WebSocket endpoint for streaming logs: `eleventh/services/logging/api.py` has `/log/ws` and a small template UI at `/log/ui`.
- In-memory queues and asyncio primitives are used for pub/sub patterns (see `InMemoryLogs.subscribe()` returning an `asyncio.Queue`).

5) Project-specific gotchas & searchable examples
- Passwords in `accounts/repo.py` use Python's built-in `hash()` (not secure) — many tests rely on this behavior. When changing auth, update tests accordingly.
- Router variable name is `route` (not `router`) in services; new endpoints should use `route` to be included by the simple `__main__.py` pattern.

6) Files you will frequently read or modify
- `eleventh/services/*/api.py` — endpoint signatures, input/output models.
- `eleventh/services/*/repo.py` — business logic and Protocol definitions.
- `eleventh/services/*/__main__.py` — start/run hints; shows ports used in examples.
- `pyproject.toml` — dependency list and pytest config.
- `README.md` and `.project/` — project goals and context for design decisions.

7) How to make safe changes
- Preserve Protocol contracts and Enum-based result types. Tests use these to assert behavior.
- If adding a new endpoint, mirror the local service pattern: add Pydantic models in `api.py`, implement logic in `repo.py`, export `route` and ensure `__main__.py` includes it.

8) Minimal examples to copy/paste
- Registering a router in a runnable module (`__main__.py`):

  from fastapi import FastAPI
  from eleventh.services.accounts import route

  app = FastAPI()
  app.include_router(route)

9) When tests fail locally
- Run `poetry run pytest -q` (project uses pytest config from pyproject). Many tests are async; ensure `pytest-asyncio` is available in the environment (pyproject lists it).

If anything here is unclear or you'd like more examples (e.g., test patterns, how DI is overridden in tests, or a list of ports used by example run commands), tell me which section to expand and I'll iterate.
