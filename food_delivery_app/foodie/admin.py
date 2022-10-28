from django.contrib import admin

from foodie.models import *

# Register your models here.
admin.site.register(UserExtra)
admin.site.register(BusinessExtra)
admin.site.register(DeliveryPersonExtra)
admin.site.register(Menu)
admin.site.register(Offer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(PaymentMethod)
admin.site.register(FavoriteItem)
admin.site.register(FavoriteRestaurant)