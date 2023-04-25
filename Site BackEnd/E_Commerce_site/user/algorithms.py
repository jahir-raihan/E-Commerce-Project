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

