"""
Signature generation and verification utilities for mPAY ONE API
"""

import hashlib
import hmac
import json
import logging
from config import API_SECRET_KEY

logger = logging.getLogger(__name__)

def generate_signature(data):
    """
    Generate HMAC signature for API requests
    
    Args:
        data (dict): Request payload
        
    Returns:
        str: Signature string
    """
    # Sort keys alphabetically
    sorted_data = {k: data[k] for k in sorted(data.keys())}
    
    # Convert to JSON string
    json_str = json.dumps(sorted_data, separators=(',', ':'))
    
    # Create HMAC-SHA256 signature
    signature = hmac.new(
        API_SECRET_KEY.encode('utf-8'),
        json_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    logger.debug(f"Generated signature for data: {json_str}")
    
    return signature

def verify_signature(data, received_signature):
    """
    Verify HMAC signature from webhook
    
    Args:
        data (dict): Webhook payload
        received_signature (str): Signature from webhook
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    # Generate signature from received data
    calculated_signature = generate_signature(data)
    
    # Compare signatures
    is_valid = hmac.compare_digest(calculated_signature, received_signature)
    
    if not is_valid:
        logger.warning("Signature verification failed")
    else:
        logger.debug("Signature verification successful")
    
    return is_valid
