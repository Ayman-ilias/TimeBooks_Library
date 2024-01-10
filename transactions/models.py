from django.db import models
from reader.models import UserBookAccount
from .constants import TRANSACTION_TYPE
# from django.contrib.auth.models import User




# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(UserBookAccount, related_name = 'transactions', on_delete = models.CASCADE) # ekjon user er multiple transactions hote pare
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)

    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12,null = True)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['timestamp'] 
