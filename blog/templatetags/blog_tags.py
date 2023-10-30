from django import template
from blog.models import Category, Post

register = template.Library()


@register.simple_tag
def get_blog_categories():
    """Get all blog categories from the database."""
    return Category.objects.all()


@register.inclusion_tag('blog/categories_tpl.html')
def show_categories():
    """Display a list of blog categories."""
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('blog/popular_post_tpl.html')
def show_post_list(count=5):
    """Display a list of the most popular blog posts."""
    posts = Post.objects.order_by('-views')[:count]
    return {'posts': posts}
