# Generated by Django 3.2 on 2021-12-05 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0029_auto_20211205_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accredit',
            name='camping',
            field=models.BooleanField(),
        ),
    ]
