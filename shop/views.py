from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import F
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .models import Product, Category
from .forms import ReviewForm
from cart.forms import CartAddProductForm, CartAddSeveralProductForm


class Shop(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Магазин'
        context['cart_form'] = CartAddProductForm
        return context


class ProductsByCategory(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 9
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['cart_form'] = CartAddProductForm
        return context


class DetailProduct(FormMixin, DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    form_class = ReviewForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['cart_form'] = CartAddSeveralProductForm
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        product = self.get_object()
        if form.is_valid():
            if request.POST.get('parent', None):
                form.instance.parent_id = int(request.POST.get('parent'))
            form.instance.product = product
            form.instance.user = self.request.user
            form.save()
        return redirect(product.get_absolute_url())

    def get_success_url(self):
        return reverse_lazy('shop:product', kwargs={'slug': self.kwargs['slug']})


class Search(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результати пошуку'
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['cart_form'] = CartAddProductForm
        return context
