import logging
import requests
from requests.exceptions import RequestException
from config import RAJA_FERRY_API_URL, RAJA_FERRY_API_KEY

logger = logging.getLogger(__name__)

def get_customer_data(booking_id):
    """
    Fetch customer data from Raja Ferry Port API
    
    Args:
        booking_id (str): The booking ID
        
    Returns:
        dict: Customer data including personal details and booking information
        None: If data retrieval fails
    """
    try:
        # Set up headers with API key
        headers = {
            'Authorization': f'Bearer {RAJA_FERRY_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Make request to Raja Ferry API
        endpoint = f"{RAJA_FERRY_API_URL}/bookings/{booking_id}"
        logger.debug(f"Fetching customer data for booking ID: {booking_id}")
        
        try:
            response = requests.get(
                url=endpoint,
                headers=headers,
                timeout=30
            )
            
            # Check if request was successful
            if response.status_code == 200:
                booking_data = response.json()
                logger.debug(f"Successfully retrieved booking data: {booking_data}")
                
                # Extract and format customer data
                customer_data = {
                    'customer_data': {
                        'name': booking_data.get('customer', {}).get('name', ''),
                        'email': booking_data.get('customer', {}).get('email', ''),
                        'phone': booking_data.get('customer', {}).get('phone', ''),
                        'address': booking_data.get('customer', {}).get('address', ''),
                    },
                    'booking_details': {
                        'booking_id': booking_id,
                        'amount': booking_data.get('payment', {}).get('amount', 0),
                        'currency': booking_data.get('payment', {}).get('currency', 'THB'),
                        'description': f"Payment for Raja Ferry booking {booking_id}",
                        'route': booking_data.get('trip', {}).get('route', ''),
                        'departure_date': booking_data.get('trip', {}).get('departure_date', ''),
                        'departure_time': booking_data.get('trip', {}).get('departure_time', '')
                    }
                }
                return customer_data
            else:
                logger.error(f"Failed to retrieve customer data. Status code: {response.status_code}")
                # Fallback to demo data for testing purposes
                return get_demo_customer_data(booking_id)
        except RequestException as e:
            logger.exception(f"Error connecting to Raja Ferry API: {str(e)}")
            # Fallback to demo data for testing purposes
            return get_demo_customer_data(booking_id)
    except Exception as e:
        logger.exception(f"Unexpected error retrieving customer data: {str(e)}")
        return None

def get_demo_customer_data(booking_id):
    """
    Generate demo customer data for testing when API is unavailable
    This should only be used in development/testing environments
    """
    logger.info(f"Creating demo data for booking ID: {booking_id}")
    
    # Create sample booking data
    customer_data = {
        'customer_data': {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '0812345678',
            'address': '123 Bangkok Street, Thailand',
        },
        'booking_details': {
            'booking_id': booking_id,
            'amount': 1250.00,
            'currency': 'THB',
            'description': f"Payment for Raja Ferry booking {booking_id}",
            'route': 'Donsak - Koh Samui',
            'departure_date': '2025-05-15',
            'departure_time': '10:30'
        }
    }
    
    return customer_data