#!/usr/bin/env python3
"""
Simplified setup script that avoids ChromaDB import issues
"""

import os
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/documents",
        "data/vector_db", 
        "data/tickets",
        "data/logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists() and env_example_path.exists():
        import shutil
        shutil.copy(env_example_path, env_path)
        print("✅ Created .env file from example")
        print("📝 Please edit .env file with your API keys")
    else:
        print("⏭️  .env file already exists or .env.example not found")

def create_sample_documents():
    """Create sample text documents"""
    print("📝 Creating sample documents...")
    
    # Create a comprehensive FAQ document
    faq_content = """# TechCorp Solutions - Frequently Asked Questions

## Account Management

### Q: How do I reset my password?
A: To reset your password:
1. Go to the login page at https://portal.techcorp.com
2. Click "Forgot Password" link
3. Enter your email address
4. Check your email for reset instructions
5. Follow the link in the email to create a new password

### Q: How do I update my account information?
A: To update your account:
1. Log into your account dashboard
2. Navigate to "Account Settings"
3. Update your information
4. Click "Save Changes"
5. You'll receive a confirmation email

### Q: How can I change my email address?
A: To change your email:
1. Contact our support team at support@techcorp.com
2. Provide your current email and desired new email
3. We'll send verification to both addresses
4. Follow the verification process

## Technical Support

### Q: What are your business hours?
A: Our support team is available:
- Monday-Friday: 9 AM to 6 PM EST
- Emergency support: 24/7 for critical issues
- Email support: Always available with 24-hour response

### Q: How can I contact technical support?
A: You can reach technical support:
- Email: support@techcorp.com
- Phone: 1-800-TECH-HELP
- Live chat: Available on our website
- Support portal: https://support.techcorp.com

### Q: What information should I include in a support ticket?
A: Please include:
- Your account username or email
- Detailed description of the issue
- Screenshots if applicable
- Steps you've already tried
- Your operating system and browser version

## Billing and Subscriptions

### Q: What is your refund policy?
A: We offer:
- Full refunds within 30 days of purchase
- Pro-rated refunds for annual subscriptions
- No questions asked for first-time customers
- Contact billing@techcorp.com for refund requests

### Q: How do I upgrade my subscription?
A: To upgrade:
1. Log into your account
2. Go to "Billing" section
3. Select "Upgrade Plan"
4. Choose your new plan
5. Payment will be pro-rated automatically

### Q: When will I be charged?
A: Billing cycles:
- Monthly plans: Charged on the same date each month
- Annual plans: Charged annually on signup date
- Upgrades: Pro-rated immediately
- Downgrades: Applied at next billing cycle

## Product Features

### Q: What platforms do you support?
A: We support:
- Windows 10 and 11
- macOS 10.15 and later
- Linux (Ubuntu, CentOS, Debian)
- iOS 13 and later
- Android 8.0 and later

### Q: Is there a mobile app?
A: Yes! Our mobile apps are available:
- iOS App Store: "TechCorp Mobile"
- Google Play Store: "TechCorp Mobile"
- Features include full account access and notifications

### Q: Do you offer API access?
A: API access is available:
- Free tier: 1,000 requests/month
- Pro tier: 10,000 requests/month
- Enterprise: Unlimited requests
- Documentation: https://api.techcorp.com/docs

## Security and Privacy

### Q: How do you protect my data?
A: We use:
- 256-bit SSL encryption
- SOC 2 Type II compliance
- Regular security audits
- GDPR compliance
- Data centers in US and EU

### Q: Can I export my data?
A: Yes, you can:
- Export all data in JSON or CSV format
- Request data deletion (GDPR right to be forgotten)
- Download via account settings
- Contact us for large data exports

Contact us at support@techcorp.com for any questions not covered here.
"""
    
    # Create product manual content
    manual_content = """# TechCorp Solutions - Product Manual

## Table of Contents
1. Getting Started
2. Installation Guide
3. Configuration
4. Features Overview
5. Troubleshooting
6. Advanced Settings

## 1. Getting Started

Welcome to TechCorp Solutions! This manual will guide you through setup and usage.

### System Requirements
- Operating System: Windows 10+, macOS 10.15+, or Linux
- RAM: Minimum 4GB, Recommended 8GB
- Storage: 2GB free space
- Internet: Broadband connection required

### Quick Start
1. Download the installer from https://download.techcorp.com
2. Run the installer as administrator
3. Follow the setup wizard
4. Enter your license key
5. Complete initial configuration

## 2. Installation Guide

### Windows Installation
1. Download TechCorp-Setup.exe
2. Right-click and "Run as administrator"
3. Accept the license agreement
4. Choose installation directory
5. Select components to install
6. Wait for installation to complete
7. Launch the application

### macOS Installation
1. Download TechCorp.dmg
2. Open the DMG file
3. Drag TechCorp to Applications folder
4. Open Applications and launch TechCorp
5. Allow security permissions if prompted
6. Enter your license key

### Linux Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install techcorp

# CentOS/RHEL
sudo yum install techcorp

# From source
wget https://download.techcorp.com/linux/techcorp.tar.gz
tar -xzf techcorp.tar.gz
cd techcorp
sudo ./install.sh
```

## 3. Configuration

### Initial Setup
1. Launch TechCorp
2. Click "First Time Setup"
3. Enter license information
4. Configure user preferences
5. Set up integrations
6. Test connectivity

### License Configuration
- Business licenses support up to 100 users
- Enterprise licenses are unlimited
- Educational discounts available
- Contact sales@techcorp.com for pricing

### Network Configuration
- Port 443 must be open for HTTPS
- Port 22 for SSH connections
- Firewall exceptions may be required
- VPN compatibility included

## 4. Features Overview

### Dashboard
The main dashboard provides:
- Real-time system status
- Performance metrics
- Recent activity logs
- Quick action buttons
- Customizable widgets

### User Management
- Create and manage user accounts
- Set role-based permissions
- Integration with Active Directory
- Single sign-on (SSO) support
- Multi-factor authentication

### Reporting
- Generate custom reports
- Schedule automated reports
- Export to PDF, Excel, CSV
- Real-time analytics
- Historical data analysis

### Integration Options
- REST API for custom integrations
- Webhook support
- Third-party connectors available
- Custom plugin development
- Enterprise integration services

## 5. Troubleshooting

### Common Issues

#### Installation Problems
Problem: "Installation failed with error 1603"
Solution:
1. Run installer as administrator
2. Disable antivirus temporarily
3. Clear temp files
4. Restart and try again

#### Connection Issues
Problem: "Cannot connect to server"
Solution:
1. Check internet connection
2. Verify firewall settings
3. Test with different network
4. Contact support if persistent

#### Performance Issues
Problem: "Application running slowly"
Solution:
1. Check system resources
2. Close unnecessary programs
3. Increase available RAM
4. Contact support for optimization

#### License Issues
Problem: "License key not accepted"
Solution:
1. Verify key is entered correctly
2. Check license expiration date
3. Ensure proper license type
4. Contact licensing@techcorp.com

### Log Files
Logs are located at:
- Windows: C:\\ProgramData\\TechCorp\\logs\\
- macOS: ~/Library/Logs/TechCorp/
- Linux: /var/log/techcorp/

### Support Resources
- Knowledge base: https://kb.techcorp.com
- Video tutorials: https://learn.techcorp.com
- Community forum: https://community.techcorp.com
- Email support: support@techcorp.com

## 6. Advanced Settings

### Performance Tuning
- Adjust memory allocation
- Configure caching settings
- Optimize database connections
- Set up load balancing

### Security Configuration
- Configure SSL certificates
- Set up encryption keys
- Configure audit logging
- Implement access controls

### Backup and Recovery
- Automated backup schedules
- Disaster recovery procedures
- Data retention policies
- Recovery testing protocols

For technical support, contact us at support@techcorp.com or call 1-800-TECH-HELP.

Version 2.1.0 - Last updated: January 2025
"""
    
    # Save FAQ document
    faq_path = Path("data/documents/FAQ_TechCorp.txt")
    with open(faq_path, 'w', encoding='utf-8') as f:
        f.write(faq_content)
    print("✅ Created FAQ document")
    
    # Save manual document
    manual_path = Path("data/documents/Product_Manual_TechCorp.txt")
    with open(manual_path, 'w', encoding='utf-8') as f:
        f.write(manual_content)
    print("✅ Created Product Manual")
    
    # Create a policies document
    policies_content = """# TechCorp Solutions - Company Policies

## Privacy Policy

Last updated: January 2025

### Information We Collect
- Account information (name, email, company)
- Usage data and analytics
- Support communications
- Payment information (processed securely)

### How We Use Information
- Provide and improve our services
- Communicate with customers
- Process payments
- Comply with legal requirements

### Data Protection
- Encryption in transit and at rest
- Regular security audits
- Limited access controls
- GDPR and CCPA compliance

## Terms of Service

### Acceptable Use
- Use services for legitimate business purposes
- Do not violate laws or regulations
- Respect intellectual property rights
- No unauthorized access attempts

### Service Availability
- 99.9% uptime SLA
- Scheduled maintenance windows
- Emergency maintenance as needed
- Service credits for downtime

### Limitation of Liability
- Services provided "as is"
- No warranties beyond legal requirements
- Liability limited to fees paid
- Indemnification clauses apply

## Return and Refund Policy

### Eligibility
- 30-day money-back guarantee
- Full refund for defective products
- Pro-rated refunds for subscriptions
- No refund for misuse or policy violations

### Process
1. Contact support@techcorp.com
2. Provide order number and reason
3. Return products if applicable
4. Refund processed within 5-7 business days

### Exceptions
- Custom development work
- Third-party licenses
- Services already delivered
- Violation of terms of service

For questions about these policies, contact legal@techcorp.com
"""
    
    policies_path = Path("data/documents/Company_Policies.txt")
    with open(policies_path, 'w', encoding='utf-8') as f:
        f.write(policies_content)
    print("✅ Created Company Policies document")

