"""
Report Generator for Mailchimp Audit
Generates reports in multiple formats: HTML, JSON, and Text
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any
from jinja2 import Template

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate audit reports in multiple formats"""
    
    @staticmethod
    def generate_html(audit_data: Dict[str, Any], output_file: str) -> None:
        """Generate an HTML report"""
        logger.info(f"Generating HTML report: {output_file}")
        
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mailchimp Account Audit Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.9; }
        .content { padding: 40px; }
        .section { margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 40px; }
        .section:last-child { border-bottom: none; }
        .section-title { font-size: 1.8em; margin-bottom: 20px; color: #333; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; border-radius: 5px; }
        .metric-value { font-size: 2em; font-weight: bold; color: #667eea; margin-bottom: 5px; }
        .metric-label { font-size: 0.9em; color: #666; text-transform: uppercase; }
        .health-score { font-size: 3em; font-weight: bold; color: {{ 'green' if health_score >= 70 else 'orange' if health_score >= 50 else 'red' }}; }
        .recommendation { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .recommendation.critical { background: #f8d7da; border-left-color: #dc3545; }
        .recommendation.high { background: #fff3cd; border-left-color: #ffc107; }
        .recommendation.medium { background: #d1ecf1; border-left-color: #17a2b8; }
        .recommendation.low { background: #d4edda; border-left-color: #28a745; }
        .recommendation-priority { font-weight: bold; text-transform: uppercase; font-size: 0.8em; margin-bottom: 5px; }
        .recommendation-category { font-weight: bold; color: #333; }
        .list-item { background: #f8f9fa; padding: 15px; margin-bottom: 10px; border-radius: 5px; border-left: 4px solid #667eea; }
        .list-item-name { font-weight: bold; color: #333; margin-bottom: 5px; }
        .list-item-stat { font-size: 0.9em; color: #666; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th { background: #f8f9fa; padding: 12px; text-align: left; font-weight: bold; color: #333; border-bottom: 2px solid #667eea; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f8f9fa; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 0.9em; color: #666; }
        .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.8em; font-weight: bold; }
        .badge.success { background: #d4edda; color: #155724; }
        .badge.warning { background: #fff3cd; color: #856404; }
        .badge.danger { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Mailchimp Account Audit</h1>
            <p>Comprehensive Account Analysis Report</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Generated: {{ timestamp }}</p>
        </div>
        
        <div class="content">
            <!-- Executive Summary -->
            <div class="section">
                <h2 class="section-title">Executive Summary</h2>
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-label">Health Score</div>
                        <div class="health-score">{{ health_score }}/100</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ account.lists.total_lists }}</div>
                        <div class="metric-label">Mailing Lists</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ account.lists.total_subscribers|default(0) }}</div>
                        <div class="metric-label">Total Subscribers</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ account.campaigns.total_campaigns }}</div>
                        <div class="metric-label">Campaigns Sent</div>
                    </div>
                </div>
            </div>
            
            <!-- Account Details -->
            <div class="section">
                <h2 class="section-title">Account Details</h2>
                <div class="list-item">
                    <div class="list-item-name">Account: {{ account_name }}</div>
                    <div class="list-item-stat">Email: {{ email }}</div>
                    <div class="list-item-stat">Plan: {{ plan_type }}</div>
                    <div class="list-item-stat">Timezone: {{ timezone }}</div>
                </div>
            </div>
            
            <!-- Lists Overview -->
            {% if lists.total_lists > 0 %}
            <div class="section">
                <h2 class="section-title">📋 Mailing Lists ({{ lists.total_lists }})</h2>
                {% for list in lists.lists %}
                <div class="list-item">
                    <div class="list-item-name">{{ list.name }}</div>
                    <div class="list-item-stat">Subscribers: <strong>{{ list.subscriber_count }}</strong></div>
                    <div class="list-item-stat">Avg Open Rate: <strong>{{ (list.open_rate * 100)|round(2) }}%</strong></div>
                    <div class="list-item-stat">Avg Click Rate: <strong>{{ (list.click_rate * 100)|round(2) }}%</strong></div>
                    <div class="list-item-stat">List Rating: <strong>{{ list.list_rating }}/5</strong></div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Campaign Performance -->
            {% if campaigns.total_campaigns > 0 %}
            <div class="section">
                <h2 class="section-title">📧 Campaign Performance</h2>
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-value">{{ campaigns.total_campaigns }}</div>
                        <div class="metric-label">Total Campaigns</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ (campaigns.avg_open_rate * 100)|round(2) }}%</div>
                        <div class="metric-label">Avg Open Rate</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ (campaigns.avg_click_rate * 100)|round(2) }}%</div>
                        <div class="metric-label">Avg Click Rate</div>
                    </div>
                </div>
            </div>
            {% endif %}
            
            <!-- Automations -->
            {% if automations.total_automations > 0 %}
            <div class="section">
                <h2 class="section-title">⚙️ Automations ({{ automations.total_automations }})</h2>
                <div class="metric-card">
                    <div class="metric-value">{{ automations.active_automations }}</div>
                    <div class="metric-label">Active Automations</div>
                </div>
            </div>
            {% endif %}
            
            <!-- Integrations -->
            {% if integrations.total_integrations > 0 %}
            <div class="section">
                <h2 class="section-title">🔗 Integrations ({{ integrations.total_integrations }})</h2>
                {% for integration in integrations.integrations %}
                <div class="list-item">
                    <div class="list-item-name">{{ integration.name }}</div>
                    <div class="list-item-stat">Status: {% if integration.authenticated %}<span class="badge success">Connected</span>{% else %}<span class="badge danger">Not Connected</span>{% endif %}</div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Recommendations -->
            {% if recommendations %}
            <div class="section">
                <h2 class="section-title">💡 Recommendations</h2>
                {% for rec in recommendations %}
                <div class="recommendation {{ rec.priority.lower() }}">
                    <div class="recommendation-priority">{{ rec.priority }} Priority</div>
                    <div class="recommendation-category">{{ rec.category }}</div>
                    <div>{{ rec.message }}</div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Mailchimp Account Audit Tool | Generated: {{ timestamp }}</p>
            <p>This report provides insights into your Mailchimp account health and recommendations for improvement.</p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            timestamp=audit_data['timestamp'],
            health_score=audit_data['health_score'],
            account_name=audit_data['account'].get('account_name', 'N/A'),
            email=audit_data['account'].get('email', 'N/A'),
            plan_type=audit_data['account'].get('plan_type', 'N/A'),
            timezone=audit_data['account'].get('timezone', 'N/A'),
            lists=audit_data['lists'],
            campaigns=audit_data['campaigns'],
            automations=audit_data['automations'],
            integrations=audit_data['integrations'],
            recommendations=audit_data['recommendations'],
        )
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved to {output_file}")
    
    @staticmethod
    def generate_json(audit_data: Dict[str, Any], output_file: str) -> None:
        """Generate a JSON report"""
        logger.info(f"Generating JSON report: {output_file}")
        
        with open(output_file, 'w') as f:
            json.dump(audit_data, f, indent=2)
        
        logger.info(f"JSON report saved to {output_file}")
    
    @staticmethod
    def generate_text(audit_data: Dict[str, Any], output_file: str) -> None:
        """Generate a text report"""
        logger.info(f"Generating text report: {output_file}")
        
        report = []
        report.append("=" * 80)
        report.append("MAILCHIMP ACCOUNT AUDIT REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {audit_data['timestamp']}\n")
        
        # Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(f"Health Score: {audit_data['health_score']}/100")
        report.append(f"Mailing Lists: {audit_data['lists']['total_lists']}")
        report.append(f"Total Subscribers: {audit_data['lists']['total_subscribers']}")
        report.append(f"Campaigns Sent: {audit_data['campaigns']['total_campaigns']}")
        report.append(f"Active Automations: {audit_data['automations']['active_automations']}")
        report.append("")
        
        # Account Info
        report.append("ACCOUNT INFORMATION")
        report.append("-" * 80)
        report.append(f"Account: {audit_data['account'].get('account_name', 'N/A')}")
        report.append(f"Email: {audit_data['account'].get('email', 'N/A')}")
        report.append(f"Plan: {audit_data['account'].get('plan_type', 'N/A')}")
        report.append("")
        
        # Recommendations
        if audit_data['recommendations']:
            report.append("RECOMMENDATIONS")
            report.append("-" * 80)
            for rec in audit_data['recommendations']:
                report.append(f"[{rec['priority'].upper()}] {rec['category']}: {rec['message']}")
            report.append("")
        
        report.append("=" * 80)
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(report))
        
        logger.info(f"Text report saved to {output_file}")
