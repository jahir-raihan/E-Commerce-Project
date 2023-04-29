from django.shortcuts import redirect

from products.models import *
from django.utils.timezone import datetime


def get_client_ip(request):

    """Takes request object as input
        and returns ip address of the request client"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Product on discount

def on_discount(data, product):

    """Function to mark a product on discount"""

    product.on_discount = True
    product.discount_percentage = int(data['discount_percentage'])
    product.discount_price = int(int(data['price']) - (int(data['discount_percentage'])/100)*int(data['price']))
    if data['discount_reason'] != '':
        reason = DiscountReason.objects.get(pk=data['discount_reason'])
    else:
        reason = DiscountReason(discount_reason=data['discount_reason_new'])
        reason.save()

    product.discount_reason = reason
    product.discount_expiry = data['discount_expiry_date']

    product.save()

# Save product images


def save_product_images(product, alt_texts, images):

    """Saves product images"""

    for i in range(len(images)):
        try:
            alt_txt = alt_texts[i]
        except:
            alt_txt = 'Product Image'
        img = ProductImages(product=product, image_alt_tag=alt_txt, image=images[i])
        img.save()


# Edit product

def save_edited_product(product, data):

    """Saves edited products details, it is linked with user that's why it's here inside user app"""

    files = data.FILES
    data = data.POST

    product.product_title = data['title']
    product.product_code = data['product_code']
    product.product_price = data['price']
    product.color_type = data['color_type']
    product.yarn_type = data['yarn_type']
    product.yarn_count = data['yarn_count']
    product.brand = data['brand']
    product.product_tags = data['tags']
    product.product_more_information = data['more_info']
    product.product_search_keyword = data['search_keywords']

    if 'on_discount' in data:
        on_discount(data, product)
    if data['category'] == '':
        category = Category(category_name=data['category_new'])
        category.save()
    else:
        category = Category.objects.get(pk=data['category'])
    product.product_category = category

    if 'primary_image' in files:
        product.product_primary_image = files['primary_image']
    if 'images' in files:
        alt_texts = data['image_alt_texts']
        images = files.getlist('images')
        save_product_images(product, alt_texts.split(','), images)

    product.save()


# Router

def router(request, accept):

    """Determine user permission label and redirect them to their destination page,
        Check if they are verified to access a particular page.
        Conditions : -> If user is Normal user only allow normal user functionalities,
                     -> If user is Staff , allow him to access staff functionality only, (Two types of staff)
                     -> If user is Admin , allow him to access admin panel, nothing else , only admin panel.
                     -> Keep pages isolated from each other , such that the database behaves as multi tenet database"""
    user = request.user
    if user.is_authenticated:
        if accept['is_order_handler'] and user.is_order_handler:
            return [True]
        elif accept['is_product_adder'] and user.is_product_adder:
            return [True]
        if accept['is_admin'] and user.is_admin:
            return [True]
        elif accept['is_user'] and not (user.is_admin or user.is_product_adder or user.is_order_handler):
            return [True]
        else:
            if user.is_order_handler:
                return [False, 'staff_main1']
            elif user.is_product_adder:
                return [False, 'staff_main2']
            elif user.is_admin:
                return [False, 'admin_dashboard']
            else:
                return [False, 'account']
    else:
        return [False, 'account', 1]

