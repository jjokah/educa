from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def product_list(request, category_slug=None):
    """
    View function for displaying a list of products.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # If a category slug is provided, filter product by that category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
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
    View function for displaying details of a specific product.
    """
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    return render(
        request,
        'shop/product/detail.html',
        {'product': product}
    )
