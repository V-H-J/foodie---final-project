from json import load
from foodie.models import *
from django.contrib.auth.models import User
import csv
import os


def business_data():
    business_data = open(os.getcwd()+"/foodie/default_data/restaurants.csv", encoding='utf-8-sig')
    dict = csv.DictReader(business_data)
    for i in dict:
        email = "{}@foodie.com".format(i['legal_name'].lower().replace(" ","_").replace("'",""))
        password = "foodie123"
        user = User.objects.create_user(email, email, password, first_name=i['legal_name'])
        user_extra = UserExtra.objects.create(user_id=user, phone="1111111111", user_type='business')
        business_extra = BusinessExtra.objects.create(user_id=user, user_extra_id=user_extra, legal_name=i['legal_name'].strip(), business_address=i['business_address'], business_city=i['business_city'], business_state=i['business_state'], business_zipcode=i['business_zipcode'], approval_status="approved")

def menu_items():
    menu_items = open(os.getcwd()+"/foodie/default_data/menu_items.csv", encoding='utf-8-sig')
    dict = csv.DictReader(menu_items)
    for i in dict:
        business_extra = BusinessExtra.objects.get(legal_name=i['legal_name'])
        menu = Menu.objects.create(restaurant_id=business_extra, item_name=i['item_name'], item_price=i['item_price'])

def offers():
    offers = open(os.getcwd()+"/foodie/default_data/offers.csv",encoding='utf-8-sig')
    dict = csv.DictReader(offers)
    for i in dict:
        offer = Offer.objects.create(offer_name=i['offer_name'], offer_description=i['offer_description'], discount=i['discount'], promo_code=i['promo_code'])

def delivery_persons():
    delivery_persons = open(os.getcwd()+"/foodie/default_data/delivery_persons.csv", encoding='utf-8-sig')
    dict = csv.DictReader(delivery_persons)
    for i in dict:
        email = "{}@foodie.com".format(i['legal_name'].lower())
        password = "foodie123"
        user = User.objects.create_user(email, email, password, first_name=i['legal_name'])
        user_extra = UserExtra.objects.create(user_id=user, phone="1111111111", user_type='delivery')
        delivery_extra = DeliveryPersonExtra.objects.create(user_id=user, user_extra_id=user_extra, legal_name=i['legal_name'].strip(), ssn=i['ssn'], approval_status="approved")

def user():
    users = [{"email": "user1@gmail.com", "first_name": "User1"},
            {"email": "user2@gmail.com", "first_name": "User2"}]
    for i in users:
        email = i["email"]
        password = "foodie123"
        user = User.objects.create_user(email, email, password, first_name=i['first_name'])
        user_extra = UserExtra.objects.create(user_id=user, phone="1111111111", user_type='customer')


# if __name__=="__main__":
business_data()
menu_items()
offers()
delivery_persons()
user()
