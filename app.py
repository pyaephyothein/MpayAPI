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

# Main routes
@app.route('/')
@app.route('/payment')
def payment_form():
    """Render the payment form page"""
    # Sample order data (in a real app, this would come from a database)
    order_data = {
        'id': 'ORD-2025001',
        'merchant_id': 'MERCH-12345',
        'route': 'Donsak - Samui',
        'date_time': 'March 15, 2025 - 10:00 AM',
        'fare': 450.00,
        'service_fee': 45.00,
        'tax': 34.73,
        'total': 529.73,
        'currency': 'THB'
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
            'name': 'Internet Banking',
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
    
    # Installment options
    installment_plans = [
        {'value': '3', 'name': '3 months'},
        {'value': '6', 'name': '6 months'},
        {'value': '10', 'name': '10 months'}
    ]
    
    installment_banks = [
        {'code': 'KTC', 'name': 'KTC Credit Card'},
        {'code': 'BAY', 'name': 'Krungsri Credit Card'},
        {'code': 'FCY', 'name': 'First Choice Card'}
    ]
    
    return render_template(
        'payment_form.html',
        order=order_data,
        payment_methods=payment_methods,
        bank_options=bank_options,
        installment_plans=installment_plans,
        installment_banks=installment_banks
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
