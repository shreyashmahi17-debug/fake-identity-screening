# 🧪 TEST YOUR APP NOW!

## ✅ Everything is Running!

- **Backend**: http://localhost:10000 (Mock OCR Mode)
- **Frontend**: http://localhost:5173

## 📋 Quick Test Steps:

### 1. Open Browser
```
http://localhost:5173
```

### 2. Upload Images

**Document Image:**
- Upload ANY image (JPEG/PNG)
- Can be any photo (mock mode doesn't actually read it)

**Reference Face:**
- Upload a face photo
- Or ANY image (mock mode)

### 3. Click "Analyze Document"

### 4. See Results!

You'll see:
- ✅ Risk Score
- ✅ OCR Confidence (mock: 85.5%)
- ✅ Extracted Data (mock: Rajesh Kumar Sharma)
- ✅ Face Verification
- ✅ Tampering Detection
- ✅ Data Consistency Check

### 5. Download Report

Click "Download Screening Report" to get a text file!

---

## ⚠️ Mock Mode Notice

You'll see this in backend logs:
```
🧪 [MOCK OCR] Using test data for: <filename>
```

This is NORMAL and EXPECTED! 

**Why Mock Mode?**
- Tesseract binary not installed
- Perfect for testing UI/flow
- Production (Render) has real OCR

**Real OCR on Render**: ✅ Automatic (Dockerfile installs it)

---

## 🐛 If You See Errors:

### Network Error
- Check backend is running: `curl http://localhost:10000/health`
- Check frontend .env.local has: `VITE_API_URL=http://localhost:10000`

### CORS Error
- Backend already configured for CORS
- Restart backend if needed

### Upload Fails
- Any image format works (JPEG, PNG)
- File size < 10MB recommended

---

## 📊 What to Check:

✅ Upload interface works
✅ Processing steps animate
✅ Results display correctly
✅ All signals show (OCR, Face, Tampering, etc.)
✅ Report downloads
✅ No JavaScript errors in console

---

## 🚀 Ready for Deployment?

If everything works locally:

1. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: Local + Vercel setup with mock OCR fallback"
   git push
   ```

2. **Wait for Render** to redeploy backend (2-3 min)

3. **Deploy frontend to Vercel**:
   ```bash
   cd frontend
   vercel --prod
   ```

4. **Test live deployment** - will have REAL OCR!

---

**GO TEST IT NOW!** 🎯

Browser → http://localhost:5173
