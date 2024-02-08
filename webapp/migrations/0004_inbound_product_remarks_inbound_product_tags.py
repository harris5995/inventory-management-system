# Generated by Django 5.0.1 on 2024-02-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_remove_product_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbound_product',
            name='remarks',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inbound_product',
            name='tags',
            field=models.CharField(default=12, max_length=100),
            preserve_default=False,
        ),
    ]
