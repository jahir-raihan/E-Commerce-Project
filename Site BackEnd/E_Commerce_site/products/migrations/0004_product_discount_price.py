# Generated by Django 4.2 on 2023-04-09 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productimages_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.IntegerField(default=0),
        ),
    ]