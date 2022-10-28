from datetime import datetime
from foodie.models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    title = "Home"
    if request.user.is_authenticated:
        user_extra = UserExtra.objects.filter(user_id=request.user)
        if user_extra:
            user_extra = user_extra[0]
            if user_extra.user_type == "business":
                return redirect('/business-orders')
            if user_extra.user_type == "delivery":
                return redirect('/delivery-person-orders')
        return redirect("/search-restaurants")
    return render(request, "index.html", locals())


def userprofiles(request):
    title = "UserProfile"
    try:
        userprofiledata = UserProfile.objects.get(user_id=request.user)
    except:
        userprofiledata = None
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        dob = request.POST.get('dob',  False)
        favorite_food = request.POST.get('favorite_food', False)
        gender = request.POST.get('gender', False)
        favorite_restaurant = request.POST.get('favorite_restaurant', False)
        if userprofiledata:
            userprofiledata = UserProfile.objects.filter(id=userprofiledata.id).update(
                dob=dob, favorite_food=favorite_food, gender=gender, favorite_restaurant=favorite_restaurant)
        else:
            userprofiledata = UserProfile(user_id=request.user, dob=dob, favorite_food=favorite_food,
                                          gender=gender, favorite_restaurant=favorite_restaurant)
            userprofiledata.save()
        return redirect('/user-profile')

    return render(request, "userprofile.html", locals())


def search_restaurants(request):
    title = "Search Restaurants"
    user_default = Default.objects.filter(user_id=request.user).all()
    if user_default:
        default_address = user_default[0].address_id
        if default_address:
            default_zipcode = default_address.zipcode
            is_modal = False
        else:
            default_address = ""
            default_zipcode = ""
            is_modal = True
    else:
        default_address = ""
        default_zipcode = ""
        is_modal = True

    restaurants = BusinessExtra.objects.filter(
        business_zipcode=default_zipcode, approval_status="approved")

    if request.POST:
        all_restaurants = BusinessExtra.objects.filter(
            approval_status="approved")

        search_keyword = request.POST.get("search_keyword")

        restaurants = []
        for restaurant in all_restaurants:
            if search_keyword.strip().lower() in restaurant.legal_name.strip().lower():
                restaurants.append(restaurant)

    return render(request, "food_home.html", locals())


def user_view(request):
    title = "{} {}".format(request.user.first_name, request.user.last_name)
    return render(request, "user_view.html", locals())


def add_default_address(request):
    if request.method == 'POST':
        data = request.POST

        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zipcode')

        address_obj = Address.objects.filter(
            user_id=request.user, street=street, city=city, state=state, zipcode=zipcode)

        if not address_obj:
            address = Address.objects.create(
                user_id=request.user, street=street, city=city, state=state, zipcode=zipcode)
        else:
            address = address_obj[0]

        default = Default.objects.filter(user_id=request.user).all()

        if default:
            default.update(address_id=address)
        else:
            Default.objects.create(user_id=request.user, address_id=address)

    return redirect("/")


def business_orders(request):
    title = "Business Order"
    business = BusinessExtra.objects.filter(user_id=request.user)
    if business:
        new_orders = Order.objects.filter(
            restaurant_id=business[0], status='ordered').all()
        new_orders_dict = {}
        for order in new_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            new_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
        confirmed_orders = Order.objects.filter(
            restaurant_id=business[0], status='confirmed').all()
        confirmed_orders_dict = {}
        for order in confirmed_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            confirmed_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
        preparing_orders = Order.objects.filter(
            restaurant_id=business[0], status='preparing').all()
        preparing_orders_dict = {}
        for order in preparing_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            preparing_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
        ready_orders = Order.objects.filter(
            restaurant_id=business[0], status='ready').all()
        ready_orders_dict = {}
        for order in ready_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            ready_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
    else:
        return redirect("/")

    return render(request, "business_orders.html", locals())


