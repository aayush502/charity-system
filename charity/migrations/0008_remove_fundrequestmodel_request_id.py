# Generated by Django 3.2.10 on 2022-01-23 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0007_alter_fundrequestmodel_request_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fundrequestmodel',
            name='request_id',
        ),
    ]
