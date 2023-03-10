from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from shop.models import Product


def cart_detail(request):
    cart = Cart(request)
    return render(request, template_name='cart/cart_detail.html', context={'cart': cart, 'title': 'Корзина'})


@require_POST
def cart_add(request):
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST['product_id'])
    cart.add(product=product)
    return JsonResponse({'cart_total_quantity': len(cart)})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    input_quantity = int(request.POST['input_quantity'])
    if input_quantity <= 0:
        product_quantity = 1
    elif product.quantity <= input_quantity:
        product_quantity = int(product.quantity)
    else:
        product_quantity = input_quantity
    cart.update(product=product, quantity=product_quantity)
    response = {'available_product_quantity': product.quantity,
                'product_quantity': cart[product.id]['quantity'],
                'product_total_price': cart.get_product_total_price(product),
                'cart_total_price': cart.get_total_price(),
                'cart_total_quantity': len(cart)}
    return JsonResponse(response)


def cart_delete(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.delete(product)
    return redirect('shop:cart:cart_detail')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER'))
