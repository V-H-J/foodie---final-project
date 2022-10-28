from django.contrib.sessions.middleware import *

from foodie.models import *


class CustomizeRequest(SessionMiddleware):

    def process_request(self, request):
        if request.user.is_authenticated:
            user_extra = UserExtra.objects.filter(user_id = request.user)
            if user_extra:
                request.user_extra = user_extra[0]
            else:
                request.user_extra = None
            defaults = Default.objects.filter(user_id=request.user)
            if defaults:
                request.user_default = defaults[0]
            else:
                request.user_default = None
            cart = Cart.objects.filter(user_id = request.user)
            if cart:
                cart_items = CartItem.objects.filter(cart_id = cart[0])
                if cart_items:
                    request.cart_items = list(cart_items)
                    request.cart_items_ids = list(cart_items.values_list('item_id_id',flat=True))
                else:
                    request.cart_items = []
                    request.cart_items_ids = []
            else:
                request.cart_items = []
                request.cart_items_ids = []