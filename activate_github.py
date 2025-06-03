#!/usr/bin/env python3
"""
Script to activate GitHub Issues integration
"""

import os

def setup_github_integration():
    """Setup GitHub Issues for ticket management"""
    
    print("🔧 Setting up GitHub Issues integration...")
    
    # 1. Create a GitHub repository for tickets
    print("\n📋 Step 1: Create GitHub Repository")
    print("1. Go to https://github.com/new")
    print("2. Repository name: 'customer-support-tickets'")
    print("3. Make it public or private")
    print("4. Create repository")
    
    # 2. Generate GitHub token
    print("\n🔑 Step 2: Generate GitHub Token")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Select scopes: 'repo' (for private repos) or 'public_repo'")
    print("4. Copy the generated token")
    
    # 3. Update .env file
    print("\n📝 Step 3: Update .env file")
    env_content = """# GitHub Integration for Tickets
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=your-username/customer-support-tickets

# Other settings
USE_HUGGINGFACE=true
COMPANY_NAME=TechCorp Solutions
COMPANY_EMAIL=support@techcorp.com
COMPANY_PHONE=+1-800-TECH-HELP
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file template")
    print("📝 Please edit .env with your actual GitHub token and repo")
    
    # 4. Test integration
    print("\n🧪 Step 4: Test Integration")
    print("After updating .env, restart the app and create a test ticket")
    print("Check your GitHub repository for the new issue")

if __name__ == "__main__":
    setup_github_integration()