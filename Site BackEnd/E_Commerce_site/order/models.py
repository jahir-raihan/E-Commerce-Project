from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Order(models.Model):

    # Order items and person details

    order_items = models.CharField(max_length=1500)
    order_id = models.BigIntegerField(null=True, blank=True)
    delivery_location = models.CharField(max_length=250)
    order_person_name = models.CharField(max_length=30)
    order_person_email = models.EmailField()
    order_person_phone = models.CharField(max_length=14)
    order_person_ip = models.GenericIPAddressField()
    order_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_handle_date = models.DateTimeField(blank=True, null=True)
    order_handled_by = models.IntegerField(default=0)

    # Order Status

    order_is_cancelled = models.BooleanField(default=False)
    order_is_confirmed = models.BooleanField(default=False)
    order_is_pending = models.BooleanField(default=True)
    order_is_delivered = models.BooleanField(default=False)

    # Order price

    order_total_price = models.FloatField()

    # Order payment method
    payment_choices = (('cash_on_delivery', 'cash_on_delivery'), ('bkash', 'bkash'), ('sslcom', 'sslcom'))

    order_payment_method = models.CharField(max_length=50, choices=payment_choices, default='cash_on_delivery')
    note_msg = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f'{self.order_id, self.order_person_name}'


class OrderID(models.Model):
    order_id = models.BigIntegerField(default=1000)


class Transaction(models.Model):
    # All transaction information goes here
    transaction_id = models.CharField(max_length=34)
    transaction_amount = models.FloatField()
    transaction_method = models.CharField(max_length=20)
    bank_tran_id = models.CharField(max_length=50)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_person = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    transaction_person_name = models.CharField(max_length=30)
    transaction_person_phone = models.CharField(max_length=14)
    transaction_person_email = models.EmailField()
    transaction_person_ip = models.GenericIPAddressField()
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

