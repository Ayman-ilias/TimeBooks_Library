# Generated by Django 5.0.1 on 2024-01-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposite'), (2, 'Borrow Book'), (3, 'Return Book')], null=True),
        ),
    ]
