# Generated by Django 4.1.6 on 2023-02-13 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_created',
        ),
    ]