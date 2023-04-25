from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .algorithms import *
from django.db.models import Q
from django.middleware.csrf import get_token


# Base Home
def home(request):

    """Landing page view, with new arrival products on display"""

    products = Product.objects.filter(product_in_stock=True).order_by('product_last_update')[:20]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'index.html', context)


# Products Page
def products(request):

    """Products page view , with filtering and searching capability"""

    # If request method is post filter out products by search query
    if request.method == 'POST':
        query_data = request.POST

        # Calling out filter function from products.algorithms to filter the products
        products_list = filter_products(query_data)

        # Generating new csrf token for another post request --> Supports simultaneous request
        new_token = get_token(request)

        context = {
            'template': render_to_string('products_filter_template.html',context={'products': products_list},
                                         request=request),
            'token': new_token
        }
        return JsonResponse(context)

    # If request is GET and there is a query string filter out by query string then return the products anyway.

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

    # Search keywords for search suggestions
    search_keywords = Product.objects.all()

    # For filtering purpose
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


# View a product details Page
def view_details(request, pk):
    product = Product.objects.get(pk=pk)
    query = product.product_title
    search_keywords = Product.objects.all()

    # Getting average rating of the product -> Algorithm defined in algorithms
    avg_rating = get_avg_rating(product)

    # Getting similar products
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

# Review
def review(request, pk):

    """Saving review of a product"""

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


# Review Reply
def replay(request, pk):

    """Review reply"""

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


# All Review
def show_all_reviews(request, pk):

    """Show all review of a product"""

    product = Product.objects.get(pk=pk)
    context = {
        'product': product,
        'loop': [0, 1, 2, 3, 4],
        'limiter': False
    }
    return render(request, 'review_template.html', context)


# Cart and wishlist


# Cart
@csrf_exempt
def cart(request):

    """Cart functionalities is handled on the frontEnd side"""

    return render(request, 'cart.html')


# Wishlist
def wishlist(request):

    """Wishlist functionalities is handled on the frontEnd side"""

    return render(request, 'wishlist.html')


# Check product availability --> Simultaneous request
def check_product_availability(request, pk):

    """Returns product status"""

    product = Product.objects.get(pk=pk)
    if product.product_in_stock:
        return True
    return False

