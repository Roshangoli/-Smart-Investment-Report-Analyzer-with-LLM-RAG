#!/usr/bin/env python3

"""
Test script to verify the installation of the Smart Investment Report Analyzer.
This script checks for required dependencies and environment variables.
"""

import sys
import os
import importlib.util
import platform

def check_python_version():
    """Check if Python version is compatible."""
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"   Current version: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return False
    else:
        print(f"✅ Python version: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return True

def check_package(package_name):
    """Check if a package is installed."""
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"❌ {package_name} is not installed.")
        return False
    else:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package_name} is installed (version: {version})")
            return True
        except ImportError:
            print(f"❌ {package_name} is installed but could not be imported.")
            return False

def check_openai_api_key():
    """Check if OpenAI API key is set."""
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:]
        print(f"✅ OpenAI API key is set: {masked_key}")
        return True
    else:
        print("❌ OpenAI API key is not set in environment variables.")
        print("   You can set it in the .env file or enter it in the application.")
        return False

def check_system_info():
    """Display system information."""
    print(f"\nSystem Information:")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Python: {sys.version}")
    print(f"  Executable: {sys.executable}")

def main():
    print("\n=== Smart Investment Report Analyzer - Installation Test ===\n")
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check required packages
    print("\nChecking required packages:")
    packages = [
        'streamlit',
        'langchain',
        'openai',
        'chromadb',
        'pandas',
        'dotenv',
        'PyPDF2',
        'docx2txt',
        'matplotlib',
        'plotly'
    ]
    
    packages_ok = True
    for package in packages:
        package_ok = check_package(package)
        packages_ok = packages_ok and package_ok
    
    # Check OpenAI API key
    print("\nChecking environment:")
    api_key_ok = check_openai_api_key()
    
    # Display system information
    check_system_info()
    
    # Overall status
    print("\nOverall Status:")
    if python_ok and packages_ok and api_key_ok:
        print("✅ All checks passed! The system is ready to use.")
        print("   Run './run.sh' to start the application.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above before running the application.")
        if not api_key_ok:
            print("   Note: You can still run the application and enter your API key there.")
        return 1

if __name__ == "__main__":
    sys.exit(main())