from django.contrib import admin
from .models import *


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(DiscountReason)
admin.site.register(ProductImages)
admin.site.register(Review)
admin.site.register(ReviewReply)
admin.site.register(WishList)
# Register your models here.
