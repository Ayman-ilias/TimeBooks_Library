# Generated by Django 5.0.1 on 2024-01-09 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transaction_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
    ]