def confirm_order(request, order_id):
    try:
        business = BusinessExtra.objects.get(user_id=request.user)
        order = Order.objects.get(id=order_id, restaurant_id=business)
    except:
        return render(request, "404.html")

    Order.objects.filter(id=order.id).update(status="confirmed")

    return redirect("/business-orders")


def prepare_order(request, order_id):
    try:
        business = BusinessExtra.objects.get(user_id=request.user)
        order = Order.objects.get(id=order_id, restaurant_id=business)
    except:
        return render(request, "404.html")

    Order.objects.filter(id=order.id).update(status="preparing")

    return redirect("/business-orders")


def ready_order(request, order_id):
    try:
        business = BusinessExtra.objects.get(user_id=request.user)
        order = Order.objects.get(id=order_id, restaurant_id=business)
    except:
        return render(request, "404.html")

    Order.objects.filter(id=order.id).update(status="ready")

    return redirect("/business-orders")


def accept_order_delivery(request, order_id):
    try:
        delivery = DeliveryPersonExtra.objects.get(user_id=request.user)
        order = Order.objects.get(id=order_id)
    except:
        return render(request, "404.html")

    Order.objects.filter(id=order.id).update(
        status="delivery-accepted", delivery_id=delivery)

    return redirect("/business-orders")


def order_out_delivery(request, order_id):
    try:
        delivery = DeliveryPersonExtra.objects.get(user_id=request.user)
        order = Order.objects.get(id=order_id, delivery_id=delivery)
    except:
        return render(request, "404.html")

    Order.objects.filter(id=order.id).update(status="out")

    return redirect("/business-orders")


def order_delivered(request, order_id):
    try:
        delivery = DeliveryPersonExtra.objects.get(user_id=request.user)
        order = Order.objects.get(id=order_id, delivery_id=delivery)
    except:
        return render(request, "404.html")

    Order.objects.filter(id=order.id).update(status="delivered")

    return redirect("/business-orders")


def delivery_person_orders(request):
    delivery = DeliveryPersonExtra.objects.filter(user_id=request.user)
    if delivery:
        ready_orders = Order.objects.filter(status='ready').all()
        ready_orders_dict = {}
        for order in ready_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            ready_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
        accepted_orders = Order.objects.filter(
            status='delivery-accepted', delivery_id=delivery[0])
        accepted_orders_dict = {}
        for order in accepted_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            accepted_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
        out_orders = Order.objects.filter(
            status='out', delivery_id=delivery[0])
        out_orders_dict = {}
        for order in out_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            out_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
        delivered_orders = Order.objects.filter(
            status='delivered', delivery_id=delivery[0])
        delivered_orders_dict = {}
        for order in delivered_orders:
            order_items = OrderItem.objects.filter(order_id=order)
            delivered_orders_dict[order.id] = {
                'order': order, 'order_items': order_items}
    else:
        return redirect("/")
    return render(request, "delivery_person_orders.html", locals())


def about_us(request):
    title = "About Us"
    return render(request, "aboutus.html", locals())


def contact_us(request):
    title = "Contact Us"
    if request.method == 'POST':
        data = request.POST
        firstname = data.get('first_name')
        lastname = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone')
        information = data.get('message')

        contact = Contact.objects.create(
            first_name=firstname, last_name=lastname, email=email, phone=phone_number, message=information)
        text = "Thank you for submiting, Our representative will get in touch with you. Happy Eating!"
    return render(request, "contactus.html", locals())


