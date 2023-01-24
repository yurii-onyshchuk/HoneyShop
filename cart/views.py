from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    cart = Cart(request)
    return render(request, template_name='cart/cart_detail.html',
                  context={'cart': cart, 'cart_form': CartAddProductForm, 'title': 'Корзина'})


@require_POST
def cart_add(request):
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST['product_id'])
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'])
    cart_total = cart.__len__()
    return JsonResponse({'cart_total': cart_total})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.update(product=product, quantity=data['quantity'])
    return redirect('shop:cart:cart_detail')


def cart_delete(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.delete(product)
    return redirect('shop:cart:cart_detail')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER'))
