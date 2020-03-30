# Generated by Django 3.0.3 on 2020-03-30 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook_exchange', '0004_auto_20200329_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textbook',
            name='bookstore_new_price',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='bookstore_used_price',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='google_rating',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='num_reviews',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='page_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]