# Generated by Django 5.1.2 on 2024-10-22 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_task_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tasks', to='main.group'),
        ),
    ]
