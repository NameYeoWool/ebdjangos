# Generated by Django 2.0.3 on 2019-06-10 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0002_auto_20190610_0205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coment',
            old_name='title',
            new_name='coment_title',
        ),
    ]
