# Generated by Django 3.2 on 2021-09-23 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_remove_bib_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tent',
            name='tent_tag',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='tent',
            name='tent_tag_colour',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]