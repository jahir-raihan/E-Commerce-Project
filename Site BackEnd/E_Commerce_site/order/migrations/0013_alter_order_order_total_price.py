# Generated by Django 4.2 on 2023-04-24 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_transaction_transaction_person_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_total_price',
            field=models.FloatField(),
        ),
    ]
