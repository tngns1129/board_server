# Generated by Django 4.0.3 on 2023-10-11 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0002_users_delete_test'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='users',
            table='user',
        ),
    ]
