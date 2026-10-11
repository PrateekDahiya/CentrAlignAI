# CONTEXT.md — `backend/models/`

SQLAlchemy tables. No queries here — queries live in routers/services/agent.

## Files
- `run.py:1` — `Run`: `id` (uuid str PK), `task` TEXT, `status` (`running`/`waiting`/`done`/`failed`/`cancelled`), `plan_json` TEXT, `created_at`.
- `step.py:1` — `Step`: `id` autoincrement, `run_id` FK→runs, `n`, `thought`, `tool`, `args_json`, `obs`. Agent trace mirror.
- `fact.py:1` — `Fact`: `run_id` FK, `k`, `v`. Agent memory (e.g. `invoice_no`, `user_approval`).
- `invoice.py:1` — `Invoice` (`erp_invoices`): `id`, `vendor`, `invoice_no` UNIQUE (idempotency key), `amount` Numeric(12,2), `due_date` Date nullable, `source_file`, `created_at`.
- `__init__.py` — marker (import models in `seed_db.py` before `create_all`).
