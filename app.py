import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_restful import Api

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Set up API
api = Api(app)

# Import API resources
from api.credit_card import CreditCardPayment
from api.qr_payment import GenerateQR
from api.rabbit_line_pay import RabbitLinePayPayment
from api.installment import InstallmentPayment
from api.internet_banking import InternetBankingPayment
from api.inquiry import PaymentInquiry
from api.void_refund import VoidRefund
from api.webhook import WebhookHandler

# Register API endpoints
api.add_resource(CreditCardPayment, '/api/credit-card/payment')
api.add_resource(GenerateQR, '/api/qr/generate')
api.add_resource(RabbitLinePayPayment, '/api/rabbit-line-pay/payment')
api.add_resource(InstallmentPayment, '/api/installment/payment')
api.add_resource(InternetBankingPayment, '/api/banking/payment')
api.add_resource(PaymentInquiry, '/api/payment/inquiry')
api.add_resource(VoidRefund, '/api/payment/void-refund')
api.add_resource(WebhookHandler, '/api/webhook')

from config import DEFAULT_MERCHANT_ID
import uuid

# Main routes
@app.route('/')
@app.route('/payment')
def payment_form():
    """Render the payment form page"""
    # Sample order data (in a real app, this would come from Raja Ferry Port)
    order_data = {
        'id': 'ORD-2025001',
        'merchant_id': 'MERCH-12345',
        'route': 'Donsak - Samui',
        'date_time': 'March 15, 2025 - 10:00 AM',
        'fare': 450.00,
        'service_fee': 45.00,
        'tax': 34.73,
        'total': 529.73,
        'currency': 'THB',
        'customer_name': 'John Doe',
        'customer_email': 'john@example.com',
        'customer_phone': '0812345678',
        'passengers': 2
    }
    
    # Payment method options
    payment_methods = [
        {
            'id': 'credit_card',
            'name': 'Credit/Debit Card',
            'icon': 'credit-card',
            'icon_class': 'credit-card-icon'
        },
        {
            'id': 'qr_payment',
            'name': 'QR Payment',
            'icon': 'qrcode',
            'icon_class': 'qr-icon'
        },
        {
            'id': 'rabbit_line_pay',
            'name': 'Rabbit Line Pay',
            'icon': 'mobile-alt',
            'icon_class': 'line-pay-icon'
        },
        {
            'id': 'internet_banking',
            'name': 'Net Banking',
            'icon': 'university',
            'icon_class': 'banking-icon'
        }
    ]
    
    # Bank options for internet banking
    bank_options = [
        {'code': 'SCB', 'name': 'Siam Commercial Bank'},
        {'code': 'KTB', 'name': 'Krungthai Bank'},
        {'code': 'BBL', 'name': 'Bangkok Bank'},
        {'code': 'BAY', 'name': 'Krungsri Bank'},
        {'code': 'KBANK', 'name': 'Kasikorn Bank'}
    ]
    
    # Return the payment form template with order data
    return render_template(
        'payment_form.html',
        order=order_data,
        payment_methods=payment_methods,
        bank_options=bank_options
    )

@app.route('/process-payment', methods=['POST'])
def process_payment():
    """
    Step 3: Handle payment method selection and redirect to mPAY
    
    Process the payment form submission and redirect to the appropriate mPAY endpoint
    """
    # Get form data
    booking_id = request.form.get('order_id')
    payment_method = request.form.get('payment_method')
    merchant_id = request.form.get('merchant_id', DEFAULT_MERCHANT_ID)
    amount = request.form.get('amount')
    currency = request.form.get('currency', 'THB')
    
    if not booking_id or not payment_method or not amount:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Generate a unique transaction ID
    transaction_id = str(uuid.uuid4())
    
    # Get current website domain for redirects and webhooks
    base_url = request.host_url.rstrip('/')
    success_url = f"{base_url}/payment/success/{booking_id}"
    cancel_url = f"{base_url}/payment/cancel/{booking_id}"
    webhook_url = f"{base_url}/api/webhook"
    
    # Prepare common payment data
    payment_data = {
        'merchant_id': merchant_id,
        'order_id': booking_id,
        'transaction_id': transaction_id,
        'amount': float(amount),
        'currency': currency,
        'description': f"Payment for Raja Ferry booking {booking_id}",
        'redirect_url': success_url,
        'cancel_url': cancel_url,
        'backend_url': webhook_url,
    }
    
    # Get customer information if available
    customer_name = request.form.get('customer_name', '')
    customer_email = request.form.get('customer_email', '')
    customer_phone = request.form.get('customer_phone', '')
    
    if customer_name:
        payment_data['customer_name'] = customer_name
    if customer_email:
        payment_data['customer_email'] = customer_email
    if customer_phone:
        payment_data['customer_phone'] = customer_phone
    
    # Add payment method specific data
    if payment_method == 'credit_card':
        endpoint = '/api/credit-card/payment'
    elif payment_method == 'qr_payment':
        endpoint = '/api/qr/generate'
    elif payment_method == 'rabbit_line_pay':
        endpoint = '/api/rabbit-line-pay/payment'
    elif payment_method == 'internet_banking':
        endpoint = '/api/banking/payment'
        # Add selected bank code
        bank_code = request.form.get('bank_code')
        if bank_code:
            payment_data['bank_code'] = bank_code
    else:
        return jsonify({'error': 'Invalid payment method'}), 400
    
    # Normally would make an internal API call here, but for simplicity,
    # we'll redirect to the actual endpoint
    return redirect(endpoint, code=307)  # 307 preserves the POST method

@app.route('/payment/success/<booking_id>')
def payment_success(booking_id):
    """Handle successful payment redirect"""
    return render_template('payment_success.html', booking_id=booking_id)

@app.route('/payment/cancel/<booking_id>')
def payment_cancel(booking_id):
    """Handle cancelled payment redirect"""
    return render_template('payment_cancel.html', booking_id=booking_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
