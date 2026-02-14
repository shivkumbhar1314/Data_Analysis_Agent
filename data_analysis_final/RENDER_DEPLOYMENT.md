# Deploy Backend to Render

Complete guide to deploy the Data Analysis Agent backend to Render.

---

## 🎯 What You'll Have After This

- Backend API running on Render: `https://your-service-name.onrender.com`
- Frontend communicates with this backend
- Fully functional web application accessible worldwide

---

## ✅ Prerequisites

1. ✅ GitHub account (with your repo pushed)
2. ✅ Render account (free tier available)
3. ✅ Code ready to deploy (all files configured)

---

## 📋 Step 1: Prepare Code for Render

Your code is already configured! But verify these files exist:

### ✅ Files to Check
- `app.py` - Flask backend
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment config (should say: `web: gunicorn app:app --timeout 120`)
- All source files in `src/` folder

If any file is missing, Render won't work. Check with:
```bash
ls -la app.py requirements.txt Procfile
```

---

## 🔧 Step 2: Create Render Account & Deploy

### **Part A: Sign Up on Render**

1. Go to [render.com](https://render.com)
2. Click **"Sign up"** (top right)
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub repositories
5. Complete registration

### **Part B: Create New Web Service**

1. On Render dashboard, click **"New +"** (top right)
2. Select **"Web Service"**
3. Choose **"Build and deploy from a Git repository"**

### **Part C: Connect Your GitHub Repository**

1. Under "Connect Repository":
   - Select your GitHub account
   - Search for `Data-Analysis-Agent` repository
   - Click **"Connect"** button
   
   *(If you don't see it: click "Configure account" to give Render permission)*

### **Part D: Configure Service**

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `data-analysis-agent-backend` |
| **Environment** | `Python 3` |
| **Region** | `Ohio (us-east)` or closest to you |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --timeout 120` |

### **Part E: Set Environment Variables (Optional)**

Most settings work with defaults, but if you need to customize:

1. Scroll to **"Environment"** section
2. Click **"Add Environment Variable"**
3. Add these if desired:
   ```
   FLASK_ENV = production
   MAX_FILE_SIZE = 52428800
   ```

4. Leave other settings as default
5. Click **"Create Web Service"**

---

## 🚀 Step 3: Wait for Deployment

Render will:
1. Build the Docker container
2. Install Python dependencies
3. Run your Flask app
4. Show you the deployed URL

This takes 2-5 minutes. You can watch the logs in real-time:
- Render shows build logs directly on the dashboard
- You'll see `Deployed` status when complete ✅

---

## 📍 Step 4: Get Your Backend URL

Once deployed, Render shows your URL at the top:

```
https://your-service-name.onrender.com
```

The full API URL is:
```
https://your-service-name.onrender.com/api
```

**Important:** Save this URL - you'll use it in the next step!

---

## 🔗 Step 5: Connect Frontend to Backend

Now update your frontend to use the Render backend:

### **In `index.html` (Line 3):**

Find this line:
```javascript
const API_URL = 'http://localhost:5000/api';
```

Replace with your Render URL:
```javascript
const API_URL = 'https://your-service-name.onrender.com/api';
```

### **Example:**
If Render gave you: `https://my-agent-xyz123.onrender.com`

Then API_URL should be: `https://my-agent-xyz123.onrender.com/api`

### **Save the file!**

---

## 🌐 Step 6: Deploy Frontend (Optional)

If you also want to deploy the frontend to Netlify:

1. **Commit changes** to GitHub:
   ```bash
   git add index.html
   git commit -m "Update backend API URL for Render"
   git push
   ```

2. **Deploy to Netlify** (if not already done):
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Select your repository
   - Build settings:
     - Build command: (leave empty)
     - Publish directory: `.`
   - Deploy!

---

## ✅ Step 7: Test Everything

### **Test Backend**

1. Go to Render dashboard → Your service
2. Click the URL at the top
3. You should see: `Data-Analysis-Agent API - Backend is running successfully!`

Or test the health endpoint:
```
https://your-service-name.onrender.com/api/health
```

Should show: `{"status": "healthy"}`

### **Test Frontend**

1. Open `index.html` in your browser
2. Upload a CSV file
3. Click "Analyze"
4. Check if results appear

If you see results → Success! 🎉

---

## 🐛 Troubleshooting

### **Problem: "Build failed"**

**Check:**
- Does `requirements.txt` have all dependencies?
- Is `app.py` in the root folder?
- Is there a syntax error in the code?

**Solution:**
Look at Render's build logs (shown on dashboard) for error details.

### **Problem: "CORS error" or "Cannot reach backend"**

**Check:**
- Is API_URL correct in `index.html`?
- Did you include `/api` at the end?
- Is backend still running on Render?

**Solution:**
Test endpoint directly:
```
https://your-service-name.onrender.com/api/health
```

Should work in browser.

### **Problem: File upload says "Server error"**

**Check:**
- Is file size under 50MB?
- Is file format supported (CSV, Parquet, Excel)?
- Does backend have enough memory?

**Solution:**
- Smaller files first
- Check Render logs for exact error
- Render free tier may have limits

### **Problem: Analysis times out**

**Why:** Free tier has CPU limitations

**Solutions:**
1. Use smaller datasets
2. Upgrade to paid plan
3. Increase timeout (already set to 120s)

---

## 📊 Monitoring & Logs

### **View Logs**
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time output

### **Monitor Performance**
1. Click "Metrics" tab
2. See CPU, memory, and requests

### **Restart Service**
If something breaks:
1. Click "..." menu
2. Select "Restart"

---

## 💰 Pricing (Render)

| Plan | Cost | Best For |
|------|------|----------|
| **Free** | $0/month | Testing, hobby projects |
| **Starter** | $7/month | Small production apps |
| **Standard** | $25/month | Medium-scale usage |

**Free tier includes:**
- 750 hours/month
- 0.5GB RAM
- Up to ~50 small analyses/month

For serious use, upgrade to Starter.

---

## 🔐 Security Notes

### Current Setup
- ✅ CORS enabled (allows frontend to access)
- ❌ No authentication (anyone can use API)
- ❌ File uploads stored temporarily (then deleted)

### For Production
Add authentication to `app.py`:

```python
from functools import wraps
from flask import request

API_KEY = "your-secret-key-here"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if not key or key != API_KEY:
            return {'error': 'Invalid API key'}, 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/analyze', methods=['POST'])
@require_api_key
def analyze():
    # ... rest of code
```

Then update frontend:
```javascript
const response = await fetch(`${API_URL}/analyze`, {
    method: 'POST',
    headers: {
        'X-API-Key': 'your-secret-key-here'
    },
    body: formData
});
```

---

## 📚 Useful Links

- **Render Docs**: https://render.com/docs
- **Python Deployment**: https://render.com/docs/deploy-python
- **Environment Variables**: https://render.com/docs/environment-variables
- **Build & Deploy**: https://render.com/docs/deploys

---

## 🎯 What's Next?

1. ✅ Deploy backend to Render
2. ✅ Get the Render URL
3. ✅ Update frontend API_URL
4. ✅ Deploy frontend to Netlify (if not done)
5. ✅ Test with sample data
6. ✅ Share the live link!

---

## 🚀 Summary

```mermaid
1. Sign up on render.com (GitHub)
   ↓
2. Create Web Service from GitHub repo
   ↓
3. Configure: Python 3, gunicorn start command
   ↓
4. Wait for deployment (~2-5 minutes)
   ↓
5. Copy backend URL from Render
   ↓
6. Update API_URL in index.html
   ↓
7. Deploy frontend to Netlify
   ↓
8. Test and share! 🎉
```

---

**Need help? Check the logs on Render dashboard - they usually show exactly what went wrong.**

**Good luck! Your app is about to go live! 🚀**
