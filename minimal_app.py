import streamlit as st
import os
from datetime import datetime

# Minimal configuration
COMPANY_INFO = {
    "name": "TechCorp Solutions",
    "email": "support@techcorp.com", 
    "phone": "+1-800-TECH-HELP"
}

# Simple document storage
if "documents" not in st.session_state:
    st.session_state.documents = []

def load_documents():
    """Load documents from both text and PDF files"""
    docs_dir = "data/documents"
    documents = []
    
    if not os.path.exists(docs_dir):
        st.error(f"Directory {docs_dir} not found!")
        return documents
    
    files = os.listdir(docs_dir)
    st.info(f"Found {len(files)} files in {docs_dir}")
    
    for filename in files:
        file_path = os.path.join(docs_dir, filename)
        
        try:
            if filename.lower().endswith('.txt'):
                # Process text files
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        "filename": filename,
                        "content": content,
                        "pages": 1,
                        "type": "text"
                    })
                    st.success(f"✅ Loaded text file: {filename}")
            
            elif filename.lower().endswith('.pdf'):
                # Try to process PDF files
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        total_pages = len(pdf_reader.pages)
                        
                        # Extract text from all pages
                        full_text = ""
                        for page_num, page in enumerate(pdf_reader.pages):
                            try:
                                page_text = page.extract_text()
                                if page_text:
                                    full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                            except Exception as e:
                                st.warning(f"Could not read page {page_num + 1} of {filename}: {e}")
                        
                        if full_text.strip():
                            documents.append({
                                "filename": filename,
                                "content": full_text,
                                "pages": total_pages,
                                "type": "pdf"
                            })
                            st.success(f"✅ Loaded PDF file: {filename} ({total_pages} pages)")
                        else:
                            st.warning(f"⚠️ PDF {filename} appears to be empty or unreadable")
                
                except ImportError:
                    st.error("PyPDF2 not installed. Install with: pip install PyPDF2")
                except Exception as e:
                    st.error(f"❌ Error reading PDF {filename}: {e}")
            
            else:
                st.info(f"ℹ️ Skipping unsupported file: {filename}")
                
        except Exception as e:
            st.error(f"❌ Error processing {filename}: {e}")
    
    st.success(f"📚 Total documents loaded: {len(documents)}")
    return documents

def simple_search(query, documents):
    """Enhanced search in documents"""
    results = []
    query_words = query.lower().split()
    
    for doc in documents:
        content_lower = doc["content"].lower()
        
        # Check if any query words are in the document
        matches = sum(1 for word in query_words if word in content_lower)
        
        if matches > 0:
            # Find the most relevant paragraph
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
                # Extract page number if it's a PDF
                page_num = 1
                if doc["type"] == "pdf":
                    # Try to find page number in the paragraph
                    import re
                    page_match = re.search(r'--- Page (\d+) ---', best_para)
                    if page_match:
                        page_num = int(page_match.group(1))
                        # Clean the paragraph from page markers
                        best_para = re.sub(r'--- Page \d+ ---\n?', '', best_para)
                
                results.append({
                    "filename": doc["filename"],
                    "content": best_para[:800] + "..." if len(best_para) > 800 else best_para,
                    "page": page_num,
                    "score": best_score,
                    "type": doc["type"]
                })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]  # Return top 3 results

def generate_response(query, search_results):
    """Generate a response based on search results"""
    if not search_results:
        return {
            "answer": f"I couldn't find specific information about '{query}' in our documentation. Would you like to create a support ticket for assistance?",
            "sources": []
        }
    
    # Use the best result
    result = search_results[0]
    
    response = f"Based on our documentation, here's what I found:\n\n{result['content']}\n\n"
    
    if len(search_results) > 1:
        response += "I also found related information in other documents. "
    
    response += "For more detailed information, please contact our support team."
    
    sources = []
    for res in search_results:
        sources.append({
            "filename": res["filename"],
            "page": res["page"],
            "chunk": res["content"][:200] + "...",
            "type": res["type"]
        })
    
    return {
        "answer": response,
        "sources": sources
    }

