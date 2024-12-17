#!/bin/bash

echo "=== Persona Simulator Setup ==="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "⚠️  Please edit .env file and add your OpenAI API key"
fi

# Run setup test
echo "Running setup test..."
python test_setup.py

echo """
=== Setup Complete ===

To start the application:
1. Make sure your virtual environment is activated:
   source venv/bin/activate
2. Edit .env file and add your OpenAI API key
3. Run: streamlit run app.py

Enjoy using Persona Simulator!
"""
