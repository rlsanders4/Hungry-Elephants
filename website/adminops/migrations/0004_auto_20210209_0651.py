# Generated by Django 3.1.5 on 2021-02-09 12:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminops', '0002_pi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pi',
            name='path',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='pi',
            name='port',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)]),
        ),
    ]
