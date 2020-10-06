from decimal import Decimal
from django.conf import settings
from shop.models import Item

class Cart(object):
    # initiating session
    def __init__(self, request):
        #get session
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        # get items from database
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)

        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]['item'] = item

        for cart_item in cart.values():
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def overall_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def add_item(self, item, quantity=1, override_quantity=False):
        # add to cart or update
        # converting id to string cuz item.id is not serializable
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0,
                                  'price': str(item.price)}
        if override_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save
    
    def reduce_item(self, item, quantity):
        item_id = str(item.id)
        if override_quantity:
            self.cart[item_id][quantity] = quantity
        else:
            self.cart[item_id][quantity] -= quantity
        self.save
    
    def save(self):
        # marking session as modified so django can save
        self.session.modified = True

    def remove_item(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id] 
            self.save 
    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()