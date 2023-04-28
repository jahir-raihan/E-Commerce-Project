from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.models import Q
from .models import *

User = get_user_model()


class OrderModelTests(TestCase):

    """A single Order should only have one status at any moment, it can be pending, confirmed , cancelled or delivered,
        We are ignoring delivered , as we'll not use this status anyway.

       -> If order is confirmed, order_handled_date should be > order_date
       -> If order has amount was payment by an online service, then the Order should have a Transaction Row,
            -> order_person == transaction_person
            -> order_person_email == transaction_person_email
            -> order_person_phone == transaction_person_phone
            -> order_total_price == transaction_amount
            -> transaction_date > order_date"""

    # Using fixtures to load data from real database
    fixtures = ['order/test_data.json']

    # Setting up dummy test data
    def setUp(self):
        pass

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
            self.assertEquals(status_list, pending_status ,"An order can't have two or more status")

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

    def test_online_payment_order(self):

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
            self.assertIs(order.order_date > tran.transaction_date, True, "Transaction date cannot be < order_date")






