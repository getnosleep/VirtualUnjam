# Generated by Django 3.1.7 on 2021-06-21 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck', '0002_auto_20210615_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='truckentity',
            name='address',
            field=models.TextField(default='127.0.0.1:1031', max_length=50),
        ),
    ]
