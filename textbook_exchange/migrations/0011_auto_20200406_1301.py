# Generated by Django 3.0.3 on 2020-04-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook_exchange', '0010_auto_20200406_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlisting',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
