# Deployment Guide for HuggingFace Spaces

This guide explains how to deploy your AI Customer Support System to HuggingFace Spaces.

## 📋 Pre-deployment Checklist

- [ ] All code files are ready
- [ ] PDF documents are added to `data/documents/`
- [ ] Requirements.txt includes all dependencies
- [ ] Runtime.txt specifies Python version
- [ ] Environment variables are configured

## 🚀 Step-by-Step Deployment

### 1. Create HuggingFace Account
1. Go to [HuggingFace](https://huggingface.co/)
2. Sign up or log in
3. Verify your email address

### 2. Create New Space
1. Navigate to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `ai-customer-support`
   - **License**: MIT
   - **SDK**: Streamlit
   - **Hardware**: CPU basic (free tier)
4. Make the space public or private
5. Click "Create Space"

### 3. Prepare Files for Upload

Ensure your project structure looks like this:
```
your-project/
├── app.py
├── requirements.txt
├── runtime.txt
├── config.py
├── .env.example
├── src/
│   ├── document_processor.py
│   ├── vector_store.py
│   ├── chat_engine.py
│   ├── ticket_manager.py
│   └── utils.py
├── data/
│   └── documents/
│       ├── your-manual.pdf (400+ pages)
│       ├── faq-document.pdf
│       └── policies.pdf
└── README.md
```

### 4. Upload Files

#### Option A: Web Interface
1. In your new Space, click "Files and versions"
2. Click "Upload files"
3. Drag and drop all your project files
4. Maintain the folder structure
5. Commit changes

#### Option B: Git (Recommended)
```bash
# Clone your space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-customer-support
cd ai-customer-support

# Copy your project files
cp -r /path/to/your/project/* .

# Add and commit
git add .
git commit -m "Initial deployment of AI Customer Support System"
git push
```

### 5. Configure Environment Variables

1. Go to your Space settings
2. Click on "Variables and secrets"
3. Add these environment variables:

**Required:**
```
USE_HUGGINGFACE=true
```

**Optional (for better functionality):**
```
OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=username/repository-name
```

### 6. Configure Secrets (if using APIs)

For sensitive information like API keys:
1. In Space settings, go to "Variables and secrets"
2. Click "Add secret"
3. Add your API keys as secrets

### 7. Monitor Deployment

1. Go to your Space's main page
2. Check the "Logs" tab for any errors
3. Wait for the build to complete (usually 5-10 minutes)
4. Your app will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/ai-customer-support`

## 🔧 Configuration for HuggingFace

### Memory Optimization

Since HuggingFace has memory limits, optimize your deployment:

1. **Use smaller embedding models:**
   ```python
   # In config.py
   HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Smaller model
   ```

2. **Limit document processing:**
   ```python
   # Process documents in smaller batches
   CHUNK_SIZE = 500  # Smaller chunks
   MAX_DOCUMENTS = 10  # Limit number of documents
   ```

3. **Use CPU-optimized models:**
   ```python
   # In config.py  
   USE_HUGGINGFACE = True
   ```

### File Size Limits

HuggingFace Spaces have file size limits:
- Individual files: 50MB max
- Total repository: 1GB max

If your PDFs are too large:
1. Split large PDFs into smaller files
2. Compress PDFs while maintaining quality
3. Use external storage for very large documents

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check requirements.txt for compatible versions
   - Ensure runtime.txt has supported Python version
   - Check logs for specific error messages

2. **Out of Memory**
   - Reduce CHUNK_SIZE in config.py
   - Use smaller embedding models
   - Process fewer documents at once

3. **App Won't Start**
   - Check app.py for syntax errors
   - Verify all imports are available
   - Check if data/documents/ directory exists
   - Review environment variables

4. **Documents Not Loading**
   - Ensure PDFs are in data/documents/
   - Check file permissions
   - Verify PDF files are not corrupted
   - Check logs for processing errors

5. **Vector Store Issues**
   - Clear vector_db directory and rebuild
   - Check ChromaDB compatibility
   - Ensure sufficient disk space

### Debug Mode

Enable debug logging by adding this to your Space secrets:
```
DEBUG_MODE=true
```

### Performance Optimization

For better performance on HuggingFace:

1. **Preprocess documents locally:**
   ```bash
   # Run locally first to create vector database
   python -c "
   from src.document_processor import DocumentProcessor
   from src.vector_store import VectorStore
   
   processor = DocumentProcessor()
   vector_store = VectorStore()
   
   docs = processor.load_documents('data/documents/')
   vector_store.add_documents(docs)
   print('Vector database created')
   "
   ```

2. **Include preprocessed vector database:**
   - Upload the generated `data/vector_db/` folder
   - This reduces startup time significantly

## 📊 Monitoring and Analytics

### Usage Tracking

Monitor your Space usage:
1. Check "Analytics" tab in your Space
2. Monitor API usage if using OpenAI
3. Track user interactions through logs

### Health Checks

Add health monitoring to your app:
```python
# In app.py, add a health check endpoint
def health_check():
    health = show_system_health()
    for component, status in health.items():
        st.write(f"{component}: {status}")
```

## 🔄 Updates and Maintenance

### Updating Your Deployment

1. **Make changes locally**
2. **Test thoroughly**
3. **Push to HuggingFace:**
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```

### Adding New Documents

1. Add PDFs to `data/documents/`
2. Push changes to trigger rebuild
3. Vector database will update automatically

### Monitoring Costs

If using paid APIs:
- Monitor OpenAI usage dashboard
- Set up usage alerts
- Consider rate limiting for high traffic

## 🏆 Best Practices

### Security
- Never commit API keys to git
- Use HuggingFace secrets for sensitive data
- Validate all user inputs
- Implement rate limiting

### Performance
- Cache frequently accessed data
- Optimize vector search parameters
- Use smaller models for faster responses
- Implement lazy loading for large documents

### User Experience
- Add loading indicators
- Provide clear error messages
- Include help documentation
- Test on different devices

## 📞 Support

If you encounter issues:

1. **Check HuggingFace Documentation:**
   - [Spaces Documentation](https://huggingface.co/docs/hub/spaces)
   - [Streamlit on Spaces](https://huggingface.co/docs/hub/spaces-sdks-streamlit)

2. **Community Support:**
   - HuggingFace Discord
   - HuggingFace Forums
   - Stack Overflow

3. **Logs and Debugging:**
   - Always check the "Logs" tab first
   - Enable debug mode for detailed output
   - Use st.write() for debugging in Streamlit

## 🎯 Post-Deployment Checklist

After successful deployment:

- [ ] Test all core functionality
- [ ] Verify document search works
- [ ] Test ticket creation
- [ ] Check mobile responsiveness
- [ ] Validate environment variables
- [ ] Monitor initial performance
- [ ] Share with stakeholders
- [ ] Document any custom configurations

## 📈 Scaling Considerations

For production use:

1. **Upgrade to paid HuggingFace plan** for better hardware
2. **Implement caching** for frequently asked questions
3. **Add user authentication** if needed
4. **Set up monitoring and alerting**
5. **Consider dedicated hosting** for high-volume usage

---

**Congratulations!** Your AI Customer Support System should now be live on HuggingFace Spaces. 

Access your deployed application at:
`https://huggingface.co/spaces/YOUR_USERNAME/ai-customer-support`