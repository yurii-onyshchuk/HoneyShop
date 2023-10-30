from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    """A shopping cart for a user's session.

    This class represents a shopping cart that allows users to add, update
    and remove products during their session.
    """

    def __init__(self, request):
        """Initialize the Cart object.

        If a cart does not exist in the session, a new empty cart
        is created and stored in the session.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __getitem__(self, item_id):
        """Get an item from the cart by its ID."""
        return self.cart[str(item_id)]

    def __len__(self):
        """Calculate and return the total number of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """Iterate over the items in the cart and return associated product details."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product):
        """Add a product to the cart."""
        product_id = str(product.id)
        self.cart[product_id] = {'quantity': 1, 'price': str(product.price)}
        self.save()

    def update(self, product, quantity):
        """Update the quantity of a product in the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def delete(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """Save the cart data to the session."""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_product_quantity(self, product):
        """Get the quantity of a specific product in the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            quantity = self.cart[product_id]['quantity']
            return quantity

    def get_product_total_price(self, product):
        """Calculate and return the total price of a specific product in the cart."""
        product_id = str(product.id)
        quantity = self.get_product_quantity(product)
        price = self.cart[product_id]['price']
        return Decimal(price) * quantity

    def get_total_price(self):
        """Calculate and return the total price of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Clear all items from the cart."""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
