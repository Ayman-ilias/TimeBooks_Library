from django.shortcuts import render
from books.models import Book,Category

def all_books(request):
    return render(request,'index.html')


def home(request,category_slug=None):
    data = Book.objects.all()
    # catagory=None
    if category_slug is not None:
        category=Category.objects.get(slug=category_slug)
        data = Book.objects.filter(category = category)
    categories = Category.objects.all()
    return render(request,'home.html',{'data' : data, 'category': categories})
