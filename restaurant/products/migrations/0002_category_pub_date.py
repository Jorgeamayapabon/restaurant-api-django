# Generated by Django 4.1.6 on 2023-02-10 18:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 10, 18, 57, 3, 300339, tzinfo=datetime.timezone.utc), verbose_name='date published'),
        ),
    ]
