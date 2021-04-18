# Generated by Django 3.1.6 on 2021-04-13 09:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminops', '0001_ACTUAL_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elephant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('rfid', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date_time', models.DateTimeField()),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_date_time', models.DateTimeField()),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('interval', models.DurationField()),
                ('max_feeds', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('name', models.CharField(max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('elephant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elephants.elephant')),
                ('feeder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminops.feeder')),
                ('presets', models.ManyToManyField(to='elephants.Preset')),
            ],
        ),
        migrations.CreateModel(
            name='PresetSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('interval', models.DurationField()),
                ('max_feeds', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('name', models.CharField(max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('elephant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elephants.elephant')),
                ('feeder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminops.feeder')),
                ('presets', models.ManyToManyField(to='elephants.Preset')),
            ],
        ),
    ]
