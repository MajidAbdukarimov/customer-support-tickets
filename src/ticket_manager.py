import requests
import json
from datetime import datetime
from typing import Dict, Any
from config import GITHUB_TOKEN, GITHUB_REPO

class TicketManager:
    def __init__(self):
        self.github_token = GITHUB_TOKEN
        self.github_repo = GITHUB_REPO
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}/issues"
    
    def create_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a support ticket"""
        
        # Try GitHub Issues first
        if self.github_token and self.github_repo:
            return self._create_github_issue(ticket_data)
        else:
            # Fallback to local storage for demo
            return self._create_local_ticket(ticket_data)
    
    def _create_github_issue(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create GitHub issue as support ticket"""
        try:
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            
            # Format issue body
            body = f"""**Customer Information:**
- Name: {ticket_data['name']}
- Email: {ticket_data['email']}
- Created: {ticket_data['created_at']}

**Description:**
{ticket_data['description']}
"""
            
            payload = {
                "title": f"[SUPPORT] {ticket_data['title']}",
                "body": body,
                "labels": ["support", "customer-request"]
            }
            
            response = requests.post(
                self.github_api_url,
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                return {
                    "success": True,
                    "ticket_id": f"#{issue_data['number']}",
                    "url": issue_data['html_url']
                }
            else:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create GitHub issue: {str(e)}"
            }
    
    def _create_local_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create local ticket for demo purposes"""
        try:
            import os
            
            # Create tickets directory if it doesn't exist
            tickets_dir = "data/tickets"
            os.makedirs(tickets_dir, exist_ok=True)
            
            # Generate ticket ID
            ticket_id = f"TICKET-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Save ticket to file
            ticket_file = os.path.join(tickets_dir, f"{ticket_id}.json")
            
            ticket_record = {
                "ticket_id": ticket_id,
                "status": "open",
                "priority": "normal",
                **ticket_data
            }
            
            with open(ticket_file, 'w') as f:
                json.dump(ticket_record, f, indent=2)
            
            return {
                "success": True,
                "ticket_id": ticket_id,
                "message": "Ticket created locally (demo mode)"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create local ticket: {str(e)}"
            }
    
    def get_ticket_status(self, ticket_id: str) -> Dict[str, Any]:
        """Get ticket status (for future implementation)"""
        return {
            "ticket_id": ticket_id,
            "status": "open",
            "message": "Ticket status check not implemented yet"
        }
    
    def list_recent_tickets(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent tickets (for admin interface)"""
        try:
            tickets_dir = "data/tickets"
            if not os.path.exists(tickets_dir):
                return []
            
            tickets = []
            ticket_files = sorted(
                [f for f in os.listdir(tickets_dir) if f.endswith('.json')],
                reverse=True
            )
            
            for ticket_file in ticket_files[:limit]:
                with open(os.path.join(tickets_dir, ticket_file), 'r') as f:
                    ticket_data = json.load(f)
                    tickets.append(ticket_data)
            
            return tickets
            
        except Exception as e:
            return []