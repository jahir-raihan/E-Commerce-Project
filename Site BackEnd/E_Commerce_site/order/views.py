from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from user.models import Address
from user.algorithms import get_client_ip
import json
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
import shortuuid


def checkout(request):

    """Checkout view if there's items in the cart"""

    # No need to check this page for routing , cz it's already in stealth mode

    if request.method == 'POST':
        data = request.POST

        # Saving  Address Data if save address is checked in frontEnd, and user is registered.

        if request.user.is_authenticated and data['save_address'] == 'true':
            adrs = Address(
                address=data['address[address]'],
                city=data['address[city]'],
                zipcode=data['address[zipcode]'],
                user=request.user
            )
            adrs.save()

        # Getting Address Data

        address = ''
        if 'address' in data:
            tmp_address = Address.objects.get(pk=data['address'])
            city = tmp_address.city
            address += tmp_address.address + ' ' + 'City: ' + tmp_address.city + ', Zip: ' + f'{tmp_address.zipcode}'
        else:
            address += data['address[address]'] + ' ' + 'City: ' + data['address[city]'] + ', Zip: ' +\
                       data['address[zipcode]']
            city = data['address[city]']

        # Retrieving user data (Registered / Unregistered)

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

        # Calculating items quantity -> tity ->

        items_count = 0
        for i in map(int, data.getlist('items_quantity[]')):
            items_count += i

        # Generating  order id

        order_id = OrderID.objects.get(id=1)
        order_id.order_id += 1
        order_id.save()

        # Gathering items data to store them as compressed string json data

        items = {
            "ids": data.getlist('items_ids[]'),
            "prices": data.getlist('items_prices[]'),
            "sizes": data.getlist('items_sizes[]'),
            "quantities": data.getlist('items_quantities[]')
        }

        tran_id = shortuuid.ShortUUID('1234567890WqQZzLlSsXxYyTtEeBbQqPpNnMmSs').random(25)

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

        # Payment method

        # If Cash on delivery (User doesn't trust you) --> Redirect user to account page

        if data['payment_method'] == 'cod':
            try:
                return JsonResponse({'url': f"{request.META['HTTP_ORIGIN']}/account/order-history/"})
            except:
                return JsonResponse({'response': 'Cash on delivery was successful'})

        # If sslcommerze or bkash , Redirect them to payment page

        # Actually We'll do bkash lately

        # If sslcommerze

        if data['payment_method'] == 'sslcom':

            # Initiating payment

            setting = {'store_id': settings.STORE_ID, 'store_pass': settings.STORE_PASS, 'issandbox': True}
            sslcz = SSLCOMMERZ(setting)

            post_body = {'total_amount': data['total_price'], 'currency': "BDT", 'tran_id': f'{tran_id}',

                         # Extra check only for testing purpose -> cz META is not available in django client request
                         'success_url': 'test_url' if 'test' in data else f"{request.META['HTTP_ORIGIN']}/account/order-history/",
                         'fail_url': 'test_url' if 'test' in data else f"{request.META['HTTP_ORIGIN']}/cart/",
                         'cancel_url': 'test_url' if 'test' in data else f"{request.META['HTTP_ORIGIN']}/cart/",

                         'emi_option': 0,
                         'cus_name': name,
                         'cus_email': email, 'cus_phone': phone, 'cus_add1': "Null",
                         'cus_city': city, 'cus_country': "Bangladesh", 'shipping_method': "NO", 'multi_card_name':"",
                         'num_of_item': items_count, 'product_name': 'Cloths', 'product_category': "Cloths",
                         'product_profile': "general", 'value_a': [order.id]
                         }

            response = sslcz.createSession(post_body)  # API response

            return JsonResponse({'url': response['GatewayPageURL']})

    return render(request, 'order_info.html')


def get_pending_order_count(request):

    """Returns pending order count"""

    orders = Order.objects.filter(order_is_pending=True).count()
    return JsonResponse({'count': orders})
