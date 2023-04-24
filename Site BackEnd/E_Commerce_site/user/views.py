from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from order.models import *
from .forms import UserRegisterForm
from django.middleware.csrf import get_token
from .algorithms import *
from products.models import *
from django.db.models import Q

from django.db.models import Sum
import json
User = get_user_model()


# Create your views here.


def register_user(request):
    if request.user.is_authenticated and request.method == 'POST':
        return JsonResponse({'redirect': False})
    if request.user.is_authenticated:
        return redirect('redirect_origin')

    """View for register"""

    if request.method == 'POST' and not request.user.is_authenticated:
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            user = authenticate(request, email=form.cleaned_data['email'], password=request.POST['password1'])
            login(request, user)
            if 'redirect_url' in request.POST:
                return JsonResponse({'success': True, 'redirect': f'{request.POST["redirect_url"]}'})
            else:
                return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return JsonResponse({'error': True})

    return render(request, 'account/register.html')


def login_user(request):
    if request.user.is_authenticated and request.method == 'POST':
        return JsonResponse({'redirect': False})
    if request.user.is_authenticated:
        return redirect('redirect_origin')

    """Login view """
    if request.method == 'POST' and not request.user.is_authenticated:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            if 'redirect_url' in request.POST:
                return JsonResponse({'success': True, 'redirect': f'{request.POST["redirect_url"]}'})
            else:
                return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return JsonResponse({'error': True})
    return render(request, 'account/login.html')


@login_required
def logout_user(request):

    """Logs out a user"""

    pass


def redirect_origin(request):
    return render(request, 'redirect_user_base_url.html')


# Staff panel

def staff_main1(request):
    if request.method == 'POST':
        query = request.POST['query']
        orders = Order.objects.filter(
            Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(
                order_person_email__icontains=query)
            | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query)
        )
    else:
        orders = Order.objects.filter(order_handled_by=request.user.id).order_by('order_handle_date')

    real_orders = []
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    confirmed_orders = len(orders.filter(
        Q(order_is_confirmed=True) | Q(order_is_delivered=True)
    ))
    cancelled_orders = len(orders.filter(order_is_cancelled=True))
    token = get_token(request)
    context = {
        'orders': real_orders,
        'token': token,
        'confirmed_orders': confirmed_orders,
        'cancelled_orders': cancelled_orders
    }
    if request.method == 'POST':
        template = render_to_string('pending_orders_template.html', request=request, context=context)

        return JsonResponse({'template': template, 'token': token})

    return render(request, 'staff_main.html', context)


def staff_main2(request):
    if request.method == 'POST':
        pass
    products = Product.objects.filter(product_added_by=request.user)

    return render(request, 'staff2_main.html', {'products': products})


def pending_orders(request):
    if request.method == 'POST' or 's' in request.GET:
        try:
            query = request.POST['query']
        except:
            if 's' in request.GET:
                query = request.GET['s']

        orders = Order.objects.filter(
            Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(
                order_person_email__icontains=query)
            | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query)
        )
    else:
        orders = Order.objects.filter(order_is_pending=True).order_by('order_date')

    real_orders = []
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    token = get_token(request)
    context = {
        'orders': real_orders,
        'token': token
    }
    if request.method == 'POST' or 's' in request.GET:
        template = render_to_string('pending_orders_template.html', request=request, context=context)

        return JsonResponse({'template': template, 'token': token})

    return render(request, 'staff_pending_orders.html', context)


def pending_order_action(request):

    action = request.POST['action']
    order = Order.objects.get(pk=request.POST['order_id'])

    if action == 'confirm':
        order.order_is_confirmed = True
        order.order_is_pending = False
    else:
        order.order_is_cancelled = True
        order.order_is_pending = False
    import datetime
    order.order_handle_date = datetime.datetime.now()
    order.order_handled_by = request.user.id
    order.save()
    token = get_token(request)

    return JsonResponse({'success': True, 'token': token, 'cancelled': order.order_is_cancelled,
                         'confirmed': order.order_is_confirmed})


def add_products(request):
    if request.method == 'POST':
        data = request.POST
        if data['category'] == '':
            category = Category(category_name=data['category_new'])
            category.save()
        else:
            category = Category.objects.get(pk=data['category'])

        product = Product(
            product_title=data['title'].lower(),
            product_code=data['product_code'],
            product_price=data['price'],
            product_category=category,
            color_type=data['color_type'],
            yarn_type=data['yarn_type'],
            yarn_count=data['yarn_count'],
            brand=data['brand'],
            product_in_stock=bool(data['status']),
            product_tags=data['tags'].lower(),
            product_primary_image=request.FILES['primary_image'],
            product_more_information=data['more_info'].lower(),
            product_search_keyword=data['search_keywords'].lower(),
        )

        if 'on_discount' in data:
            on_discount(data, product)
        product.save()
        #  Save all images

        alt_texts = request.POST['image_alt_texts']
        images = request.FILES.getlist('images')
        save_product_images(product, alt_texts.split(','), images)

        new_token = get_token(request)

        return JsonResponse({'success': True, 'token': new_token, 'edit': False})

    categories = Category.objects.all()
    discount_reasons = DiscountReason.objects.all()

    context = {
        'categories': categories,
        'discount_reasons': discount_reasons
    }
    return render(request, 'add_a_product.html', context)


