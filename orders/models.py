from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from coupons.models import Coupon


class Order(models.Model):
    """
    Model representing a customer order.
    
    Stores customer details, shipping information, and order status.
    Related to OrderItem through a one-to-many relationship.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when order is created
    updated = models.DateTimeField(auto_now=True)      # Timestamp when order is updated
    paid = models.BooleanField(default=False)          # Payment status
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['-created']  # Orders sorted by creation date (newest first)
        indexes = [
            models.Index(fields=['-created']),  # Index for faster queries on created field
        ]

    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)
    
    def get_total_cost(self):
        """Calculate the total cost of all items in the order."""
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()
    

class OrderItem(models.Model):
    """
    Model representing individual items within an order.
    
    Links products to orders and stores quantity and price information
    for each item at the time of purchase.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        """Calculate the total cost of this order item."""
        return self.price * self.quantity
