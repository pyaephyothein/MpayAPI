import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, QR_GENERATE_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class GenerateQR(Resource):
    """Handle QR Payment Generation API"""
    
    def post(self):
        """
        Generate a QR code for payment
        
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
            "backend_url": "https://merchant.com/webhook",
            "reference1": "ref1",
            "reference2": "ref2",
            "reference3": "ref3",
            "settlement": true
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'amount', 'currency']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # In a development environment, we'll simulate a successful response
            # In a production environment, we would make the actual API call
            
            # Make request to mPAY ONE API
            # endpoint = f"{MPAY_ONE_BASE_URL}{QR_GENERATE_ENDPOINT}"
            # response = make_request('POST', endpoint, payload)
            
            # Simulated successful response with QR image (SVG)
            qr_svg = """
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <rect x="10" y="10" width="180" height="180" fill="none" stroke="#000" stroke-width="2" />
              <rect x="50" y="50" width="100" height="100" fill="none" stroke="#000" stroke-width="2" />
              <rect x="70" y="70" width="60" height="60" fill="#000" />
            </svg>
            """
            
            success_response = {
                "status": "SUCCESS",
                "message": "QR code generated successfully",
                "order_id": payload['order_id'],
                "amount": payload['amount'],
                "currency": payload['currency'],
                "qr_image": "data:image/svg+xml;base64," + qr_svg.encode('utf-8').hex(),
                "qr_code": "00020101021229370016A000000677010111011300669000000115802TH53037645406529.736304FDF0"
            }
            
            return success_response, 200
                
        except Exception as e:
            logger.exception("Error generating QR code")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
