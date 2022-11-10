from django import template
from shop.models import Product

register = template.Library()


@register.inclusion_tag('shop/top_products.html', takes_context=True)
def get_top_products(context, top_title, param, count):
    products = Product.objects.filter(available__gt=0).order_by(param)[:count]
    return {'user': context['user'],
            'cart': context['cart'],
            'cart_form': context['cart_form'],
            'cart_item_ids': context['cart_item_ids'],
            'wish_list': context['wish_list'],
            'top_title': top_title,
            'products': products, }
