from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    category_name = models.CharField(max_length=30)


# Discount reason

class DiscountReason(models.Model):
    discount_reason = models.CharField(max_length=30)


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
    product_added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    product_last_update = models.DateTimeField(auto_now_add=True)
    product_type = models.CharField(max_length=40, null=True, blank=True)
    # Product images

    product_primary_image = models.ImageField(upload_to='product_primary_images/')

    # Seo section

    product_more_information = models.CharField(max_length=200)
    product_search_keyword = models.CharField(max_length=400)

    # Offer Section

    on_discount = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    discount_reason = models.ForeignKey(DiscountReason, on_delete=models.DO_NOTHING, null=True, blank=True)
    discount_expiry = models.DateTimeField(null=True, blank=True)

    wish_count = models.IntegerField(default=0)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    image_alt_tag = models.CharField(max_length=30)


class Cart(models.Model):
    cart_items = models.CharField(max_length=400)
    cart_person_ip = models.GenericIPAddressField()
    cart_person = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    cart_items_price = models.IntegerField()
    cart_added_date = models.DateTimeField(auto_now_add=True)
    cart_id = models.UUIDField(auto_created=True)


# Wishlist model

class WishList(models.Model):
    wishlist_items = models.CharField(max_length=100)
    wisher_person_ip = models.GenericIPAddressField()
    wisher_person = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


# Reviews and replays

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    review_text = models.CharField(max_length=500)
    rating = models.IntegerField(default=1)


class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    replay_text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
