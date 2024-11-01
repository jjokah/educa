from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInlne(admin.TabularInline):
    """
    Inline admin interface for OrderItem model that allows editing order items
    directly within the Order admin page in a tabular format.
    """
    model = OrderItem
    raw_id_fields = ['product']  # Uses raw ID widget for product selection


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Order model.
    Customizes how orders are displayed and managed in Django admin.
    """
    # Fields to display in the orders list view
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        'created',
        'updated',
    ]
    # Fields available for filtering orders in the admin interface
    list_filter = ['paid', 'created', 'updated']
    # Include OrderItem inline admin interface
    inlines = [OrderItemInlne]