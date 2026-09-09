#!/usr/bin/env python3
"""
Startup diagnostics — runs before uvicorn.
Prints exactly which import or step fails so we can debug on Render.
"""
import sys
import os

print("==> Python version:", sys.version)
print("==> Testing imports...")

try:
    import cv2
    print("    [OK] cv2:", cv2.__version__)
except Exception as e:
    print("    [FAIL] cv2:", e)
    sys.exit(1)

try:
    import numpy as np
    print("    [OK] numpy:", np.__version__)
except Exception as e:
    print("    [FAIL] numpy:", e)
    sys.exit(1)

try:
    import pytesseract
    print("    [OK] pytesseract:", pytesseract.get_tesseract_version())
except Exception as e:
    print("    [WARN] pytesseract:", e)
    # Not fatal — continue

try:
    from PIL import Image
    print("    [OK] PIL/Pillow")
except Exception as e:
    print("    [FAIL] PIL:", e)
    sys.exit(1)

try:
    import fastapi
    print("    [OK] fastapi:", fastapi.__version__)
except Exception as e:
    print("    [FAIL] fastapi:", e)
    sys.exit(1)

try:
    import uvicorn
    print("    [OK] uvicorn:", uvicorn.__version__)
except Exception as e:
    print("    [FAIL] uvicorn:", e)
    sys.exit(1)

print("==> All imports OK. Starting server...")

port = int(os.environ.get("PORT", 10000))
uvicorn.run("main:app", host="0.0.0.0", port=port)
