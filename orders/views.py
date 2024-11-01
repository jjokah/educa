from django.shortcuts import render

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import OrderItem


def order_create(request):
    """
    Handle order creation process.
    
    This view performs two main functions:
    1. Displays the order form when accessed via GET
    2. Processes the order submission when accessed via POST
    
    Args:
        request: HTTP request object
    
    Returns:
        Rendered template with either:
        - Order form and cart (GET)
        - Order confirmation page (successful POST)
    """
    # Initialize shopping cart from session
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create new order instance
            order = form.save()
            
            # Create OrderItem for each product in cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Empty the cart after order creation
            cart.clear()
            
            # Render success page
            return render(
                request, 'orders/order/created.html', {'order': order}
            )
    else:
        # Display empty order form
        form = OrderCreateForm()
        
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )
