"""
Configuration Management
Handles environment variables and configuration
"""

import os
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration management"""
    
    @staticmethod
    def get_config() -> Dict[str, str]:
        """Get configuration from environment"""
        api_key = os.getenv('MAILCHIMP_API_KEY')
        
        if not api_key:
            raise ValueError(
                "MAILCHIMP_API_KEY environment variable is not set. "
                "Please set it in your .env file or as an environment variable."
            )
        
        return {
            'api_key': api_key,
            'base_url': os.getenv('MAILCHIMP_BASE_URL', 'https://api.mailchimp.com'),
            'api_version': os.getenv('MAILCHIMP_API_VERSION', '3.0'),
        }


# Initialize global config
try:
    config = Config.get_config()
    logger.info("✅ Configuration loaded successfully")
except ValueError as e:
    logger.warning(f"⚠️ Configuration warning: {e}")
    config = None
