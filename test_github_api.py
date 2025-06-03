#!/usr/bin/env python3
"""
Test GitHub API integration for ticket creation
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_github_connection():
    """Test GitHub API connection and permissions"""
    
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    
    print("🔍 Testing GitHub API Connection...")
    print(f"Repository: {GITHUB_REPO}")
    print(f"Token exists: {'Yes' if GITHUB_TOKEN else 'No'}")
    print(f"Token length: {len(GITHUB_TOKEN) if GITHUB_TOKEN else 0}")
    
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN not found in .env file")
        return False
    
    if not GITHUB_REPO:
        print("❌ GITHUB_REPO not found in .env file")
        return False
    
    # Test 1: Check token validity
    print("\n🧪 Test 1: Checking token validity...")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get("https://api.github.com/user", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Token valid! User: {user_data['login']}")
        else:
            print(f"❌ Token invalid. Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False
    
    # Test 2: Check repository access
    print(f"\n🧪 Test 2: Checking repository access...")
    repo_url = f"https://api.github.com/repos/{GITHUB_REPO}"
    
    try:
        response = requests.get(repo_url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ Repository accessible: {repo_data['full_name']}")
            print(f"Repository has issues: {repo_data.get('has_issues', False)}")
            
            # Check if issues are enabled
            if not repo_data.get('has_issues', False):
                print("⚠️ WARNING: Issues are disabled for this repository!")
                print("Enable issues in repository settings")
        else:
            print(f"❌ Cannot access repository. Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error accessing repository: {e}")
        return False
    
    # Test 3: Check permissions
    print(f"\n🧪 Test 3: Checking issue creation permissions...")
    
    # Try to list existing issues first
    issues_url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    
    try:
        response = requests.get(issues_url, headers=headers)
        print(f"List issues status: {response.status_code}")
        
        if response.status_code == 200:
            issues = response.json()
            print(f"✅ Can read issues. Found {len(issues)} existing issues")
        else:
            print(f"⚠️ Cannot read issues: {response.text}")
    except Exception as e:
        print(f"❌ Error reading issues: {e}")
    
    # Test 4: Try creating a test issue
    print(f"\n🧪 Test 4: Creating test issue...")
    
    test_issue = {
        "title": "[TEST] API Connection Test",
        "body": "This is a test issue created by the diagnostic script. You can safely close this.",
        "labels": ["test", "api-test"]
    }
    
    try:
        response = requests.post(issues_url, headers=headers, data=json.dumps(test_issue))
        print(f"Create issue status: {response.status_code}")
        
        if response.status_code == 201:
            issue_data = response.json()
            print(f"✅ Test issue created successfully!")
            print(f"Issue number: #{issue_data['number']}")
            print(f"Issue URL: {issue_data['html_url']}")
            return True
        else:
            print(f"❌ Cannot create issue. Response: {response.text}")
            
            # Try to parse error message
            try:
                error_data = response.json()
                if 'message' in error_data:
                    print(f"Error message: {error_data['message']}")
                if 'errors' in error_data:
                    for error in error_data['errors']:
                        print(f"Error detail: {error}")
            except:
                pass
                
            return False
    except Exception as e:
        print(f"❌ Error creating test issue: {e}")
        return False

def fix_common_issues():
    """Provide solutions for common issues"""
    print("\n🔧 Common Issues and Solutions:")
    print("\n1. **Token Permissions:**")
    print("   - Go to https://github.com/settings/tokens")
    print("   - Edit your token")
    print("   - Make sure 'repo' scope is checked")
    print("   - Regenerate token if needed")
    
    print("\n2. **Repository Issues Disabled:**")
    print("   - Go to your repository settings")
    print("   - Scroll to 'Features' section")
    print("   - Check ✅ 'Issues' checkbox")
    
    print("\n3. **Repository Access:**")
    print("   - Make sure repository name is correct: username/repo-name")
    print("   - Repository must exist and be accessible with your token")
    
    print("\n4. **Token Expiration:**")
    print("   - Check if your token hasn't expired")
    print("   - Create a new token if needed")

if __name__ == "__main__":
    print("🧪 GitHub API Diagnostic Tool")
    print("=" * 40)
    
    success = test_github_connection()
    
    if not success:
        fix_common_issues()
    else:
        print("\n🎉 All tests passed! GitHub integration should work.")