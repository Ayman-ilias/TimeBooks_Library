# Generated by Django 5.0.1 on 2024-01-08 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_rename_title_purchase_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
