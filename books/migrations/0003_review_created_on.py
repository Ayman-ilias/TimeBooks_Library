# Generated by Django 5.0.1 on 2024-01-07 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_remove_book_user_reviews_book_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]