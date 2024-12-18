from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Coupon model in Django admin interface.
    """
    list_display = [
        'code',
        'valid_from',
        'valid_to',
        'discount',
        'active'
    ]
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
