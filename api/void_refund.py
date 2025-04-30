import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, VOID_REFUND_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class VoidRefund(Resource):
    """Handle Void & Refund API"""
    
    def post(self):
        """
        Void or refund a payment
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,  # For partial refund, not required for full void
            "description": "Refund for order ORDER123",
            "refund_type": "REFUND"  # or "VOID"
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'refund_type']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # If refund type is REFUND, amount is required
            if payload['refund_type'] == 'REFUND' and 'amount' not in payload:
                return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": "Amount is required for refund"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # In a development environment, we'll simulate a successful response
            # In a production environment, we would make the actual API call
            
            # Make request to mPAY ONE API
            # endpoint = f"{MPAY_ONE_BASE_URL}{VOID_REFUND_ENDPOINT}"
            # response = make_request('POST', endpoint, payload)
            
            # Simulated successful response
            success_response = {
                "status": "SUCCESS",
                "message": f"{payload['refund_type']} successful",
                "order_id": payload['order_id'],
                "refund_id": f"REF-{payload['order_id']}",
                "amount": payload.get('amount', 0.00),
                "currency": "THB",
                "refund_type": payload['refund_type']
            }
            
            return success_response, 200
                
        except Exception as e:
            logger.exception("Error processing void/refund")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
