#!/bin/bash

# Smart Investment Report Analyzer Launcher

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if needed
if [ ! -f "venv/requirements_installed" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch venv/requirements_installed
    else
        echo "Error: Failed to install requirements."
        exit 1
    fi
fi

# Check for .env file, create from example if not exists
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "Please edit the .env file to add your OpenAI API key."
    echo "You can also enter it directly in the application."
fi

# Run the Streamlit app
echo "Starting Smart Investment Report Analyzer..."
streamlit run app.py