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
CREDIT_CARD_PAYMENT_ENDPOINT = " /service-txn-gateway/v1/cc/txns/payment_order"
CREDIT_CARD_TOKEN_PAYMENT_ENDPOINT = "/service-txn-gateway/v1/cc/txns/payment_order"
CREDIT_CARD_TOKEN_INQUIRY_ENDPOINT = "/service-txn-gateway/v1/cc/cards/inquiry"
CREDIT_CARD_TOKEN_TERMINATE_ENDPOINT = "/service-txn-gateway/v1/cc/cards/unregister"
CREDIT_CARD_CAPTURE_ENDPOINT = "/service-txn-gateway/v1/cc/txns/authorize/capture"
CREDIT_CARD_CANCEL_ENDPOINT = "/service-txn-gateway/v1/cc/txns/authorize/cancel"
CREDIT_CARD_SEAMLESS_PAYMENT_ENDPOINT = "/service-txn-gateway/v1/cc/txns/payment_order"
CREDIT_CARD_SEAMLESS_REGISTER_ENDPOINT = "/credit-card/seamless/register"
CREDIT_CARD_SEAMLESS_CONFIRM_ENDPOINT = "/service-txn-gateway/v1/cc/txns/payment_ref"

QR_GENERATE_ENDPOINT = "/service-txn-gateway/v1/qr"

RLP_PAYMENT_ENDPOINT = "/service-txn-gateway/v1/rlp/txns/payment"
RLP_PREAPPROVED_PAYMENT_ENDPOINT = "/service-txn-gateway/v1/rlp/txns/preapproved/payment"
RLP_TOKEN_TERMINATE_ENDPOINT = "/service-txn-gateway/v1/rlp/token/forget"

INSTALLMENT_PLAN_INQUIRY_ENDPOINT = "/service-txn-gateway/v1/inst/inquiry_plan"
INSTALLMENT_PAYMENT_ENDPOINT = "/service-txn-gateway/v1/inst/txns/payment"

INTERNET_BANKING_ENDPOINT = "/service-txn-gateway/v1/ib/payment_order"
REQUEST_TO_PAY_ENDPOINT = "/service-txn-gateway/v1/createlink"

PAYMENT_INQUIRY_ENDPOINT = "/payment/inquiry"
VOID_REFUND_ENDPOINT = "/payment/void-refund"

# Error Codes
ERROR_CODES = {
    "INVALID_REQUEST": "INVALID_REQUEST",
    "PAYMENT_FAILED": "PAYMENT_FAILED",
    "RESOURCE_NOT_FOUND": "RESOURCE_NOT_FOUND",
    "SYSTEM_ERROR": "SYSTEM_ERROR"
}
