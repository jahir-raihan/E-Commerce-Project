from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from user.models import Address
from user.algorithms import get_client_ip
import json
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
import shortuuid
# Checkout


def checkout(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        if request.user.is_authenticated and data['save_address'] == 'true':
            adrs = Address(
                address=data['address[address]'],
                city=data['address[city]'],
                zipcode=data['address[zipcode]'],
                user=request.user
            )
            adrs.save()

        # Drilling out address from anywhere
        address = ''
        city = ''
        if 'address' in data:
            tmp_address = Address.objects.get(pk=data['address'])
            city = tmp_address.city
            address += tmp_address.address + ' ' + 'City: ' + tmp_address.city + ', Zip: ' + f'{tmp_address.zipcode}'
        else:
            address += data['address[address]'] + ' ' + 'City: ' + data['address[city]'] + ', Zip: ' +\
                       data['address[zipcode]']
            city = data['address[city]']

        # Taking phone number and fucking user data (registered or unregistered)
        user = None
        phone = data['phone']

        if data['guest_checkout'] == 'true':
            name = data['first_name'] + ' ' + data['last_name']
            email = data['email']
        elif request.user.is_authenticated:
            name = request.user.name
            email = request.user.email
        else:
            name = data['first_name'] + ' ' + data['last_name']
            email = data['email']
        if request.user.is_authenticated:
            user = request.user

        # Calculating asshole price of shitty cart items
        items_count = 0
        for i in map(int, data.getlist('items_quantity[]')):
            items_count += i

        # Generating naughty order id

        order_id = OrderID.objects.get(id=1)
        order_id.order_id += 1
        order_id.save()

        # Gathering items data to scoot them

        items = {
            "ids": data.getlist('items_ids[]'),
            "prices": data.getlist('items_prices[]'),
            "sizes": data.getlist('items_sizes[]'),
            "quantities": data.getlist('items_quantities[]')
        }
        tran_id = shortuuid.ShortUUID('1234567890WqQZzLlSsXx').random(15)

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
            order_total_price=float(data['total_price']),
            order_payment_method=data['payment_method'],
            note_msg=data['note_to_seller'],
        )

        order.save()

        print('Amount ', data['total_price'])

        # Payment method stuff

        # If Cash on delivery (I don't trust you bitch) Do your job here -- Redirect user to account page

        if data['payment_method'] == 'cod':
            return JsonResponse({'url': f"{request.META['HTTP_ORIGIN']}/account/order-history/"})

        # If bkash do it here , what the fuck is this

        #  We'll do bkash lately
        # If sslcommerze do your naughty work here bitch
        if data['payment_method'] == 'sslcom':
            setting = {'store_id': settings.STORE_ID, 'store_pass': settings.STORE_PASS, 'issandbox': True}
            sslcz = SSLCOMMERZ(setting)
            post_body = {'total_amount': data['total_price'], 'currency': "BDT", 'tran_id': f'{tran_id}',
                         'success_url': f"{request.META['HTTP_ORIGIN']}/account/order-history/",
                         'fail_url': f"{request.META['HTTP_ORIGIN']}/cart/",
                         'cancel_url': f"{request.META['HTTP_ORIGIN']}/cart/",
                         'emi_option': 0,
                         'cus_name': name,
                         'cus_email': email, 'cus_phone': phone, 'cus_add1': "Null",
                         'cus_city': city, 'cus_country': "Bangladesh", 'shipping_method': "NO", 'multi_card_name': "",
                         'num_of_item': items_count, 'product_name': 'Cloths', 'product_category': "Cloths",
                         'product_profile': "general", 'value_a': [order.id]
                         }

            response = sslcz.createSession(post_body)  # API response

            return JsonResponse({'url': response['GatewayPageURL']})

    return render(request, 'order_info.html')

