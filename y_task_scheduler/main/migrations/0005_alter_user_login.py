# Generated by Django 5.1.2 on 2024-10-17 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_delete_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
