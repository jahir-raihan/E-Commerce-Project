from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('view-details/<str:pk>/', view_details, name='view_details'),
    path('review/<str:pk>/', review, name='review'),
    path('replay/<str:pk>/', replay, name='replay'),
    path('get-all-review/<str:pk>/', show_all_reviews, name='show_all_reviews'),
    path('cart/', cart, name='cart'),

    path('check-product-availability/<str:pk>/', check_product_availability, name='check_product_availability'),
]