def login_view(request):
    title = "Login"
    next = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        data = request.POST
        email_address = data.get("email")
        password = data.get("password")
        user = authenticate(username=email_address, password=password)
        if user and user.is_active:
            user_extra = UserExtra.objects.filter(user_id=user)
            if user_extra:
                user_extra = user_extra[0]
                user_type = user_extra.user_type
                user_obj = user
                if user_extra.user_type == "business":
                    extra_obj = BusinessExtra.objects.filter(
                        user_id=user, user_extra_id=user_extra)
                    if not extra_obj:
                        return render(request, "extra_information.html", locals())
                    elif extra_obj[0].approval_status == 'pending_approval':
                        message = "Your Profile is waiting for Approval."
                        return render(request, "message.html", locals())

                if user_extra.user_type == "delivery":
                    extra_obj = DeliveryPersonExtra.objects.filter(
                        user_id=user, user_extra_id=user_extra)
                    if not extra_obj:
                        return render(request, "extra_information.html", locals())
                    elif extra_obj[0].approval_status == 'pending_approval':
                        message = "Your Profile is waiting for Approval."
                        return render(request, "message.html", locals())
            login(request, user)
            request.session['username'] = email_address
            if next:
                return redirect(next)

            return redirect('/')
        else:
            message = "Invalid Credentials"
    return render(request, "login.html", locals())


def signup(request):
    title = "Sign Up"
    if request.method == "POST":
        data = request.POST
        email_address = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        confirm_password = data.get('confirm_password')
        user_type = data.get('user_type')
        if password != confirm_password:
            message = "Password and Confirm Password should match."
            return render(request, "signup.html", locals())
        user_obj = User.objects.filter(username=email_address)
        if not user_obj:
            user = User.objects.create_user(
                email_address, email_address, password, first_name=first_name, last_name=last_name)
            user_obj = user
            if user:
                user_extra = UserExtra.objects.create(
                    user_id=user, phone=phone, user_type=user_type)
            if user_type == "delivery" or user_type == "business":
                return render(request, "extra_information.html", locals())
            else:
                return redirect('/')
        else:
            message = "User Already Existed! Try Sign In or Create a new one with different email."
    return render(request, "signup.html", locals())


def extra_information(request):
    if request.method == "POST":
        data = request.POST

        user_type = data.get("user_type")
        user_obj = User.objects.get(id=data.get("user_id"))
        user_extra = UserExtra.objects.get(id=data.get("user_extra_id"))

        if user_type == 'business':
            legal_name = data.get("legal_name")
            business_address = data.get("business_address")
            business_city = data.get("business_city")
            business_state = data.get("business_state")
            business_zipcode = data.get("business_zipcode")
            approval_status = "pending_approval"

            business_extra = BusinessExtra.objects.create(user_id=user_obj, user_extra_id=user_extra, legal_name=legal_name, business_address=business_address,
                                                          business_city=business_city, business_state=business_state, business_zipcode=business_zipcode, approval_status=approval_status)
        if user_type == 'delivery':
            legal_name = data.get("legal_name")
            ssn = data.get("ssn")
            approval_status = "pending_approval"
            delivery_extra = DeliveryPersonExtra.objects.create(
                user_id=user_obj, user_extra_id=user_extra, legal_name=legal_name, ssn=ssn, approval_status=approval_status)

        success = True
    return render(request, "extra_information.html", locals())


def add_menu_item(request):
    title = "Add Menu Item"
    if request.method == "POST":
        data = request.POST
        item_name = data.get('item_name')
        item_price = data.get('item_price')
        restaurant = BusinessExtra.objects.filter(user_id=request.user)
        no_item = Menu.objects.filter(
            item_name=item_name, item_price=item_price, restaurant_id=restaurant[0])
        if not no_item:
            item = Menu.objects.create(
                item_name=item_name, item_price=item_price, restaurant_id=restaurant[0])
            message = "New Item '{}' Added to the Menu".format(item_name)
            return redirect("/menu-items")

    return render(request, "add_menu_item.html", locals())


def edit_menu_item(request, menu_id):
    title = "Edit Menu Item"
    try:
        menu = Menu.objects.get(id=menu_id)
    except:
        return render(request, "404.html", locals())
    if request.method == "POST":
        data = request.POST
        item_name = data.get('item_name')
        item_price = data.get('item_price')
        restaurant = BusinessExtra.objects.filter(user_id=request.user)
        item = Menu.objects.filter(id=menu_id)
        if item:
            item = item.update(
                item_name=item_name, item_price=item_price)
            message = "New Item '{}' Added to the Menu".format(item_name)
            return redirect("/menu-items")

    return render(request, "edit_menu_item.html", locals())


