from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('redirect-user/base-location/', redirect_origin, name='redirect_origin'),
    path('logout/', logout_user, name='logout'),

    # Staff Area

    # Product Handler

    path('staff-main-1/', staff_main1, name='staff_main1'),
    path('pending-orders/', pending_orders, name='pending_orders'),
    path('pending-order-action/', pending_order_action, name='pending_order_action'),

    # Product Adder

    path('staff-main-2/', staff_main2, name='staff_main2'),
    path('add-edit-products/', add_products, name='add_products'),
    path('add-edit-products/<str:pk>/', edit_products, name='edit_products'),

    # Normal & unregistered user

    path('', account, name='account'),
    path('order-history/', order_history, name='order_history'),
    path('query-order-history/', query_order_history, name='query_order_history'),
    path('save-wishlist-item/', save_wishlist_item, name='save_wishlist_item'),
    path('check-wishlist-item-availability/', check_product_availability, name='check_product_availability'),
    path('remove-wishlist-item/', remove_wishlist_item, name='remove_wishlist_item'),
    path('wishlist/', wishlist, name='wishlist'),
    path('transaction/', transactions, name='transaction'),

    # Admin

    path('admin/', dashboard, name='admin_dashboard'),
    path('statistics/', statistics, name='statistics'),
    path('admin/product-list/', admin_product_list, name='admin_product_list'),
    path('admin/orders/', admin_orders, name='admin_orders'),
    path('admin/add-edit-product/', admin_add_product, name='admin_add_product'),
    path('admin/add-edit-product/<str:pk>/', admin_edit_product, name='admin_edit_product'),
    path('admin/transactions/', admin_transactions, name='admin_transactions'),








]