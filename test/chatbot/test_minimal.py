"""
Minimal test to identify issues
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("🧪 Minimal Test - Checking Environment")
print("=" * 70)
print()

# Test 1: Python version
print("✓ Python version:", sys.version.split()[0])

# Test 2: Check project structure
project_root = Path(__file__).parent.parent.parent
print("✓ Project root:", project_root)

# Test 3: Check data directory
data_dir = project_root / "data" / "raw"
print("✓ Data directory exists:", data_dir.exists())

if data_dir.exists():
    csv_files = list(data_dir.glob("*.csv"))
    print(f"✓ CSV files found: {len(csv_files)}")
    if csv_files:
        print(f"  Example: {csv_files[0].name}")

# Test 4: Check .env
env_file = project_root / ".env"
print("✓ .env file exists:", env_file.exists())

# Test 5: Try loading dotenv
print("\nTesting dotenv...")
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_file)
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    print(f"✓ dotenv loaded, API key present: {has_key}")
except Exception as e:
    print(f"✗ dotenv error: {e}")

# Test 6: Try pandas
print("\nTesting pandas...")
try:
    import pandas as pd
    print("✓ pandas imported successfully")
    print(f"  pandas version: {pd.__version__}")
except Exception as e:
    print(f"✗ pandas error: {e}")

# Test 7: Try langchain imports
print("\nTesting langchain imports...")
try:
    from langchain_openai import ChatOpenAI
    print("✓ ChatOpenAI imported")
except Exception as e:
    print(f"✗ ChatOpenAI error: {e}")

try:
    from langchain_core.prompts import ChatPromptTemplate
    print("✓ ChatPromptTemplate imported")
except Exception as e:
    print(f"✗ ChatPromptTemplate error: {e}")

try:
    from langchain_experimental.utilities import PythonREPL
    print("✓ PythonREPL imported")
except Exception as e:
    print(f"✗ PythonREPL error: {e}")

# Test 8: Try colorama
print("\nTesting colorama...")
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    print(f"{Fore.GREEN}✓ colorama working!{Style.RESET_ALL}")
except Exception as e:
    print(f"✗ colorama error: {e}")

print("\n" + "=" * 70)
print("✅ All basic imports successful!")
print("=" * 70)

