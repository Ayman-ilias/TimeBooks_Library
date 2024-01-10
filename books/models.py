from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug= models.SlugField(max_length=100,null=True, blank= True,unique = True)


    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    writter_name = models.CharField(max_length=200,default =None)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to ='uploads/', blank = True, null = True)
    

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Book, on_delete=models.CASCADE ,related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    body = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" comments by {self.user}"
    

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null = True, blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)