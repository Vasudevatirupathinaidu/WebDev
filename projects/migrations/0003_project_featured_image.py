# Generated by Django 3.2.8 on 2021-10-06 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20211006_0702'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to=''),
        ),
    ]
