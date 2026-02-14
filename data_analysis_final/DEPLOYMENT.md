# Data Analysis Agent - Deployment Guide

## Overview
This guide explains how to deploy the Data Analysis Agent as a full-stack web application:
- **Frontend**: Hosted on Netlify (static site)
- **Backend**: Hosted on Railway or Render (Python Flask API)
- **Architecture**: Serverless web application with automated analysis engine

---

## Deployment Architecture

```
┌─────────────────┐
│  Frontend       │
│  (Netlify)      │
│  - index.html   │────┐
│  - vanilla JS   │    │
└─────────────────┘    │
                       │ HTTP/CORS
                       │
                       ▼
┌─────────────────────────────┐
│  Backend API (Railway/Render)│
│  - Flask App                 │
│  - Analysis Engine           │
│  - Data Processing           │
└─────────────────────────────┘
```

---

## Quick Start (Local Testing)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Backend Server
```bash
python app.py
```
Backend will run on `http://localhost:5000`

### 3. Open Frontend
- Open `index.html` in your browser
- Or serve it with a local server:
  ```bash
  python -m http.server 8000
  ```
  Then visit `http://localhost:8000`

---

## Production Deployment

### Option 1: Netlify Frontend + Railway Backend (RECOMMENDED)

#### Frontend Deployment (Netlify)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/data-analysis-agent.git
   git push -u origin main
   ```

2. **Connect to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Select your GitHub repository
   - Build settings:
     - **Build command**: (leave empty)
     - **Publish directory**: `.` (root directory)
   - Click "Deploy site"

3. **Update API URL in Frontend**
   After deploying backend (see below), update the API URL in `index.html`:
   ```javascript
   const API_URL = 'https://YOUR_BACKEND_URL/api';
   ```

#### Backend Deployment (Railway)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy Flask App**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python/Flask app
   - Add environment variables (if needed)
   - Click "Deploy"

3. **Get Backend URL**
   - Your backend URL will be something like: `https://YOUR-PROJECT.railway.app`
   - Update this in `index.html` as `API_URL`

### Option 2: Netlify Frontend + Heroku Backend

#### Heroku Deployment
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

Your backend will be at: `https://your-app-name.herokuapp.app`

### Option 3: All-in-One Render Deployment

Deploy both frontend and backend to Render:

1. Create two services on [render.com](https://render.com):
   - **Static Site** (for `index.html`)
   - **Web Service** (for Flask app)

2. Configure static site to redirect API calls to web service

---

## Configuration

### Environment Variables

If deploying backend, set these environment variables:

- `FLASK_ENV=production`
- `MAX_FILE_SIZE=52428800` (50MB in bytes)
- `API_TIMEOUT=120` (seconds)

### CORS Settings

The Flask app already has CORS enabled. For custom origins, update `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-netlify-domain.netlify.app"]
    }
})
```

---

## Monitoring & Debugging

### Backend Logs
- **Railway**: View in dashboard
- **Render**: View in "Logs" tab
- **Heroku**: `heroku logs --tail` or dashboard

### Common Issues

#### CORS Error
**Problem**: "Access to XMLHttpRequest blocked by CORS"

**Solution**: 
- Verify backend API URL in `index.html` is correct
- Check Flask-CORS is installed: `pip install flask-cors`
- Backend must be running and accessible

#### File Upload Fails
**Problem**: "No file provided" error

**Solution**:
- Check file size doesn't exceed `MAX_FILE_SIZE`
- Verify supported formats: CSV, Parquet, Excel
- Check backend timeout isn't exceeded

#### Long Analysis Timeout
**Problem**: "Request timeout" after 120 seconds

**Solution**:
- Reduce dataset size
- Run fewer agents
- Increase backend timeout in Procfile: `--timeout 300`

---

## API Endpoints

### Analyze Database
**POST** `/api/analyze`

**Parameters:**
- `file` (multipart): CSV/Parquet/Excel file
- `datasetName` (string): Name for analysis
- `targetColumn` (string, optional): Target variable for supervised learning
- `agents` (JSON array): List of agents to run
  - `"profiling"`, `"visualization"`, `"insights"`, `"anomalies"`, `"automl"`

**Response:**
```json
{
  "success": true,
  "timestamp": "2026-02-13T10:00:00",
  "dataset_profile": {...},
  "agent_results": {...},
  "summary": "...",
  "html_report": "...",
  "json_report": "..."
}
```

### Health Check
**GET** `/api/health`

Response: `{"status": "healthy"}`

---

## Performance Tips

### Optimize Analysis Speed
1. **Reduce dataset size**: Limit to <100MB for faster processing
2. **Select specific agents**: Don't run all agents if not needed
3. **Use sampling**: For large datasets, consider analyzing a sample

### Reduce File Sizes
- Use Parquet format instead of CSV (more compressed)
- Specify data types when loading data
- Remove unnecessary columns

---

## Security Considerations

### File Upload Security
- ✅ Filenames are sanitized with `secure_filename()`
- ✅ File size limited to 50MB
- ✅ Format validation (CSV/Parquet/Excel only)

### API Security
- ⚠️ CORS enabled - in production, restrict to your domain
- ⚠️ No authentication - add if exposure to sensitive data
- ⚠️ File storage temporary - reports deleted after request

### Recommendations
```python
# In app.py, add authentication:
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == os.getenv('API_USER') and password == os.getenv('API_PASSWORD'):
        return username

@app.route('/api/analyze', methods=['POST'])
@auth.login_required
def analyze():
    # Protected endpoint
    ...
```

### Environment Variables (Secure)
For sensitive config, use environment variables:
```bash
# In deployment platform
FLASK_ENV=production
API_USER=your_username
API_PASSWORD=your_password
DATABASE_URL=postgresql://...
```

---

## Scaling & Advanced Deployment

### For High Traffic
1. **Add caching** (Redis)
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   ```

2. **Use CDN** (CloudFlare, CloudFront)
3. **Add load balancer** (for multiple backend instances)

### For Long-Running Tasks
1. **Use job queue** (Celery + Redis)
2. **Implement webhooks** for async notifications
3. **Add progress tracking** for long analyses

---

## Cost Estimate

| Service | Cost | Notes |
|---------|------|-------|
| Netlify | Free | 100GB bandwidth/month |
| Railway | $5/month minimum | Or free tier with limits |
| Render | Free | 750 hours/month (one app) |
| Total | ~$5/month | Very affordable! |

---

## Next Steps

1. ✅ Deploy frontend to Netlify
2. ✅ Deploy backend to Railway/Render
3. ✅ Test with sample CSV file
4. ✅ Share application link
5. ✅ Monitor logs for issues
6. ✅ Optimize based on usage patterns

---

## Support

For issues or questions:
- Check backend logs: `https://your-backend-domain/logs`
- Test API directly: `POST https://your-backend-domain/api/analyze`
- Debug frontend: Open Browser DevTools (F12) → Console tab

---

**Happy deploying! 🚀**
