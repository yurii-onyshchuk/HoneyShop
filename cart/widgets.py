from django.forms.widgets import Input


class CartProductNumberInput(Input):
    template_name = "cart/widgets/cart_product_number_input.html"
