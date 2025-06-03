import os
from dotenv import load_dotenv

load_dotenv()

# Company Information
COMPANY_INFO = {
    "name": "TechCorp Solutions",
    "email": "support@techcorp.com", 
    "phone": "+1-800-TECH-HELP"
}

# AI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"

# Alternative: Use Hugging Face models for free deployment
USE_HUGGINGFACE = os.getenv("USE_HUGGINGFACE", "true").lower() == "true"
HF_MODEL_NAME = "microsoft/DialoGPT-medium"
HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Vector Store Configuration
VECTOR_DB_PATH = "data/vector_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# GitHub Issues Configuration (for ticket system)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO", "your-username/support-tickets")

# Chat Configuration  
MAX_HISTORY_LENGTH = 10
CONFIDENCE_THRESHOLD = 0.7