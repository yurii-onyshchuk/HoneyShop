from django import template
from shop.models import Category

register = template.Library()


@register.inclusion_tag('shop/categories_tpl.html')
def show_category():
    categories = Category.objects.all()
    return {'categories': categories}
