# Vercel Deployment Guide for Fake Identity Screening System

## Architecture
- **Frontend**: React + Vite → Deploy on **Vercel**
- **Backend**: FastAPI + Python → Deploy on **Render** (already configured)

## Why This Setup?
- Backend has heavy dependencies (OpenCV, Tesseract) that cannot run on Vercel serverless
- Frontend is static and perfect for Vercel's edge network
- Backend stays on Render where Docker support exists

---

## Step 1: Deploy Backend on Render (Already Done ✅)

Your backend is already deployed at:
```
https://fake-identity-screening.onrender.com
```

Test it:
```bash
curl https://fake-identity-screening.onrender.com/
```

**Important**: Render free tier goes to sleep after 15 minutes of inactivity. First request takes 30-60 seconds to wake up.

---

## Step 2: Deploy Frontend on Vercel

### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy from frontend directory**
```bash
cd frontend
vercel
```

4. **For Production Deployment**
```bash
vercel --prod
```

### Option B: Using Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your Git repository
4. **Root Directory**: Set to `frontend`
5. **Framework Preset**: Vite
6. **Build Command**: `npm run build`
7. **Output Directory**: `dist`
8. **Environment Variables**: Add `VITE_API_URL` = `https://fake-identity-screening.onrender.com`
9. Click "Deploy"

---

## Step 3: Configure Environment Variables

### In Vercel Dashboard:
1. Go to Project Settings
2. Navigate to "Environment Variables"
3. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://fake-identity-screening.onrender.com`
   - **Environment**: Production, Preview, Development

---

## Step 4: Verify Deployment

After deployment, test your Vercel URL:

1. **Check Frontend**
```
https://your-project.vercel.app
```

2. **Check Backend Connection**
   - Upload a test document
   - Should connect to Render backend
   - First request might take 30-60 seconds (cold start)

---

## Troubleshooting

### Issue 1: "Failed to fetch" or CORS Error

**Solution**: Backend CORS is already configured to allow all origins including Vercel domains.

If still facing issues, check backend logs:
```bash
# Go to Render dashboard → Your service → Logs
```

### Issue 2: "Request timeout"

**Cause**: Render free tier cold start

**Solution**: 
- Wait 30-60 seconds
- Try again
- Consider upgrading Render plan for instant response

### Issue 3: Environment Variable Not Working

**Check**:
1. Vercel environment variable is set correctly
2. Variable name starts with `VITE_` (required for Vite)
3. Redeploy after changing environment variables

### Issue 4: Backend Not Responding

**Check Backend Health**:
```bash
curl https://fake-identity-screening.onrender.com/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "Fake Document Screening API"
}
```

---

## Local Development Setup

### Frontend (with local backend)
```bash
cd frontend
cp .env.local .env
npm install
npm run dev
```

### Backend (local)
```bash
cd backend
pip install -r requirements.txt
python start.py
```

---

## Project Structure

```
fake-identity-screening/
├── frontend/                 # Vercel deployment
│   ├── src/
│   ├── .env                 # Current config
│   ├── .env.production      # Production config (new)
│   ├── .env.local           # Local development (new)
│   ├── vercel.json          # Updated with proper config
│   └── package.json
│
└── backend/                  # Render deployment
    ├── main.py              # Updated with better CORS
    ├── start.py
    ├── Dockerfile
    ├── requirements.txt
    └── services/
```

---

## What Was Fixed?

### Backend (`main.py`)
✅ Enhanced CORS configuration
✅ Added `/health` endpoint for monitoring
✅ Added OPTIONS handler for preflight requests
✅ Better error responses

### Frontend
✅ Created `.env.production` for Vercel
✅ Created `.env.local` for local development
✅ Updated `vercel.json` with full configuration
✅ Enhanced error handling with detailed messages
✅ Increased timeout to 120 seconds for cold starts
✅ Added console logging for debugging

---

## Next Steps

1. **Deploy Backend Changes**:
```bash
git add .
git commit -m "fix: Enhanced CORS and error handling for Vercel deployment"
git push
```

Render will auto-deploy from your Git repository.

2. **Deploy Frontend to Vercel**:
```bash
cd frontend
vercel --prod
```

3. **Test the Full Flow**:
   - Visit your Vercel URL
   - Upload test document and reference face
   - Wait for analysis (first request = cold start)
   - Verify results display correctly

---

## Environment Variables Reference

| Variable | Value | Where |
|----------|-------|-------|
| `VITE_API_URL` | `https://fake-identity-screening.onrender.com` | Vercel |
| `PORT` | `10000` (auto-set) | Render |

---

## Monitoring

### Backend Logs (Render)
```
Render Dashboard → Your Service → Logs
```

### Frontend Logs (Vercel)
```
Vercel Dashboard → Your Project → Functions → Logs
```

### Browser Console
Check Network tab and Console for detailed error messages

---

## Cost Consideration

- **Vercel**: Free tier (perfect for frontend)
- **Render**: Free tier with cold starts OR $7/month for instant response

---

## Support

If issues persist:
1. Check backend health: `curl https://fake-identity-screening.onrender.com/health`
2. Check Render logs for backend errors
3. Check browser console for frontend errors
4. Verify environment variables in Vercel dashboard

---

**Status**: ✅ Ready to deploy!
