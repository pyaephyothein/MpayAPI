"""
Configuration settings for mPAY ONE API integration and Raja Ferry Port API
"""

import os

# mPAY ONE API Configuration
# API Base URL
MPAY_ONE_BASE_URL = os.environ.get("MPAY_ONE_BASE_URL", "https://sandbox.mpay.one/api/v1")

# API Secret Key
API_SECRET_KEY = os.environ.get("MPAY_ONE_SECRET_KEY", "test_secret_key")

# Merchant ID
DEFAULT_MERCHANT_ID = os.environ.get("MPAY_ONE_MERCHANT_ID", "MERCH-12345")

# Raja Ferry Port API Configuration
RAJA_FERRY_API_URL = os.environ.get("RAJA_FERRY_API_URL", "https://api.rajaferryport.com/v1")
RAJA_FERRY_API_KEY = os.environ.get("RAJA_FERRY_API_KEY", "test_raja_ferry_api_key")

# Raja Ferry Port Website URL (for redirects)
RAJA_FERRY_WEBSITE = os.environ.get("RAJA_FERRY_WEBSITE", "https://www.rajaferryport.com")

# API Endpoints
CREDIT_CARD_PAYMENT_ENDPOINT = "/credit-card/payment"
CREDIT_CARD_TOKEN_PAYMENT_ENDPOINT = "/credit-card/token-payment"
CREDIT_CARD_TOKEN_INQUIRY_ENDPOINT = "/credit-card/token-inquiry"
CREDIT_CARD_TOKEN_TERMINATE_ENDPOINT = "/credit-card/token-terminate"
CREDIT_CARD_CAPTURE_ENDPOINT = "/credit-card/capture"
CREDIT_CARD_CANCEL_ENDPOINT = "/credit-card/cancel"
CREDIT_CARD_SEAMLESS_PAYMENT_ENDPOINT = "/credit-card/seamless"
CREDIT_CARD_SEAMLESS_REGISTER_ENDPOINT = "/credit-card/seamless/register"
CREDIT_CARD_SEAMLESS_CONFIRM_ENDPOINT = "/credit-card/seamless/confirm"

QR_GENERATE_ENDPOINT = "/qr/generate"

RLP_PAYMENT_ENDPOINT = "/rabbit-line-pay/payment"
RLP_PREAPPROVED_PAYMENT_ENDPOINT = "/rabbit-line-pay/preapproved-payment"
RLP_TOKEN_TERMINATE_ENDPOINT = "/rabbit-line-pay/token-terminate"

INSTALLMENT_PLAN_INQUIRY_ENDPOINT = "/installment/plan-inquiry"
INSTALLMENT_PAYMENT_ENDPOINT = "/installment/payment"

INTERNET_BANKING_ENDPOINT = "/internet-banking/payment"
REQUEST_TO_PAY_ENDPOINT = "/internet-banking/request-to-pay"

PAYMENT_INQUIRY_ENDPOINT = "/payment/inquiry"
VOID_REFUND_ENDPOINT = "/payment/void-refund"

# Error Codes
ERROR_CODES = {
    "INVALID_REQUEST": "INVALID_REQUEST",
    "PAYMENT_FAILED": "PAYMENT_FAILED",
    "RESOURCE_NOT_FOUND": "RESOURCE_NOT_FOUND",
    "SYSTEM_ERROR": "SYSTEM_ERROR"
}
