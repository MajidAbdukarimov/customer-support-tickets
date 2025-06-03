import streamlit as st
import os
from datetime import datetime

# ВАЖНО: st.set_page_config должен быть ПЕРВОЙ командой Streamlit
st.set_page_config(
    page_title="AI Customer Support System",
    page_icon="🤖",
    layout="wide"
)

# Company configuration
COMPANY_INFO = {
    "name": "TechCorp Solutions",
    "email": "support@techcorp.com",
    "phone": "+1-800-TECH-HELP"
}

def create_ticket(ticket_data):
    """Create a support ticket (demo version)"""
    try:
        ticket_id = f"TICKET-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        if "tickets" not in st.session_state:
            st.session_state.tickets = []
        
        ticket_record = {
            "ticket_id": ticket_id,
            "name": ticket_data['name'],
            "email": ticket_data['email'],
            "title": ticket_data['title'],
            "description": ticket_data['description'],
            "created_at": ticket_data['created_at']
        }
        
        st.session_state.tickets.append(ticket_record)
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "platform": "Demo System"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def process_pdf_file(file_path, filename, show_debug=False):
    """Process PDF file with optional debugging"""
    try:
        import PyPDF2
        
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            if show_debug:
                st.error(f"❌ File {filename} is empty (0 bytes)")
            return None
        
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            total_pages = len(pdf_reader.pages)
            
            if show_debug:
                st.info(f"📄 PDF {filename} has {total_pages} pages, size: {file_size} bytes")
            
            if total_pages == 0:
                if show_debug:
                    st.warning(f"⚠️ PDF {filename} has no pages")
                return None
            
            full_text = ""
            pages_with_text = 0
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        full_text += f"\n--- Page {page_num} ---\n{page_text}\n"
                        pages_with_text += 1
                except Exception:
                    continue
            
            if show_debug:
                st.info(f"📝 Extracted text from {pages_with_text}/{total_pages} pages, {len(full_text)} chars")
            
            if full_text.strip():
                return {
                    "filename": filename,
                    "content": full_text,
                    "pages": total_pages,
                    "type": "pdf"
                }
            else:
                if show_debug:
                    st.warning(f"⚠️ No readable text found in PDF {filename}")
                return None
                    
    except ImportError:
        if show_debug:
            st.error("❌ PyPDF2 not available")
        return None
    except Exception as e:
        if show_debug:
            st.error(f"❌ Error processing PDF {filename}: {str(e)}")
        return None

