from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


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
            # Launch asynchronous task to send confirmation email
            order_created.delay(order.id)
            # Set the order in the session
            request.session['order_id'] = order.id
            # Redirect for payment
            return redirect('payment:process')
    else:
        # Display empty order form
        form = OrderCreateForm()
        
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )


@staff_member_required
def admin_order_detail(request, order_id):
    """
    Display detailed order information for admin users (staff only)
    """
    order = get_object_or_404(Order, id=order_id)
    return render(
        request, 'admin/orders/order/detail.html', {'order': order}
    )
