# Generated by Django 5.1.2 on 2024-10-22 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_task_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='group',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='main.group'),
        ),
    ]