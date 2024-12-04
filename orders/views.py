from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render

import weasyprint

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generate a PDF document for a specific order.
    """
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('shop/css/pdf.css'))]
    )
    return response


def order_create(request):
    """
    Handle order creation process.
    """
    # Initialize shopping cart from session
    cart = Cart(request)
    
    # Process Order submission
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
