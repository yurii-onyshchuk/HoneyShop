from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import ReviewForm
from .models import Product, Category, Review


class ProductList(ListView):
    model = Product
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Shop(ProductList):
    allow_empty = False
    extra_context = {'title': 'Магазин'}
    template_name = 'shop/index.html'


class ProductsByCategory(ProductList):
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class Search(ProductList):
    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результати пошуку'
        context['q'] = self.request.GET.get('q')
        return context


class WishListView(LoginRequiredMixin, ProductList):
    extra_context = {'title': 'Список вподобань'}
    template_name = 'shop/wishlist.html'

    def get_queryset(self):
        return Product.objects.filter(users_wishlist=self.request.user)


class DetailProduct(FormMixin, DetailView):
    model = Product
    form_class = ReviewForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        _list = Review.objects.filter(product__slug=self.kwargs.get('slug'), parent__isnull=True)
        paginator = Paginator(_list, 10)
        page = self.request.GET.get('page')
        context['reviews'] = paginator.get_page(page)
        context['title'] = self.object.title
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


@login_required
def wishlist_button_action(request):
    product = get_object_or_404(Product, id=request.POST['product_id'])
    if product.users_wishlist.filter(pk=request.user.pk).exists():
        product.users_wishlist.remove(request.user)
        action_result = 'removed'
    else:
        product.users_wishlist.add(request.user)
        action_result = 'added'
    wishlist_total = Product.users_wishlist.through.objects.filter(user=request.user).count()
    return JsonResponse({'wishlist_total': wishlist_total, 'action_result': action_result})


@login_required
def clear_wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    for product in products:
        product.users_wishlist.remove(request.user)
    return redirect('shop:wishlist')
