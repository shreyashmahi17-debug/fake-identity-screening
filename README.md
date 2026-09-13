# Fake Identity & Document Screening System

AI-powered document screening system that analyzes identity documents using OCR, face verification, tampering detection, and risk assessment.

## 🚀 Quick Start

### Frontend (Vercel)
```bash
cd frontend
npm install
npm run dev
```

### Backend (Render)
```bash
cd backend
pip install -r requirements.txt
python start.py
```

## 🌐 Live Deployment

- **Frontend**: Deploy on [Vercel](https://vercel.com)
- **Backend**: Deploy on [Render](https://render.com)

See [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md) for complete deployment guide.

## 📋 Features

- 📄 **OCR Text Extraction** - Extract text from identity documents
- 🧠 **Document Classification** - Detect document type
- 👤 **Face Verification** - Compare document face with reference image
- 🔍 **Tampering Detection** - Analyze image manipulation (ELA)
- ✅ **Data Consistency Check** - Validate extracted fields
- 📊 **Risk Assessment** - Calculate overall screening risk
- 📥 **Report Download** - Download detailed screening report

## 🛠️ Tech Stack

### Frontend
- React 19
- Vite
- CSS (Custom styling)

### Backend
- FastAPI
- OpenCV
- Tesseract OCR
- PIL (Pillow)
- NumPy

## 🔧 Configuration

### Environment Variables

Create `.env` in frontend directory:
```env
VITE_API_URL=https://fake-identity-screening.onrender.com
```

For local development:
```env
VITE_API_URL=http://localhost:10000
```

## 📦 Project Structure

```
fake-identity-screening/
├── frontend/                # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main component
│   │   ├── App.css         # Styles
│   │   └── main.jsx        # Entry point
│   ├── vercel.json         # Vercel config
│   └── package.json
│
├── backend/                 # FastAPI backend
│   ├── main.py             # API endpoints
│   ├── start.py            # Server startup
│   ├── services/           # Core services
│   │   ├── ocr.py
│   │   ├── face_verification.py
│   │   ├── tampering_detection.py
│   │   ├── risk_engine.py
│   │   └── ...
│   ├── Dockerfile
│   └── requirements.txt
│
└── render.yaml             # Render config
```

## 🚀 Deployment

### Deploy Frontend to Vercel

**Option 1: CLI**
```bash
cd frontend
vercel --prod
```

**Option 2: Dashboard**
1. Connect your Git repository
2. Set Root Directory: `frontend`
3. Add environment variable: `VITE_API_URL`
4. Deploy

### Deploy Backend to Render

1. Connect your Git repository
2. Render auto-detects `render.yaml`
3. Backend deploys automatically

See [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md) for detailed instructions.

## 🔍 API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "success",
  "message": "Fake Document Screening API is running!"
}
```

### `GET /health`
Service health status
```json
{
  "status": "healthy",
  "service": "Fake Document Screening API"
}
```

### `POST /ocr`
Analyze document and reference face

**Request**: `multipart/form-data`
- `document_file`: Identity document image
- `reference_file`: Reference face image

**Response**: Complete analysis including OCR, face verification, tampering, and risk assessment

## 📊 Screening Signals

| Signal | Description | Weight |
|--------|-------------|--------|
| OCR Confidence | Text extraction quality | - |
| Face Similarity | Document vs reference face match | 30% |
| Tampering Signal | ELA-based manipulation detection | 30% |
| Data Consistency | Field validation and completeness | 10% |
| Image Quality | Blur, brightness analysis | 10% |
| Field Validation | Name, DOB, document number check | 20% |

## 🐛 Troubleshooting

### Frontend Connection Error

**Symptom**: "Failed to fetch" or "Network error"

**Solution**:
1. Check backend is running: `curl https://fake-identity-screening.onrender.com/health`
2. Verify `VITE_API_URL` environment variable
3. Wait 30-60 seconds (Render free tier cold start)
4. Check browser console for detailed errors

### Backend Cold Start

**Symptom**: First request takes 30-60 seconds

**Solution**: This is normal for Render free tier. Upgrade to paid plan for instant response.

### CORS Error

**Solution**: Backend already configured with proper CORS. If error persists, check backend logs on Render dashboard.

## 📝 Notes

⚠️ **Prototype Disclaimer**: This system provides preliminary risk screening only. It is not a legal determination of document authenticity or final identity verification. Manual verification is recommended for high-risk cases.

## 🔐 Security

- File uploads use UUID-based temporary storage
- Path traversal protection
- CORS properly configured
- No sensitive data in logs
- Automatic temp file cleanup

## 📄 License

This is a prototype project for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For deployment issues, see [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)

---

**Built with ❤️ for secure identity verification**
