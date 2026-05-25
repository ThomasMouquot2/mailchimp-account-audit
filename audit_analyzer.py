"""
Audit Analysis Engine
Performs comprehensive analysis of Mailchimp account
"""

import logging
from datetime import datetime
from typing import Dict, Any, List
from mailchimp_client import MailchimpClient

logger = logging.getLogger(__name__)


class AuditAnalyzer:
    """Analyzes Mailchimp account data"""
    
    def __init__(self, client: MailchimpClient):
        self.client = client
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Run a complete audit of the account"""
        logger.info("Starting full account audit...")
        
        try:
            # Fetch all data
            account = self.client.get_account()
            lists = self.client.get_lists()
            campaigns = self.client.get_campaigns()
            automations = self.client.get_automations()
            integrations = self.client.get_integrations()
            
            # Analyze data
            lists_analysis = self._analyze_lists(lists)
            campaigns_analysis = self._analyze_campaigns(campaigns)
            automations_analysis = self._analyze_automations(automations)
            integrations_analysis = self._analyze_integrations(integrations)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                account, lists_analysis, campaigns_analysis, 
                automations_analysis, integrations_analysis
            )
            
            # Calculate health score
            health_score = self._calculate_health_score(
                lists_analysis, campaigns_analysis, 
                automations_analysis, recommendations
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'health_score': health_score,
                'account': self._extract_account_info(account),
                'lists': lists_analysis,
                'campaigns': campaigns_analysis,
                'automations': automations_analysis,
                'integrations': integrations_analysis,
                'recommendations': recommendations,
            }
        except Exception as e:
            logger.error(f"Audit failed: {e}")
            raise
    
    def _extract_account_info(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant account information"""
        return {
            'account_name': account.get('account_name', 'N/A'),
            'email': account.get('email', 'N/A'),
            'plan_type': account.get('plan', {}).get('name', 'N/A'),
            'timezone': account.get('timezone', 'N/A'),
            'industry': account.get('industry', 'N/A'),
        }
    
    def _analyze_lists(self, lists: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze mailing lists"""
        logger.info(f"Analyzing {len(lists)} lists...")
        
        total_subscribers = sum(l.get('stats', {}).get('member_count', 0) for l in lists)
        
        list_details = []
        for lst in lists:
            stats = lst.get('stats', {})
            list_details.append({
                'id': lst.get('id'),
                'name': lst.get('name'),
                'subscriber_count': stats.get('member_count', 0),
                'open_rate': stats.get('open_rate', 0),
                'click_rate': stats.get('click_rate', 0),
                'list_rating': lst.get('list_rating', 0),
                'double_optin': lst.get('double_optin', False),
                'marketing_permissions': lst.get('marketing_permissions', False),
            })
        
        return {
            'total_lists': len(lists),
            'total_subscribers': total_subscribers,
            'lists': list_details,
            'avg_subscriber_count': total_subscribers / len(lists) if lists else 0,
        }
    
    def _analyze_campaigns(self, campaigns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze campaigns"""
        logger.info(f"Analyzing {len(campaigns)} campaigns...")
        
        open_rates = []
        click_rates = []
        
        for campaign in campaigns:
            report = campaign.get('report', {})
            if report.get('open_rate'):
                open_rates.append(report.get('open_rate', 0))
            if report.get('click_rate'):
                click_rates.append(report.get('click_rate', 0))
        
        return {
            'total_campaigns': len(campaigns),
            'avg_open_rate': sum(open_rates) / len(open_rates) if open_rates else 0,
            'avg_click_rate': sum(click_rates) / len(click_rates) if click_rates else 0,
            'campaigns': campaigns[:10],  # Keep last 10 for details
        }
    
    def _analyze_automations(self, automations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze automations"""
        logger.info(f"Analyzing {len(automations)} automations...")
        
        active_automations = sum(1 for a in automations if a.get('status') == 'sending')
        
        return {
            'total_automations': len(automations),
            'active_automations': active_automations,
            'automations': automations,
        }
    
    def _analyze_integrations(self, integrations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze integrations"""
        logger.info(f"Analyzing {len(integrations)} integrations...")
        
        return {
            'total_integrations': len(integrations),
            'integrations': integrations,
        }
    
    def _generate_recommendations(self, account, lists, campaigns, automations, integrations) -> List[Dict[str, str]]:
        """Generate audit recommendations"""
        logger.info("Generating recommendations...")
        
        recommendations = []
        
        # List recommendations
        if lists['total_lists'] == 0:
            recommendations.append({
                'priority': 'Critical',
                'category': 'Lists',
                'message': 'No mailing lists found. Create at least one list to start sending campaigns.'
            })
        
        if lists['total_subscribers'] == 0:
            recommendations.append({
                'priority': 'Critical',
                'category': 'Subscribers',
                'message': 'No subscribers found. Build your mailing list to enable email marketing.'
            })
        
        if campaigns['total_campaigns'] == 0:
            recommendations.append({
                'priority': 'High',
                'category': 'Campaigns',
                'message': 'No campaigns sent yet. Create and send your first campaign to engage subscribers.'
            })
        
        if campaigns['avg_open_rate'] < 0.15 and campaigns['total_campaigns'] > 5:
            recommendations.append({
                'priority': 'High',
                'category': 'Engagement',
                'message': f'Low average open rate ({campaigns["avg_open_rate"]*100:.1f}%). Test subject lines and send times for improvement.'
            })
        
        if automations['total_automations'] == 0:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Automations',
                'message': 'Set up automations like welcome series to nurture subscribers automatically.'
            })
        
        # Double opt-in check
        double_optin_count = sum(1 for lst in lists['lists'] if lst.get('double_optin'))
        if double_optin_count < len(lists['lists']):
            recommendations.append({
                'priority': 'Medium',
                'category': 'Compliance',
                'message': 'Consider enabling double opt-in for better list hygiene and compliance.'
            })
        
        # Integrations check
        if integrations['total_integrations'] == 0:
            recommendations.append({
                'priority': 'Low',
                'category': 'Integrations',
                'message': 'Connect your e-commerce or CRM platform to sync data automatically.'
            })
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def _calculate_health_score(self, lists, campaigns, automations, recommendations) -> int:
        """Calculate account health score (0-100)"""
        score = 50  # Base score
        
        # Lists: 20 points
        if lists['total_lists'] > 0:
            score += 10
        if lists['total_subscribers'] > 100:
            score += 10
        
        # Campaigns: 20 points
        if campaigns['total_campaigns'] > 0:
            score += 10
        if campaigns['avg_open_rate'] > 0.15:
            score += 10
        
        # Automations: 20 points
        if automations['total_automations'] > 0:
            score += 10
        if automations['active_automations'] > 0:
            score += 10
        
        # Reduce for issues: 20 points
        critical_issues = sum(1 for r in recommendations if r['priority'] == 'Critical')
        high_issues = sum(1 for r in recommendations if r['priority'] == 'High')
        
        score -= critical_issues * 5
        score -= high_issues * 2
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))
