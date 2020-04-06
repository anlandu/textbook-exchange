# Generated by Django 3.0.3 on 2020-04-06 17:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook_exchange', '0014_auto_20200406_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlisting',
            name='price',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(500)]),
        ),
    ]