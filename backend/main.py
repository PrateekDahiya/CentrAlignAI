"""FastAPI entrypoint: wiring only, no business logic."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import erp_router, inbox_router, runs_router, approval_router, events_router, trace_router

app = FastAPI(title="CentrAlignAI Worker")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(erp_router.router)
app.include_router(inbox_router.router)
app.include_router(runs_router.router)
app.include_router(approval_router.router)
app.include_router(events_router.router)
app.include_router(trace_router.router)


@app.get("/api/health")
def health():
    return {"ok": True}
