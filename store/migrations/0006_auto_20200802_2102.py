# Generated by Django 3.0.8 on 2020-08-02 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='state',
            new_name='country',
        ),
    ]
