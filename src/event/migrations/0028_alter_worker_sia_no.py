# Generated by Django 3.2 on 2021-11-21 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0027_auto_20211115_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='sia_no',
            field=models.CharField(blank=True, max_length=19, null=True),
        ),
    ]
