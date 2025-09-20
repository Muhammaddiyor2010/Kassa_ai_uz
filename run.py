#!/usr/bin/env python3
"""
Kassa AI Bot - Easy runner script
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.dist'):
            print("❌ Error: .env file not found!")
            print("Please copy .env.dist to .env and fill in your tokens:")
            print("cp .env.dist .env")
            print("Then edit .env file with your actual tokens")
        else:
            print("❌ Error: .env file not found!")
            print("Please create .env file with:")
            print("BOT_TOKEN=your_telegram_bot_token")
            print("GEMINI_API_KEY=your_gemini_api_key")
        sys.exit(1)
    print("✅ .env file found")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing requirements")
        sys.exit(1)

def run_bot():
    """Run the bot"""
    print("🚀 Starting Kassa AI Bot...")
    try:
        subprocess.run([sys.executable, "bot.py"])
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🤖 Kassa AI Bot Setup")
    print("=" * 30)
    
    # Check Python version
    check_python_version()
    
    # Check .env file
    check_env_file()
    
    # Install requirements
    install_requirements()
    
    # Run bot
    run_bot()

if __name__ == "__main__":
    main()
