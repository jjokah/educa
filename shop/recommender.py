import redis
from django.conf import settings
from .models import Product


# Connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


class Recommender:
    """
    A product recommendation system that tracks and suggests products 
    based on purchase patterns using Redis sorted sets.
    """

    def get_product_key(self, id):
        """
        Generate a unique Redis key for storing product relationships.
        """
        return f'product:{id}:purchased_with'
    
    def products_bought(self, products):
        """
        Track products that were bought together.
        Updates the sorted set scores in Redis for product relationships.
        """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(
                        self.get_product_key(product_id), 1, with_id
                    )

    def suggest_products_for(self, products, max_results=6):
        """
        Get product recommendations based on purchase history.
        """
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # For single product, get directly from its sorted set
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # For multiple products, combine scores from all products
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # Merge the sorted sets of all input products
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # Remove the input products from suggestions
            r.zrem(tmp_key, *product_ids)
            # Get top scored products
            suggestions = r.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            # Cleanup temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # Fetch actual product objects and maintain score ordering
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids)
        )
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products
    
    def clear_purchases(self):
        """
        Remove all product purchase history from Redis.
        """
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
            