# Generated by Django 3.2 on 2021-10-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0017_alter_workerimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workerimage',
            name='image',
            field=models.ImageField(default="C:\\Users\\O'Niel Richards\\Documents\\workspace\\festival2\\media/avatar.png", upload_to='photo/<function WorkerImage.uploadLocation at 0x04B0E8A0>'),
        ),
    ]
