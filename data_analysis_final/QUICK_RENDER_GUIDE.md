# Render Deployment - Quick Visual Guide

## 🎯 5-Minute Deployment

### **Step 1: Go to Render.com**
```
1. Open: https://render.com
2. Click "Sign Up" (top right)
3. Choose "Sign up with GitHub"
4. Authorize & confirm
```

### **Step 2: Create Web Service**
```
Home Dashboard → New (+) → Web Service
```

### **Step 3: Connect GitHub Repo**
```
1. Under "Connect Repository" click "New Repository"
2. Or select existing repo "data-analysis-agent"
3. Click "Connect"
```

### **Step 4: Fill in Settings**

```
Name:                    data-analysis-agent-backend
Environment:             Python 3
Region:                  Ohio or closest to you
Branch:                  main
Root Directory:          (leave empty)
Build Command:           pip install -r requirements.txt
Start Command:           gunicorn app:app --timeout 120
```

### **Step 5: Keep Scrolling (No other changes needed)**

```
Instance Type:           Free (default)
Auto Deploy:             Yes (default)
Click "Create Web Service"
```

### **Step 6: Wait for Deployment**

```
You'll see:
├─ Building
├─ Installing dependencies
├─ Starting server
└─ Deployed! ✅
```

Takes 2-5 minutes. Watch the logs!

### **Step 7: Copy Your URL**

```
At the top of the page you'll see:
https://data-analysis-agent-backend-xxxx.onrender.com

Full API URL is:
https://data-analysis-agent-backend-xxxx.onrender.com/api
```

### **Step 8: Update Frontend**

Open `index.html` and change line 3:

**From:**
```javascript
const API_URL = 'http://localhost:5000/api';
```

**To:**
```javascript
const API_URL = 'https://data-analysis-agent-backend-xxxx.onrender.com/api';
```

(Replace `xxxx` with your actual Render URL)

### **Step 9: Deploy Frontend (Optional)**

If you want the frontend on Netlify too:
```bash
git add index.html
git commit -m "Update API URL"
git push
```

Then on Netlify: New Site → Select repo → Deploy

---

## ✅ Test Your Deployment

### **Test 1: Check Backend Health**
Open in browser:
```
https://data-analysis-agent-backend-xxxx.onrender.com/api/health
```

Should show:
```json
{"status": "healthy"}
```

### **Test 2: Try the Web App**
- Open `index.html` locally in browser
- Upload `data/sample_data.csv`
- Click "Analyze"
- See results! 🎉

---

## 🔗 Full URLs After Deployment

| Component | URL |
|-----------|-----|
| **Backend API** | `https://data-analysis-agent-backend-xxxx.onrender.com` |
| **Health Check** | `https://data-analysis-agent-backend-xxxx.onrender.com/api/health` |
| **Analysis Endpoint** | `https://data-analysis-agent-backend-xxxx.onrender.com/api/analyze` |
| **Frontend (Local)** | `file:///path/to/index.html` |
| **Frontend (Netlify, if deployed)** | `https://yourname.netlify.app` |

---

## ⚡ Common Issues & Fixes

### ❌ "Build failed"
**Check logs** on Render dashboard. Most likely:
- Missing `requirements.txt`
- Typo in `Procfile`
- Python version issue

**Fix:** Check file contents and redeploy

### ❌ "Port xxx required"
**Not an issue** - Render auto-assigns ports

### ❌ "Timeout after 120s"
**Likely:** Analysis taking too long
- Start with smaller files
- Or upgrade to paid plan for more CPU

### ❌ "CORS error" when testing
**Check:**
```javascript
// Should be EXACTLY (with /api at end):
const API_URL = 'https://your-render-url.onrender.com/api';
```

### ❌ "Cannot reach backend"
1. Test health endpoint in browser
2. Check Render logs for errors
3. Restart service (Render dashboard → ... → Restart)

---

## 📋 Checklist Before Deploying

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` includes Flask, Flask-CORS, gunicorn
- [ ] `Procfile` contains: `web: gunicorn app:app --timeout 120`
- [ ] `app.py` exists in root folder
- [ ] `src/` folder with all analysis code
- [ ] Render account created (GitHub login)

---

## 🎯 After Deployment

1. ✅ Backend running on Render
2. ✅ Update API_URL in `index.html`
3. ✅ Deploy frontend to Netlify (optional)
4. ✅ Test with sample data
5. ✅ Share live link with team!

---

## 💾 Files Needed on Render

```
your-repo/
├── app.py                    ✅ Must exist
├── requirements.txt          ✅ Must exist
├── Procfile                  ✅ Must exist
├── src/                      ✅ Analysis code
│   ├── data_analysis_agent.py
│   ├── core/
│   ├── agents/
│   └── utils/
├── index.html                (not needed for backend)
└── data/                      (not needed for backend)
```

---

## 🚀 You're Ready!

Your deployment will take about 5 minutes total. Most of it is Render building the environment.

**Once deployed, you have a live API that anyone in the world can use!** 🌍

---

## 📞 Quick Support

| Problem | Solution |
|---------|----------|
| Can't connect repo | Authorize Render on GitHub settings |
| Build failed | Check Render logs for exact error |
| App won't start | Verify Procfile and app.py are correct |
| Can't upload files | Check backend logs, may be out of memory |
| Takes too long | Render free tier has limited CPU |

---

**Click "Create Web Service" and watch the magic happen!** ✨
