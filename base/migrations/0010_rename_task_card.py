# Generated by Django 4.1.7 on 2023-05-12 20:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0009_alter_task_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Task',
            new_name='Card',
        ),
    ]