# Generated by Django 3.1.5 on 2021-04-06 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminops', '0008_auto_20210331_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pi',
            name='path',
        ),
    ]
