# Generated by Django 3.2.10 on 2022-03-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0025_auto_20220319_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundrequestmodel',
            name='reason',
            field=models.CharField(max_length=50, null=True),
        ),
    ]