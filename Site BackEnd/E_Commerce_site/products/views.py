from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import *
from .algorithms import *
from django.db.models import Q
from django.middleware.csrf import get_token

"""Home views"""


def home(request):
    products = Product.objects.all().order_by('product_last_update')[:20]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'index.html', context)


def products(request):
    if request.method == 'POST':
        query_data = request.POST
        products_list = filter_products(query_data)
        new_token = get_token(request)

        context = {
            'template': render_to_string('products_filter_template.html',context={'products': products_list},
                                         request=request),
            'token': new_token
        }
        return JsonResponse(context)

    query = ''
    if 's' in request.GET:
        query = request.GET['s']
    category = Category.objects.filter(category_name__icontains=query)
    reasons = DiscountReason.objects.filter(discount_reason__icontains=query)

    products_list = Product.objects.filter(
        Q(product_title__icontains=query) | Q(brand__icontains=query) | Q(product_tags__icontains=query) |
        Q(product_search_keyword__icontains=query) | Q(product_more_information__icontains=query) |
        Q(product_category__in=category) | Q(discount_reason__in=reasons)

    )
    search_keywords = Product.objects.all()
    categories = Category.objects.all()
    reasons = DiscountReason.objects.all()
    context = {
        'products': products_list,
        'query': query,
        'query_string': True if query != '' else False,
        'search_keywords': search_keywords,
        'categories': categories,
        'reasons': reasons
    }
    return render(request, 'products.html', context)


def view_details(request, pk):
    product = Product.objects.get(pk=pk)
    query = product.product_title
    search_keywords = Product.objects.all()

    avg_rating = get_avg_rating(product)

    similar_products = Product.objects.filter(
        Q(product_title__icontains=query) | Q(brand__icontains=query) | Q(product_tags__icontains=query) |
        Q(product_search_keyword__icontains=query) | Q(product_more_information__icontains=query) |
        Q(product_category__in=[product.product_category]) | Q(discount_reason__in=[product.discount_reason]))
    context = {
        'product': product,
        'search_keywords': search_keywords,
        'loop': [0, 1, 2, 3, 4],
        'similar_products': similar_products,
        'avg_rating': avg_rating,
        'avg_abs_rating': abs(avg_rating)

    }
    return render(request, 'view_details.html', context)


# Reviews and rating

def review(request, pk):
    product = Product.objects.get(pk=pk)
    rev = Review(review_text=request.POST['review_text'], user=request.user, product=product,
                 rating=int(request.POST['rating']))
    context = {
        'product': product,
        'loop': [0, 1, 2, 3, 4],
        'limiter': True
    }
    rev.save()
    template = render_to_string('review_template.html', context=context, request=request)
    new_token = get_token(request)

    return JsonResponse({'template': template, 'token': new_token})


def replay(request, pk):
    rev = Review.objects.get(pk=pk)
    product = rev.product
    rep = ReviewReply(replay_text=request.POST['replay_text'], user=request.user, review=rev)
    rep.save()
    context = {
        'product': product,
        'loop': [0, 1, 2, 3, 4],
        'limiter': True
    }
    rev.save()
    template = render_to_string('review_template.html', context=context, request=request)
    new_token = get_token(request)

    return JsonResponse({'template': template, 'token': new_token})


def show_all_reviews(request, pk):
    product = Product.objects.get(pk=pk)
    print(pk)
    context = {
        'product': product,
        'loop': [0, 1, 2, 3, 4],
        'limiter': False
    }
    return render(request, 'review_template.html', context)


# Cart and wishlist

def cart(request):

    return render(request, 'cart.html')


def wishlist(request):
    return render(request, 'wishlist.html')


def check_product_availability(request, pk):
    product = Product.objects.get(pk=pk)
    if product.product_in_stock:
        return True
    return False

