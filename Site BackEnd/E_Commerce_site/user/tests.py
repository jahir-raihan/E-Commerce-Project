from django.test import TestCase
from django.db.models import Q
from .models import *
from django.urls import reverse, reverse_lazy
import json
from products.models import *
from order.models import *
from django.db.models import Sum


class UserModelTests(TestCase):

    """User Model tests includes:
            -> At a time one user can have at most one permission label, can be normal, admin or staff
    """

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']

    def test_permission_label(self):

        """Test if user is having only one status at a moment"""

        users = User.objects.all()

        # Loop through all users to check every single one
        for user in users:
            perms = [user.is_admin, user.is_order_handler, user.is_product_adder, True]  # Default True for normal user
            self.assertLessEqual(perms.count(True), 2, "A user can't have multiple permissions !")


class UserViewsTests(TestCase):

    """Here we're going to test out every single view of User app
       Test includes :
        -> Test Register and Login mechanism
        -> Access of saved_addresses
        -> Can set create and get items of a user wishlist
        -> Test if we're able to update a user wishlist
        -> Test that wishlist items are removable
        -> Test product availability view

       As we've tested out router algorithm in products/test.py, half of our work is completed, because
       Lots of views are dependent on user permission label here."""

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']

    def test_register_mechanism(self):

        """Test out to see if our register mechanism is working fine or not"""

        # Create a sample account to see if it is registering or not
        data = {
            'email': 'testuser@gmail.com',
            'name': 'test_user_name',
            'phone': '01975498434',
            'password1': 'jr101525',
            'password2': 'jr101525'
        }
        response = self.client.post(reverse('register'), data)
        # As we're not passing any redirect_url it should return '/' in response of redirect
        self.assertEqual(response.json()['redirect'], '/')

        # when we pass redirect origin
        data['redirect_url'] = reverse('account')
        response = self.client.post(reverse('register'), data)
        # This one request should return False -> Because we've just logged in with this credentials
        # Look few lines upper, If it returns False, then it verifies that our mechanism is working perfectly.

        self.assertEqual(response.json()['redirect'], False)

    def test_register_mechanism_with_redirect_url(self):

        """Test register mechanism with redirect url"""

        # Create a sample account to see if it is registering or not
        data = {
            'email': 'testuser@gmail.com',
            'name': 'test_user_name',
            'phone': '01975498434',
            'password1': 'jr101525',
            'password2': 'jr101525',
            'redirect_url': reverse('account')
        }
        response = self.client.post(reverse('register'), data)
        # As we're  passing redirect_url it should return url to account page in response of redirect
        self.assertEqual(response.json()['redirect'], '/account/')

    def test_login(self):

        """Test out if login mechanism is working or not"""

        user = User.objects.all()[0]  # At least one user is required

        data = {
            'email': user.email,
            'password': 'jr101525',
        }
        response = self.client.post(reverse('login'), data)

        # The request should return '/' in response after successfully executing
        # It verifies that our login is working perfectly
        self.assertEqual(response.json()['redirect'], '/')
        self.assertIs(response.json()['success'], True)

    def test_login_when_already_signed_in(self):

        """Test out our login mechanism , when we're already logged in, it should return
            False if reqeust method is post , and redirects the user if request method is GET"""

        # Logging in -> There's another way of logging-in by using self.client.login.
        user = User.objects.all()  # At least one user is required
        if user:
            data = {
                'email': user[0].email,
                'password': 'jr101525',  # I know I'll give this password to every test account.
            }
            response = self.client.post(reverse('login'), data)

            # Again trying to log in by post request -> Should return a Forbidden response
            response1 = self.client.post(reverse('login'), data)
            self.assertEqual(response1.status_code, 403)

            # Trying to access login page while logged in -> Should redirect us to a location except login page.
            # It will give us a redirect code of 302 -> Then it verifies our login mechanism is also working.
            response1 = self.client.get(reverse('login'))
            self.assertEqual(response1.status_code, 302)

    def test_can_access_saved_addresses_of_a_authenticated_user(self):

        """Test if we can access saved_addresses of an authenticated user"""

        # Get user and login sample user -> Must be a registered user

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')

            # If we can't, it will fail the test case
            addresses = user.address_set.all()

    def test_get_wishlist_items_of_a_authenticated_user(self):

        """Test if we can set , create and get wishlist items of an authenticated user"""

        # Get user and login sample user -> Must be a registered user

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')

            # If we can't, it will fail the test case
            sample_product = Product.objects.filter(product_in_stock=True).first()

            wishlist = WishList(wishlist_items=f'[{sample_product.id}]', wisher_person=user,
                                wisher_person_ip='172.168.0.1')
            wishlist.save()
            response = self.client.post(reverse('wishlist'))

            # Looping through each wishlist items,if their index is not same or product id is not same
            # it will fail the test
            for i in range(len(response.context['items'])):
                self.assertEqual(response.context['items'][i].id, json.loads(user.wishlist.wishlist_items)[i])

    def test_update_wishlist_items_of_a_authenticated_user(self):

        """Test if we can update wishlist items of an authenticated user"""

        # Get user and login sample user -> Must be a registered user -> At least one user without wishlist instance

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')

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

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')

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

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')

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

        user = User.objects.filter(
            Q(is_admin=True) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')
            response = self.client.get(reverse('admin_dashboard'))
            self.assertEqual(response.status_code, 200)

            total_earnings = Order.objects.filter(order_is_confirmed=True).aggregate(Sum('order_total_price'))[
                'order_total_price__sum']
            total_orders = Order.objects.filter(order_is_confirmed=True).count()
            total_products = Product.objects.all().count()

            self.assertEquals([total_earnings, total_orders, total_products], [response.context['total_earnings'],
                                                                               response.context['total_orders'],
                                                                               response.context['total_products']])

    def test_only_admin_access_product_list(self):

        """Test admin product list view, only admin can access this view"""

        # Get user and login sample user -> Must be a registered user and should be admin

        user = User.objects.filter(
            Q(is_admin=True) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')
            response = self.client.get(reverse('admin_product_list'))
            self.assertEqual(response.status_code, 200)

    def test_only_admin_access_transactions(self):

        """Test admin product list view, only admin can access this view"""

        # Get user and login sample user -> Must be a registered user and should be admin

        user = User.objects.filter(
            Q(is_admin=True) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')
            response = self.client.get(reverse('admin_transactions'))
            self.assertEqual(response.status_code, 200)

    def test_only_product_adder_main_page_access(self):

        """Test product adder account main page, its only accessible by product_adder"""

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=True)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')
            response = self.client.get(reverse('staff_main2'))
            self.assertEqual(response.status_code, 200)

    def test_only_order_handler_main_page_access(self):

        """Test order handler account main page, its only accessible by order_handler"""

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=True) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')
            response = self.client.get(reverse('staff_main1'))
            self.assertEqual(response.status_code, 200)

    def test_pending_orders_view(self):

        """This view by default should return orders containing pending status, except in case of query.
           We'll test out for default case , that we're getting all orders with pending status."""

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=True) & Q(is_product_adder=False)
        ).first()
        if user:
            self.client.login(email=user.email, password='jr101525')
            response = self.client.get(reverse('pending_orders'))

            # Checking status
            self.assertEqual(response.status_code, 200)

            # Looping through each returned order items to check their status
            for order in response.context['orders']:
                self.assertIs(order['order'].order_is_pending, True, "Only pending orders should be returned !")

    def test_pending_order_action(self):

        """Test pending order action, accept or cancel, this one is same for admin pending orders too."""

        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=True) & Q(is_product_adder=False)
        ).first()
        if user:

            # Get a sample order
            sample_order = Order.objects.filter(order_is_pending=True).first()

            # Before action order status
            self.assertEqual(sample_order.order_is_pending, True)

            # After action
            self.client.login(email=user.email, password='jr101525')
            response = self.client.post(reverse('pending_order_action'), {'action': 'confirm',
                                                                          'order_id': sample_order.id})
            self.assertEqual(response.status_code, 200)

            # Getting the same order
            order = Order.objects.get(order_id=sample_order.order_id)

            # After confirm operation their status should've been changed
            self.assertNotEqual(sample_order.order_is_pending, order.order_is_pending)
            self.assertNotEqual(sample_order.order_is_confirmed, order.order_is_confirmed)
