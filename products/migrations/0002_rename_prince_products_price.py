# Generated by Django 3.2 on 2021-04-16 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='prince',
            new_name='price',
        ),
    ]