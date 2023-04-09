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
    product.on_discount = True
    product.discount_percentage = int(data['discount_percentage'])
    product.discount_price = int(int(data['price']) - (int(data['discount_percentage'])/100)*int(data['price']))
    if data['discount_reason'] != '':
        reason = DiscountReason.objects.get(pk=data['discount_reason'])
    else:
        reason = DiscountReason(discount_reason=data['discount_reason_new'])
        reason.save()

    product.discount_reason = reason
    product.discount_expiry = ['discount_expiry_date']

    product.save()

# Save product images


def save_product_images(product, alt_texts, images):
    for i in range(len(images)):
        img = ProductImages(product=product, image_alt_tag=alt_texts[i], image=images[i])
        img.save()
