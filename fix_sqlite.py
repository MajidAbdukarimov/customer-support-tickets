#!/usr/bin/env python3
"""
SQLite Fix Script for ChromaDB Compatibility
This script helps resolve SQLite version issues on Windows
"""

import sys
import sqlite3
import subprocess
import os

def check_sqlite_version():
    """Check current SQLite version"""
    version = sqlite3.sqlite_version
    print(f"Current SQLite version: {version}")
    
    # Check if version is sufficient
    version_parts = [int(x) for x in version.split('.')]
    required_parts = [3, 35, 0]
    
    is_sufficient = version_parts >= required_parts
    print(f"Required version: 3.35.0 or higher")
    print(f"Version check: {'✅ PASS' if is_sufficient else '❌ FAIL'}")
    
    return is_sufficient

def install_pysqlite3():
    """Install pysqlite3-binary as a replacement"""
    try:
        print("Installing pysqlite3-binary...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pysqlite3-binary"])
        print("✅ Successfully installed pysqlite3-binary")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install pysqlite3-binary: {e}")
        return False

def install_faiss():
    """Install FAISS as alternative"""
    try:
        print("Installing faiss-cpu...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu"])
        print("✅ Successfully installed faiss-cpu")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install faiss-cpu: {e}")
        return False

def create_sqlite_patch():
    """Create a patch to use pysqlite3 instead of sqlite3"""
    patch_content = """# SQLite Version Patch for ChromaDB
# This file should be imported before importing chromadb

import sys

try:
    # Try to use pysqlite3 if available (newer SQLite)
    import pysqlite3.dbapi2 as sqlite3
    # Replace the built-in sqlite3 module
    sys.modules['sqlite3'] = sqlite3
    print("Using pysqlite3-binary for SQLite compatibility")
except ImportError:
    # Fall back to built-in sqlite3
    import sqlite3
    print(f"Using built-in SQLite version: {sqlite3.sqlite_version}")
"""
    
    try:
        with open('sqlite_patch.py', 'w') as f:
            f.write(patch_content)
        print("✅ Created sqlite_patch.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create patch file: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 SQLite Compatibility Fix for ChromaDB")
    print("-" * 50)
    
    # Check current SQLite version
    if check_sqlite_version():
        print("✅ SQLite version is sufficient!")
        return
    
    print("\n🛠️  Applying fixes...")
    
    # Install required packages
    print("\n1. Installing required packages...")
    install_pysqlite3()
    install_faiss()
    
    # Create patch file
    print("\n2. Creating SQLite patch...")
    create_sqlite_patch()
    
    print("\n✅ Fixes applied!")
    print("\nNext steps:")
    print("1. Try running: python simple_setup.py")
    print("2. Then run: streamlit run app.py")
    print("3. If issues persist, the app will use FAISS instead of ChromaDB")

if __name__ == "__main__":
    main()