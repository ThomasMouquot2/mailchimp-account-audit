"""
Mailchimp API Client
Handles all API calls to Mailchimp v3 API
"""

import logging
import requests
from typing import Dict, List, Any
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class MailchimpClient:
    """Mailchimp API v3 Client"""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the API client"""
        self.api_key = config['api_key']
        self.base_url = config['base_url']
        self.api_version = config['api_version']
        
        # Extract server from API key (e.g., 'us1' from 'xxx-us1')
        self.server = self.api_key.split('-')[-1]
        self.api_url = f"{self.base_url}/{self.api_version}"
        
        # Set up authentication
        self.auth = HTTPBasicAuth('apikey', self.api_key)
        self.headers = {
            'Content-Type': 'application/json',
        }
        
        logger.info(f"MailchimpClient initialized for server: {self.server}")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make an API request"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            response = requests.request(
                method,
                url,
                auth=self.auth,
                headers=self.headers,
                timeout=30,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ValueError(f"Mailchimp API error: {e}")
    
    def get_account(self) -> Dict[str, Any]:
        """Get account information"""
        logger.info("Fetching account information...")
        return self._make_request('GET', '/').get('account', {})
    
    def get_lists(self, count: int = 100) -> List[Dict[str, Any]]:
        """Get all mailing lists"""
        logger.info(f"Fetching lists (limit: {count})...")
        response = self._make_request('GET', '/lists', params={'count': count})
        return response.get('lists', [])
    
    def get_list_details(self, list_id: str) -> Dict[str, Any]:
        """Get details for a specific list"""
        logger.info(f"Fetching list details: {list_id}")
        return self._make_request('GET', f'/lists/{list_id}')
    
    def get_list_members(self, list_id: str, count: int = 100) -> List[Dict[str, Any]]:
        """Get members of a list"""
        logger.info(f"Fetching list members: {list_id}")
        response = self._make_request('GET', f'/lists/{list_id}/members', params={'count': count})
        return response.get('members', [])
    
    def get_campaigns(self, count: int = 50) -> List[Dict[str, Any]]:
        """Get all campaigns"""
        logger.info(f"Fetching campaigns (limit: {count})...")
        response = self._make_request('GET', '/campaigns', params={'count': count})
        return response.get('campaigns', [])
    
    def get_campaign_details(self, campaign_id: str) -> Dict[str, Any]:
        """Get details for a specific campaign"""
        logger.info(f"Fetching campaign details: {campaign_id}")
        return self._make_request('GET', f'/campaigns/{campaign_id}')
    
    def get_campaign_report(self, campaign_id: str) -> Dict[str, Any]:
        """Get report for a campaign"""
        logger.info(f"Fetching campaign report: {campaign_id}")
        return self._make_request('GET', f'/reports/{campaign_id}')
    
    def get_automations(self, count: int = 50) -> List[Dict[str, Any]]:
        """Get all automations"""
        logger.info(f"Fetching automations (limit: {count})...")
        response = self._make_request('GET', '/automations', params={'count': count})
        return response.get('automations', [])
    
    def get_automation_details(self, workflow_id: str) -> Dict[str, Any]:
        """Get details for a specific automation"""
        logger.info(f"Fetching automation details: {workflow_id}")
        return self._make_request('GET', f'/automations/{workflow_id}')
    
    def get_integrations(self, count: int = 50) -> List[Dict[str, Any]]:
        """Get all integrations"""
        logger.info(f"Fetching integrations (limit: {count})...")
        response = self._make_request('GET', '/integrations', params={'count': count})
        return response.get('integrations', [])
    
    def get_integration_details(self, integration_id: str) -> Dict[str, Any]:
        """Get details for a specific integration"""
        logger.info(f"Fetching integration details: {integration_id}")
        return self._make_request('GET', f'/integrations/{integration_id}')
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            logger.info("Testing Mailchimp API connection...")
            account = self.get_account()
            if 'account_name' in account or 'email' in account:
                logger.info("✅ API connection successful!")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ API connection failed: {e}")
            return False
