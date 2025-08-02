#!/bin/bash

# Smart Investment Report Analyzer Installation Script

echo "=== Installing Smart Investment Report Analyzer ==="
echo ""

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

# Install requirements
echo "Installing required packages..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install required packages."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit the .env file to add your OpenAI API key."
fi

# Create sample PDF
echo "Creating sample PDF for testing..."
python3 create_sample_pdf.py

if [ $? -ne 0 ]; then
    echo "Warning: Failed to create sample PDF. You can create it later with 'python3 create_sample_pdf.py'."
fi

echo ""
echo "=== Installation Complete! ==="
echo ""
echo "To run the application:"
echo "1. Make sure your OpenAI API key is set in the .env file or enter it in the app"
echo "2. Run './run.sh' or 'streamlit run app.py'"
echo ""
echo "For more information, see the README.md file."