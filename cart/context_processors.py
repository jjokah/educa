from .cart import Cart


def cart(request):
    # Instantiate the Cart variable using the request object
    # and make it accessible in ALL templates as a variable "cart"
    return {'cart': Cart(request)}