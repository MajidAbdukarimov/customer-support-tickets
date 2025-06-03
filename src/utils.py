import re
import streamlit as st
from typing import List, Dict, Any
import os
from datetime import datetime

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def create_download_link(content: str, filename: str, link_text: str) -> str:
    """Create a download link for text content"""
    import base64
    
    b64_content = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64_content}" download="{filename}">{link_text}</a>'
    return href

def log_interaction(user_query: str, ai_response: str, sources: List[Dict] = None):
    """Log user interactions for analytics"""
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "ai_response": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response,
        "sources_count": len(sources) if sources else 0,
        "has_sources": bool(sources)
    }
    
    # Simple logging - in production, use proper logging framework
    log_file = os.path.join(log_dir, f"interactions_{datetime.now().strftime('%Y%m%d')}.txt")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{log_entry}\n")

def display_metrics_sidebar():
    """Display system metrics in sidebar"""
    with st.sidebar:
        st.header("📊 System Metrics")
        
        # Check vector store status
        try:
            from src.vector_store import VectorStore
            vector_store = VectorStore()
            stats = vector_store.get_stats()
            
            st.metric("Documents Loaded", stats.get("total_files", 0))
            st.metric("Text Chunks", stats.get("total_chunks", 0))
            
            if stats.get("files"):
                with st.expander("📁 Loaded Files"):
                    for file in stats["files"]:
                        st.text(f"• {file}")
                        
        except Exception as e:
            st.error(f"Error loading metrics: {str(e)}")

def show_system_health():
    """Display system health check"""
    health_status = {}
    
    # Check vector store
    try:
        from src.vector_store import VectorStore
        vector_store = VectorStore()
        health_status["Vector Store"] = "✅ Connected" if not vector_store.is_empty() else "⚠️ Empty"
    except Exception as e:
        health_status["Vector Store"] = f"❌ Error: {str(e)}"
    
    # Check documents directory
    docs_dir = "data/documents"
    if os.path.exists(docs_dir):
        pdf_count = len([f for f in os.listdir(docs_dir) if f.lower().endswith('.pdf')])
        health_status["Documents"] = f"✅ {pdf_count} PDF files" if pdf_count > 0 else "⚠️ No PDFs found"
    else:
        health_status["Documents"] = "❌ Directory not found"
    
    # Check API keys (without exposing them)
    from config import OPENAI_API_KEY, GITHUB_TOKEN
    health_status["OpenAI API"] = "✅ Configured" if OPENAI_API_KEY else "⚠️ Not configured"
    health_status["GitHub API"] = "✅ Configured" if GITHUB_TOKEN else "⚠️ Not configured"
    
    return health_status

class StreamlitLogger:
    """Custom logger for Streamlit apps"""
    
    @staticmethod
    def info(message: str):
        st.info(f"ℹ️ {message}")
    
    @staticmethod
    def success(message: str):
        st.success(f"✅ {message}")
    
    @staticmethod
    def warning(message: str):
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def error(message: str):
        st.error(f"❌ {message}")
    
    @staticmethod
    def debug(message: str):
        if st.session_state.get("debug_mode", False):
            st.code(f"DEBUG: {message}")

def init_session_state():
    """Initialize Streamlit session state variables"""
    defaults = {
        "messages": [],
        "show_ticket_form": False,
        "debug_mode": False,
        "user_feedback": {},
        "current_session_id": datetime.now().strftime("%Y%m%d_%H%M%S")
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def export_chat_history() -> str:
    """Export chat history as text"""
    if not st.session_state.get("messages"):
        return "No chat history available."
    
    export_text = f"Chat History Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    export_text += "=" * 50 + "\n\n"
    
    for i, message in enumerate(st.session_state.messages, 1):
        role = "User" if message["role"] == "user" else "Assistant"
        export_text += f"{i}. {role}: {message['content']}\n"
        
        if message.get("sources"):
            export_text += "   Sources:\n"
            for source in message["sources"]:
                export_text += f"   - {source['filename']} (Page {source['page']})\n"
        
        export_text += "\n"
    
    return export_text