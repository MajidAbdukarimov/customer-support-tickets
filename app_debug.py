import streamlit as st
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuration
COMPANY_INFO = {
    "name": os.getenv("COMPANY_NAME", "TechCorp Solutions"),
    "email": os.getenv("COMPANY_EMAIL", "support@techcorp.com"),
    "phone": os.getenv("COMPANY_PHONE", "+1-800-TECH-HELP")
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def create_github_ticket(ticket_data):
    """Create GitHub issue with detailed error reporting"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        st.warning("GitHub not configured, using local storage")
        return create_local_ticket(ticket_data)
    
    try:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        body = f"""**Customer Information:**
- Name: {ticket_data['name']}
- Email: {ticket_data['email']}
- Created: {ticket_data['created_at']}

**Description:**
{ticket_data['description']}

---
*This ticket was created automatically by the AI Customer Support system.*
"""
        
        payload = {
            "title": f"[SUPPORT] {ticket_data['title']}",
            "body": body,
            "labels": ["support", "customer-request", "automated"]
        }
        
        url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
        
        # Show debug info
        st.info(f"🔍 Creating issue in repository: {GITHUB_REPO}")
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        st.info(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 201:
            issue_data = response.json()
            return {
                "success": True,
                "ticket_id": f"#{issue_data['number']}",
                "url": issue_data['html_url'],
                "platform": "GitHub Issues"
            }
        else:
            # Detailed error reporting
            st.error(f"❌ GitHub API Error: {response.status_code}")
            st.error(f"Response: {response.text}")
            
            try:
                error_data = response.json()
                if 'message' in error_data:
                    st.error(f"Error message: {error_data['message']}")
                if 'errors' in error_data:
                    for error in error_data['errors']:
                        st.error(f"Error detail: {error}")
            except:
                pass
            
            # Fallback to local storage
            st.warning("Falling back to local storage...")
            return create_local_ticket(ticket_data)
            
    except Exception as e:
        st.error(f"❌ Exception creating GitHub issue: {str(e)}")
        return create_local_ticket(ticket_data)

def test_github_connection():
    """Test GitHub connection and show results"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return False, "GitHub not configured"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Test repository access
        repo_url = f"https://api.github.com/repos/{GITHUB_REPO}"
        response = requests.get(repo_url, headers=headers)
        
        if response.status_code == 200:
            repo_data = response.json()
            has_issues = repo_data.get('has_issues', False)
            
            if not has_issues:
                return False, "Issues disabled in repository settings"
            
            return True, f"Connected to {repo_data['full_name']}"
        else:
            return False, f"Cannot access repository (Status: {response.status_code})"
            
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def create_local_ticket(ticket_data):
    """Fallback: Create local ticket"""
    try:
        os.makedirs("data/tickets", exist_ok=True)
        ticket_id = f"TICKET-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        ticket_file = f"data/tickets/{ticket_id}.txt"
        with open(ticket_file, 'w', encoding='utf-8') as f:
            f.write(f"Ticket ID: {ticket_id}\n")
            f.write(f"Name: {ticket_data['name']}\n")
            f.write(f"Email: {ticket_data['email']}\n")
            f.write(f"Title: {ticket_data['title']}\n")
            f.write(f"Description: {ticket_data['description']}\n")
            f.write(f"Created: {ticket_data['created_at']}\n")
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "platform": "Local Storage"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def load_documents():
    """Load documents with better error handling"""
    docs_dir = "data/documents"
    documents = []
    
    if not os.path.exists(docs_dir):
        st.error(f"Directory {docs_dir} not found!")
        return documents
    
    files = os.listdir(docs_dir)
    
    for filename in files:
        file_path = os.path.join(docs_dir, filename)
        
        try:
            if filename.lower().endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        "filename": filename,
                        "content": content,
                        "pages": 1,
                        "type": "text"
                    })
            
            elif filename.lower().endswith('.pdf'):
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        total_pages = len(pdf_reader.pages)
                        
                        full_text = ""
                        for page_num, page in enumerate(pdf_reader.pages):
                            try:
                                page_text = page.extract_text()
                                if page_text:
                                    full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                            except Exception:
                                continue
                        
                        if full_text.strip():
                            documents.append({
                                "filename": filename,
                                "content": full_text,
                                "pages": total_pages,
                                "type": "pdf"
                            })
                
                except ImportError:
                    st.error("PyPDF2 not installed. Run: pip install PyPDF2")
                except Exception as e:
                    st.error(f"Error reading PDF {filename}: {e}")
                    
        except Exception as e:
            st.error(f"Error processing {filename}: {e}")
    
    return documents

