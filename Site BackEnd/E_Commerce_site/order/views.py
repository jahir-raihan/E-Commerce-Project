from django.shortcuts import render
from .models import *
from user.models import Address
from user.algorithms import get_client_ip
import json
# Checkout


def checkout(request):
    if request.method == 'POST':
        data = request.POST

        # Drilling out address from anywhere
        address = ''
        if 'address' in data:
            tmp_address = Address.objects.get(pk=data['address'])
            address += tmp_address.address + ' ' + 'City: ' + tmp_address.city + ', Zip: ' + f'{tmp_address.zipcode}'
        else:
            address += data['address[address]'] + ' ' + 'City: ' + data['address[city]'] + ', Zip: ' +\
                       data['address[zipcode]']

        # Taking phone number and fucking user data (registered or unregistered)
        user = None
        phone = data['phone']

        if data['guest_checkout'] == 'true':
            name = data['first_name'] + ' ' + data['last_name']
            email = data['email']
        else:
            name = request.user.name
            email = request.user.email
            user = request.user

        # Calculating asshole price of shitty cart items

        price = 0
        for i in map(int, data.getlist('items_prices[]')):
            price += i

        # Generating naughty order id

        order_id = OrderID.objects.get(id=1)
        order_id.order_id += 1
        order_id.save()

        # Gathering items data to scoot them

        items = {
            "ids": data.getlist('items_ids[]'),
            "prices": data.getlist('items_prices[]'),
            "sizes": data.getlist('items_sizes[]')
        }

        # Creating order instance

        order = Order(
            order_id=order_id.order_id,
            order_items=json.dumps(items),
            delivery_location=address,
            order_person_name=name,
            order_person_phone=phone,
            order_person_email=email,
            order_person_ip=get_client_ip(request),
            order_person=user,
            order_total_price=price,
            order_payment_method=data['payment_method'],
            note_msg=data['note_to_seller'],
        )

        order.save()

        # Payment method stuff

        # If Cash on delivery (I don't trust you bitch) Do your job here -- Redirect user to account page

        # If bkash do it here , what the fuck is this

        # If sslcommerze do your naughty work here bitch

    return render(request, 'order_info.html')

