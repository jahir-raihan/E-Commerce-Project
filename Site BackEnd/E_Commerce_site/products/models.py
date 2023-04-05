from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    category_name = models.CharField(max_length=30)


class ProductImages(models.Model):
    image = models.ImageField(upload_to='product-images/')
    image_alt_tag = models.CharField(max_length=30)


class Product(models.Model):

    # Product details

    product_title = models.CharField(max_length=200)
    product_code = models.CharField(max_length=15)
    product_price = models.IntegerField()
    product_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    color_type = models.CharField(max_length=100)
    yarn_type = models.CharField(max_length=100)
    yarn_count = models.IntegerField()
    brand = models.CharField(max_length=30)
    product_in_stock = models.BooleanField(default=True)
    product_tags = models.CharField(max_length=300)

    # Product images

    product_primary_image = models.ImageField()
    product_images = models.ForeignKey(ProductImages, on_delete=models.DO_NOTHING)

    # Seo section

    product_more_information = models.CharField(max_length=200)
    product_search_keyword = models.CharField(max_length=400)

    # Offer Section

    on_discount = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=0)
    discount_reason = models.CharField(max_length=50)
    discount_expiry = models.DateTimeField()


class Cart(models.Model):
    cart_items = models.CharField(max_length=400)
    cart_person_ip = models.GenericIPAddressField()
    cart_person = models.OneToOneField(User, null=True, balnk=True, on_delete=models.DO_NOTHING)
    cart_items_price = models.IntegerField()
    cart_added_date = models.DateTimeField(auto_now_add=True)
    cart_id = models.UUIDField(auto_created=True)


# Wishlist model

class WishList(models.Model):
    wishlist_items = models.CharField(max_length=100)
    wisher_person_ip = models.GenericIPAddressField()
    wisher_person = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

