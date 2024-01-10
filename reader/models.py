from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE
# django amaderke built in user niye kaj korar facility dey


class UserBookAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_id = models.IntegerField(unique=True) # account no duijon user er kokhono same hobe na
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2) 
    
    def __str__(self):
        return str(self.account_id)
    
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    

    def __str__(self):
        return str(self.user.email)
    