def load_documents_from_root(show_debug=False):
    """Load documents from the same directory as app.py"""
    documents = []
    current_dir = "."
    
    try:
        all_files = os.listdir(current_dir)
        
        # Фильтровать файлы
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
        txt_files = [f for f in all_files if f.lower().endswith('.txt') and 
                    f.lower() not in ['requirements.txt', 'runtime.txt']]
        
        if show_debug:
            st.header("🔍 Document Loading Debug Information")
            st.info(f"📁 Directory: {os.path.abspath(current_dir)}")
            st.info(f"📄 All files: {', '.join(sorted(all_files))}")
            st.success(f"📄 PDF files: {pdf_files if pdf_files else 'None found'}")
            st.success(f"📝 TXT files: {txt_files if txt_files else 'None found'}")
        
        # Process PDF files
        for filename in pdf_files:
            file_path = os.path.join(current_dir, filename)
            
            if show_debug:
                st.markdown(f"**Processing: {filename}**")
            
            pdf_doc = process_pdf_file(file_path, filename, show_debug)
            if pdf_doc:
                documents.append(pdf_doc)
                if show_debug:
                    st.success(f"✅ Successfully loaded: {filename}")
        
        # Process TXT files
        for filename in txt_files:
            file_path = os.path.join(current_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        documents.append({
                            "filename": filename,
                            "content": content,
                            "pages": 1,
                            "type": "text"
                        })
                        if show_debug:
                            st.success(f"✅ Loaded text file: {filename}")
            except Exception as e:
                if show_debug:
                    st.error(f"❌ Error processing {filename}: {str(e)}")
        
        if show_debug:
            st.markdown("---")
            st.header("📊 Loading Summary")
            total_loaded = len(documents)
            pdf_loaded = len([d for d in documents if d["type"] == "pdf"])
            txt_loaded = len([d for d in documents if d["type"] == "text"])
            
            st.success(f"✅ Total documents loaded: {total_loaded}")
            st.info(f"📄 PDF documents: {pdf_loaded}")
            st.info(f"📝 Text documents: {txt_loaded}")
    
    except Exception as e:
        if show_debug:
            st.error(f"❌ Error reading directory: {str(e)}")
    
    return documents

def get_sample_documents():
    """Get sample documents for the system"""
    documents = [
        {
            "filename": "FAQ_Sample.txt",
            "content": """# Frequently Asked Questions

## Account Management
**Q: How do I reset my password?**
A: To reset your password, go to the login page and click "Forgot Password". Enter your email address and follow the instructions sent to your email.

**Q: How do I update my account information?**
A: Log into your account, navigate to "Account Settings", update your information, and click "Save Changes".

## Technical Support
**Q: What are your business hours?**
A: Our support team is available Monday-Friday, 9 AM to 6 PM EST. Emergency support is available 24/7 for critical issues.

**Q: How can I contact technical support?**
A: You can reach us at support@techcorp.com, call 1-800-TECH-HELP, or use our live chat feature.

## Billing
**Q: What is your refund policy?**
A: We offer full refunds within 30 days of purchase. Contact billing@techcorp.com for refund requests.

**Q: How do I upgrade my subscription?**
A: Log into your account, go to the Billing section, select "Upgrade Plan", and choose your new plan.
""",
            "pages": 1,
            "type": "text"
        }
    ]
    return documents

def search_documents(query, documents):
    """Improved search through documents with correct page detection"""
    results = []
    query_lower = query.lower()
    query_words = [word for word in query_lower.split() if len(word) > 2]
    
    for doc in documents:
        content_lower = doc["content"].lower()
        
        # Проверяем, есть ли хотя бы одно слово из запроса в документе
        if any(word in content_lower for word in query_words):
            
            if doc["type"] == "pdf":
                # Для PDF файлов ищем по страницам
                # Улучшенный парсинг страниц
                pages = doc["content"].split('\n--- Page ')
                all_page_results = []
                
                for i, page_content in enumerate(pages):
                    if i == 0 and not page_content.startswith('--- Page '):
                        # Первая часть может не содержать номер страницы
                        continue
                    
                    # Извлекаем номер страницы
                    try:
                        if i == 0:
                            # Если первая часть начинается с '--- Page '
                            page_content = page_content[4:]  # Убираем '--- '
                        
                        page_num_end = page_content.find(' ---')
                        if page_num_end > 0:
                            page_num = int(page_content[:page_num_end])
                            page_text = page_content[page_num_end + 4:]  # Убираем " ---\n"
                        else:
                            continue
                    except (ValueError, IndexError):
                        continue
                    
                    # Проверяем, содержит ли эта страница искомый текст
                    page_text_lower = page_text.lower()
                    
                    # Специальная проверка для точного поиска (например, "Essay#288")
                    exact_match = query_lower in page_text_lower
                    word_matches = sum(1 for word in query_words if word in page_text_lower)
                    
                    if exact_match or word_matches > 0:
                        # Находим контекст вокруг совпадения
                        context = ""
                        
                        if exact_match:
                            # Для точного совпадения находим позицию и берем контекст
                            pos = page_text_lower.find(query_lower)
                            start = max(0, pos - 200)
                            end = min(len(page_text), pos + 400)
                            context = page_text[start:end].strip()
                            if start > 0:
                                context = "..." + context
                            if end < len(page_text):
                                context = context + "..."
                        else:
                            # Для поиска по словам - находим наиболее релевантный параграф
                            paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
                            best_para = None
                            max_matches = 0
                            
                            for para in paragraphs:
                                para_matches = sum(1 for word in query_words if word in para.lower())
                                if para_matches > max_matches:
                                    max_matches = para_matches
                                    best_para = para
                            
                            if best_para:
                                context = best_para[:600] + "..." if len(best_para) > 600 else best_para
                        
                        if context:
                            all_page_results.append({
                                "filename": doc["filename"],
                                "content": context,
                                "page": page_num,
                                "type": doc["type"],
                                "matches": word_matches + (10 if exact_match else 0),  # Бонус за точное совпадение
                                "exact_match": exact_match
                            })
                
                # Добавляем все найденные результаты для этого документа
                results.extend(all_page_results)
                
            else:
                # Для текстовых файлов
                exact_match = query_lower in content_lower
                
                if exact_match:
                    # Для точного совпадения
                    pos = content_lower.find(query_lower)
                    start = max(0, pos - 200)
                    end = min(len(doc["content"]), pos + 400)
                    context = doc["content"][start:end].strip()
                    if start > 0:
                        context = "..." + context
                    if end < len(doc["content"]):
                        context = context + "..."
                    
                    results.append({
                        "filename": doc["filename"],
                        "content": context,
                        "page": 1,
                        "type": doc["type"],
                        "matches": 10,  # Высокий приоритет для точного совпадения
                        "exact_match": True
                    })
                else:
                    # Поиск по словам
                    paragraphs = [p.strip() for p in doc["content"].split('\n\n') if p.strip()]
                    best_para = None
                    max_matches = 0
                    
                    for para in paragraphs:
                        para_matches = sum(1 for word in query_words if word in para.lower())
                        if para_matches > max_matches:
                            max_matches = para_matches
                            best_para = para
                    
                    if best_para and max_matches > 0:
                        results.append({
                            "filename": doc["filename"],
                            "content": best_para[:600] + "..." if len(best_para) > 600 else best_para,
                            "page": 1,
                            "type": doc["type"],
                            "matches": max_matches,
                            "exact_match": False
                        })
    
    # Сортируем по приоритету: сначала точные совпадения, потом по количеству совпадений
    results.sort(key=lambda x: (x.get("exact_match", False), x.get("matches", 0)), reverse=True)
    
    # Если есть точные совпадения, показываем все страницы где они найдены
    if results and results[0].get("exact_match", False):
        exact_results = [r for r in results if r.get("exact_match", False)]
        return exact_results[:5]  # Показываем до 5 точных совпадений
    
    return results[:3]

def generate_response(query, search_results):
    """Generate response based on search results"""
    if not search_results:
        return {
            "answer": f"I couldn't find specific information about '{query}' in our documentation.\n\nI'd be happy to help you create a support ticket so our team can provide detailed assistance.\n\nContact us:\n📧 {COMPANY_INFO['email']}\n📞 {COMPANY_INFO['phone']}",
            "sources": []
        }
    
    # Проверяем, есть ли точные совпадения
    exact_matches = [r for r in search_results if r.get("exact_match", False)]
    
    if exact_matches:
        # Если есть точные совпадения, показываем их все
        if len(exact_matches) == 1:
            result = exact_matches[0]
            response = f"I found an exact match for '{query}' in our documentation:\n\n"
            response += f"📄 **{result['filename']}** (Page {result['page']})\n\n"
            response += f"{result['content']}\n\n"
        else:
            response = f"I found {len(exact_matches)} exact matches for '{query}' in our documentation:\n\n"
            for idx, result in enumerate(exact_matches, 1):
                response += f"**Match {idx}:** 📄 {result['filename']} (Page {result['page']})\n"
                response += f"{result['content']}\n\n"
                if idx < len(exact_matches):
                    response += "---\n\n"
    else:
        # Если точных совпадений нет, показываем наиболее релевантные результаты
        result = search_results[0]
        response = f"Based on our documentation, here's what I found related to '{query}':\n\n"
        response += f"{result['content']}\n\n"
        
        if len(search_results) > 1:
            response += "**Other relevant information:**\n"
            for res in search_results[1:]:
                response += f"- 📄 {res['filename']} (Page {res['page']})\n"
            response += "\n"
    
    response += f"For additional assistance, contact us at {COMPANY_INFO['email']} or {COMPANY_INFO['phone']}."
    
    return {
        "answer": response,
        "sources": [{"filename": res["filename"], "page": res["page"], "type": res["type"]} for res in search_results]
    }

# Main application
st.title("🤖 AI Customer Support System")
st.markdown(f"Welcome to **{COMPANY_INFO['name']}** - Your AI-powered support assistant!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_ticket_form" not in st.session_state:
    st.session_state.show_ticket_form = False
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False
if "documents" not in st.session_state:
    st.session_state.documents = []
if "show_debug" not in st.session_state:
    st.session_state.show_debug = False

# Load documents silently on first run
if not st.session_state.documents_loaded:
    # Load documents without showing debug info
    root_docs = load_documents_from_root(show_debug=False)
    
    if root_docs:
        st.session_state.documents = root_docs
    else:
        st.session_state.documents = get_sample_documents()
    
    st.session_state.documents_loaded = True

documents = st.session_state.documents

# Show debug information if requested
if st.session_state.show_debug:
    st.markdown("---")
    load_documents_from_root(show_debug=True)
    st.markdown("---")
    
    if st.button("❌ Hide Debug Info"):
        st.session_state.show_debug = False
        st.rerun()

# Sidebar
with st.sidebar:
    st.header("📞 Company Information")
    st.info(f"""
    **{COMPANY_INFO['name']}**
    
    📧 **Email:** {COMPANY_INFO['email']}
    📞 **Phone:** {COMPANY_INFO['phone']}
    
    🕒 **Hours:** Mon-Fri, 9 AM - 6 PM EST
    """)
    
    st.header("📊 System Status")
    total_docs = len(documents)
    pdf_docs = len([d for d in documents if d["type"] == "pdf"])
    text_docs = len([d for d in documents if d["type"] == "text"])
    total_pages = sum(d["pages"] for d in documents)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Docs", total_docs)
        st.metric("PDF Files", pdf_docs)
    with col2:
        st.metric("Text Files", text_docs)
        st.metric("Total Pages", total_pages)
    
    with st.expander("📄 Document Details"):
        for doc in documents:
            icon = "📄" if doc["type"] == "pdf" else "📝"
            st.write(f"{icon} **{doc['filename']}** ({doc['pages']} pages)")
    
    st.header("🔧 System Tools")
    
    if st.button("🔄 Reload Documents", use_container_width=True):
        st.session_state.documents_loaded = False
        st.rerun()
    
    if st.button("🔍 Show Debug Info", use_container_width=True):
        st.session_state.show_debug = True
        st.rerun()
    
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

# Chat input
if prompt := st.chat_input("Ask me anything about our products and services..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching..."):
            search_results = search_documents(prompt, documents)
            response = generate_response(prompt, search_results)
        
        st.markdown(response["answer"])
        
        if response.get("sources"):
            with st.expander("📚 Sources"):
                for source in response["sources"]:
                    icon = "📄" if source.get("type") == "pdf" else "📝"
                    st.markdown(f"{icon} **{source['filename']}** (Page {source['page']})")
        
        # Suggest ticket creation if no results
        if not response.get("sources"):
            if st.button("🎫 Create Ticket for This Question"):
                st.session_state.show_ticket_form = True
                st.session_state.ticket_question = prompt
    
    # Add assistant message
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
                                placeholder="Brief description")
        
        description = st.text_area("Detailed Description *", 
                                 height=150,
                                 placeholder="Describe your issue in detail...")
        
        col_submit, col_cancel = st.columns([1, 1])
        
        with col_submit:
            submitted = st.form_submit_button("🚀 Create Ticket")
        
        with col_cancel:
            cancelled = st.form_submit_button("❌ Cancel")
        
        if submitted:
            if name and email and title and description:
                ticket_data = {
                    "name": name,
                    "email": email,
                    "title": title,
                    "description": description,
                    "created_at": datetime.now().isoformat()
                }
                
                result = create_ticket(ticket_data)
                
                if result["success"]:
                    st.success(f"✅ Ticket created successfully!")
                    st.info(f"**Ticket ID:** {result['ticket_id']}")
                    st.info(f"**Platform:** {result['platform']}")
                    
                    st.session_state.show_ticket_form = False
                    if "ticket_question" in st.session_state:
                        del st.session_state.ticket_question
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result.get('error')}")
            else:
                st.error("⚠️ Please fill in all required fields.")
        
        if cancelled:
            st.session_state.show_ticket_form = False
            if "ticket_question" in st.session_state:
                del st.session_state.ticket_question
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**AI Customer Support System** - Capstone Project for Advanced Generative AI")

# Show created tickets for demo
if "tickets" in st.session_state and st.session_state.tickets:
    with st.expander(f"📋 Created Tickets ({len(st.session_state.tickets)})"):
        for ticket in st.session_state.tickets[-3:]:
            st.write(f"**{ticket['ticket_id']}** - {ticket['title']}")
            st.caption(f"By: {ticket['name']} ({ticket['email']})")