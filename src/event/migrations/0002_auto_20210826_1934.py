# Generated by Django 3.2 on 2021-08-26 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bib',
            name='worker',
        ),
        migrations.RemoveField(
            model_name='tent',
            name='worker',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='role',
        ),
        migrations.RemoveField(
            model_name='wristband',
            name='worker',
        ),
        migrations.AlterField(
            model_name='bib',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Accredit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camping', models.BooleanField(blank=True, null=True)),
                ('transport_home', models.CharField(blank=True, max_length=50, null=True)),
                ('bib', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='event.bib')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='event.role')),
                ('tent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='event.tent')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.worker')),
            ],
        ),
    ]
