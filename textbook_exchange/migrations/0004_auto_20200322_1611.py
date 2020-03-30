# Generated by Django 3.0.3 on 2020-03-22 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook_exchange', '0003_auto_20200322_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='class_acronym',
            new_name='dept',
        ),
        migrations.RemoveField(
            model_name='class',
            name='class_code',
        ),
        migrations.RemoveField(
            model_name='class',
            name='subject',
        ),
        migrations.AddField(
            model_name='class',
            name='class_info',
            field=models.CharField(default='CS', max_length=200, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='course_code',
            field=models.IntegerField(default=0),
        ),
    ]
