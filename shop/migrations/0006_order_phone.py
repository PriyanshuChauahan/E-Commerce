# Generated by Django 4.1.5 on 2023-02-15 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_rename_orders_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.IntegerField(default='0'),
        ),
    ]
