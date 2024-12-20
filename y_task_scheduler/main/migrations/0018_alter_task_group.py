# Generated by Django 5.1.2 on 2024-10-22 12:04

import django.db.models.deletion
import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_task_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='group',
            field=models.ForeignKey(default=main.models.get_default_group, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='main.group'),
        ),
    ]