def edit_products(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        save_edited_product(product, request)
        new_token = get_token(request)
        return JsonResponse({'success': True, 'token': new_token, 'edit': True})

    product = Product.objects.get(pk=pk)
    product_images = product.productimages_set.all()
    context = {
        'product': product,
        'product_images': product_images
    }

    return render(request, 'add_a_product.html', context)

# User Section


@csrf_exempt
def account(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(order_person=request.user).order_by('-order_date')
    else:
        orders = Order.objects.filter(order_person_ip=get_client_ip(request)).order_by('-order_date')
    real_orders = []

    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    context = {
        'orders': real_orders
    }

    return render(request, 'page_profile.html', context)


@csrf_exempt
def order_history(request):
    if request.method == 'POST':

        # Response from sslcommerze payment system

        data = request.POST
        order_id = data['value_a']
        order = Order.objects.get(pk=order_id)

        transaction_method = 'sslcom'
        if data['card_issuer'] == 'Bkash Mobile Banking':
            transaction_method = 'bkash'

        tran = Transaction(
            transaction_id=data['tran_id'],
            transaction_amount=float(data['store_amount']),
            transaction_method=transaction_method,
            bank_tran_id=data['bank_tran_id'],
            transaction_person=order.order_person,
            transaction_person_name=order.order_person_name,
            transaction_person_phone=order.order_person_phone,
            transaction_person_email=order.order_person_email,
            transaction_person_ip=order.order_person_ip,
            order=order
        )
        tran.save()

    if request.user.is_authenticated:
        orders = Order.objects.filter(order_person=request.user).order_by('-order_date')
    else:
        orders = Order.objects.filter(order_person_ip=get_client_ip(request)).order_by('-order_date')
    real_orders = []

    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    token = get_token(request)
    context = {
        'orders': real_orders,
        'token': token
    }

    return render(request, 'order_history.html', context)


def query_order_history(request):
    if request.method == 'POST':
        query = request.POST['query']
        orders = Order.objects.filter(
            Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(order_person_email__icontains=query)
            | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query)
        )
        real_orders = []
        for order in orders:
            o_items = json.loads(order.order_items)
            items = []
            for idx in range(len(o_items['ids'])):
                tmp = {
                    'item': Product.objects.get(pk=o_items['ids'][idx]),
                    'quantity': o_items['quantities'][idx],
                    'size': o_items['sizes'][idx],
                    'price': o_items['prices'][idx]
                }
                items.append(tmp)

            real_orders.append(
                {
                    "order": order,
                    "items": items
                }
            )

        token = get_token(request)
        context = {
            'orders': real_orders,
            'token': token
        }
        template = render_to_string('order_history_search_template.html', request=request, context=context)

        return JsonResponse({'template': template, 'token': token})
# Wishlist section


def save_wishlist_item(request):
    product = Product.objects.get(pk=request.POST['product_id'])
    product.wish_count += 1
    product.save()
    try:
        wishlist_obj = WishList.objects.get(wisher_person=request.user)
        items = json.loads(wishlist_obj.wishlist_items)
        items.append(product.id)
        wishlist_obj.wishlist_items = f'{items}'
        wishlist_obj.save()
    except:
        wishlist_obj = WishList(wishlist_items=f'[{product.id}]', wisher_person=request.user,
                                wisher_person_ip=get_client_ip(request))
        wishlist_obj.save()
    token = get_token(request)
    return JsonResponse({'success': True, 'token': token})


def remove_wishlist_item(request):

    product = Product.objects.get(pk=request.GET['product_id'])
    product.wish_count -= 1
    product.save()

    wishlist_obj = WishList.objects.get(wisher_person=request.user)
    items = json.loads(wishlist_obj.wishlist_items)
    items.remove(product.id)
    wishlist_obj.wishlist_items = f'{items}'
    wishlist_obj.save()


    return JsonResponse({'success': True, 'items_count': len(items)})


def wishlist(request):
    items = []
    try:
        wishlist_itm = WishList.objects.get(wisher_person=request.user)

        for p_id in json.loads(wishlist_itm.wishlist_items):
            product = Product.objects.get(pk=p_id)
            items.append(product)
    except:pass
    context = {
        'items': items
    }
    return render(request, 'wishlist.html', context)


def check_product_availability(request):
    product = Product.objects.get(pk=request.GET['p_id'])
    context = {
        'status': True if product.product_in_stock else False
    }
    return JsonResponse(context)

# Admin section


def dashboard(request):

    total_earnings = Order.objects.filter(order_is_confirmed=True).aggregate(Sum('order_total_price'))['order_total_price__sum']
    total_orders = Order.objects.filter(order_is_confirmed=True).count()
    total_products = Product.objects.all().count()

    orders = Order.objects.all().order_by('-order_date')[:50]

    context = {
        'total_earnings': total_earnings,
        'total_orders': total_orders,
        'total_products': total_products,
        'orders': orders
    }
    return render(request, 'admin/dashboard.html', context)


def admin_product_list(request):

    if request.method == 'POST':

        query = request.POST['query']
        category = Category.objects.filter(category_name__icontains=query)
        reasons = DiscountReason.objects.filter(discount_reason__icontains=query)

        products_list = Product.objects.filter(
            Q(product_title__icontains=query) | Q(brand__icontains=query) | Q(product_tags__icontains=query) |
            Q(product_search_keyword__icontains=query) | Q(product_more_information__icontains=query) |
            Q(product_category__in=category) | Q(discount_reason__in=reasons)

        )

        token = get_token(request)
        context = {
            'products': products_list,
        }
        template = render_to_string('admin/product_list_template.html', context=context, request=request)

        return JsonResponse({'template': template, 'token': token})

    products = Product.objects.all().order_by('-product_last_update')
    context = {
        'products': products
    }
    return render(request, 'admin/products_list.html', context)


def admin_add_product(request):
    if request.method == 'POST':
        data = request.POST
        if data['category'] == '':
            category = Category(category_name=data['category_new'])
            category.save()
        else:
            category = Category.objects.get(pk=data['category'])

        product = Product(
            product_title=data['title'].lower(),
            product_code=data['product_code'],
            product_price=data['price'],
            product_category=category,
            color_type=data['color_type'],
            yarn_type=data['yarn_type'],
            yarn_count=data['yarn_count'],
            brand=data['brand'],
            product_in_stock=bool(data['status']),
            product_tags=data['tags'].lower(),
            product_primary_image=request.FILES['primary_image'],
            product_more_information=data['more_info'].lower(),
            product_search_keyword=data['search_keywords'].lower(),
        )

        if 'on_discount' in data:
            on_discount(data, product)
        product.save()
        #  Save all images

        alt_texts = request.POST['image_alt_texts']
        images = request.FILES.getlist('images')
        save_product_images(product, alt_texts.split(','), images)

        new_token = get_token(request)

        return JsonResponse({'success': True, 'token': new_token, 'edit': False})

    categories = Category.objects.all()
    discount_reasons = DiscountReason.objects.all()

    context = {
        'categories': categories,
        'discount_reasons': discount_reasons
    }
    return render(request, 'admin/add_edit_products.html', context)


def admin_edit_product(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        save_edited_product(product, request)
        new_token = get_token(request)
        return JsonResponse({'success': True, 'token': new_token, 'edit': True})

    product = Product.objects.get(pk=pk)
    product_images = product.productimages_set.all()
    context = {
        'product': product,
        'product_images': product_images
    }

    return render(request, 'admin/add_edit_products.html', context)


def admin_orders(request):
    if request.method == 'POST' or 's' in request.GET:
        try:
            query = request.POST['query']
        except:
            if 's' in request.GET:
                query = request.GET['s']

        orders = Order.objects.filter(
            Q(order_id__icontains=query) | Q(order_person_name__icontains=query) | Q(
                order_person_email__icontains=query)
            | Q(order_person_phone__icontains=query) | Q(order_payment_method__icontains=query)
        )
    else:
        orders = Order.objects.filter(order_is_pending=True).order_by('order_date')

    real_orders = []
    for order in orders:
        o_items = json.loads(order.order_items)
        items = []
        for idx in range(len(o_items['ids'])):
            tmp = {
                'item': Product.objects.get(pk=o_items['ids'][idx]),
                'quantity': o_items['quantities'][idx],
                'size': o_items['sizes'][idx],
                'price': o_items['prices'][idx]
            }
            items.append(tmp)

        real_orders.append(
            {
                "order": order,
                "items": items
            }
        )

    token = get_token(request)
    context = {
        'orders': real_orders,
        'token': token
    }
    if request.method == 'POST':
        template = render_to_string('pending_orders_template.html', request=request, context=context)

        return JsonResponse({'template': template, 'token': token})

    return render(request, 'admin/orders.html', context)


def admin_transactions(request):
    if request.method == 'POST':
        query = request.POST['query']
        context = {
            'transactions': 'transactions',
        }
        token = get_token(request)
        template = render_to_string('admin/transactions_template.html', context, request)

        return JsonResponse({'template': template, 'token': token})

    return render(request, 'admin/transactions.html')