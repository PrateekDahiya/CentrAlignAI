# CONTEXT.md — `backend/schemas/`

Pydantic DTOs. No DB/LLM code.

## Files
- `run_schema.py:1` — `RunCreate{task}`, `RunOut{id,task,status}`.
- `invoice_schema.py:1` — `InvoiceCreate{vendor,invoice_no,amount,due_date?,source_file}`, `InvoiceOut(+id)`.
- `approval_schema.py:1` — `ApprovalIn{approved:bool,answer:str}`.
- `__init__.py` — marker.
