# Generated by Django 3.1.4 on 2021-05-01 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file_location',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
    ]
