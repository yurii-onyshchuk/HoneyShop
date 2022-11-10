from .cart import Cart


def cart(request):
    return {'cart': Cart(request), 'cart_item_ids': [int(i) for i in Cart(request).cart.keys()]}
