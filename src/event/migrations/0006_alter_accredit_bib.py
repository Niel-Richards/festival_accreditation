# Generated by Django 3.2 on 2021-08-26 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_alter_accredit_bib'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accredit',
            name='bib',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.bib'),
        ),
    ]