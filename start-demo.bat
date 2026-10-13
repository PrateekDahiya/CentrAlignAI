@echo off
REM One-command demo launcher. Run from repo root:  start-demo.bat
REM Opens backend (8000) + frontend (5173) in two windows.
start "CentrAlignAI-backend" powershell -NoExit -Command "uvicorn backend.main:app --port 8000 --reload"
start "CentrAlignAI-frontend" powershell -NoExit -Command "cd frontend; npm run dev"
echo API: http://localhost:8000/api/health   UI: http://localhost:5173
