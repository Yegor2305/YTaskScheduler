# Generated by Django 5.1.2 on 2024-10-24 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_user_groups_remove_user_user_permissions_and_more'),
        ('main', '0024_group_user_resource_user_alter_task_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='accounts.user'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='accounts.user'),
        ),
    ]
