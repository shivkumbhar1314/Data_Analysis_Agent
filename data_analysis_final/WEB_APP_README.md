# Data Analysis Agent - Web Application

A full-stack web application for automated data analysis featuring:
- 📤 **File Upload**: Upload CSV, Parquet, or Excel files
- 🔍 **Automated Analysis**: Profile data, detect anomalies, generate insights
- 🤖 **AI Recommendations**: Automated machine learning model suggestions
- 📊 **Interactive Reports**: HTML and JSON exports
- ⚡ **Fast Compression**: 96%+ metadata compression with ScaleDown engine

---

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
python app.py
```
Server runs on `http://localhost:5000`

### 3. Open the Web Application
- Open `index.html` in your browser (file:// protocol works)
- Or use a local server:
  ```bash
  python -m http.server 8000
  Open: http://localhost:8000
  ```

### 4. Upload and Analyze
- Select a CSV/Parquet/Excel file
- Configure analysis options (dataset name, target column, agents)
- Click "Analyze" to run the full pipeline
- View interactive results and download reports

---

## 📱 Features

### Analysis Components
- **Data Profiling**: Column statistics, data quality metrics, compression ratios
- **Visualization Recommendations**: Smart chart suggestions based on data type
- **Insight Generation**: Pattern discovery and statistical insights
- **Anomaly Detection**: Outlier detection using IQR and Mahalanobis distance
- **AutoML**: Automatic problem type detection and model recommendations

### Reports
- **HTML Report**: Styled, interactive report with all findings
- **JSON Report**: Machine-readable export for integration

---

## 🌐 Deploy to Production

### Option 1: Netlify + Railway (Recommended)

#### **Step 1: Deploy Frontend to Netlify**

1. Push code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/data-analysis-agent
   git push -u origin main
   ```

2. Go to [netlify.com](https://netlify.com)
3. Click "New site from Git" → Select repository
4. Build settings:
   - Build command: (leave empty)
   - Publish directory: `.`
5. Deploy!

#### **Step 2: Deploy Backend to Railway**

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys automatically
6. Get your backend URL (e.g., `https://your-project.railway.app`)

#### **Step 3: Update Frontend with Backend URL**

Edit `index.html` (line ~3):
```javascript
const API_URL = 'https://YOUR-RAILWAY-URL/api';
```

Redeploy to Netlify.

### Option 2: Heroku + Netlify

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create your-app-name
git push heroku main

# Get URL and update index.html
heroku apps:info your-app-name
```

### Option 3: Docker (Any Cloud)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app"]
```

Deploy to: Docker Hub → Cloud Run, Render, or any Kubernetes cluster

---

## 📊 Example Workflow

1. **Upload Data**
   - Drop a CSV file (loan_data.csv, customer_data.csv, etc.)
   - Set dataset name and optional target column

2. **Select Analysis Type**
   - Profiling: Get data characteristics
   - Visualization: See recommended charts
   - Insights: Discover patterns
   - Anomalies: Find outliers
   - AutoML: Get model recommendations

3. **View Results**
   - **Summary Tab**: Overall findings and agent status
   - **Profile Tab**: Column-by-column statistics
   - **Insights Tab**: Key patterns and correlations
   - **Anomalies Tab**: Outliers and data quality issues
   - **Recommendations Tab**: Suggested models and preprocessing

4. **Export Results**
   - Download HTML report for sharing
   - Download JSON for integration with other tools

---

## 🔧 Configuration

### File Size Limits
- Default: 50MB
- To change in `app.py`:
  ```python
  MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
  ```

### Timeout Settings
- Default: 120 seconds
- In `Procfile` (Railway/Heroku):
  ```
  web: gunicorn app:app --timeout 300
  ```

### Supported File Formats
- CSV (`.csv`)
- Parquet (`.parquet`)
- Excel (`.xls`, `.xlsx`)

---

## 🛠️ API Reference

### Analyze Endpoint
**POST** `/api/analyze`

Request (multipart form):
```
file: <your-data-file>
datasetName: "my_dataset"
targetColumn: "approved"
agents: ["profiling", "visualization", "insights", "anomalies", "automl"]
```

Response:
```json
{
  "success": true,
  "summary": "Dataset: my_dataset\n...",
  "dataset_profile": {...},
  "agent_results": {...},
  "html_report": "...",
  "json_report": "..."
}
```

### Health Check
**GET** `/api/health`

Response:
```json
{"status": "healthy"}
```

---

## 📈 Performance Metrics

On 500-row sample dataset:
- Total execution time: ~1 second
- Compression ratio: 96.8%
- File size reduction: 83KB → 2.7KB

---

## 🐛 Troubleshooting

### CORS Error
**Problem**: "Access to XMLHttpRequest blocked by CORS"

**Solution**:
- Check `API_URL` in `index.html` is correct
- Verify backend is running
- Ensure Flask-CORS is installed

### File Upload Fails
**Problem**: "File too large" or "Invalid format"

**Solution**:
- Use CSV, Parquet, or Excel format
- Keep file under 50MB
- Ensure no special characters in filename

### Long-Running Analysis
**Problem**: Request times out after 120s

**Solution**:
- Reduce dataset size
- Select fewer agents to run
- Increase timeout in Procfile: `--timeout 300`

---

## 📚 File Structure

```
data-analysis-agent/
├── index.html              # Web UI (frontend)
├── app.py                  # Flask API (backend)
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment config
├── DEPLOYMENT.md          # Detailed deployment guide
├── src/
│   ├── data_analysis_agent.py      # Main orchestrator
│   ├── core/
│   │   ├── scaledown_engine.py    # Compression engine
│   │   └── data_ingestion.py      # Data loading
│   ├── agents/                     # Analysis agents
│   │   ├── profiling_agent.py
│   │   ├── visualization_agent.py
│   │   ├── anomaly_detection_agent.py
│   │   ├── insight_generator_agent.py
│   │   └── automl_agent.py
│   └── utils/
│       └── report_generator.py    # Report generation
└── data/
    └── sample_data.csv            # Test dataset
```

---

## 💡 Tips

### For Best Results
1. Use datasets with 100+ rows
2. Include mix of numeric and categorical columns
3. Set target column for supervised learning
4. Run all agents for comprehensive analysis

### For Faster Analysis
1. Reduce dataset to <10,000 rows
2. Select specific agents only
3. Use Parquet format (more compressed)

### For Production
1. Add authentication to `/api/analyze`
2. Implement rate limiting
3. Use caching for repeated analyses
4. Monitor backend logs regularly

---

## 🚀 Next Steps

1. **Test locally** with `python app.py` and `index.html`
2. **Deploy frontend** to Netlify (free)
3. **Deploy backend** to Railway/Render (free tier available)
4. **Share the link** with your team
5. **Customize branding** in `index.html`

---

## 📞 Support

- Check logs: Backend logs visible in Railway/Heroku dashboard
- Test API: Make a test request to `/api/health`
- Debug frontend: Use Browser DevTools (F12)
- Common issues: See DEPLOYMENT.md

---

**Ready to deploy? Start with [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions! 🎉**
