from .models import *
from django.db.models import Q

# Filter products on query


def filter_products(query_data):
    query = query_data['search_query']
    category = query_data['current_category']
    offers = query_data.getlist('offerings[]')
    refinements = [ref.lower() for ref in query_data.getlist('refinements[]')]
    price_range = query_data.getlist('price_range[]')
    sort = query_data['sort_by_price']
    print()

    products_list = Product.objects.filter(
        Q(product_price__gte=int(price_range[0])) &
        Q(product_price__lte=int(price_range[1]))
    )
    print('product_list 1', price_range)

    if category != '':
        category = Category.objects.get(pk=category)
        products_list = products_list.filter(product_category=category)
        print('product_list 2', products_list)

    if offers:
        offers = [DiscountReason.objects.filter(discount_reason=of)[0] for of in offers]
        products_list = products_list.filter(discount_reason__in=offers)
        print('product_list 3', products_list)

    if refinements:
        products_list = products_list.filter(
            Q(product_title__in=refinements) | Q(product_tags__in=refinements) |
            Q(product_search_keyword__in=refinements) | Q(product_more_information__in=refinements)
        )
        print('product_list 3.5', products_list, refinements)

    products_list = products_list.filter(
        Q(product_title__icontains=query) | Q(brand__icontains=query) | Q(product_tags__icontains=query) |
        Q(product_search_keyword__icontains=query) | Q(product_more_information__icontains=query)

    )
    print('product_list 4', products_list)
    if sort == 'true':
        products_list = products_list.order_by('-product_price')
        print('product_list 5', products_list)
    elif sort == 'false':
        products_list = products_list.order_by('product_price')
        print('product_list 6', products_list)

    return products_list


