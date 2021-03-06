# Generated by Django 3.1.6 on 2021-04-13 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminops', '0001_ACTUAL_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_uuid', models.CharField(max_length=36)),
                ('execute_after_UNIX_time', models.CharField(max_length=10)),
                ('target_site_code', models.CharField(max_length=3)),
                ('target_feeder_number', models.CharField(max_length=2)),
                ('amount', models.CharField(max_length=1)),
                ('if_recieve_from_antenna_number', models.CharField(max_length=2)),
                ('if_recieve_from_tag_number', models.CharField(max_length=16)),
                ('interval_time', models.CharField(max_length=4)),
                ('expire_time', models.CharField(max_length=10)),
                ('repeat_X_times', models.CharField(max_length=1)),
                ('completed_time', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RFIDLogData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plaintext', models.CharField(max_length=100)),
                ('unix_time', models.CharField(max_length=20)),
                ('site_code', models.CharField(max_length=10)),
                ('antenna_tag', models.CharField(max_length=10)),
                ('rfid', models.CharField(max_length=50)),
                ('pi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adminops.pi')),
            ],
        ),
    ]
