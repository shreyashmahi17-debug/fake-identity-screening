# 🚀 Vercel Deployment - Environment Variable Setup

## ⚠️ CRITICAL: Environment Variable Required!

Your Vercel deployment **MUST** have the environment variable set, otherwise frontend cannot connect to backend.

---

## 📋 Step-by-Step Vercel Setup

### Method 1: Vercel Dashboard (Recommended)

#### Step 1: Go to Your Project Settings

1. Open [vercel.com](https://vercel.com)
2. Select your project: `fake-identity-screening`
3. Click **"Settings"** tab
4. Click **"Environment Variables"** in left sidebar

#### Step 2: Add Environment Variable

Click **"Add New"** and enter:

```
Name:  VITE_API_URL
Value: https://fake-identity-screening.onrender.com
```

**Important:**
- ✅ Check **Production**
- ✅ Check **Preview**  
- ✅ Check **Development**

Click **"Save"**

#### Step 3: Redeploy

After adding the variable:

1. Go to **"Deployments"** tab
2. Find latest deployment
3. Click **⋮** (three dots)
4. Click **"Redeploy"**
5. Select **"Use existing Build Cache"**
6. Click **"Redeploy"**

Wait 30-60 seconds for deployment to complete.

---

### Method 2: Vercel CLI

```bash
cd frontend

# Set environment variable
vercel env add VITE_API_URL

# When prompted:
# Value: https://fake-identity-screening.onrender.com
# Expose to: Production, Preview, Development

# Redeploy
vercel --prod
```

---

## 🧪 Verify Environment Variable

After redeployment, check in browser console:

```javascript
// Open your Vercel site
// Press F12 (DevTools)
// Go to Console tab
// Type:
import.meta.env.VITE_API_URL

// Should show:
// "https://fake-identity-screening.onrender.com"
```

---

## 🔍 Debugging Connection Issues

### Issue 1: "Cannot connect to backend"

**Check:**
```bash
# Test backend is running
curl https://fake-identity-screening.onrender.com/health

# Should return:
{"status":"healthy","service":"Fake Document Screening API"}
```

**If 404 or timeout:**
- Backend might be sleeping (Render free tier)
- Wait 30-60 seconds for cold start
- Try again

### Issue 2: CORS Error

**Check backend logs on Render:**
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Select your service
3. Click **"Logs"** tab
4. Look for CORS-related errors

**Solution:**
- Backend already has CORS configured
- Make sure latest backend code is deployed
- Redeploy backend if needed

### Issue 3: Environment Variable Not Working

**Symptoms:**
- Backend URL shows as `undefined`
- Console shows `https://undefined/ocr`

**Solution:**
1. Check environment variable is set in Vercel
2. Variable name MUST be `VITE_API_URL` (case-sensitive)
3. Redeploy after setting variable
4. Clear browser cache

---

## 📝 Complete Deployment Checklist

### Backend (Render):

- [ ] Code pushed to Git
- [ ] Render auto-deployed
- [ ] Health endpoint working: `curl https://fake-identity-screening.onrender.com/health`
- [ ] CORS configured (already done in code)

### Frontend (Vercel):

- [ ] Environment variable `VITE_API_URL` set
- [ ] Variable includes all environments (Production, Preview, Development)
- [ ] Code deployed via `vercel --prod` or dashboard
- [ ] Deployment successful (no build errors)
- [ ] Site accessible

### Testing:

- [ ] Open Vercel site in browser
- [ ] Upload document and reference images
- [ ] Click "Analyze Document"
- [ ] Wait 30-60 seconds (cold start on first request)
- [ ] Results display correctly
- [ ] No console errors

---

## 🎯 Quick Test Script

After deployment, run this in browser console:

```javascript
// Test 1: Check environment variable
console.log('Backend URL:', import.meta.env.VITE_API_URL);
// Expected: https://fake-identity-screening.onrender.com

// Test 2: Check backend health
fetch('https://fake-identity-screening.onrender.com/health')
  .then(r => r.json())
  .then(d => console.log('Backend health:', d))
  .catch(e => console.error('Backend error:', e));
// Expected: {status: "healthy", service: "..."}
```

---

## 🚨 Common Mistakes

### ❌ Wrong variable name
```
VITE_BACKEND_URL  ← WRONG
API_URL           ← WRONG
VITE_API_URL      ← CORRECT ✅
```

### ❌ Missing protocol
```
fake-identity-screening.onrender.com  ← WRONG
https://fake-identity-screening.onrender.com  ← CORRECT ✅
```

### ❌ Forgot to redeploy after setting variable
- Environment variables require a redeploy to take effect!

### ❌ Not checking all environments
- Make sure Production, Preview, AND Development are checked

---

## 📊 Expected Result After Fix

**Before (Error):**
```
❌ Network error: Cannot connect to backend
```

**After (Working):**
```
✅ Processing steps animate
✅ Results display
✅ Risk score shown
✅ All signals present
```

---

## 💡 Pro Tips

1. **First request is slow**: Render free tier sleeps after 15 minutes. First request takes 30-60 seconds to wake up. This is normal!

2. **Use browser DevTools**: 
   - Network tab shows API calls
   - Console shows errors
   - Application tab shows environment

3. **Test backend separately**:
   ```bash
   curl https://fake-identity-screening.onrender.com/health
   ```

4. **Check Render logs** if backend issues persist

---

## 🎉 Success Indicators

✅ No "Failed to fetch" errors
✅ Backend URL visible in error messages
✅ Processing animation runs
✅ Results display after analysis
✅ Download report works
✅ Console shows "✅ Analysis complete"

---

**Current Status**: Environment variable setup ready

**Next**: Set `VITE_API_URL` in Vercel dashboard → Redeploy → Test!
