#!/usr/bin/env python3
"""
Deployment script for News Digest Microsite
Handles setup, configuration, and deployment tasks
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit', 'requests', 'google-generativeai', 
        'python-dotenv', 'pandas', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    news_key = os.getenv('NEWS_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not news_key:
        print("❌ NEWS_API_KEY not found")
        return False
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found")
        return False
    
    print("✅ API keys are configured")
    return True

def create_env_file():
    """Create .env file template"""
    env_template = """# API Keys
NEWS_API_KEY=your_news_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings
DEBUG=True
LOG_LEVEL=INFO

# Database Settings
DATA_DIR=./data

# Streamlit Settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_template)
        print("✅ Created .env file template")
        print("📝 Please edit .env file with your API keys")
    else:
        print("ℹ️ .env file already exists")

def setup_directories():
    """Create necessary directories"""
    directories = ['data', 'utils', 'static', 'static/css', 'static/js', 'static/images']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created project directories")

def run_tests():
    """Run basic functionality tests"""
    print("🧪 Running tests...")
    
    try:
        # Test imports
        from utils import NewsAPIClient, GeminiAPIClient, DataManager
        print("✅ Utility modules imported successfully")
        
        # Test data manager
        data_manager = DataManager()
        print("✅ Data manager initialized")
        
        # Test API clients (without making actual requests)
        try:
            news_client = NewsAPIClient()
            print("✅ NewsAPI client initialized")
        except Exception as e:
            print(f"⚠️ NewsAPI client error: {str(e)}")
        
        try:
            gemini_client = GeminiAPIClient()
            print("✅ Gemini API client initialized")
        except Exception as e:
            print(f"⚠️ Gemini API client error: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def start_application():
    """Start the Streamlit application"""
    print("🚀 Starting News Digest application...")
    
    try:
        # Check if app.py exists
        if not os.path.exists('app.py'):
            print("❌ app.py not found")
            return False
        
        # Start Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        return False

def show_help():
    """Show help information"""
    help_text = """
📰 News Digest Microsite - Deployment Script

Usage: python deploy.py [command]

Commands:
  setup     - Set up the project (create directories, env file)
  test      - Run tests to verify installation
  start     - Start the Streamlit application
  deploy    - Full deployment process
  help      - Show this help message

Examples:
  python deploy.py setup
  python deploy.py test
  python deploy.py start
  python deploy.py deploy

Requirements:
  - Python 3.8+
  - API keys for NewsAPI and Gemini API
  - Internet connection for package installation
"""
    print(help_text)

def main():
    """Main deployment function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'help':
        show_help()
    elif command == 'setup':
        print("🔧 Setting up News Digest project...")
        if not check_python_version():
            return
        
        setup_directories()
        create_env_file()
        print("\n✅ Setup complete!")
        print("📝 Next steps:")
        print("1. Edit .env file with your API keys")
        print("2. Run: python deploy.py test")
        print("3. Run: python deploy.py start")
        
    elif command == 'test':
        print("🧪 Testing News Digest installation...")
        if not check_python_version():
            return
        if not check_dependencies():
            return
        if not check_api_keys():
            print("⚠️ API keys not found. Please set them in .env file")
            return
        
        if run_tests():
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed")
            
    elif command == 'start':
        print("🚀 Starting News Digest application...")
        if not check_api_keys():
            print("❌ API keys required to start application")
            return
        
        start_application()
        
    elif command == 'deploy':
        print("🚀 Full deployment process...")
        
        # Run all steps
        if not check_python_version():
            return
        
        setup_directories()
        create_env_file()
        
        if not check_dependencies():
            print("📦 Installing dependencies...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        if not check_api_keys():
            print("⚠️ Please set API keys in .env file before continuing")
            return
        
        if run_tests():
            print("\n✅ Deployment successful!")
            print("🚀 Starting application...")
            start_application()
        else:
            print("\n❌ Deployment failed during testing")
            
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
