# Generated by Django 3.1.7 on 2021-06-09 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truckentity',
            name='currentDistance',
            field=models.FloatField(default=0.0),
        ),
    ]