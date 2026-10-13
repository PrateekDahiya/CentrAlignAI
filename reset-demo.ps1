# Reset local demo state before recording: clears run trace mirrors and
# regenerates mock inbox PDFs. ERP rows in MySQL are left untouched
# (the video enters INV-1001, which is not in the ERP yet).
# Run from repo root:  powershell -ExecutionPolicy Bypass -File reset-demo.ps1
Remove-Item -Recurse -Force runs/* -ErrorAction SilentlyContinue
python -m backend.seed.make_pdfs
Write-Output 'reset done: runs/ cleared, inbox PDFs regenerated'
