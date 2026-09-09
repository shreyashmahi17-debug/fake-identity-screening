import sys
import os
import traceback

print("==> Diagnostic start.py running", flush=True)
print("==> Python:", sys.version, flush=True)
print("==> PORT env:", os.environ.get("PORT", "NOT SET"), flush=True)

# Test cv2
try:
    import cv2
    print("[OK] cv2:", cv2.__version__, flush=True)
except Exception as e:
    print("[FAIL] cv2:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)

# Test numpy
try:
    import numpy as np
    print("[OK] numpy:", np.__version__, flush=True)
except Exception as e:
    print("[FAIL] numpy:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)

# Test PIL
try:
    from PIL import Image
    print("[OK] PIL", flush=True)
except Exception as e:
    print("[FAIL] PIL:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)

# Test pytesseract
try:
    import pytesseract
    print("[OK] pytesseract imported", flush=True)
except Exception as e:
    print("[FAIL] pytesseract:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)

# Test fastapi
try:
    import fastapi
    print("[OK] fastapi:", fastapi.__version__, flush=True)
except Exception as e:
    print("[FAIL] fastapi:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)

# Test uvicorn
try:
    import uvicorn
    print("[OK] uvicorn:", uvicorn.__version__, flush=True)
except Exception as e:
    print("[FAIL] uvicorn:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)

# Test main app import
try:
    from main import app
    print("[OK] main:app imported", flush=True)
except Exception as e:
    print("[FAIL] main:app:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)

# Start server
port = int(os.environ.get("PORT", 10000))
print(f"==> Starting uvicorn on port {port}", flush=True)

try:
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
except Exception as e:
    print("[FAIL] uvicorn.run:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)
