from django.contrib import admin
from .models import UserInfo,UserBookAccount

# Register your models here.
admin.site.register(UserBookAccount)
admin.site.register(UserInfo)