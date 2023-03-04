from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, template_name='cart/cart_detail.html', context={'cart': cart, 'title': 'Корзина'})


@require_POST
def cart_add(request):
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST['product_id'])
    cart.add(product=product)
    return JsonResponse({'cart_total': cart.__len__()})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if product.quantity >= int(request.POST['quantity']):
        cart.update(product=product, quantity=int(request.POST['quantity']))
    json = {'available_quantity': product.quantity,
            'product_total_price': cart.get_product_total_price(product),
            'total_price': cart.get_total_price(),
            'cart_total': cart.__len__()}
    return JsonResponse(json)


def cart_delete(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.delete(product)
    return redirect('shop:cart:cart_detail')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER'))