def display_next_steps():
    """Display instructions for next steps"""
    print("\n" + "="*50)
    print("🚀 SETUP COMPLETE!")
    print("="*50)
    print("\nNext steps:")
    print("1. ✅ Directory structure created")
    print("2. ✅ Sample documents added")
    print("3. 📝 Add your own PDF documents to data/documents/")
    print("4. 🔧 Edit .env file with API keys (optional)")
    print("5. 🚀 Run: streamlit run app.py")
    print("\n📄 Sample documents created:")
    print("- FAQ_TechCorp.txt")
    print("- Product_Manual_TechCorp.txt") 
    print("- Company_Policies.txt")
    print("\n📋 Requirements checklist:")
    print("- ✅ 3+ documents (text format)")
    print("- 📋 Add 2+ PDF documents")
    print("- 📋 Add 1 PDF with 400+ pages")
    print("\n🌐 For HuggingFace deployment:")
    print("- Ensure all files are in the project")
    print("- Set USE_HUGGINGFACE=true in .env")
    print("- The app will automatically use FAISS if ChromaDB fails")

def main():
    """Main setup function"""
    print("🔧 Simple Setup for AI Customer Support")
    print("-" * 50)
    
    # Create directory structure
    create_directories()
    
    # Create sample documents
    create_sample_documents()
    
    # Create .env file
    create_env_file()
    
    # Display next steps
    display_next_steps()

if __name__ == "__main__":
    main()