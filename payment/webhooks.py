import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order
from shop.models import Product
from shop.recommender import Recommender
from .tasks import payment_completed


@csrf_exempt
def paystack_webhook(request):
    """
    Handle Paystack webhook notifications for payment processing.
    
    This view handles webhook events from Paystack, specifically the charge.success event.
    It verifies the webhook signature for security and updates order payment status.
    
    Args:
        request: HTTP request object containing webhook payload
        
    Returns:
        HttpResponse: 200 for success, 400 for invalid signature, 404 for order not found
    """

    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    payload = request.body
    signature = request.headers['x-paystack-signature']
    event = None

    # Verify webhook authenticity by computing HMAC SHA512 hash
    try:
        hash_value = hmac.new(
            key=SECRET_KEY.encode('utf-8'),
            msg=payload,
            digestmod=hashlib.sha512
        ).hexdigest()
    except:
        # Return 400 if hash computation fails
        return HttpResponse(status=400)

    # Validate webhook signature by comparing computed hash
    if hmac.compare_digest(hash_value, signature):
        body = json.loads(payload.decode('utf-8'))
        event = body['event']
    else:
        # Return 400 for invalid signature
        return HttpResponse(status=400)

    # Process successful payment notification from Paystack
    if event == 'charge.success':
        data = body['data']
        # Retrieve order ID from payment metadata
        order_id = body['data']['metadata']['order_id']

        # Double check payment status from Paystack
        if (data['status'] == 'success') and (data['gateway_response'] == 'Successful'):
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                # Return 404 if order doesn't exist
                return HttpResponse(status=404)
            # Mark order as paid in the database
            order.paid = True
            order.save()

            # Update product recommendations based on purchase
            product_ids = order.items.values_list('product_id')
            products = Product.objects.filter(id__in=product_ids)
            r = Recommender()
            r.products_bought(products)

            # Trigger async task for additional payment completion processing
            payment_completed.delay(order.id)
    
    # Return success response for webhook processing
    return HttpResponse(status=200)