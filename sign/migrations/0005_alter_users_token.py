# Generated by Django 4.0.3 on 2023-10-12 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0004_users_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.CharField(default='', max_length=200),
        ),
    ]
