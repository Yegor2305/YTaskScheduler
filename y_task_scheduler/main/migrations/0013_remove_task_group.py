# Generated by Django 5.1.2 on 2024-10-22 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_task_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='group',
        ),
    ]
