# Generated by Django 3.0.3 on 2020-03-20 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supportteamapp', '0002_remove_systemupdatemodel_orgname'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemupdatemodel',
            name='orgname',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='supportteamapp.OrgInsertion'),
            preserve_default=False,
        ),
    ]