def simple_search(query, documents):
    """Simple but effective document search"""
    results = []
    query_words = [word.lower() for word in query.split() if len(word) > 2]
    
    for doc in documents:
        content_lower = doc["content"].lower()
        matches = sum(1 for word in query_words if word in content_lower)
        
        if matches > 0:
            paragraphs = doc["content"].split('\n\n')
            best_para = ""
            best_score = 0
            
            for para in paragraphs:
                para_lower = para.lower()
                score = sum(1 for word in query_words if word in para_lower)
                if score > best_score and len(para.strip()) > 50:
                    best_score = score
                    best_para = para
            
            if best_para:
                page_num = 1
                if doc["type"] == "pdf":
                    import re
                    page_match = re.search(r'--- Page (\d+) ---', best_para)
                    if page_match:
                        page_num = int(page_match.group(1))
                        best_para = re.sub(r'--- Page \d+ ---\n?', '', best_para)
                
                results.append({
                    "filename": doc["filename"],
                    "content": best_para[:800] + "..." if len(best_para) > 800 else best_para,
                    "page": page_num,
                    "score": best_score,
                    "type": doc["type"]
                })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]

def generate_response(query, search_results):
    """Generate response with proper formatting"""
    if not search_results:
        return {
            "answer": f"I couldn't find specific information about '{query}' in our documentation.\n\nI'd be happy to help you create a support ticket so our team can provide detailed assistance.\n\nYou can also contact us directly:\n📧 {COMPANY_INFO['email']}\n📞 {COMPANY_INFO['phone']}",
            "sources": []
        }
    
    result = search_results[0]
    response = f"Based on our documentation, here's what I found:\n\n{result['content']}\n\n"
    
    if len(search_results) > 1:
        response += "I also found related information in other documents. "
    
    response += f"For additional assistance, contact us at {COMPANY_INFO['email']} or {COMPANY_INFO['phone']}."
    
    sources = []
    for res in search_results:
        sources.append({
            "filename": res["filename"],
            "page": res["page"],
            "chunk": res["content"][:200] + "...",
            "type": res["type"]
        })
    
    return {"answer": response, "sources": sources}

