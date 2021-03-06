# Generated by Django 3.2.10 on 2022-01-23 15:25

from django.db import migrations, models
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0008_remove_fundrequestmodel_request_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngo',
            name='current_user',
            field=models.CharField(blank=True, default=django_currentuser.middleware.get_current_authenticated_user, max_length=40),
        ),
    ]
