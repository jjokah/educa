import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def order_detail(obj):
    """
    Generate a clickable 'View' link for details in Django admin.
    """
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def export_to_csv(modeladmin, request, queryset):
    """
    Export selected model records to CSV file.
    """
    # Get model metadata
    opts = modeladmin.model._meta
    # Set filename using model's verbose name
    content_dispostion = (
        f'attachment; filename={opts.verbose_name}.csv'
    )
    # Configure response as CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_dispostion
    writer = csv.writer(response)

    # Get all direct fields (excluding many-to-many and one-to-many) 
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


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
        order_detail,
    ]
    # Fields available for filtering orders in the admin interface
    list_filter = ['paid', 'created', 'updated']
    # Include OrderItem inline admin interface
    inlines = [OrderItemInlne]
    # Additional actions to be performed on model list displayed
    actions = [export_to_csv]