from .cart import Cart


def cart(request):
    """Add cart-related data to the context."""
    return {'cart': Cart(request), 'cart_item_ids': [int(i) for i in Cart(request).cart.keys()]}
