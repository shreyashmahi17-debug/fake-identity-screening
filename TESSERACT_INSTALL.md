# Tesseract OCR Installation Guide

## ⚠️ Current Status

**Tesseract binary is NOT installed** on your system. The application is running with **MOCK OCR** for testing.

## 🧪 Mock Mode

The app will work but return fake data:
- Mock name: "Rajesh Kumar Sharma"
- Mock DOB: "15/08/1990"
- Mock confidence: 85.5%

This is perfect for testing the UI and flow!

## 📦 Install Tesseract (For Real OCR)

### On Kali Linux / Debian / Ubuntu:

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng
```

### Verify Installation:

```bash
tesseract --version
```

Should show:
```
tesseract 5.x.x
```

### Restart Backend After Installation:

```bash
cd backend
source venv/bin/activate
python start.py
```

## ✅ How to Test Now (Mock Mode)

1. **Open browser**: http://localhost:5173

2. **Upload any images**:
   - Document: Any image file (doesn't matter)
   - Reference: Any face image (doesn't matter)

3. **Click "Analyze Document"**

4. **Results will show**:
   - Mock OCR data
   - Real face verification (if faces detected)
   - Real tampering detection
   - Real risk assessment

## 🎯 What Works in Mock Mode?

✅ UI/UX testing
✅ Upload flow
✅ Error handling
✅ Results display
✅ Report download
✅ Face verification (uses OpenCV)
✅ Tampering detection (uses OpenCV)
✅ Risk engine calculations

❌ Real OCR from uploaded documents

## 🚀 Production Deployment

On **Render**, tesseract is installed automatically via Dockerfile:

```dockerfile
RUN apt-get install -y tesseract-ocr tesseract-ocr-eng
```

So production will have real OCR! Mock mode is ONLY for local testing.

## 💡 Tips

- Mock mode is great for frontend development
- No need to install tesseract just to test UI
- For full E2E testing, install tesseract
- Render deployment will have real OCR automatically

---

**Current Mode**: 🧪 MOCK OCR (Test Mode)

**To enable real OCR**: Install tesseract and restart backend
