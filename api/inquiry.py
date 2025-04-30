import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, PAYMENT_INQUIRY_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class PaymentInquiry(Resource):
    """Handle Payment Inquiry API"""
    
    def post(self):
        """
        Inquire about a payment status
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123"
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # In a development environment, we'll simulate a successful response
            # In a production environment, we would make the actual API call
            
            # Make request to mPAY ONE API
            # endpoint = f"{MPAY_ONE_BASE_URL}{PAYMENT_INQUIRY_ENDPOINT}"
            # response = make_request('POST', endpoint, payload)
            
            # Simulated successful response
            success_response = {
                "status": "SUCCESS",
                "message": "Payment inquiry successful",
                "order_id": payload['order_id'],
                "amount": 529.73,
                "currency": "THB",
                "payment_method": "Credit Card",
                "payment_channel": "VISA",
                "paid_agent": "BANK",
                "paid_channel": "CC",
                "transaction_time": "2025-03-10T15:30:25+07:00"
            }
            
            return success_response, 200
                
        except Exception as e:
            logger.exception("Error processing payment inquiry")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
