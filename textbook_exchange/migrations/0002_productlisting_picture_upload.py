# Generated by Django 3.0.3 on 2020-04-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook_exchange', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlisting',
            name='picture_upload',
            field=models.CharField(default='', max_length=500),
        ),
    ]