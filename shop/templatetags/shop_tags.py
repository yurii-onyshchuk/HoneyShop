from django import template
from shop.models import Product, Category

register = template.Library()


@register.simple_tag
def get_shop_categories():
    return Category.objects.all()


@register.inclusion_tag('shop/categories_tpl.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('shop/top_products_tpl.html', takes_context=True)
def get_top_products(context, top_title, param, count):
    product_list = Product.objects.filter(available__gt=0).order_by(param)[:count]
    return {'user': context['user'],
            'cart': context['cart'],
            'cart_form': context['cart_form'],
            'cart_item_ids': context['cart_item_ids'],
            'wish_list': context['wish_list'],
            'top_title': top_title,
            'product_list': product_list, }
