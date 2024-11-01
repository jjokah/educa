from django.db import models


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

    class Meta:
        ordering = ['-created']  # Orders sorted by creation date (newest first)
        indexes = [
            models.Index(fields=['-created']),  # Index for faster queries on created field
        ]

    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        """Calculate the total cost of all items in the order."""
        return sum(item.get_cost() for item in self.items.all())
    

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
