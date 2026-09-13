# 🚀 Deployment Checklist

Follow this checklist to deploy your application successfully.

---

## ☑️ Pre-Deployment Checklist

- [x] Backend CORS updated
- [x] Health endpoint added
- [x] Frontend error handling enhanced
- [x] Environment files created
- [x] Vercel configuration updated
- [x] Documentation written
- [ ] **Backend changes pushed to Git** ⬅️ START HERE
- [ ] **Render redeployment complete**
- [ ] **Frontend deployed to Vercel**

---

## 📝 Step-by-Step Deployment

### ✅ Step 1: Push Backend Changes (5 minutes)

```bash
cd /home/gunjan/Ritik/fake-identity-screening

# Check what files changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "fix: Enhanced CORS and error handling for Vercel deployment

- Updated CORS middleware with explicit Vercel domain support
- Added /health endpoint for monitoring
- Added OPTIONS handler for CORS preflight
- Enhanced frontend error messages
- Increased timeout to 120s for cold starts
- Created deployment documentation"

# Push to remote
git push
```

**Expected Output:**
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
Total X (delta X), reused 0 (delta 0)
To <your-git-repo>
   abc1234..def5678  main -> main
```

✅ **Mark as done when pushed successfully**

---

### ✅ Step 2: Wait for Render Deployment (2-3 minutes)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Open your service: `fake-identity-screening`
3. Watch the "Events" tab for new deployment

**Expected Events:**
```
⏳ Deploy started
📦 Building...
🚀 Deploy live
```

4. Once you see "Deploy live", proceed to next step

✅ **Mark as done when deployment is live**

---

### ✅ Step 3: Test Backend (1 minute)

```bash
cd /home/gunjan/Ritik/fake-identity-screening
./test-backend.sh
```

**Expected Output:**
```
✅ Root endpoint working!
✅ Health endpoint working!
✅ CORS preflight working!
✅ Response time: Xs (Backend is warm)
```

**If health endpoint fails (404):**
- Backend not redeployed yet, wait 1 more minute
- Then run test again

✅ **Mark as done when all tests pass**

---

### ✅ Step 4: Deploy Frontend to Vercel

#### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI (if not installed)
npm install -g vercel

# Login to Vercel
vercel login

# Deploy frontend
cd frontend
vercel --prod
```

**Follow the prompts:**
```
? Set up and deploy "frontend"? [Y/n] Y
? Which scope? <your-account>
? Link to existing project? [y/N] N
? What's your project's name? fake-identity-screening
? In which directory is your code located? ./
? Want to override the settings? [y/N] N
```

**Expected Output:**
```
🔍 Inspect: https://vercel.com/...
✅ Production: https://fake-identity-screening-xxx.vercel.app
```

#### Option B: Using Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select your repository
4. **Configure Project:**
   - Project Name: `fake-identity-screening`
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Environment Variables:**
   - Key: `VITE_API_URL`
   - Value: `https://fake-identity-screening.onrender.com`
   - Environment: Production, Preview, Development
6. Click **"Deploy"**

✅ **Mark as done when deployment is complete**

---

### ✅ Step 5: Test Full Application (2 minutes)

1. **Open your Vercel URL** in browser:
   ```
   https://fake-identity-screening-xxx.vercel.app
   ```

2. **Upload test files:**
   - Document: Any ID card or document image
   - Reference: Face photo

3. **Click "Analyze Document"**
   - First request may take 30-60 seconds (cold start)
   - Watch for processing steps animation

4. **Verify results displayed:**
   - Risk score shown
   - All signals displayed
   - No connection errors

**Success Indicators:**
- ✅ No "Failed to fetch" error
- ✅ No CORS error in browser console
- ✅ Results displayed correctly
- ✅ Can download report

✅ **Mark as done when full flow works**

---

## 🎊 Post-Deployment

### Share Your Links

**Frontend (Vercel):**
```
https://fake-identity-screening-xxx.vercel.app
```

**Backend (Render):**
```
https://fake-identity-screening.onrender.com
```

**Health Check:**
```
https://fake-identity-screening.onrender.com/health
```

---

## 🐛 Troubleshooting

### Problem: Git push rejected

**Solution:**
```bash
git pull --rebase
git push
```

### Problem: Vercel build fails

**Check:**
1. Root directory is set to `frontend`
2. Build command is `npm run build`
3. Node version is compatible (use 18.x or 20.x)

**Solution:**
```bash
# In Vercel dashboard → Settings → General
# Node.js Version: 20.x
```

### Problem: Frontend shows "Failed to fetch"

**Debug Steps:**
1. Check browser console for exact error
2. Test backend: `curl https://fake-identity-screening.onrender.com/health`
3. Check Network tab in browser DevTools
4. Verify VITE_API_URL in Vercel environment variables

### Problem: Backend not responding

**Check Render Logs:**
1. Render Dashboard → Your Service → Logs
2. Look for errors or crash reports
3. Verify deployment succeeded

### Problem: Cold start taking too long

**Expected:** 30-60 seconds on Render free tier

**Solutions:**
- Wait patiently for first request
- Upgrade to Render paid plan ($7/month) for instant response
- Keep backend warm with external monitoring (uptime robot)

---

## 📊 Deployment Status

```
┌─────────────────────────────────────┐
│  Component    │  Status   │  URL    │
├─────────────────────────────────────┤
│  Backend      │  ⏳ TODO  │  Render │
│  Frontend     │  ⏳ TODO  │  Vercel │
│  Testing      │  ⏳ TODO  │  Manual │
└─────────────────────────────────────┘
```

---

## 🎯 Success Criteria

- [ ] Backend health endpoint returns 200 OK
- [ ] Frontend loads without errors
- [ ] File upload works
- [ ] Document analysis completes successfully
- [ ] Results display correctly
- [ ] Report download works
- [ ] No CORS errors in console
- [ ] No connection errors

---

## 📞 Need Help?

1. Check `VERCEL_DEPLOYMENT.md` for detailed guide
2. Check `FIXED_ISSUES.md` for what was changed
3. Run `./test-backend.sh` to diagnose backend issues
4. Check browser console for frontend errors
5. Check Render logs for backend errors

---

**Time Estimate:** 10-15 minutes total

**Current Step:** Push backend changes to Git (Step 1)

**GO! 🚀**
