import os
from typing import List, Dict, Any
from config import (
    OPENAI_API_KEY, MODEL_NAME, USE_HUGGINGFACE, 
    MAX_HISTORY_LENGTH, CONFIDENCE_THRESHOLD, COMPANY_INFO
)

# Import based on configuration
if USE_HUGGINGFACE or not OPENAI_API_KEY:
    from transformers import pipeline
    USE_OPENAI = False
else:
    import openai
    USE_OPENAI = True
    openai.api_key = OPENAI_API_KEY

class ChatEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        
        if not USE_OPENAI:
            # Initialize Hugging Face pipeline for free deployment
            self.generator = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                device=-1  # Use CPU
            )
    
    def get_response(self, query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate response to user query"""
        
        # Search for relevant documents
        relevant_docs = self.vector_store.search(query, n_results=5)
        
        # Calculate confidence based on search results
        confidence = self._calculate_confidence(relevant_docs)
        
        # Generate response
        if relevant_docs and confidence >= CONFIDENCE_THRESHOLD:
            response = self._generate_response_with_context(query, relevant_docs, chat_history)
            sources = [
                {
                    "filename": doc["filename"],
                    "page": doc["page"],
                    "chunk": doc["chunk"]
                }
                for doc in relevant_docs[:3]  # Top 3 sources
            ]
        else:
            response = self._generate_fallback_response(query)
            sources = []
        
        return {
            "answer": response,
            "sources": sources,
            "confidence": confidence
        }
    
    def _calculate_confidence(self, relevant_docs: List[Dict]) -> float:
        """Calculate confidence score based on search results"""
        if not relevant_docs:
            return 0.0
        
        # Use inverse of distance as confidence measure
        # ChromaDB returns lower distances for more similar documents
        if relevant_docs[0]["distance"] < 0.5:
            return 1.0
        elif relevant_docs[0]["distance"] < 0.8:
            return 0.8
        elif relevant_docs[0]["distance"] < 1.2:
            return 0.6
        else:
            return 0.4
    
    def _generate_response_with_context(self, query: str, relevant_docs: List[Dict], chat_history: List[Dict] = None) -> str:
        """Generate response using retrieved context"""
        
        # Prepare context from relevant documents
        context = "\n\n".join([
            f"From {doc['filename']} (Page {doc['page']}):\n{doc['content']}"
            for doc in relevant_docs[:3]
        ])
        
        # Prepare chat history
        history_text = ""
        if chat_history:
            recent_history = chat_history[-MAX_HISTORY_LENGTH:]
            history_text = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in recent_history
            ])
        
        # Create prompt
        prompt = f"""You are a helpful customer support assistant for {COMPANY_INFO['name']}.
        
Company Information:
- Name: {COMPANY_INFO['name']}
- Email: {COMPANY_INFO['email']}
- Phone: {COMPANY_INFO['phone']}

Context from documentation:
{context}

Recent conversation history:
{history_text}

Current question: {query}

Please provide a helpful and accurate response based on the documentation context. If you cite information, mention the document name and page number. Be concise but thorough."""
        
        if USE_OPENAI:
            return self._generate_openai_response(prompt)
        else:
            return self._generate_hf_response(prompt)
    
    def _generate_fallback_response(self, query: str) -> str:
        """Generate fallback response when no relevant context is found"""
        return f"""I apologize, but I couldn't find specific information about "{query}" in our documentation. 

I'd be happy to help you create a support ticket so our team can provide you with detailed assistance. 

You can also contact us directly:
📧 Email: {COMPANY_INFO['email']}
📞 Phone: {COMPANY_INFO['phone']}

Would you like me to help you create a support ticket for this question?"""
    
    def _generate_openai_response(self, prompt: str) -> str:
        """Generate response using OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again or contact support at {COMPANY_INFO['email']}. Error: {str(e)}"
    
    def _generate_hf_response(self, prompt: str) -> str:
        """Generate response using Hugging Face model"""
        try:
            # For free deployment, use a simple template-based response
            if "contact" in prompt.lower() or "phone" in prompt.lower() or "email" in prompt.lower():
                return f"""For support, you can reach us at:
📧 Email: {COMPANY_INFO['email']}
📞 Phone: {COMPANY_INFO['phone']}

How else can I help you today?"""
            
            # Simple response generation for demonstration
            # In production, you might want to use a more sophisticated model
            return """Based on the available documentation, I can help you with your question. 
            
If you need more specific information, I recommend creating a support ticket so our team can provide detailed assistance tailored to your needs.

Is there anything specific from our documentation you'd like me to clarify?"""
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please contact support at {COMPANY_INFO['email']}."