def create_local_ticket(ticket_data):
    """Create a simple local ticket"""
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
        
        return {"success": True, "ticket_id": ticket_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    st.set_page_config(
        page_title="AI Customer Support",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Customer Support Assistant")
    st.markdown(f"Welcome to **{COMPANY_INFO['name']}** support!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_ticket_form" not in st.session_state:
        st.session_state.show_ticket_form = False
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False
    
    # Sidebar
    with st.sidebar:
        st.header("Company Information")
        st.info(f"""
        **{COMPANY_INFO['name']}**
        
        📧 Email: {COMPANY_INFO['email']}
        📞 Phone: {COMPANY_INFO['phone']}
        """)
        
        st.header("Document Management")
        
        # Load documents button
        if st.button("🔄 Load/Reload Documents", use_container_width=True):
            with st.spinner("Loading documents..."):
                st.session_state.documents = load_documents()
                st.session_state.documents_loaded = True
        
        # Load documents on first run
        if not st.session_state.documents_loaded:
            with st.spinner("Loading documents for the first time..."):
                st.session_state.documents = load_documents()
                st.session_state.documents_loaded = True
        
        # Display document stats
        if hasattr(st.session_state, 'documents'):
            st.metric("Documents Loaded", len(st.session_state.documents))
            
            if st.session_state.documents:
                with st.expander("📁 Available Documents"):
                    for doc in st.session_state.documents:
                        icon = "📄" if doc["type"] == "pdf" else "📝"
                        st.write(f"{icon} **{doc['filename']}**")
                        st.caption(f"Type: {doc['type'].upper()}, Pages: {doc['pages']}")
        
        st.header("Actions")
        if st.button("🎫 Create Support Ticket"):
            st.session_state.show_ticket_form = True
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat area
    st.header("Chat")
    
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
    if prompt := st.chat_input("Ask a question about our products or services..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Search and respond
        with st.chat_message("assistant"):
            if not hasattr(st.session_state, 'documents') or not st.session_state.documents:
                st.error("No documents loaded. Please load documents first using the sidebar.")
                response = {
                    "answer": "I don't have access to any documents yet. Please load documents first using the 'Load/Reload Documents' button in the sidebar.",
                    "sources": []
                }
            else:
                with st.spinner("Searching through documents..."):
                    search_results = simple_search(prompt, st.session_state.documents)
                    response = generate_response(prompt, search_results)
            
            st.markdown(response["answer"])
            
            if response.get("sources"):
                with st.expander("📚 Sources"):
                    for source in response["sources"]:
                        icon = "📄" if source.get("type") == "pdf" else "📝"
                        st.markdown(f"{icon} **{source['filename']}** (Page {source['page']})")
                        st.markdown(f"_{source['chunk']}_")
            
            # Suggest ticket if no results
            if not response.get("sources"):
                if st.button("Create Ticket for This Question"):
                    st.session_state.show_ticket_form = True
                    st.session_state.ticket_question = prompt
        
        # Add response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["answer"],
            "sources": response.get("sources", [])
        })
        
        st.rerun()
    
    # Ticket form section
    if st.session_state.show_ticket_form:
        st.header("🎫 Create Support Ticket")
        
        with st.form("ticket_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name *")
                email = st.text_input("Your Email *")
            
            with col2:
                title = st.text_input("Title *", 
                                    value=st.session_state.get("ticket_question", ""))
            
            description = st.text_area("Description *", height=150)
            
            col_submit, col_cancel = st.columns([1, 1])
            
            with col_submit:
                submitted = st.form_submit_button("Create Ticket", use_container_width=True)
            
            with col_cancel:
                cancelled = st.form_submit_button("Cancel", use_container_width=True)
            
            if submitted:
                if name and email and title and description:
                    ticket_data = {
                        "name": name,
                        "email": email,
                        "title": title,
                        "description": description,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    result = create_local_ticket(ticket_data)
                    
                    if result["success"]:
                        st.success(f"✅ Ticket created successfully! Ticket ID: {result['ticket_id']}")
                        st.session_state.show_ticket_form = False
                        if "ticket_question" in st.session_state:
                            del st.session_state.ticket_question
                        st.rerun()
                    else:
                        st.error(f"❌ Error creating ticket: {result['error']}")
                else:
                    st.error("Please fill in all required fields.")
            
            if cancelled:
                st.session_state.show_ticket_form = False
                if "ticket_question" in st.session_state:
                    del st.session_state.ticket_question
                st.rerun()
    
    # Help section
    if not st.session_state.show_ticket_form:
        st.header("📖 Help & Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **How to use this system:**
            1. Documents are automatically loaded from the `data/documents/` folder
            2. Type your question in the chat box above
            3. The system will search through all documents
            4. You'll get an answer with source citations
            5. Create a support ticket for complex issues
            """)
            
            st.markdown("""
            **Sample questions to try:**
            - "How do I reset my password?"
            - "What is your refund policy?"
            - "How can I contact support?"
            - "What are your business hours?"
            - "How do I update my account?"
            """)
        
        with col2:
            st.markdown(f"""
            **Contact Information:**
            - 📧 Email: {COMPANY_INFO['email']}
            - 📞 Phone: {COMPANY_INFO['phone']}
            
            **System Information:**
            - Documents loaded: {len(st.session_state.documents) if hasattr(st.session_state, 'documents') else 0}
            - Supports: PDF and Text files
            - Search: Keyword-based with relevance scoring
            """)

if __name__ == "__main__":
    main()