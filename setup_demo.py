#!/usr/bin/env python3
"""
Demo setup script for AI Customer Support System
This script helps set up the demo environment with sample documents
"""

import os
import requests
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/documents",
        "data/vector_db", 
        "data/tickets",
        "data/logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def download_sample_pdfs():
    """Download sample PDF documents for testing"""
    sample_pdfs = [
        {
            "name": "sample_manual.pdf",
            "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "description": "Sample technical manual"
        }
    ]
    
    docs_dir = Path("data/documents")
    
    for pdf_info in sample_pdfs:
        file_path = docs_dir / pdf_info["name"]
        
        if file_path.exists():
            print(f"⏭️  File already exists: {pdf_info['name']}")
            continue
        
        try:
            print(f"📥 Downloading {pdf_info['name']}...")
            response = requests.get(pdf_info["url"])
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {pdf_info['name']}")
            
        except Exception as e:
            print(f"❌ Failed to download {pdf_info['name']}: {str(e)}")

def create_sample_documents():
    """Create sample text documents converted to PDF format"""
    print("📝 Creating sample documents...")
    
    # Create a sample FAQ document
    faq_content = """
    FREQUENTLY ASKED QUESTIONS
    
    Q: How do I reset my password?
    A: To reset your password, go to the login page and click "Forgot Password". 
    Follow the instructions sent to your email.
    
    Q: What are your business hours?
    A: Our support team is available Monday-Friday, 9 AM to 6 PM EST.
    
    Q: How can I contact technical support?
    A: You can reach technical support at support@techcorp.com or call 1-800-TECH-HELP.
    
    Q: What is your refund policy?
    A: We offer full refunds within 30 days of purchase. Contact our billing team for assistance.
    
    Q: How do I update my account information?
    A: Log into your account dashboard and navigate to "Account Settings" to update your information.
    """
    
    # Save as text file (in real scenario, you'd convert to PDF)
    faq_path = Path("data/documents/FAQ_TechCorp.txt")
    with open(faq_path, 'w', encoding='utf-8') as f:
        f.write(faq_content)
    
    print("✅ Created sample FAQ document")

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists() and env_example_path.exists():
        import shutil
        shutil.copy(env_example_path, env_path)
        print("✅ Created .env file from example")
        print("📝 Please edit .env file with your API keys")
    else:
        print("⏭️  .env file already exists or .env.example not found")

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")
    
    try:
        import streamlit
        import langchain
        import chromadb
        import sentence_transformers
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def display_next_steps():
    """Display instructions for next steps"""
    print("\n" + "="*50)
    print("🚀 SETUP COMPLETE!")
    print("="*50)
    print("\nNext steps:")
    print("1. Add your PDF documents to data/documents/")
    print("2. Edit .env file with your API keys (optional)")
    print("3. Run the application: streamlit run app.py")
    print("\nFor HuggingFace deployment:")
    print("- Set USE_HUGGINGFACE=true in .env")
    print("- Upload all files to your HuggingFace Space")
    print("\nDocumentation requirements:")
    print("- Add at least 3 documents")
    print("- At least 2 should be PDF format") 
    print("- At least 1 should have 400+ pages")

def main():
    """Main setup function"""
    print("🔧 Setting up AI Customer Support Demo Environment")
    print("-" * 50)
    
    # Check requirements first
    if not check_requirements():
        return
    
    # Create directory structure
    create_directories()
    
    # Create sample documents
    create_sample_documents()
    
    # Try to download sample PDFs
    download_sample_pdfs()
    
    # Create .env file
    create_env_file()
    
    # Display next steps
    display_next_steps()

if __name__ == "__main__":
    main()