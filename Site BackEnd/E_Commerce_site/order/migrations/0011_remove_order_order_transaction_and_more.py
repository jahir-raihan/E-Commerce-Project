# Generated by Django 4.2 on 2023-04-24 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0010_alter_order_order_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_transaction',
        ),
        migrations.AddField(
            model_name='transaction',
            name='bank_tran_id',
            field=models.CharField(default='hello', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='order',
            field=models.OneToOneField(default=40, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_amount',
            field=models.IntegerField(default=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default=1, max_length=34),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_method',
            field=models.CharField(default='cod', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_person_name',
            field=models.CharField(default='joy', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_person_phone',
            field=models.CharField(default='91281', max_length=14),
            preserve_default=False,
        ),
    ]