def help(request):
    return render(request, "help.html", locals())


def logout_view(request):
    logout(request)
    return redirect("/")


def payment_methods(request):
    title = "Payment Methods"
    payment_methods = PaymentMethod.objects.filter(user_id=request.user)
    return render(request, "payment_methods.html", locals())


def addresses(request):
    title = "Addresses"
    addresses = Address.objects.filter(user_id=request.user)
    return render(request, "addresses.html", locals())


def restaurant_view(request, restaurant_id):
    try:
        restaurant = BusinessExtra.objects.get(id=restaurant_id)
        title = restaurant.legal_name
    except:
        title = "404"
        return render(request, "404.html", locals())

    restaurant_reviews = RatingReviewRestaurant.objects.filter(
        user_id=request.user, restaurant_id_id=restaurant_id)

    menu_items = Menu.objects.filter(restaurant_id=restaurant).all()
    is_favorite = False
    favorite = FavoriteRestaurant.objects.filter(
        user_id=request.user, restaurant_id=restaurant)
    if favorite:
        is_favorite = True

    cart_item_dict = {}
    for cart_item in request.cart_items:
        cart_item_dict[cart_item.item_id.id] = {
            "cart_item_id": cart_item.id, "quantity": cart_item.quantity}

    menu_items_dict = {}
    for item in menu_items:
        menu_items_dict[item.id] = {
            "item_name": item.item_name, "item_price": item.item_price}
        if cart_item_dict.get(item.id):
            menu_items_dict[item.id]["cart_item_id"] = cart_item_dict.get(
                item.id).get("cart_item_id")
            menu_items_dict[item.id]["quantity"] = cart_item_dict.get(
                item.id).get("quantity")
        else:
            menu_items_dict[item.id]["cart_item_id"] = ""
            menu_items_dict[item.id]["quantity"] = ""
        is_favorite_item = False
        favorite_item = FavoriteItem.objects.filter(
            user_id=request.user, item_id=item)
        if favorite_item:
            is_favorite_item = True

        menu_items_dict[item.id]["is_favorite"] = is_favorite_item

    return render(request, "restaurant_view.html", locals())


def add_cart_items(request, item_id):
    try:
        item = Menu.objects.get(id=item_id)
    except:
        return render(request, "404.html")

    cart = Cart.objects.filter(user_id=request.user)

    if cart:
        if cart[0].restaurant_id != item.restaurant_id:
            CartItem.objects.filter(cart_id=cart[0]).delete()
        cart.update(restaurant_id=item.restaurant_id)
        CartItem.objects.create(cart_id=cart[0], item_id=item, quantity=1)
    else:
        cart = Cart.objects.create(
            restaurant_id=item.restaurant_id, user_id=request.user)
        CartItem.objects.create(cart_id=cart, item_id=item, quantity=1)

    return redirect("/restaurant/{}".format(item.restaurant_id.id))


def cart_view(request):
    title = "Cart"
    return render(request, "cart_view.html", locals())


def cart_item_quanity_update(request, action):
    if request.method == "POST":
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('cart_item_count')
        if 'decrement' in action:
            cart_item = CartItem.objects.filter(id=cart_item_id)
            restaurant_id = cart_item[0].cart_id.restaurant_id.id
            if int(quantity) == 1:
                cart_item.delete()
            else:
                cart_item.update(quantity=int(quantity)-1)
        if 'increment' in action:
            cart_item = CartItem.objects.filter(id=cart_item_id)
            restaurant_id = cart_item[0].cart_id.restaurant_id.id
            cart_item.update(quantity=int(quantity)+1)
    if "restaurant" in action:
        return redirect("/restaurant/{}".format(restaurant_id))
    return redirect("/cart")


