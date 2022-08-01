# Generated by Django 4.0.6 on 2022-08-01 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_user_managers_alter_user_full_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestDb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Phone')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
