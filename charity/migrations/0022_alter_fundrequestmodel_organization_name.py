# Generated by Django 3.2.10 on 2022-03-10 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0021_auto_20220310_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundrequestmodel',
            name='organization_name',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
    ]
