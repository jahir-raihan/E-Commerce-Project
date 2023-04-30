from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.models import Q
from .models import *
from django.urls import reverse

User = get_user_model()


class OrderModelTests(TestCase):

    """Tests includes: A single Order should only have one status at any moment, it can be pending, confirmed , cancelled or delivered,
        We are ignoring delivered , as we'll not use this status anyway.

       -> If order is confirmed, order_handled_date should be > order_date
       -> If order was payment by an online service, then the Order should have a Transaction Row,
            -> order_person == transaction_person
            -> order_person_email == transaction_person_email
            -> order_person_phone == transaction_person_phone
            -> order_total_price == transaction_amount
            -> transaction_date > order_date"""

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']

    def test_order_pending(self):

        """Test order status when in pending"""

        # Looping through orders items
        for order in Order.objects.filter(order_is_pending=True):

            # Testing  status
            status_list = [order.order_is_pending, order.order_is_confirmed, order.order_is_cancelled,
                           order.order_is_delivered]
            pending_status = [True, False, False, False]
            self.assertEquals(status_list, pending_status, "An order can't have two or more status")

    def test_order_confirmed(self):

        """Test order status when confirmed and action date of confirmation"""

        # Looping through orders items
        for order in Order.objects.filter(order_is_confirmed=True):

            # Testing status
            status_list = [order.order_is_pending, order.order_is_confirmed, order.order_is_cancelled,
                           order.order_is_delivered]
            pending_status = [False, True, False, False]
            self.assertEquals(status_list, pending_status, "An order can't have two or more status")

            # Testing action date
            self.assertIs(order.order_date < order.order_handle_date, True, "Order handle date can't be < order_date")

    def test_order_cancelled(self):

        """Test order status when cancelled and action date of cancellation"""

        # Looping through orders items
        for order in Order.objects.filter(order_is_cancelled=True):

            # Testing status
            status_list = [order.order_is_pending, order.order_is_confirmed, order.order_is_cancelled,
                           order.order_is_delivered]
            pending_status = [False, False, True, False]
            self.assertEquals(status_list, pending_status, "An order can't have two or more status")

            # Testing action date
            self.assertIs(order.order_date < order.order_handle_date, True, "Order handle date can't be < order_date")

    def test_online_payment_order_and_transaction(self):

        """Test order details with its transaction details, when order payment method is not cash_on_delivery
            and compare order date with transaction date where order date should be < transaction date"""

        # Looping through each order items
        for order in Order.objects.filter(Q(order_payment_method='sslcom') | Q(order_payment_method='bkash')):

            # Test if their data equal or different, -> if different it will fail the test case
            order_datas = [order.order_person_name, order.order_person_phone, order.order_person_email,
                           order.order_total_price]
            tran = order.transaction
            transaction_replicated_datas = [tran.transaction_person_name, tran.transaction_person_phone,
                                            tran.transaction_person_email, tran.transaction_amount]
            self.assertEquals(order_datas, transaction_replicated_datas,
                              "Order data and its transaction data should be same")

            # Test if transaction date is grater than order date or not, -> if False the test case will fail
            self.assertIs(order.order_date < tran.transaction_date, True, "Transaction date cannot be < order_date")


