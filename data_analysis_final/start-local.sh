#!/bin/bash

echo "=========================================="
echo "Data Analysis Agent - Local Setup"
echo "=========================================="
echo ""

echo "1. Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "2. Starting Flask backend server..."
echo "   Server will run on: http://localhost:5000"
echo "   Frontend can be opened from: file://$(pwd)/index.html"
echo ""
echo "3. Backend is ready! Open index.html in your browser to start."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