def checkout(request):
    title = "Checkout"
    cart_items = request.cart_items

    total_price = 0
    for item in cart_items:
        total_price += (item.item_id.item_price * item.quantity)

    total_price = round(total_price, 2)

    offers = Offer.objects.all()

    offers_dict = {}

    offer_id = ""

    for offer in offers:
        offers_dict[offer.promo_code] = (offer.discount, offer.id)

    addresses = Address.objects.filter(user_id=request.user)

    payment_methods = PaymentMethod.objects.filter(user_id=request.user)

    if request.method == "POST":
        data = request.POST

        promo = data.get("promo")

        if promo:
            discount = offers_dict[promo.strip()][0]
            discounted_price = total_price - \
                (total_price * discount / 100)
            discounted_price = round(discounted_price, 2)
            offer_id = offers_dict[promo.strip()][1]
            return render(request, "checkout.html", locals())

        offer_id = data.get('offer_id')
        total_price = data.get('total_price')
        payment_method_id = data.get('payment')
        address_id = data.get('address')

        if not payment_method_id or not address_id:
            messgae = "Pyament Method and Address are mandatory!"
            return render(request, "checkout.html", locals())

        order = Order.objects.create(
            user_id=request.user, restaurant_id=cart_items[0].item_id.restaurant_id, offer_id_id=offer_id, status="ordered", datetime=datetime.now(), total_price=total_price, payment_method_id_id=payment_method_id, address_id_id=address_id)

        for item in cart_items:
            order_item = OrderItem.objects.create(
                order_id=order, item_id=item.item_id, quantity=item.quantity)

        CartItem.objects.filter(cart_id=cart_items[0].cart_id).delete()
        Cart.objects.filter(user_id=request.user).delete()

        return render(request, "order_success.html", locals())
    return render(request, "checkout.html", locals())


def add_payment_method(request):
    title = "Add Payment Method"

    if request.method == "POST":
        data = request.POST
        cardnumber = data.get('cardnumber')
        cardname = data.get('cardname')
        cardtype = data.get('cardtype')
        expires = data.get('expires')
        cvv = data.get('cvv')
        payment = PaymentMethod.objects.create(
            user_id=request.user, cardnumber=cardnumber, cardname=cardname, cardtype=cardtype, expires=expires, cvv=cvv)
        message = "Payment succesfully completed"
        return redirect("/payment-methods")

    return render(request, "add_payment_method.html", locals())


def edit_payment_method(request, payment_method_id):
    title = "Edit Payment Method"

    try:
        payment_method = PaymentMethod.objects.get(id=payment_method_id)
    except:
        return render(request, "404.html")

    if request.method == "POST":
        data = request.POST
        cardnumber = data.get('cardnumber')
        cardname = data.get('cardname')
        cardtype = data.get('cardtype')
        expires = data.get('expires')
        cvv = data.get('cvv')
        payment = PaymentMethod.objects.filter(
            id=payment_method_id, user_id=request.user)
        if payment:
            payment.update(cardnumber=cardnumber, cardname=cardname,
                           cardtype=cardtype, expires=expires, cvv=cvv)
        message = "Payment succesfully completed"
        return redirect("/payment-methods")

    return render(request, "edit_payment_method.html", locals())


def add_address(request):
    title = "Add Address"

    if request.method == "POST":
        data = request.POST
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zipcode')
        address = Address.objects.create(
            user_id=request.user, street=street, state=state, city=city, zipcode=zipcode)
        message = "Added the address succesfully"
        return redirect("/addresses")

    return render(request, "add_address.html", locals())


def edit_address(request, address_id):
    title = "Edit Address"
    try:
        address = Address.objects.get(id=address_id)
    except:
        return render(request, "404.html", locals())
    if request.method == "POST":
        data = request.POST
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zipcode')
        address = Address.objects.filter(id=address_id, user_id=request.user)
        if address:
            address.update(street=street, state=state,
                           city=city, zipcode=zipcode)
        message = "Added the address succesfully"
        return redirect("/addresses")

    return render(request, "edit_address.html", locals())


