// Main JavaScript for mPay ONE API integration with Bootstrap 4

document.addEventListener('DOMContentLoaded', function() {
    // Initialize payment method selector
    initPaymentMethodSelector();
    
    // Initialize payment form
    initPaymentForm();
});

/**
 * Initialize payment method selector
 * Shows only the selected payment method form while hiding others
 */
function initPaymentMethodSelector() {
    const paymentMethodRadios = document.querySelectorAll('input[name="payment_method"]');
    const paymentForms = document.querySelectorAll('.payment-form');
    
    // Make sure the first payment form (credit card) is active on page load
    const creditCardForm = document.getElementById('credit_card-form');
    if (creditCardForm) {
        creditCardForm.classList.add('active');
    }
    
    // Handle payment method selection
    paymentMethodRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const selectedFormId = `${this.value}-form`;
            
            // First, remove active class from all forms
            paymentForms.forEach(form => {
                form.classList.remove('active');
            });
            
            // Then add active class to the selected form
            const selectedForm = document.getElementById(selectedFormId);
            if (selectedForm) {
                selectedForm.classList.add('active');
            }
        });
    });
}

/**
 * Initialize payment form submission
 */
function initPaymentForm() {
    const paymentForm = document.getElementById('payment-form');
    
    if (paymentForm) {
        paymentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state on button
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            
            // Get selected payment method
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
            
            try {
                // Build form data based on payment method
                const formData = buildFormData(paymentMethod);
                
                // Call appropriate API endpoint
                const endpoint = getEndpointForPaymentMethod(paymentMethod);
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    handleSuccessResponse(result, paymentMethod);
                } else {
                    handleErrorResponse(result);
                }
            } catch (error) {
                console.error('Payment processing error:', error);
                showErrorMessage('An unexpected error occurred. Please try again.');
            } finally {
                // Restore submit button
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    }
}

/**
 * Build form data based on payment method
 */
function buildFormData(paymentMethod) {
    const formData = {
        merchant_id: document.getElementById('merchant_id').value,
        order_id: document.getElementById('order_id').value,
        amount: parseFloat(document.getElementById('amount').value),
        currency: document.getElementById('currency').value,
        description: document.getElementById('description').value
    };
    
    // Add common customer details if available based on the selected payment method
    let customerEmail, customerName, customerPhone;
    
    switch(paymentMethod) {
        case 'credit_card':
            customerEmail = document.getElementById('customer_email');
            customerName = document.getElementById('cardholder_name');
            break;
        case 'rabbit_line_pay':
            customerEmail = document.getElementById('rlp_customer_email');
            customerName = document.getElementById('rlp_customer_name');
            customerPhone = document.getElementById('rlp_customer_phone');
            break;
        case 'installment':
            customerEmail = document.getElementById('installment_customer_email');
            customerName = document.getElementById('installment_customer_name');
            break;
        case 'internet_banking':
            customerEmail = document.getElementById('ib_customer_email');
            customerName = document.getElementById('ib_customer_name');
            break;
    }
    
    if (customerEmail && customerEmail.value) formData.customer_email = customerEmail.value;
    if (customerName && customerName.value) formData.customer_name = customerName.value;
    if (customerPhone && customerPhone.value) formData.customer_phone = customerPhone.value;
    
    // Set backend URL for webhook
    formData.backend_url = window.location.origin + "/api/webhook";
    
    // Add method-specific fields
    switch (paymentMethod) {
        case 'installment':
            // Add installment specific fields
            const installmentPlan = document.getElementById('installment_plan');
            const installmentBank = document.querySelector('input[name="installment_bank"]:checked');
            
            if (installmentPlan && installmentPlan.value) formData.installment_plan = installmentPlan.value;
            if (installmentBank && installmentBank.value) formData.installment_bank = installmentBank.value;
            break;
            
        case 'internet_banking':
            // Add internet banking specific fields
            const bankCode = document.querySelector('input[name="bank_code"]:checked');
            if (bankCode && bankCode.value) formData.bank_code = bankCode.value;
            break;
    }
    
    return formData;
}

/**
 * Get API endpoint based on payment method
 */
function getEndpointForPaymentMethod(paymentMethod) {
    switch (paymentMethod) {
        case 'credit_card':
            return '/api/credit-card/payment';
        case 'qr_payment':
            return '/api/qr/generate';
        case 'rabbit_line_pay':
            return '/api/rabbit-line-pay/payment';
        case 'installment':
            return '/api/installment/payment';
        case 'internet_banking':
            return '/api/banking/payment';
        default:
            throw new Error(`Unknown payment method: ${paymentMethod}`);
    }
}

/**
 * Handle successful API response
 */
function handleSuccessResponse(result, paymentMethod) {
    if (paymentMethod === 'qr_payment' && result.qr_image) {
        // Show QR code for QR payment
        showQRCode(result.qr_image);
    } else if (result.redirect_url) {
        // For demo purposes, just show success message instead of redirecting
        showSuccessMessage(`Payment initiated successfully for ${paymentMethod}. Order ID: ${result.order_id}`);
    } else {
        // Show success message
        showSuccessMessage(`Payment initiated successfully. Order ID: ${result.order_id}`);
    }
}

/**
 * Handle error API response
 */
function handleErrorResponse(result) {
    let errorMessage = 'Payment processing failed.';
    
    if (result.error && result.message) {
        errorMessage = `${result.error}: ${result.message}`;
    } else if (result.error) {
        errorMessage = result.error;
    } else if (result.message) {
        errorMessage = result.message;
    }
    
    showErrorMessage(errorMessage);
}

/**
 * Show QR code in modal
 */
function showQRCode(qrImageData) {
    const modalBody = document.querySelector('#qr-modal .modal-body');
    modalBody.innerHTML = `
        <div class="text-center">
            <img src="${qrImageData}" alt="QR Code" class="img-fluid qr-image">
            <p class="mt-3">Scan this QR code with your banking application to complete the payment</p>
        </div>
    `;
    
    // Use jQuery to show modal (Bootstrap 4 style)
    $('#qr-modal').modal('show');
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    alertContainer.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <i class="fas fa-check-circle mr-2"></i>
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
    
    // Scroll to alert
    alertContainer.scrollIntoView({ behavior: 'smooth' });
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        $('.alert').alert('close');
    }, 5000);
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    alertContainer.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <i class="fas fa-exclamation-circle mr-2"></i>
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
    
    // Scroll to alert
    alertContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Format currency
 */
function formatCurrency(amount, currency = 'THB') {
    return new Intl.NumberFormat('th-TH', {
        style: 'currency',
        currency: currency
    }).format(amount);
}
