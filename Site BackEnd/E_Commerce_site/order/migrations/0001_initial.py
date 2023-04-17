# Generated by Django 4.2 on 2023-04-06 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(auto_created=True)),
                ('order_items', models.CharField(max_length=400)),
                ('delivery_location', models.CharField(max_length=250)),
                ('order_person_name', models.CharField(max_length=30)),
                ('order_person_phone', models.CharField(max_length=14)),
                ('order_person_ip', models.GenericIPAddressField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('order_handle_date', models.DateTimeField(blank=True, null=True)),
                ('order_handled_by', models.IntegerField()),
                ('order_is_cancelled', models.BooleanField(default=False)),
                ('order_is_confirmed', models.BooleanField(default=False)),
                ('order_is_pending', models.BooleanField(default=True)),
                ('order_is_delivered', models.BooleanField(default=False)),
                ('order_total_price', models.IntegerField()),
                ('order_payment_method', models.CharField(choices=[('cash_on_delivery', 'cash_on_delivery'), ('bkash', 'bkash'), ('sslcom', 'sslcom')], default='cash_on_delivery', max_length=50)),
                ('note_msg', models.CharField(max_length=300)),
                ('order_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('order_transaction', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='order.transaction')),
            ],
        ),
    ]