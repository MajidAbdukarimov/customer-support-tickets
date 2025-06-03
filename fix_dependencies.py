#!/usr/bin/env python3
"""
Fix dependency issues for Windows systems
"""

import subprocess
import sys

def fix_cryptography():
    """Fix cryptography dependency issues"""
    try:
        print("🔧 Fixing cryptography dependency...")
        # Uninstall and reinstall cryptography
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "cryptography", "-y"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography==3.4.8"])
        print("✅ Fixed cryptography")
        return True
    except Exception as e:
        print(f"❌ Failed to fix cryptography: {e}")
        return False

def install_alternative_pdf():
    """Install alternative PDF processing library"""
    try:
        print("🔧 Installing alternative PDF library...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2==2.12.1"])
        print("✅ Installed PyPDF2")
        return True
    except Exception as e:
        print(f"❌ Failed to install PyPDF2: {e}")
        return False

def main():
    print("🔧 Fixing dependency issues...")
    print("-" * 40)
    
    # Try to fix cryptography first
    if fix_cryptography():
        print("Try running the app again!")
        return
    
    # If that fails, suggest alternative
    install_alternative_pdf()
    print("\n📝 Alternative solution applied.")
    print("The app will use PyPDF2 instead of pdfplumber.")

if __name__ == "__main__":
    main()