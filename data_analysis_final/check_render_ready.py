#!/usr/bin/env python3

import os
import sys
from pathlib import Path

print("\n" + "="*60)
print("DATA ANALYSIS AGENT - RENDER DEPLOYMENT CHECKER")
print("="*60 + "\n")

errors = []
warnings = []
success = []

# Check files exist
files_to_check = [
    ('app.py', 'Flask backend'),
    ('requirements.txt', 'Python dependencies'),
    ('Procfile', 'Deployment config'),
    ('index.html', 'Web frontend'),
    ('src/data_analysis_agent.py', 'Main analysis agent'),
    ('src/core/scaledown_engine.py', 'ScaleDown engine'),
    ('src/core/data_ingestion.py', 'Data ingestion'),
    ('src/agents/', 'Agents directory'),
]

print("📋 CHECKING FILES...")
for file_path, description in files_to_check:
    path = Path(file_path)
    if path.exists():
        success.append(f"✅ {description}: {file_path}")
    else:
        errors.append(f"❌ MISSING {description}: {file_path}")

# Check Procfile content
print("\n🔍 CHECKING PROCFILE...")
try:
    with open('Procfile', 'r') as f:
        procfile_content = f.read().strip()
    
    if 'gunicorn' in procfile_content and 'app:app' in procfile_content:
        success.append(f"✅ Procfile configured correctly")
    else:
        errors.append(f"❌ Procfile missing gunicorn or app:app reference")
except Exception as e:
    errors.append(f"❌ Error reading Procfile: {e}")

# Check requirements.txt
print("\n📦 CHECKING REQUIREMENTS...")
required_packages = [
    'flask',
    'flask-cors',
    'gunicorn',
    'pandas',
    'scikit-learn',
]

try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read().lower()
    
    for package in required_packages:
        if package in requirements:
            success.append(f"✅ {package.upper()} in requirements.txt")
        else:
            errors.append(f"❌ MISSING {package.upper()} in requirements.txt")
except Exception as e:
    errors.append(f"❌ Error reading requirements.txt: {e}")

# Check app.py
print("\n🔧 CHECKING APP.PY...")
try:
    with open('app.py', 'r') as f:
        app_content = f.read()
    
    checks = [
        ('Flask import', 'from flask import'),
        ('CORS enabled', 'CORS(app)'),
        ('/api/analyze endpoint', "@app.route('/api/analyze'"),
        ('/api/health endpoint', "@app.route('/api/health'"),
    ]
    
    for check_name, keyword in checks:
        if keyword.lower() in app_content.lower():
            success.append(f"✅ {check_name} found")
        else:
            errors.append(f"❌ {check_name} missing from app.py")
            
except Exception as e:
    errors.append(f"❌ Error reading app.py: {e}")

# Check index.html API_URL
print("\n🌐 CHECKING FRONTEND...")
try:
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    if 'const API_URL' in html_content:
        success.append(f"✅ API_URL defined in index.html")
        
        if 'http://localhost:5000/api' in html_content:
            warnings.append(f"⚠️  API_URL still points to localhost - Update after Render deployment!")
        elif 'onrender.com' in html_content:
            success.append(f"✅ API_URL already configured for Render")
    else:
        errors.append(f"❌ API_URL not found in index.html")
        
except Exception as e:
    errors.append(f"❌ Error reading index.html: {e}")

# Print results
print("\n" + "="*60)
print("📊 RESULTS")
print("="*60 + "\n")

if success:
    print("✅ CHECKS PASSED:")
    for item in success:
        print(f"   {item}")

if warnings:
    print("\n⚠️  WARNINGS:")
    for item in warnings:
        print(f"   {item}")

if errors:
    print("\n❌ ERRORS (FIX BEFORE DEPLOYING):")
    for item in errors:
        print(f"   {item}")
    print("\n" + "="*60)
    print("❌ NOT READY FOR DEPLOYMENT - Fix errors above first")
    print("="*60 + "\n")
    sys.exit(1)
else:
    print("\n" + "="*60)
    print("✅ READY FOR RENDER DEPLOYMENT!")
    print("="*60)
    print("\n📋 DEPLOYMENT STEPS:")
    print("   1. Push code to GitHub: git push")
    print("   2. Go to render.com → Sign in with GitHub")
    print("   3. Click New (+) → Web Service")
    print("   4. Connect your GitHub repository")
    print("   5. Set:")
    print("      • Name: data-analysis-agent-backend")
    print("      • Build: pip install -r requirements.txt")
    print("      • Start: gunicorn app:app --timeout 120")
    print("   6. Click 'Create Web Service'")
    print("   7. Wait 2-5 minutes for deployment")
    print("   8. Copy the URL and update API_URL in index.html")
    print("\n📚 For detailed guide, see: QUICK_RENDER_GUIDE.md")
    print("="*60 + "\n")
    sys.exit(0)