class CheckOutViewTests(TestCase):

    """Tests for checkout view, figure out if it is working perfectly or not at any valid data point.

       -> Test request methodology, get , post
       -> Test the datas being passed are correct or not,
       -> If request gets a new address that needs to be saved, check if the address being saved or not
       -> Depending on order payment method check for the order status,
            -> If payment method is cash_on_delivery
                -> Status should be pending
            -> If payment method is sslcom or bkash
                -> Status should be confirmed"""

    # Using fixtures to load data from real database
    fixtures = ['test_data.json']

    def test_checkout_passed_data_with_saved_address(self):

        """Test connections, and requests when checkout is not in guest mode, and address is from database"""

        # Getting a normal user
        user = User.objects.filter(
            Q(is_admin=False) & Q(is_order_handler=False) & Q(is_product_adder=False)
        ).first()

        if user:

            # Test authenticated user checkout with saved address -> Data from fixtures
            self.assertTrue(self.client.login(email=user.email, password='jr101525'))  # Logging-in the user

            data = {
                "address": 6, 'items_ids[]': [1], 'items_quantities[]': ['1'], 'items_prices[]': ['1554'],
                'items_sizes[]': ['M'],
                'first_name': [''], 'last_name': [''], 'phone': ['01720988071'], 'email': [''],
                'user': ['jahir raihan joy'], 'payment_method': ['cod'], 'note_to_seller': [''], 'total_price': ['1859.4'],
                'guest_checkout': ['false'], 'save_address': ['false']
            }

            # Before request order last element id
            last_element_id = Order.objects.last().order_id

            # Check status code
            response = self.client.post(reverse('checkout'), data)
            self.assertEqual(response.status_code, 200)

            # Check order is created or not -> As of our fixture data if order is created its order_id will be
            # = last_element_id + 1,
            # So we'll get the order by its order id, if no errors while accessing , test passed else fails

            order = Order.objects.get(order_id=last_element_id + 1)
        else:
            raise Exception("Register a normal user to test !")

    def test_checkout_passed_data_with_guest_mode(self):

        """Test connections, and requests when checkout in guest mode"""

        # Sending guest checkout request
        data = {
            'address[city]': ['Fenid'], 'address[address]': ['Chandrapur - Sindurpur - Dagonbhuiyan d'],
            'address[zipcode]': ['3900'], 'address[country]': ['bangladesh'], 'address[save_it]': ['false'],
            'items_ids[]': ['1'], 'items_quantities[]': ['5'], 'items_prices[]': ['7770'], 'items_sizes[]': ['XXL'],
            'first_name': ['Majibur'], 'last_name': ['Rahman Rony bsdk'], 'phone': ['01720988076'],
            'email': ['funny@gmail.com'],
            'user': ['AnonymousUser'], 'payment_method': ['cod'], 'note_to_seller': [''], 'total_price': ['8697'],
            'guest_checkout': ['false'], 'save_address': ['false']
        }

        # Before request order last element id
        last_element_id = Order.objects.last().order_id

        # Check status code
        response = self.client.post(reverse('checkout'), data)
        self.assertEqual(response.status_code, 200)

        # Check order is created or not -> As of our fixture data if order is created its order_id will be
        # = last_element_id + 1,
        # So we'll get the order by its order id, if no errors while accessing , test passed else fails

        order = Order.objects.get(order_id=last_element_id + 1)

    def test_order_when_payment_method_is_not_cod(self):  # Internet Required

        """Test order , when payment method is not cash on delivery.
            Also Check if the order is being created or not, and we're getting the desired response url"""

        # Sending guest checkout request
        data = {
            'address[city]': ['Fenid'], 'address[address]': ['Chandrapur - Sindurpur - Dagonbhuiyan d'],
            'address[zipcode]': ['3900'], 'address[country]': ['bangladesh'], 'address[save_it]': ['false'],
            'items_ids[]': ['1'], 'items_quantities[]': ['5'], 'items_prices[]': ['7770'], 'items_sizes[]': ['XXL'],
            'first_name': ['Majibur'], 'last_name': ['Rahman Rony'], 'phone': ['01720988076'],
            'email': ['funny@gmail.com'],
            'user': ['AnonymousUser'], 'payment_method': 'sslcom', 'note_to_seller': [''], 'total_price': ['8697'],
            'guest_checkout': ['false'], 'save_address': ['false'], 'test': True
        }

        # Before request order last element id
        last_element_id = Order.objects.last().order_id

        # Check status code
        response = self.client.post(reverse('checkout'), data)
        self.assertEqual(response.status_code, 200)

        # Check order is created or not -> As of our fixture data if order is created its order_id will be
        # = last_element_id + 1,
        # So we'll get the order by its order id, if no errors while accessing , test passed else fails

        order = Order.objects.get(order_id=last_element_id + 1)
        self.assertEqual(order.order_payment_method, data['payment_method'], "Payment methods can't be changed !")

        # Check redirect url, -> if no redirect url, it will cause test failure
        redirect_url = response.json()['url']
