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


