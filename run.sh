#!/bin/bash

# Workforce Intelligence Platform - Run Script
# Quick script to activate environment and run the application

echo "🚀 Starting Workforce Intelligence Platform..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run app.py
