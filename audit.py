#!/usr/bin/env python3
"""
Mailchimp Account Audit Tool - Main Entry Point
Comprehensive audit of Mailchimp accounts with detailed reporting
"""

import sys
import argparse
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import modules
try:
    from config import config
    from mailchimp_client import MailchimpClient
    from audit_analyzer import AuditAnalyzer
    from report_generator import ReportGenerator
except ImportError as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)


def main(format_type='html', output_file=None):
    """Main entry point for the audit tool"""
    
    # Validate configuration
    if not config:
        logger.error("Configuration failed to initialize. Check your .env file.")
        return False
    
    try:
        logger.info("=" * 60)
        logger.info("🔍 Mailchimp Account Audit Tool")
        logger.info("=" * 60)
        
        # Initialize API client
        logger.info("🔌 Connecting to Mailchimp...")
        client = MailchimpClient(config)
        logger.info("✅ Connected successfully!")
        
        # Run audit
        logger.info("🚀 Starting comprehensive audit...")
        analyzer = AuditAnalyzer(client)
        audit_results = analyzer.run_full_audit()
        
        # Generate report
        logger.info(f"📄 Generating {format_type.upper()} report...")
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"mailchimp_audit_{timestamp}.{format_type if format_type != 'text' else 'txt'}"
        
        if format_type == 'html':
            ReportGenerator.generate_html(audit_results, output_file)
        elif format_type == 'json':
            ReportGenerator.generate_json(audit_results, output_file)
        elif format_type == 'text':
            ReportGenerator.generate_text(audit_results, output_file)
        else:
            logger.error(f"Unknown format: {format_type}")
            return False
        
        logger.info("=" * 60)
        logger.info(f"✅ Audit complete!")
        logger.info(f"📊 Health Score: {audit_results['health_score']}/100")
        logger.info(f"📁 Report saved to: {output_file}")
        logger.info("=" * 60)
        
        # Print summary
        print("\n")
        print("=" * 60)
        print("AUDIT SUMMARY")
        print("=" * 60)
        print(f"Health Score: {audit_results['health_score']}/100")
        print(f"Lists: {audit_results['lists']['total_lists']}")
        print(f"Subscribers: {audit_results['lists']['total_subscribers']}")
        print(f"Campaigns: {audit_results['campaigns']['total_campaigns']}")
        print(f"Automations: {audit_results['automations']['total_automations']}")
        print(f"Recommendations: {len(audit_results['recommendations'])}")
        print("=" * 60)
        print(f"\nReport saved to: {output_file}\n")
        
        return True
        
    except ValueError as e:
        logger.error(f"❌ Configuration Error: {e}")
        logger.error("Please check your .env file and ensure MAILCHIMP_API_KEY is set.")
        return False
    except Exception as e:
        logger.error(f"❌ Audit failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Comprehensive Mailchimp Account Audit Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audit.py
  python audit.py --format html --output report.html
  python audit.py --format json --output report.json
  python audit.py --format text --output report.txt
        """
    )
    
    parser.add_argument(
        '--format',
        choices=['html', 'json', 'text'],
        default='html',
        help='Report format (default: html)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: auto-generated based on timestamp)'
    )
    
    parser.add_argument(
        '--api-key',
        help='Mailchimp API key (overrides .env file)'
    )
    
    args = parser.parse_args()
    
    # Override API key if provided
    if args.api_key:
        os.environ['MAILCHIMP_API_KEY'] = args.api_key
    
    # Run main function
    success = main(format_type=args.format, output_file=args.output)
    sys.exit(0 if success else 1)
