from .models import *
from django.db.models import Q

# Filter products on query


def filter_products(query_data):

    """Function to filter our products according to query_data"""

    query = query_data['search_query']
    category = query_data['current_category']
    offers = query_data.getlist('offerings[]')
    refinements = [ref.lower() for ref in query_data.getlist('refinements[]')]
    price_range = query_data.getlist('price_range[]')
    sort = query_data['sort_by_price']

    # Filtering by price range
    products_list = Product.objects.filter(
        Q(product_price__gte=int(price_range[0])) &
        Q(product_price__lte=int(price_range[1]))
    )

    # Filtering by category
    if category != '':
        category = Category.objects.get(pk=category)
        products_list = products_list.filter(product_category=category)

    # Filtering by offers specifications
    if offers:
        offers = [DiscountReason.objects.filter(discount_reason=of)[0] for of in offers]
        products_list = products_list.filter(discount_reason__in=offers)

    # Filtering by refinements and tags & search keywords
    if refinements:
        products_list = products_list.filter(
            Q(product_title__in=refinements) | Q(product_tags__in=refinements) |
            Q(product_search_keyword__in=refinements) | Q(product_more_information__in=refinements)
        )

    # Filtering by any word provided in search_query
    products_list = products_list.filter(
        Q(product_title__icontains=query) | Q(brand__icontains=query) | Q(product_tags__icontains=query) |
        Q(product_search_keyword__icontains=query) | Q(product_more_information__icontains=query)

    )

    # Sorting if sort is selected

    if sort == 'true':
        products_list = products_list.order_by('-product_price')

    elif sort == 'false':
        products_list = products_list.order_by('product_price')

    return products_list


# Get average rating point

def get_avg_rating(product):

    """Returns a product average rating point"""

    reviews = product.review_set.all()
    rating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for r in reviews:
        rating[str(r.rating)] += 1
    try:
        res = ((1*int(rating['1'])) + (2*int(rating['2'])) + (3*int(rating['3'])) + (4*int(rating['4'])) +
               (5*int(rating['5']))) / (int(rating['1']) + int(rating['2']) + int(rating['3']) + int(rating['4']) +
                                        int(rating['5']))
    except ZeroDivisionError:
        res = 5.0
    return res
