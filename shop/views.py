from django.shortcuts import render
from django.views.generic import TemplateView


class Shop(TemplateView):
    template_name = 'shop/shop_main_page.html'
