# Generated by Django 3.2.8 on 2021-10-07 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_skill_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='social_youtube',
            new_name='social_stackoverflow',
        ),
    ]
