// Main JavaScript for mPay ONE API integration

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize payment method selector
    initPaymentMethodSelector();
    
    // Initialize payment form
    initPaymentForm();
});

/**
 * Initialize payment method selector
 * This is the main function to implement the requirement of showing only
 * the selected payment method form while hiding others
 */
function initPaymentMethodSelector() {
    const paymentMethodRadios = document.querySelectorAll('input[name="payment_method"]');
    const paymentForms = document.querySelectorAll('.payment-form');
    
    // Make sure to show only the first payment form when page loads
    paymentForms.forEach(form => {
        if (form.id !== 'credit_card-form') {
            form.classList.add('d-none');
        }
    });
    
    paymentMethodRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Hide all payment forms with a fade out effect
            paymentForms.forEach(form => {
                form.classList.add('d-none');
                form.style.opacity = 0;
            });
            
            // Show selected payment form with a fade in effect
            const selectedForm = document.getElementById(`${this.value}-form`);
            if (selectedForm) {
                selectedForm.classList.remove('d-none');
                // Use setTimeout to create a smoother animation effect
                setTimeout(() => {
                    selectedForm.style.opacity = 1;
                    selectedForm.style.transition = 'opacity 0.3s ease-in';
                }, 10);
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
            
            // Show loading spinner
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
    
    // Add common customer details if available
    // For each payment method, get the respective form's customer details fields
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
    
    // Add redirect and backend URLs if available
    const redirectUrl = document.getElementById('redirect_url');
    
    if (redirectUrl && redirectUrl.value) formData.redirect_url = redirectUrl.value;
    formData.backend_url = window.location.origin + "/api/webhook";
    
    // Add method-specific fields
    switch (paymentMethod) {
        case 'credit_card':
            // Credit Card specific fields would be handled by redirect to mPAY ONE payment page
            break;
            
        case 'qr_payment':
            // QR Payment specific fields
            break;
            
        case 'rabbit_line_pay':
            // Rabbit Line Pay specific fields
            break;
            
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
    if (result.redirect_url) {
        // Redirect to payment gateway or success page
        window.location.href = result.redirect_url;
    } else if (result.qr_image) {
        // Show QR code for QR payment
        showQRCode(result.qr_image);
    } else {
        // Show success message
        showSuccessMessage('Payment initiated successfully. Order ID: ' + result.order_id);
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
    
    const qrModal = new bootstrap.Modal(document.getElementById('qr-modal'));
    qrModal.show();
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    alertContainer.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Scroll to alert
    if (alertContainer.scrollIntoView) {
        alertContainer.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    alertContainer.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Scroll to alert
    if (alertContainer.scrollIntoView) {
        alertContainer.scrollIntoView({ behavior: 'smooth' });
    }
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
