"""Independent completion check. Fail-closed: doubt means not verified."""
import json
from sqlalchemy.orm import Session
from backend.agent.groq_client import chat
from backend.agent.prompts.verifier_prompt import VERIFIER_SYSTEM
from backend.agent.memory import save_fact, get_facts
from backend.config import settings
from backend.models.invoice import Invoice
from backend.models.step import Step
from backend.utils.logging import inside


def extract_verdict(text: str) -> dict:
    inside("extract_verdict", text[:60])
    try:
        return json.loads(text)
    except ValueError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        try:
            return json.loads(text[start:end + 1])
        except ValueError:
            pass
    return {}


def gather_evidence(db: Session, run_id: str) -> str:
    inside("gather_evidence", run_id)
    facts = get_facts(db, run_id)
    steps = db.query(Step).filter_by(run_id=run_id).order_by(Step.n).all()
    rows = db.query(Invoice).order_by(Invoice.id.desc()).limit(20).all()
    lines = [f"OBJECTIVE: {facts.get('objective', '-')}",
             f"CRITERIA: {facts.get('success_criteria', '[]')}"]
    lines += [f"STEP {s.n} [{s.tool}]: {(s.obs or '')[:1500]}" for s in steps]
    trace = " ".join((s.obs or "") for s in steps).lower()

    def mentioned(r) -> bool:
        if r.invoice_no and r.invoice_no.lower() in trace:
            return True
        return any(w in trace for w in (r.vendor or "").lower().split()
                   if len(w) > 3)

    hits = [r for r in rows if mentioned(r)]
    if hits:
        lines.append("ERP (rows referenced by this run):")
        lines += [f"- {r.vendor} {r.invoice_no} {float(r.amount):.2f} {r.due_date}"
                  for r in hits]
    else:
        lines.append("ERP: (no rows referenced by this run's steps)")
    return "\n".join(lines)


def verify_run(db: Session, run_id: str) -> dict:
    inside("verify_run", run_id)
    try:
        res = chat(
            [{"role": "system", "content": VERIFIER_SYSTEM},
             {"role": "user", "content": gather_evidence(db, run_id)}],
            primary=settings.verifier_model,
            fallback=settings.executor_fallback,
        )
        verdict = extract_verdict(res.choices[0].message.content or "")
        verified = bool(verdict.get("verified", False))
        note = str(verdict.get("evidence", ""))[:1000]
    except Exception as e:
        verified, note = False, f"verifier error: {e}"
    save_fact(db, run_id, "verification",
              json.dumps({"verified": verified, "evidence": note}))
    return {"verified": verified, "evidence": note}