def order_history(request):
    title = "Order History"
    orders = Order.objects.filter(user_id=request.user)

    all_orders = []
    for order in orders:
        dictn = {'order': order}
        order_items = OrderItem.objects.filter(order_id=order)

        dictn['order_items'] = order_items

        all_orders.append(dictn)

    return render(request, "orderhistory.html", locals())


def order_details(request, order_id):
    title = "Order Details"
    try:
        order = Order.objects.get(id=order_id)
    except:
        return render(request, "404.html")

    restaurant_reviews = RatingReviewRestaurant.objects.filter(
        user_id=request.user, restaurant_id=order.restaurant_id)
    if restaurant_reviews:
        restaurant_review = restaurant_reviews[0]
    else:
        restaurant_review = None

    items = OrderItem.objects.filter(order_id=order)

    total_price = 0
    for item in items:
        total_price += (item.item_id.item_price * item.quantity)

    total_price = round(total_price, 2)

    order_status = ""
    if order.status == "ordered":
        order_status = "Ordered, Waiting for restaurant approval."
    if order.status == "confirmed":
        order_status = "Order Confirmed"
    if order.status == "preparing":
        order_status = "Food is Preparing"
    if order.status == "ready":
        order_status = "Food is Ready for Delivery"
    if order.status == "out":
        order_status = "Food is Out for Delivery"
    if order.status == "delivered":
        order_status = "Delivered"

    return render(request, "order_details.html", locals())


def add_favorite_restaurant(request, restaurant_id):

    favorite_restaurant = FavoriteRestaurant.objects.filter(
        user_id=request.user, restaurant_id_id=restaurant_id)

    if favorite_restaurant:
        FavoriteRestaurant.objects.filter(
            user_id=request.user, restaurant_id_id=restaurant_id).delete()
    else:
        FavoriteRestaurant.objects.create(
            user_id=request.user, restaurant_id_id=restaurant_id)

    return redirect("/restaurant/{}".format(restaurant_id))


def add_favorite_item(request, item_id):
    try:
        item = Menu.objects.get(id=item_id)
    except:
        return render(request, "404.html")

    favorite_item = FavoriteItem.objects.filter(
        user_id=request.user, item_id_id=item_id)

    if favorite_item:
        FavoriteItem.objects.filter(
            user_id=request.user, item_id_id=item_id).delete()
    else:
        FavoriteItem.objects.create(
            user_id=request.user, item_id_id=item_id)

    return redirect("/restaurant/{}".format(item.restaurant_id.id))


def menu_items(request):
    title = "Menu Items"
    try:
        business = BusinessExtra.objects.get(user_id=request.user)
        menu_items = Menu.objects.filter(restaurant_id=business)
    except:
        return render(request, "404.html", locals())

    return render(request, "menu_items.html", locals())


def restaurant_review(request, restaurant_id):
    if request.method == "POST":
        data = request.POST
        restaurant_reviews = RatingReviewRestaurant.objects.filter(
            user_id=request.user, restaurant_id_id=restaurant_id)
        if restaurant_reviews:
            restaurant_reviews.update(rating=data.get(
                'rating_restaurant'), review=data.get('restaurant_review'))
        else:
            RatingReviewRestaurant.objects.create(user_id=request.user, restaurant_id_id=restaurant_id, rating=data.get(
                'rating_restaurant'), review=data.get('restaurant_review'))

        return redirect('/order-details/{}'.format(data.get('order_id')))


def favorites(request):
    title = "Favorites"
    favorite_items = FavoriteItem.objects.filter(user_id=request.user)
    favorite_restaurants = FavoriteRestaurant.objects.filter(
        user_id=request.user)

    return render(request, 'favorites.html', locals())
