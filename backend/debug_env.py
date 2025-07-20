#!/usr/bin/env python3
"""
Debug script to check environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

print("🔍 Debugging environment variables...")

# Get the project root directory
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'

print(f"📁 Looking for .env at: {env_path}")
print(f"📁 File exists: {env_path.exists()}")

if env_path.exists():
    print(f"📄 File contents:")
    with open(env_path, 'r') as f:
        content = f.read()
        print(content)

# Load the .env file
print(f"\n🔄 Loading .env file...")
load_dotenv(env_path)

# Check environment variables
print(f"\n🔑 Environment variables after loading:")
eleven_labs_key = os.getenv('ELEVEN_LABS_API_KEY')
print(f"ELEVEN_LABS_API_KEY: {'✅ Found' if eleven_labs_key else '❌ Not found'}")
if eleven_labs_key:
    print(f"  Value: {eleven_labs_key[:10]}...")

# Check other API keys for comparison
vellum_key = os.getenv('VELLUM_API_KEY')
print(f"VELLUM_API_KEY: {'✅ Found' if vellum_key else '❌ Not found'}")

gemini_key = os.getenv('GEMINI_API_KEY')
print(f"GEMINI_API_KEY: {'✅ Found' if gemini_key else '❌ Not found'}") 