# CONTEXT.md — `backend/db/`

MySQL (Aiven) connection layer. SSL mandatory.

## Files
- `base.py:1` — `class Base(DeclarativeBase)`. All models inherit this.
- `engine.py:1` — `build_url()` from `config.settings` (`mysql+pymysql://user:pass@host:port/db`), `create_engine_ssl()` with `connect_args={"ssl":{"ssl":True}}` when `DB_SSL=true`, `pool_pre_ping=True`. Exposes `engine`, `SessionLocal`.
- `session.py:1` — `get_db()` FastAPI dependency (yield/close). Only way routers get a session.
- `__init__.py` — marker.

## Env used
`DB_HOST`, `DB_PORT` (17886), `DB_NAME` (centralign), `DB_USERNAME`, `DB_PASSWORD`, `DB_SSL`.

## Verify
`SELECT 1` via pymysql with `ssl={'ssl':True}` must return `(1,)`.
