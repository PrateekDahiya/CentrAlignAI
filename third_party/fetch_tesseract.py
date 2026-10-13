"""One-time setup: ensure the Tesseract OCR engine exists for image_text().

Resolution (shared with backend/agent/tools/doc_text.py):
  TESSERACT_CMD env → third_party/tesseract → PATH → Program Files.
Strategy: winget silent install (no manual steps) → RunAsInvoker installer
fallback → clean instructions (no traceback) if everything fails.
Stdlib only. Idempotent — skips when the binary already exists.
"""
import os
import shutil
import subprocess
import sys
import urllib.request

VERSION = "5.4.0.20240606"
SETUP_URL = (f"https://github.com/UB-Mannheim/tesseract/releases/download/"
             f"v{VERSION}/tesseract-ocr-w64-setup-{VERSION}.exe")
APP_ID = "UB-Mannheim.TesseractOCR"

ROOT = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(ROOT, "tesseract")


def have_binary() -> bool:
    if os.environ.get("TESSERACT_CMD", ""):
        return True
    if shutil.which("tesseract"):
        return True
    guess = os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"),
                         "Tesseract-OCR", "tesseract.exe")
    return os.path.isfile(guess)


def via_winget() -> bool:
    if not shutil.which("winget"):
        return False
    print("installing via winget (silent) ...")
    r = subprocess.run(
        ["winget", "install", "-e", "--id", APP_ID, "--silent",
         "--accept-source-agreements", "--accept-package-agreements"],
        capture_output=True, text=True)
    return r.returncode == 0 and have_binary()


def via_installer() -> bool:
    os.makedirs(DEST, exist_ok=True)
    setup = os.path.join(DEST, "setup.exe")
    if not (os.path.isfile(setup) and os.path.getsize(setup) > 10_000_000):
        print(f"downloading {SETUP_URL} ...")
        urllib.request.urlretrieve(SETUP_URL, setup)
    print("installing silently (no admin) ...")
    env = dict(os.environ, __COMPAT_LAYER="RunAsInvoker")
    r = subprocess.run([setup, "/S", f"/D={DEST}"], env=env,
                       capture_output=True, text=True)
    return (r.returncode == 0
            and os.path.isfile(os.path.join(DEST, "tesseract.exe")))


def main() -> None:
    if have_binary():
        print("tesseract already available, skipping setup")
        return
    if os.name != "nt":
        sys.exit("non-Windows: install tesseract via your package manager "
                 "and set TESSERACT_CMD in .env")
    if via_winget() or via_installer():
        print("tesseract ready")
        return
    sys.exit("automatic install failed; run this once as admin:\n"
             f"  winget install -e --id {APP_ID} --silent\n"
             "or set TESSERACT_CMD in .env to your tesseract.exe")


if __name__ == "__main__":
    main()
