# Generated by Django 3.0.3 on 2020-04-13 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook_exchange', '0003_class_class_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productlisting',
            old_name='hasBeenSoldFlag',
            new_name='has_been_sold',
        ),
        migrations.AddField(
            model_name='productlisting',
            name='sold_date',
            field=models.DateTimeField(auto_now=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='productlisting',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
    ]