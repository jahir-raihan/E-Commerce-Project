from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from products.models import Product, ProductImages, Category, DiscountReason
from django.middleware.csrf import get_token
from .algorithms import *

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

    return render(request, 'staff2_main.html')


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
            product_title=data['title'],
            product_code=data['product_code'],
            product_price=data['price'],
            product_category=category,
            color_type=data['color_type'],
            yarn_type=data['yarn_type'],
            yarn_count=data['yarn_count'],
            brand=data['brand'],
            product_in_stock=bool(data['status']),
            product_tags=data['tags'],
            product_primary_image=request.FILES['primary_image'],
            product_more_information=data['more_info'],
            product_search_keyword=data['search_keywords'],
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

    return render(request, 'add_a_product.html')


def edit_products(request, pk):
    if request.method == 'POST':
        pass

    return render(request, 'add_a_product.html')
