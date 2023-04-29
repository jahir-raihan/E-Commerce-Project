from django.test import TestCase
from django.db.models import Q
from .models import *
from django.urls import reverse
import json
from products.models import *


class UserModelTests(TestCase):

    """User Model tests includes:
            ->
            ->
            ->
            -> """

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']


class UserViewsTests(TestCase):

    """Here we're going to test out every single view of User app
       Test includes :
        ->
        ->
        ->
        ->
        ->"""

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']

    def test_can_access_saved_addresses_of_a_authenticated_user(self):

        """Test if we can access saved_addresses of an authenticated user"""

        # Get user and login sample user -> Must be a registered user
        try:
            user = User.objects.filter(
                Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
            ).first()
            self.client.login(email=user.email, password='jr101525')
        except:
            raise Exception("No user Found !")

        # If we can't, it will fail the test case
        addresses = user.address_set.all()

    def test_get_wishlist_items_of_a_authenticated_user(self):

        """Test if we can set , create and get wishlist items of an authenticated user"""

        # Get user and login sample user -> Must be a registered user
        try:
            user = User.objects.filter(
                Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
            ).first()
            self.client.login(email=user.email, password='jr101525')
        except:
            raise Exception("No user Found !")

        # If we can't, it will fail the test case
        sample_product = Product.objects.filter(product_in_stock=True).first()
        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        wishlist = WishList(wishlist_items=f'[{sample_product.id}]', wisher_person=user,
                            wisher_person_ip='172.168.0.1')
        wishlist.save()
        response = self.client.post(reverse('wishlist'))

        # Looping through each wishlist items,if their index is not same or product id is not same it will fail the test
        for i in range(len(response.context['items'])):
            self.assertEqual(response.context['items'][i].id, json.loads(user.wishlist.wishlist_items)[i])

    def test_update_wishlist_items_of_a_authenticated_user(self):

        """Test if we can update wishlist items of an authenticated user"""
