from django import template
from blog.models import Category, Post

register = template.Library()


@register.inclusion_tag('blog/categories_tpl.html')
def show_category():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('blog/popular_post_tpl.html')
def show_post_list(count=5):
    posts = Post.objects.order_by('-views')[:count]
    return {'posts': posts}
