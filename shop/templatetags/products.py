from django import template
from shop.models import Product

register = template.Library()


@register.inclusion_tag('shop/top_products.html')
def get_top_products(top_title, param, count, cart_form):
    products = Product.objects.filter(available__gt=0).order_by(param)[:count]
    return {'top_title': top_title, 'products': products, 'cart_form': cart_form}
