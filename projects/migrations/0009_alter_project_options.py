# Generated by Django 3.2.8 on 2021-10-10 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20211010_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]