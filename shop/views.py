from django.views.generic import ListView, DetailView
from django.db.models import F
from .models import Product, Category


class Shop(ListView):
    model = Product
    extra_context = {'title': 'Магазин'}
    template_name = 'shop/index.html'
    context_object_name = 'products'


class ProductsByCategory(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class DetailProduct(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Product.objects.get(slug=self.kwargs['slug'])
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Search(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['title'] = 'Результати пошуку'
        return context
