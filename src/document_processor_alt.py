import os
import PyPDF2
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_documents(self, directory_path: str) -> List[Document]:
        """Load and process all documents from directory"""
        documents = []
        
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")
            print("Please add your PDF documents to this directory")
            return documents
        
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                print(f"Processing: {filename}")
                
                try:
                    pdf_documents = self._process_pdf(file_path, filename)
                    documents.extend(pdf_documents)
                    print(f"Successfully processed {filename}: {len(pdf_documents)} chunks")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
            elif filename.lower().endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                print(f"Processing: {filename}")
                
                try:
                    txt_documents = self._process_txt(file_path, filename)
                    documents.extend(txt_documents)
                    print(f"Successfully processed {filename}: {len(txt_documents)} chunks")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
        
        return documents
    
    def _process_pdf(self, file_path: str, filename: str) -> List[Document]:
        """Process a single PDF file using PyPDF2"""
        documents = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        # Extract text from page
                        text = page.extract_text()
                        
                        if text and text.strip():
                            # Create document with metadata
                            doc = Document(
                                page_content=text,
                                metadata={
                                    "filename": filename,
                                    "page": page_num,
                                    "total_pages": total_pages,
                                    "source": file_path
                                }
                            )
                            
                            # Split into chunks
                            chunks = self.text_splitter.split_documents([doc])
                            
                            # Update metadata for each chunk
                            for i, chunk in enumerate(chunks):
                                chunk.metadata.update({
                                    "chunk_id": f"{filename}_page_{page_num}_chunk_{i}",
                                    "chunk_index": i
                                })
                            
                            documents.extend(chunks)
                            
                    except Exception as e:
                        print(f"Error processing page {page_num} of {filename}: {str(e)}")
                        continue
        
        except Exception as e:
            print(f"Error opening PDF {filename}: {str(e)}")
            return []
        
        return documents
    
    def _process_txt(self, file_path: str, filename: str) -> List[Document]:
        """Process a single text file"""
        documents = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
                if text and text.strip():
                    # Create document with metadata
                    doc = Document(
                        page_content=text,
                        metadata={
                            "filename": filename,
                            "page": 1,
                            "total_pages": 1,
                            "source": file_path
                        }
                    )
                    
                    # Split into chunks
                    chunks = self.text_splitter.split_documents([doc])
                    
                    # Update metadata for each chunk
                    for i, chunk in enumerate(chunks):
                        chunk.metadata.update({
                            "chunk_id": f"{filename}_chunk_{i}",
                            "chunk_index": i
                        })
                    
                    documents.extend(chunks)
        
        except Exception as e:
            print(f"Error processing text file {filename}: {str(e)}")
            return []
        
        return documents
    
    def get_document_stats(self, documents: List[Document]) -> Dict:
        """Get statistics about processed documents"""
        if not documents:
            return {"total_documents": 0, "total_chunks": 0, "files": []}
        
        files_info = {}
        for doc in documents:
            filename = doc.metadata["filename"]
            if filename not in files_info:
                files_info[filename] = {
                    "pages": doc.metadata["total_pages"],
                    "chunks": 0
                }
            files_info[filename]["chunks"] += 1
        
        return {
            "total_documents": len(files_info),
            "total_chunks": len(documents),
            "files": [
                {
                    "name": name, 
                    "pages": info["pages"], 
                    "chunks": info["chunks"]
                } 
                for name, info in files_info.items()
            ]
        }