# Generated by Django 3.0.3 on 2020-04-06 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supportteamapp', '0007_systemupdatemodel_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemupdatemodel',
            name='date',
            field=models.DateField(),
        ),
    ]