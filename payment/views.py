import json
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orders.models import Order


def payment_process(request):
    """
    Handle payment processing using payment gateway.
    
    Args:
        request: HTTP request object
    
    Returns:
        - Redirects to payment page on successful initialization
        - Renders payment process page for GET requests or failed initialization
    """
    # Get order from session
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Build success and cancel URLs for payment gateway callbacks
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )

        # Paystack payment session configuration
        payment_url = settings.PAYSTACK_PAYMENT_URL
        secret_key = settings.PAYSTACK_TEST_SECRET_KEY
        paystack_metadata = json.dumps({
            'order_id': str(order_id),
            'cancel_action': cancel_url,
        })
        # Prepare payment data for Paystack API
        paystack_session_data = {
            'amount': int(order.get_total_cost() * 100),
            'currency': 'NGN',
            'email': str(order.email),
            'callback_url': success_url,
            'metadata': paystack_metadata
        }
        # Make API request to initialize payment
        headers = {'Authorization': f'Bearer {secret_key}'}
        response = requests.post(payment_url, data=paystack_session_data, headers=headers)
        response = response.json()

        # Handle Paystack API response
        if response['status'] == True:
            redirect_url = response['data']['authorization_url']
            return redirect(redirect_url, code=303)
        else:
            return render(request, 'payment/process.html', locals())

        # Flutterwave implementation commented out but documented for future reference
        # Similar flow to Paystack but with different API structure
        # # Flutterwave payment session
        # payment_url = settings.FLUTTERWAVE_PAYMENT_URL
        # secret_key = settings.FLUTTERWAVE_TEST_SECRET_KEY
        # flutterwave_metadata = json.dumps({
        #     'cancel_url': cancel_url,
        # })
        # flutterwave_session_data = {
        #     'txt_ref': str(order_id),
        #     'amount': int(order.get_total_cost()),
        #     'currency': 'NGN',
        #     'redirect_url': success_url,
        #     'customer': {
        #         'email': str(order.email)
        #     },
        #     'meta': flutterwave_metadata,
        # }
        # headers = {'Authorization': f'Bearer {secret_key}'}
        # response = requests.post(payment_url, flutterwave_session_data, headers=headers)
        # print(response)
        # response = response.json()
        # if response['status'] == 'successful':
        #     redirect_url = response['data']['link']
        #     return redirect(redirect_url, code=303)
        # elif response['status'] == 'cancelled':
        #     return redirect(cancel_url, code=303)
        # else:
        #     return render(request, 'payment/process.html', locals())
    else:
        return render(request, 'payment/process.html', locals())
    

def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
