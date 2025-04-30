import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, INSTALLMENT_PLAN_INQUIRY_ENDPOINT, 
    INSTALLMENT_PAYMENT_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class InstallmentPayment(Resource):
    """Handle Installment Payment API"""
    
    def post(self):
        """
        Create an installment payment
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,
            "currency": "THB",
            "description": "Payment for order ORDER123",
            "customer_email": "customer@example.com",
            "customer_name": "John Doe",
            "customer_phone": "0812345678",
            "language": "en",
            "redirect_url": "https://merchant.com/redirect",
            "backend_url": "https://merchant.com/webhook",
            "installment_plan": "3",
            "installment_bank": "KTC",
            "settlement": true
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'amount', 'currency', 
                              'redirect_url', 'installment_plan', 'installment_bank']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # In a development environment, we'll simulate a successful response
            # In a production environment, we would make the actual API call
            
            # Make request to mPAY ONE API
            # endpoint = f"{MPAY_ONE_BASE_URL}{INSTALLMENT_PAYMENT_ENDPOINT}"
            # response = make_request('POST', endpoint, payload)
            
            # Simulated successful response
            success_response = {
                "status": "SUCCESS",
                "message": "Installment payment order created successfully",
                "redirect_url": f"/payment-success?order_id={payload['order_id']}&payment_method=Installment Plan",
                "order_id": payload['order_id'],
                "amount": payload['amount'],
                "currency": payload['currency'],
                "installment_plan": payload['installment_plan'],
                "installment_bank": payload['installment_bank']
            }
            
            return success_response, 200
                
        except Exception as e:
            logger.exception("Error processing installment payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
