from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('get-pending-order-count/', get_pending_order_count, name='get_pending_order_count')
]