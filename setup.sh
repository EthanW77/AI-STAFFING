#!/bin/bash

# Workforce Intelligence Platform - Setup Script
# This script sets up the environment and runs the application

echo "🚀 Workforce Intelligence Platform Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 To run the application:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Run the app: streamlit run app.py"
echo ""
echo "Or simply run: ./run.sh"
echo ""
