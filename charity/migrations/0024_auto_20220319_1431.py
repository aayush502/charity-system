# Generated by Django 3.2.10 on 2022-03-19 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0023_alter_fundrequestmodel_organization_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multipleimage',
            name='images',
        ),
        migrations.AddField(
            model_name='multipleimage',
            name='image1',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='multipleimage',
            name='image2',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='multipleimage',
            name='image3',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='multipleimage',
            name='image4',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
