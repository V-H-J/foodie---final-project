from django.db import models
from django.contrib.auth.models import User


class UserExtra(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10, choices=[(
        "customer", "Customer"), ("delivery", "Delivery Person"), ("business", "Business")])
    is_admin = models.BooleanField(null=True)

    class Meta:
        db_table = "user_extra"

    def __str__(self):
        return self.user_id.username

class UserProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    dob = models.CharField(max_length=100, null=True)
    favorite_food = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=50, null=True)
    favorite_restaurant = models.CharField(max_length=50, null=True)


class BusinessExtra(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_extra_id = models.ForeignKey(UserExtra, on_delete=models.DO_NOTHING)
    business_address = models.TextField(null=True)
    business_city = models.TextField(null=True)
    business_state = models.TextField(null=True)
    business_zipcode = models.TextField(null=True)
    legal_name = models.TextField(null=True)
    approval_status = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "business_extra"

    def __str__(self):
        return self.legal_name


class DeliveryPersonExtra(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_extra_id = models.ForeignKey(UserExtra, on_delete=models.DO_NOTHING)
    ssn = models.CharField(max_length=10, null=True)
    legal_name = models.TextField(null=True)
    approval_status = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "delivery_person_extra"

    def __str__(self):
        return self.legal_name


class Menu(models.Model):
    restaurant_id = models.ForeignKey(
        BusinessExtra, on_delete=models.DO_NOTHING)
    item_name = models.TextField(null=True)
    item_price = models.FloatField(null=True)

    class Meta:
        db_table = "restaurant_menu"

    def __str__(self):
        return "{} - {}".format(self.restaurant_id.legal_name, self.item_name)


class Offer(models.Model):
    offer_name = models.TextField(null=True)
    offer_description = models.TextField(null=True)
    discount = models.IntegerField(null=True)
    promo_code = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "offers"

    def __str__(self):
        return self.offer_name


class Cart(models.Model):
    restaurant_id = models.ForeignKey(
        BusinessExtra, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "carts"


class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    item_id = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=True)

    class Meta:
        db_table = "cart_items"


class PaymentMethod(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    cardnumber = models.CharField(max_length=16, null=True)
    cardname = models.TextField(null=True)
    cardtype = models.CharField(max_length=50, null=True, choices=[(
        "visa", "Visa"), ("mastercard", "Master Card"), ("americanexpress", "American Express"), ("discover", "Discover")])
    expires = models.CharField(max_length=5, null=True)
    cvv = models.IntegerField()

    class Meta:
        db_table = "payment_methods"


class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    street = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    zipcode = models.TextField(null=True)

    class Meta:
        db_table = "addresses"


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    restaurant_id = models.ForeignKey(
        BusinessExtra, on_delete=models.DO_NOTHING)
    offer_id = models.ForeignKey(Offer, on_delete=models.DO_NOTHING, null=True)
    status = models.CharField(max_length=50, null=True)
    datetime = models.DateTimeField(null=True)
    delivery_id = models.ForeignKey(
        DeliveryPersonExtra, on_delete=models.DO_NOTHING, null=True)
    total_price = models.FloatField(null=True)
    payment_method_id = models.ForeignKey(
        PaymentMethod, on_delete=models.DO_NOTHING, null=True)
    address_id = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return "{} - {}".format(self.user_id.username, self.restaurant_id.legal_name)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    item_id = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=True)

    class Meta:
        db_table = "order_items"


class Default(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    address_id = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, null=True)
    payment_method_id = models.ForeignKey(
        PaymentMethod, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = "defaults"


class Contact(models.Model):
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.TextField(null=True)
    phone = models.TextField(null=True)
    message = models.TextField(null=True)

    class Meta:
        db_table = "contact"


class FavoriteItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    item_id = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = "favorite_item"

class FavoriteRestaurant(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    restaurant_id = models.ForeignKey(BusinessExtra, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = "favorite_restaurant"

class RatingReviewRestaurant(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    restaurant_id = models.ForeignKey(BusinessExtra, on_delete=models.DO_NOTHING, null=True)
    rating = models.IntegerField(null=True)
    review = models.TextField(null=True)

    class Meta:
        db_table = "restaurant_rating_review"