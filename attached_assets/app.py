import os
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_restful import Api, Resource
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mpay_one_secret_key")

# Apply proxy fix for proper URL generation
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize REST API
api = Api(app)

# Import routes after app initialization to avoid circular imports
from api.credit_card import CreditCardPayment, CardTokenization, CardTokenInquiry, TerminateCardToken, CaptureAuthorized, CancelAuthorized
from api.credit_card import CreditCardPaymentSeamless, RegisterCard, PaymentConfirm
from api.qr_payment import GenerateQR
from api.rabbit_line_pay import RabbitLinePayPayment, PreApprovedPayment, TerminateRLPToken
from api.installment import InstallmentPlanInquiry, InstallmentPayment
from api.internet_banking import InternetBankingPayment, RequestToPay
from api.inquiry import PaymentInquiry
from api.void_refund import VoidRefund
from api.webhook import WebhookHandler
from utils.customer_data import get_customer_data
from config import MPAY_MERCHANT_ID

# Customer Data API class
class CustomerDataAPI(Resource):
    def get(self):
        """API endpoint to fetch customer data from Raja Ferry Port"""
        try:
            booking_id = request.args.get('booking_id')
            
            if not booking_id:
                return jsonify({
                    'status': 'error',
                    'message': 'Missing booking_id parameter'
                }), 400
            
            customer_data = get_customer_data(booking_id)
            
            if not customer_data:
                return jsonify({
                    'status': 'error',
                    'message': 'Could not retrieve customer data'
                }), 404
            
            return jsonify({
                'status': 'success',
                'customer_data': customer_data['customer_data'],
                'booking_details': customer_data['booking_details']
            })
            
        except Exception as e:
            logger.exception(f"Error retrieving customer data: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f"Error retrieving customer data: {str(e)}"
            }), 500

# Register API endpoints
api.add_resource(CustomerDataAPI, '/api/raja-ferry/customer-data')

# Credit Card Payment
api.add_resource(CreditCardPayment, '/api/credit-card/payment')
api.add_resource(CardTokenization, '/api/credit-card/payment-token')
api.add_resource(CardTokenInquiry, '/api/credit-card/token-inquiry')
api.add_resource(TerminateCardToken, '/api/credit-card/terminate-token')
api.add_resource(CaptureAuthorized, '/api/credit-card/capture')
api.add_resource(CancelAuthorized, '/api/credit-card/cancel')

# Credit Card Payment (Seamless)
api.add_resource(CreditCardPaymentSeamless, '/api/credit-card/seamless/payment')
api.add_resource(RegisterCard, '/api/credit-card/seamless/register')
api.add_resource(PaymentConfirm, '/api/credit-card/seamless/confirm')

# Installment Payment
api.add_resource(InstallmentPlanInquiry, '/api/installment/inquiry-plan')
api.add_resource(InstallmentPayment, '/api/installment/payment')

# Rabbit Line Pay
api.add_resource(RabbitLinePayPayment, '/api/rabbit-line-pay/payment')
api.add_resource(PreApprovedPayment, '/api/rabbit-line-pay/preapproved-payment')
api.add_resource(TerminateRLPToken, '/api/rabbit-line-pay/terminate-token')

# QR Payment
api.add_resource(GenerateQR, '/api/qr/generate')

# Internet/Mobile Banking
api.add_resource(InternetBankingPayment, '/api/banking/payment')
api.add_resource(RequestToPay, '/api/request-to-pay')

# Inquiry
api.add_resource(PaymentInquiry, '/api/payment/inquiry')

# Void & Refund
api.add_resource(VoidRefund, '/api/payment/void-refund')

# Webhook
api.add_resource(WebhookHandler, '/api/webhook')

# Web routes
@app.route('/')
def index():
    """Redirect to payment form"""
    return redirect(url_for('payment_form'))

@app.route('/payment-form')
def payment_form():
    # Get redirect URL base from config
    redirect_url_base = request.url_root.rstrip('/')
    
    return render_template(
        'payment_form.html',
        merchant_id=MPAY_MERCHANT_ID,
        redirect_url=f"{redirect_url_base}/payment/return"
    )

@app.route('/payment/return')
def payment_return():
    """Handler for payment gateway redirect back to our site"""
    # Get parameters from the request
    status = request.args.get('status')
    order_id = request.args.get('order_id')
    
    if status == 'SUCCESS' or not status:  # For demo, allow success without status
        # Show success page
        return redirect(url_for('payment_success', order_id=order_id or 'DEMO123', payment_method='Rabbit Line Pay'))
    elif status == 'PENDING':
        # Payment is still processing
        message = "Your payment is being processed. Please wait."
        message_type = "info"
    else:
        # Payment failed
        message = "Payment failed. Please try again."
        message_type = "danger"
    
    # For non-success cases, return to payment form
    return redirect(url_for('payment_form'))

@app.route('/payment-success')
def payment_success():
    """Payment success page"""
    order_id = request.args.get('order_id')
    payment_method = request.args.get('payment_method', 'Rabbit Line Pay')
    
    # In a real implementation, you would fetch order details from database
    # Here we're using demo data for display purposes
    order_details = {
        'route': 'Premium Seat - Route A7',
        'date_time': 'March 15, 2025 - 08:30',
        'fare': 750.00,
        'service_fee': 30.00,
        'tax': 52.50,
        'total': 832.50
    }
    
    payment_details = {
        'transaction_id': 'TXN-' + ''.join(order_id.split('-')),
        'payment_method': payment_method,
        'date': 'Apr 29, 2025, 14:39'
    }
    
    return render_template(
        'payment_success.html', 
        order_details=order_details,
        payment_details=payment_details
    )

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('payment_form')), 302

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)