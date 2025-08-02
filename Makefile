# Smart Investment Report Analyzer Makefile

.PHONY: setup run test clean sample-pdf help

# Default target
help:
	@echo "Smart Investment Report Analyzer"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup      - Install dependencies"
	@echo "  make run        - Run the Streamlit app"
	@echo "  make test       - Run installation test"
	@echo "  make sample-pdf - Create sample PDF for testing"
	@echo "  make clean      - Remove temporary files"
	@echo "  make help       - Show this help message"

# Setup environment and install dependencies
setup:
	@echo "Setting up environment..."
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt
	@if [ ! -f .env ] && [ -f .env.example ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example. Please edit it to add your API key."; \
	fi
	@echo "Setup complete!"

# Run the Streamlit app
run:
	@echo "Starting Streamlit app..."
	@streamlit run app.py

# Run installation test
test:
	@echo "Running installation test..."
	@python test_installation.py

# Create sample PDF for testing
sample-pdf:
	@echo "Creating sample PDF..."
	@python create_sample_pdf.py
	@echo "Sample PDF created: sample_financial_report.pdf"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name __pycache__ -exec rm -rf {} +;
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".DS_Store" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +;
	@find . -type d -name "*.egg" -exec rm -rf {} +;
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +;
	@find . -type d -name ".coverage" -exec rm -rf {} +;
	@find . -type d -name "htmlcov" -exec rm -rf {} +;
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +;
	@echo "Cleaned!"