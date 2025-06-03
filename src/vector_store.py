import os
import sys
from typing import List, Dict, Tuple
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from config import VECTOR_DB_PATH, HF_EMBEDDING_MODEL

# Try to fix SQLite issue first
try:
    import pysqlite3.dbapi2 as sqlite3
    sys.modules['sqlite3'] = sqlite3
    print("Using pysqlite3-binary for SQLite compatibility")
except ImportError:
    pass

# Try ChromaDB first, fall back to FAISS if SQLite issues
USE_CHROMADB = True
try:
    import chromadb
    from chromadb.config import Settings
    print("Using ChromaDB for vector storage")
except RuntimeError as e:
    if "sqlite3" in str(e).lower():
        print("ChromaDB SQLite issue detected, falling back to FAISS")
        USE_CHROMADB = False
        import faiss
        import numpy as np
        import pickle
    else:
        raise e

class VectorStore:
    def __init__(self):
        self.embedding_model = SentenceTransformer(HF_EMBEDDING_MODEL)
        
        if USE_CHROMADB:
            self._init_chromadb()
        else:
            self._init_faiss()
    
    def _init_chromadb(self):
        """Initialize ChromaDB"""
        self.client = chromadb.PersistentClient(
            path=VECTOR_DB_PATH,
            settings=Settings(allow_reset=True)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"description": "Customer support documents"}
        )
    
    def _init_faiss(self):
        """Initialize FAISS as fallback"""
        self.faiss_path = VECTOR_DB_PATH + "_faiss"
        os.makedirs(self.faiss_path, exist_ok=True)
        
        self.index = None
        self.documents = []
        self.metadatas = []
        
        # Try to load existing index
        self._load_faiss_index()
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store"""
        if not documents:
            return
        
        print(f"Adding {len(documents)} documents to vector store...")
        
        if USE_CHROMADB:
            self._add_documents_chromadb(documents)
        else:
            self._add_documents_faiss(documents)
    
    def _add_documents_chromadb(self, documents: List[Document]) -> None:
        """Add documents to ChromaDB"""
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [doc.metadata["chunk_id"] for doc in documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            
            self.collection.add(
                documents=texts[i:end_idx],
                metadatas=metadatas[i:end_idx],
                ids=ids[i:end_idx],
                embeddings=embeddings[i:end_idx]
            )
        
        print(f"Successfully added {len(documents)} documents to ChromaDB")
    
    def _add_documents_faiss(self, documents: List[Document]) -> None:
        """Add documents to FAISS"""
        texts = [doc.page_content for doc in documents]
        embeddings = self.embedding_model.encode(texts)
        
        # Initialize or expand FAISS index
        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        
        # Store documents and metadata
        self.documents.extend(documents)
        self.metadatas.extend([doc.metadata for doc in documents])
        
        # Save index
        self._save_faiss_index()
        
        print(f"Successfully added {len(documents)} documents to FAISS")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        if self.is_empty():
            return []
        
        if USE_CHROMADB:
            return self._search_chromadb(query, n_results)
        else:
            return self._search_faiss(query, n_results)
    
    def _search_chromadb(self, query: str, n_results: int) -> List[Dict]:
        """Search using ChromaDB"""
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                    "filename": results["metadatas"][0][i]["filename"],
                    "page": results["metadatas"][0][i]["page"],
                    "chunk": doc[:200] + "..." if len(doc) > 200 else doc
                })
        
        return formatted_results
    
    def _search_faiss(self, query: str, n_results: int) -> List[Dict]:
        """Search using FAISS"""
        query_embedding = self.embedding_model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        scores, indices = self.index.search(query_embedding.astype('float32'), n_results)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.documents):
                doc = self.documents[idx]
                metadata = self.metadatas[idx]
                
                results.append({
                    "content": doc.page_content,
                    "metadata": metadata,
                    "distance": 1 - score,  # Convert similarity to distance
                    "filename": metadata.get("filename", "unknown"),
                    "page": metadata.get("page", 0),
                    "chunk": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
        
        return results
    
    def is_empty(self) -> bool:
        """Check if vector store is empty"""
        if USE_CHROMADB:
            try:
                count = self.collection.count()
                return count == 0
            except:
                return True
        else:
            return self.index is None or len(self.documents) == 0
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        try:
            if USE_CHROMADB:
                count = self.collection.count()
                sample_results = self.collection.get(limit=min(100, count))
                files = set()
                if sample_results["metadatas"]:
                    files = {meta["filename"] for meta in sample_results["metadatas"]}
                
                return {
                    "total_chunks": count,
                    "total_files": len(files),
                    "files": list(files),
                    "backend": "ChromaDB"
                }
            else:
                if self.is_empty():
                    return {"total_chunks": 0, "total_files": 0, "files": [], "backend": "FAISS"}
                
                files = set(meta.get("filename", "unknown") for meta in self.metadatas)
                
                return {
                    "total_chunks": len(self.documents),
                    "total_files": len(files),
                    "files": list(files),
                    "backend": "FAISS"
                }
        except Exception as e:
            return {
                "total_chunks": 0,
                "total_files": 0,
                "files": [],
                "error": str(e),
                "backend": "FAISS" if not USE_CHROMADB else "ChromaDB"
            }
    
    def _save_faiss_index(self):
        """Save FAISS index and metadata"""
        try:
            if self.index is not None:
                faiss.write_index(self.index, os.path.join(self.faiss_path, "index.faiss"))
            
            with open(os.path.join(self.faiss_path, "documents.pkl"), "wb") as f:
                pickle.dump(self.documents, f)
            
            with open(os.path.join(self.faiss_path, "metadata.pkl"), "wb") as f:
                pickle.dump(self.metadatas, f)
        except Exception as e:
            print(f"Warning: Failed to save FAISS index: {e}")
    
    def _load_faiss_index(self):
        """Load FAISS index and metadata"""
        try:
            index_path = os.path.join(self.faiss_path, "index.faiss")
            docs_path = os.path.join(self.faiss_path, "documents.pkl")
            meta_path = os.path.join(self.faiss_path, "metadata.pkl")
            
            if all(os.path.exists(p) for p in [index_path, docs_path, meta_path]):
                self.index = faiss.read_index(index_path)
                
                with open(docs_path, "rb") as f:
                    self.documents = pickle.load(f)
                
                with open(meta_path, "rb") as f:
                    self.metadatas = pickle.load(f)
                
                print(f"Loaded existing FAISS index with {len(self.documents)} documents")
        except Exception as e:
            print(f"Could not load existing FAISS index: {e}")
            self.index = None
            self.documents = []
            self.metadatas = []
    
    def reset(self) -> None:
        """Reset the vector store"""
        try:
            if USE_CHROMADB:
                self.client.reset()
                self.collection = self.client.get_or_create_collection(
                    name="documents",
                    metadata={"description": "Customer support documents"}
                )
            else:
                self.index = None
                self.documents = []
                self.metadatas = []
                # Remove saved files
                for filename in ["index.faiss", "documents.pkl", "metadata.pkl"]:
                    filepath = os.path.join(self.faiss_path, filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
            
            print("Vector store reset successfully")
        except Exception as e:
            print(f"Error resetting vector store: {str(e)}")