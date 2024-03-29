from .models import Product


def wish_list(request):
    """Retrieve the user's wishlist."""
    if request.user.is_authenticated:
        return {'wish_list': Product.objects.filter(users_wishlist=request.user)}
    else:
        return {'wish_list': None}