def main():
    st.set_page_config(
        page_title="AI Customer Support System",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Customer Support System")
    st.markdown(f"Welcome to **{COMPANY_INFO['name']}** - Your AI-powered support assistant!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_ticket_form" not in st.session_state:
        st.session_state.show_ticket_form = False
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False
    
    # Sidebar
    with st.sidebar:
        st.header("📞 Company Information")
        st.info(f"""
        **{COMPANY_INFO['name']}**
        
        📧 **Email:** {COMPANY_INFO['email']}
        📞 **Phone:** {COMPANY_INFO['phone']}
        
        🕒 **Hours:** Mon-Fri, 9 AM - 6 PM EST
        """)
        
        # GitHub status with detailed testing
        st.header("🔧 System Status")
        
        if st.button("🧪 Test GitHub Connection"):
            with st.spinner("Testing GitHub connection..."):
                success, message = test_github_connection()
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
        
        if GITHUB_TOKEN and GITHUB_REPO:
            success, message = test_github_connection()
            if success:
                st.success("✅ GitHub Issues Connected")
                st.caption(f"Repo: {GITHUB_REPO}")
            else:
                st.error("❌ GitHub Connection Issue")
                st.caption(message)
        else:
            st.warning("⚠️ GitHub Not Configured")
            st.caption("Check .env file settings")
        
        # Document management
        st.header("📚 Document Management")
        
        if st.button("🔄 Load/Reload Documents", use_container_width=True):
            with st.spinner("Loading documents..."):
                st.session_state.documents = load_documents()
                st.session_state.documents_loaded = True
        
        if not st.session_state.documents_loaded:
            with st.spinner("Loading documents..."):
                st.session_state.documents = load_documents()
                st.session_state.documents_loaded = True
        
        # Document stats
        if hasattr(st.session_state, 'documents'):
            total_docs = len(st.session_state.documents)
            pdf_docs = len([d for d in st.session_state.documents if d["type"] == "pdf"])
            total_pages = sum(d["pages"] for d in st.session_state.documents)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documents", total_docs)
                st.metric("PDF Files", pdf_docs)
            with col2:
                st.metric("Total Pages", total_pages)
                large_docs = len([d for d in st.session_state.documents if d["pages"] >= 400])
                st.metric("400+ Pages", large_docs)
        
        st.header("🎫 Actions")
        if st.button("Create Support Ticket", use_container_width=True):
            st.session_state.show_ticket_form = True
        
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat area
    st.header("💬 Chat Assistant")
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        icon = "📄" if source.get("type") == "pdf" else "📝"
                        st.markdown(f"{icon} **{source['filename']}** (Page {source['page']})")
                        st.markdown(f"_{source['chunk']}_")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about our products and services..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if not hasattr(st.session_state, 'documents') or not st.session_state.documents:
                st.error("📋 No documents loaded. Please load documents using the sidebar.")
                response = {
                    "answer": "I don't have access to documents yet. Please use the 'Load/Reload Documents' button in the sidebar.",
                    "sources": []
                }
            else:
                with st.spinner("🔍 Searching through documents..."):
                    search_results = simple_search(prompt, st.session_state.documents)
                    response = generate_response(prompt, search_results)
            
            st.markdown(response["answer"])
            
            if response.get("sources"):
                with st.expander("📚 Sources"):
                    for source in response["sources"]:
                        icon = "📄" if source.get("type") == "pdf" else "📝"
                        st.markdown(f"{icon} **{source['filename']}** (Page {source['page']})")
                        st.markdown(f"_{source['chunk']}_")
            
            if not response.get("sources"):
                if st.button("🎫 Create Ticket for This Question"):
                    st.session_state.show_ticket_form = True
                    st.session_state.ticket_question = prompt
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["answer"],
            "sources": response.get("sources", [])
        })
        st.rerun()
    
    # Ticket form
    if st.session_state.show_ticket_form:
        st.header("🎫 Create Support Ticket")
        
        with st.form("ticket_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name *", placeholder="John Doe")
                email = st.text_input("Your Email *", placeholder="john@example.com")
            
            with col2:
                title = st.text_input("Ticket Title *", 
                                    value=st.session_state.get("ticket_question", ""),
                                    placeholder="Brief description of your issue")
            
            description = st.text_area("Detailed Description *", 
                                     height=150,
                                     placeholder="Please provide detailed information...")
            
            col_submit, col_cancel = st.columns([1, 1])
            
            with col_submit:
                submitted = st.form_submit_button("🚀 Create Ticket", use_container_width=True)
            
            with col_cancel:
                cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submitted:
                if name and email and title and description:
                    ticket_data = {
                        "name": name,
                        "email": email,
                        "title": title,
                        "description": description,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    with st.spinner("Creating ticket..."):
                        result = create_github_ticket(ticket_data)
                    
                    if result["success"]:
                        platform = result.get("platform", "Unknown")
                        st.success(f"✅ Ticket created successfully!")
                        st.info(f"**Ticket ID:** {result['ticket_id']}")
                        st.info(f"**Platform:** {platform}")
                        
                        if "url" in result:
                            st.markdown(f"🔗 [View Ticket on GitHub]({result['url']})")
                        
                        st.session_state.show_ticket_form = False
                        if "ticket_question" in st.session_state:
                            del st.session_state.ticket_question
                        st.rerun()
                    else:
                        st.error(f"❌ Error creating ticket: {result.get('error', 'Unknown error')}")
                else:
                    st.error("⚠️ Please fill in all required fields.")
            
            if cancelled:
                st.session_state.show_ticket_form = False
                if "ticket_question" in st.session_state:
                    del st.session_state.ticket_question
                st.rerun()

if __name__ == "__main__":
    main()