# 🔧 Fix Vercel "Cannot Connect to Backend" Error

## 🎯 The Problem

Your Vercel frontend shows:
```
❌ Network error: Cannot connect to backend
```

## ✅ The Solution (2 Minutes)

### Step 1: Open Vercel Dashboard

Go to: https://vercel.com/dashboard

### Step 2: Select Your Project

Click on: `fake-identity-screening` (or your project name)

### Step 3: Go to Settings

Top menu → Click **Settings**

### Step 4: Environment Variables

Left sidebar → Click **Environment Variables**

### Step 5: Add Variable

Click **"Add New"** button

Fill in:
```
┌─────────────────────────────────────────────────┐
│ Name                                            │
│ VITE_API_URL                                    │
├─────────────────────────────────────────────────┤
│ Value                                           │
│ https://fake-identity-screening.onrender.com    │
├─────────────────────────────────────────────────┤
│ Environments                                    │
│ ☑ Production                                    │
│ ☑ Preview                                       │
│ ☑ Development                                   │
└─────────────────────────────────────────────────┘
```

Click **"Save"**

### Step 6: Redeploy

1. Go to **"Deployments"** tab (top menu)
2. Find the latest deployment
3. Click **⋮** (three dots menu)
4. Click **"Redeploy"**
5. Click **"Redeploy"** again to confirm

### Step 7: Wait & Test

- Wait 30-60 seconds for deployment
- Refresh your Vercel site
- Upload images and test
- First request may take 30-60s (backend cold start - normal!)

---

## 🧪 Verify It's Fixed

Open browser console (F12) on your Vercel site and run:

```javascript
console.log(import.meta.env.VITE_API_URL)
```

**Should show:**
```
https://fake-identity-screening.onrender.com
```

**If it shows `undefined`:**
- Variable not set correctly
- Need to redeploy
- Try again from Step 3

---

## 📊 Before & After

### ❌ Before (Error):
```
Network error: Cannot connect to backend
Backend URL: undefined
```

### ✅ After (Fixed):
```
✅ Processing animation
✅ Results displayed
✅ Backend URL: https://fake-identity-screening.onrender.com
```

---

## ⏱️ First Request is Slow?

**This is NORMAL!**

Render free tier sleeps after 15 minutes of inactivity.

First request wakes it up:
- Takes 30-60 seconds
- Subsequent requests are fast
- Not an error, just cold start

**Solution:** Wait patiently or upgrade Render plan

---

## 🆘 Still Not Working?

### Check 1: Backend is Running

Open terminal and run:
```bash
curl https://fake-identity-screening.onrender.com/health
```

**Should return:**
```json
{"status":"healthy","service":"Fake Document Screening API"}
```

**If timeout:** Backend is waking up, wait 60s and try again

**If 404:** Backend not deployed, check Render dashboard

### Check 2: CORS Issues

If browser console shows CORS error:
1. Backend code has CORS configured (already done)
2. Make sure latest backend is deployed on Render
3. Check Render logs for errors

### Check 3: Clear Cache

- Clear browser cache
- Try incognito/private window
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

---

## 📝 Quick Checklist

- [ ] Environment variable `VITE_API_URL` added in Vercel
- [ ] Variable includes `https://` protocol
- [ ] All three environments checked (Production, Preview, Development)
- [ ] Redeployed after adding variable
- [ ] Backend health check returns 200 OK
- [ ] Waited 30-60s for backend cold start
- [ ] Browser cache cleared

---

## 🎉 Success Indicators

When everything works:

✅ Upload interface loads
✅ Can select files
✅ "Analyze Document" button works
✅ Processing steps animate
✅ Results display after analysis
✅ No errors in browser console
✅ Can download report

---

## 💡 Pro Tip

Add this to browser console for debugging:

```javascript
// Show all environment variables
console.table({
  'Backend URL': import.meta.env.VITE_API_URL,
  'Mode': import.meta.env.MODE,
  'Base URL': import.meta.env.BASE_URL
});

// Test backend connectivity
fetch('https://fake-identity-screening.onrender.com/health')
  .then(r => r.json())
  .then(d => console.log('✅ Backend:', d))
  .catch(e => console.error('❌ Backend:', e));
```

---

**Total Time:** 2-3 minutes
**Difficulty:** Easy
**Success Rate:** 100% if followed correctly

**GO FIX IT NOW!** 🚀
