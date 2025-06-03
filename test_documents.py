#!/usr/bin/env python3
"""
Test script to check document loading
"""

import os

def test_documents():
    docs_dir = "data/documents"
    
    print("🔍 Checking documents directory...")
    print(f"Directory: {docs_dir}")
    print(f"Exists: {os.path.exists(docs_dir)}")
    
    if os.path.exists(docs_dir):
        files = os.listdir(docs_dir)
        print(f"Files found: {len(files)}")
        
        for filename in files:
            file_path = os.path.join(docs_dir, filename)
            file_size = os.path.getsize(file_path)
            
            print(f"\n📄 {filename}")
            print(f"   Size: {file_size} bytes")
            print(f"   Type: {filename.split('.')[-1].upper()}")
            
            if filename.lower().endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"   Content length: {len(content)} characters")
                        print(f"   Preview: {content[:100]}...")
                except Exception as e:
                    print(f"   ❌ Error reading: {e}")
            
            elif filename.lower().endswith('.pdf'):
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        print(f"   Pages: {len(pdf_reader.pages)}")
                        
                        # Try to read first page
                        if len(pdf_reader.pages) > 0:
                            first_page = pdf_reader.pages[0].extract_text()
                            print(f"   First page length: {len(first_page)} characters")
                            if first_page:
                                print(f"   Preview: {first_page[:100]}...")
                            else:
                                print("   ⚠️ First page appears empty")
                
                except ImportError:
                    print("   ❌ PyPDF2 not installed")
                except Exception as e:
                    print(f"   ❌ Error reading PDF: {e}")
    
    else:
        print("❌ Documents directory not found!")
        print("Creating directory...")
        os.makedirs(docs_dir, exist_ok=True)
        print("✅ Directory created. Please add your documents.")

if __name__ == "__main__":
    test_documents()