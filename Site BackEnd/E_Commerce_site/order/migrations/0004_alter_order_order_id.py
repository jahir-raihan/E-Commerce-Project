# Generated by Django 4.2 on 2023-04-18 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_order_items_sizes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.UUIDField(auto_created=True, blank=True, null=True),
        ),
    ]
