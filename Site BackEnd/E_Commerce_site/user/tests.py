from django.test import TestCase
from django.db.models import Q
from .models import *
from django.urls import reverse
import json
from products.models import *
from order.models import *
from django.db.models import Sum


class UserModelTests(TestCase):

    """User Model tests includes:
            -> At a time one user can have at most one permission label, can be normal, admin or staff
            -> Check we're getting correct user details so far
            -> Test Login & Registration
            -> Test Logout"""

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']


class UserViewsTests(TestCase):

    """Here we're going to test out every single view of User app
       Test includes :
        -> Access of saved_addresses
        -> Can set create and get items of a user wishlist
        -> Test if we're able to update a user wishlist
        -> Test that wishlist items are removable
        -> Test product availability view

       As we've tested out router algorithm in products/test.py, half of our work is completed, because
       Lots of views are dependent on user permission label here."""

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

        wishlist = WishList(wishlist_items=f'[{sample_product.id}]', wisher_person=user,
                            wisher_person_ip='172.168.0.1')
        wishlist.save()
        response = self.client.post(reverse('wishlist'))

        # Looping through each wishlist items,if their index is not same or product id is not same it will fail the test
        for i in range(len(response.context['items'])):
            self.assertEqual(response.context['items'][i].id, json.loads(user.wishlist.wishlist_items)[i])

    def test_update_wishlist_items_of_a_authenticated_user(self):

        """Test if we can update wishlist items of an authenticated user"""

        # Get user and login sample user -> Must be a registered user -> At least one user without wishlist instance
        try:
            user = User.objects.filter(
                Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
            ).first()
            self.client.login(email=user.email, password='jr101525')
        except:
            raise Exception("No user Found !")

        # If we can't, it will fail the test case
        sample_product = Product.objects.filter(product_in_stock=True).first()

        wishlist = WishList(wishlist_items=f'[{sample_product.id + 1}]', wisher_person=user,
                            wisher_person_ip='172.168.0.1')
        wishlist.save()
        response = self.client.post(reverse('save_wishlist_item'), {'product_id': sample_product.id})
        after_request = WishList.objects.get(wisher_person=user).wishlist_items
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.json()['success'], True)
        self.assertEquals([sample_product.id + 1, sample_product.id], json.loads(after_request))

    def test_remove_wishlist_items_of_a_authenticated_user(self):

        """Test if we can remove wishlist items of an authenticated user"""

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

        wishlist = WishList(wishlist_items=f'[{sample_product.id}]', wisher_person=user,
                            wisher_person_ip='172.168.0.1')
        wishlist.save()
        before_request = wishlist.wishlist_items
        response = self.client.get(reverse('remove_wishlist_item'), data={'product_id': sample_product.id})
        after_request = WishList.objects.get(wisher_person=user).wishlist_items
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.json()['success'], True)
        self.assertEquals([], json.loads(after_request))

        self.assertEqual(0, response.json()['items_count'])
        self.assertNotEqual(before_request, after_request,
                            "wishlist can't be same as before after removing an item !")

    def test_product_availability_view(self):

        """Test out if product availability view is returning correct response or not"""

        # Test for in_stock product
        sample_product = Product.objects.filter(product_in_stock=True).first() # At least one in stock is required
        response = self.client.get(reverse('check_product_availability'), data={'p_id': sample_product.id})
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.json()['status'], True)

        # Test for out_of_stock product
        sample_product = Product.objects.filter(product_in_stock=False).first()  # At least one in stock is required
        response = self.client.get(reverse('check_product_availability'), data={'p_id': sample_product.id})
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.json()['status'], False)

    def test_we_are_getting_correct_transactions_of_a_registered_user(self):

        """Test to check weather we're getting correct transactions of a logged-in user"""

        # Get user and login sample user -> Must be a registered user
        try:
            user = User.objects.filter(
                Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
            ).first()
            self.client.login(email=user.email, password='jr101525')
        except:
            raise Exception("No user Found !")

        # Create a sample transaction for the user
        import datetime
        trans = Transaction(
            transaction_id=1,
            transaction_amount=200,
            transaction_method='sslcom',
            bank_tran_id='bank_tran_id',
            transaction_date=datetime.datetime.now(),
            transaction_person=user,
            transaction_person_name=user.name,
            transaction_person_phone=user.phone,
            transaction_person_email=user.email,
            transaction_person_ip='168.172.198',
            order=Order.objects.get(pk=51)
        )
        trans.save()

        transactions = Transaction.objects.filter(transaction_person=user)

        # Getting transactions list by requesting through view
        response = self.client.get(reverse('transaction'))

        # Transaction list for a user should be same at any moment, in view or in functions
        for i in range(len(transactions)):
            self.assertEqual(transactions[i].id, response.context['transactions'][i].id)

    def test_admin_dashboard_context_data(self):

        """Test that, admin dashboard is getting the correct data by context"""

        # Get user and login sample user -> Must be a registered user and should be admin
        try:
            user = User.objects.filter(
                Q(is_admin=True) & Q(is_order_handler=False) & Q(is_product_adder=False)
            ).first()
            self.client.login(email=user.email, password='jr101525')
        except:
            raise Exception("At least one user with Admin permission is required !")

        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

        total_earnings = Order.objects.filter(order_is_confirmed=True).aggregate(Sum('order_total_price'))[
            'order_total_price__sum']
        total_orders = Order.objects.filter(order_is_confirmed=True).count()
        total_products = Product.objects.all().count()

        self.assertEquals([total_earnings, total_orders, total_products], [response.context['total_earnings'],
                                                                           response.context['total_orders'],
                                                                           response.context['total_products']])




