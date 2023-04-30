import json

from django.test import TestCase

from .algorithms import get_avg_rating
from .models import *
from django.urls import reverse
from django.db.models import Q


class ProductModelTests(TestCase):

    """Tests includes : If a product is on discount
       -> There should be a discount percentage
       -> Discount price should be < product price
       -> Discount should have an expiry date
       -> Discount should have a discount reason
    """

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']

    def test_product_on_discount(self):

        """When product is on discount"""

        # Looping through each product that are on discount
        for product in Product.objects.filter(on_discount=True):

            # Check category ,-> If no category it will cause test failure
            category = product.product_category.category_name

            # Check discount reason, -> If no discount reason it will cause test failure
            reason = product.discount_reason.discount_reason

            # Check discount price, -> If discount_price > product_price it cause test failure
            self.assertGreater(product.product_price, product.discount_price, "Discount price can't be > product_price")

            # Check discount expiry date, It can't be null
            self.assertIsNotNone(product.discount_expiry, "Discount Expiry date can't be Null !")

            # Check for discount percentage
            self.assertIs(product.discount_percentage > 0, True, "Discount Percentage can't be 0 !")


class ProductAppViewTests(TestCase):

    """Here we're going to test out every single view of product app
       Test Includes :
            -> Home, Product, Cart, Wishlist, Checkout, Product Details page only accessible by non or normal users,
               not admin or staff.
            -> No products that are not in stock is displayed or passed through context dict.
            -> Check our router algorithm is working or not by changing user permission -> (Extra)
            -> If no query string provided then , there shouldn't be any out of stock status product displayed or passed

            -> Check we're getting the correct product details in details page.
            -> Check that we're getting correct average rating of a product in details page

            -> If user is authenticated, check that we're able to access his wishlist items and display them in the
               template if wishlist instance exists for the user

            -> If user is authenticated, check that we're able to access his addresses  and display them in the
               template if saved address instance exists for the user

       Lot of the things are happening in frontEnd , so it's hard to tell if anything is going wrong or not,
       Any way we'll try our best to test out frontEnd as well"""

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']

    def test_home_normal_or_non_user(self):

        """Testing out our router algorithm, router algorithm is the main culprit over here for accessing pages"""

        # Getting a normal user
        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()

        # Logging-in the user for test purpose , Anonymous users are also accepted that's why try except block.
        try:
            self.assertTrue(self.client.login(email=user.email, password='jr101525'))  # Default test user
        except: pass

        response = self.client.get(reverse('home'))

        # If user is not admin or staff , It should return a 200 status code -> Accepted
        self.assertNotEqual(response.status_code, 302, "Admin and staffs are not allowed to access Home page")

    def test_home_admin_or_staff_user_router_redirection(self):

        """If this test case fails it will verify that our router
            Algorithm is malfunctioning or something went wrong when registering a user.
            Else All the other views will also function same as home page."""

        # Getting a admin or staff user
        user = User.objects.filter(
            Q(is_admin=True) | Q(is_order_handler=True) | Q(is_product_adder=True)
        ).first()
        if user:
            # Logging-in the user for test purpose, Anonymous users are not accepted
            # To test it out , there should be at least one admin or staff in the database

            self.assertTrue(self.client.login(email=user.email, password='jr101525'))

            response = self.client.get(reverse('home'))

            # If user is admin or staff , It should return a 302 status code -> Redirect response
            self.assertEqual(response.status_code, 302, "Admin and staffs are not allowed to access Home page")
        else:
            raise Exception("Register a user with admin or staff permission !")

    def test_home_context_products(self):

        """Check products that are being passed by context is not having a status of out_of_stock.
            Request user is will be Anonymous by default."""

        response = self.client.get(reverse('home'))
        products = response.context['products']

        for product in products:
            self.assertIs(product.product_in_stock, True, "We're passing products with out_of_stock status !")

    def test_products_page_context_without_query(self):

        """When we view product page without any query or filter check products that are being passed by context is not
            having a status of out_of_stock.
            Request user is will be Anonymous by default. And query will be none too."""

        response = self.client.get(reverse('products'))
        products = response.context['products']

        for product in products:
            self.assertIs(product.product_in_stock, True, "We're passing products with out_of_stock status !")

    def test_view_details_product(self):

        """Test if we're getting the correct product details"""

        sample_product = Product.objects.filter(product_in_stock=True).first()   # At least one available product
        response = self.client.get(reverse('view_details', kwargs={'pk': sample_product.id}))
        res_prod = response.context

        # Checkers
        self.assertEqual(res_prod['product'].product_title, sample_product.product_title)
        self.assertEqual(res_prod['product'].product_price, sample_product.product_price)
        self.assertEqual(res_prod['product'].product_category, sample_product.product_category)
        self.assertEqual(res_prod['product'].product_code, sample_product.product_code)
        self.assertEqual(res_prod['avg_rating'], get_avg_rating(sample_product))
        self.assertEqual(res_prod['product'].review_set.all().count(), sample_product.review_set.all().count())
