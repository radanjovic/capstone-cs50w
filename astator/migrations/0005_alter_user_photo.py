# Generated by Django 3.2.9 on 2021-12-15 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astator', '0004_auto_20211214_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='default_profile_pic.png', upload_to='photos/%Y/%m/%D/'),
        ),
    ]
