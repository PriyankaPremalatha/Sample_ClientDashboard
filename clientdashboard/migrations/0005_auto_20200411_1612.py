# Generated by Django 3.0.3 on 2020-04-11 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientdashboard', '0004_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userimage',
            field=models.ImageField(blank=True, default='', null=True, upload_to='images/'),
        ),
    ]
