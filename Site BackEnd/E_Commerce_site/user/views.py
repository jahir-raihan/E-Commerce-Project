from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from order.models import Order
from .forms import UserRegisterForm
from products.models import Product, ProductImages, Category, DiscountReason
from django.middleware.csrf import get_token
from .algorithms import *
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
            user = authenticate(request, email=request.POST['email'], password=request.POST['password1'])
            login(user, request)
            if 'redirect_url' in request.POST:
                return JsonResponse({'success': True, 'redirect': f'{request.POST["redirect_url"]}'})
            else:
                return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return JsonResponse({'error': True})

    return render(request, 'register.html')


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
    return render(request, 'login.html')


@login_required
def logout_user(request):

    """Logs out a user"""

    pass


def redirect_origin(request):
    return render(request, 'redirect_user_base_url.html')


# Staff panel

def staff_main1(request):
    if request.method == 'POST':
        pass

    return render(request, 'staff_main.html')


def staff_main2(request):
    if request.method == 'POST':
        pass
    products = Product.objects.filter(product_added_by=request.user)

    return render(request, 'staff2_main.html', {'products': products})


def pending_orders(request):
    if request.method == 'POST':
        pass

    return render(request, 'staff_pending_orders.html')


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
        orders = Order.objects.filter(order_person=request.user)
    else:
        orders = Order.objects.filter(order_person_ip=get_client_ip(request))
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
    if request.user.is_authenticated:
        orders = Order.objects.filter(order_person=request.user)
    else:
        orders = Order.objects.filter(order_person_ip=get_client_ip(request))
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
    print(real_orders)
    context = {
        'orders': real_orders
    }

    return render(request, 'order_history.html', context)


def wishlist(request):
    return render(request, 'wishlist.html')