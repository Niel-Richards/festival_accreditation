# Generated by Django 3.2 on 2021-09-13 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_auto_20210913_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accredit',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.worker'),
        ),
    ]
