# Generated by Django 4.0.6 on 2022-07-28 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_item_date_item_item_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_access',
            field=models.BooleanField(default=False),
        ),
    ]
