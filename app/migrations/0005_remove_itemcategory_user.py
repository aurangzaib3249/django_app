# Generated by Django 4.0.6 on 2022-08-01 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_user_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcategory',
            name='user',
        ),
    ]
