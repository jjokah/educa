from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm

from .models import Category, Product
from .recommender import Recommender


def product_list(request, category_slug=None):
    """
    Get a list of available products, optionally filtered by category.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # If a category slug is provided, filter product by that category
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug
        )
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
    )


def product_detail(request, id, slug):
    """
    Get detailed information about of a specific product
    and form for adding product to cart.
    """
    # Get product or return 404 if not found/unavailable
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product, 
        id=id,
        translations__language_code=language,
        translations__slug=slug, 
        available=True
    )
    # Initialize the cart add form
    cart_product_form = CartAddProductForm()
    # Get product recommendations
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product, 
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products
        }
    )
