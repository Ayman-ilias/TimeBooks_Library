from typing import Any
from django.shortcuts import render, redirect
from .import forms,models
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from books.models import Book   
from django.contrib import messages
from django.utils import timezone
from .models import Purchase,Book,Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CommentForm
from .models import RATING_CHOICES
from transactions.models import Transaction
from reader.models import UserBookAccount
from transactions.constants import BORROW_BOOK,RETURN_BOOK
import datetime
# from reader.views import send_reg_email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives


class DetailPostView(DetailView):
    model = Book
    template_name = 'detail_book.html'
    context_object_name = 'book'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            book = self.get_object()
            comment_form = CommentForm(data=request.POST)

            has_borrowed = Purchase.objects.filter(user=request.user, book=book).exists()

            if has_borrowed:
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.post = book
                    new_comment.user = request.user
                    new_comment.save()
                    messages.success(request, 'Thank you for your Review')
                else:
                    messages.error(request, 'Invalid Information')
            else:
                messages.error(request, 'You need to borrow this book to give a review.')
        else:
            messages.error(request, 'You need to be logged in to give a review.')

        return redirect('detail_book', id=kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = book.comments.all()
        comment_form = CommentForm()
        
        
        if self.request.user.is_authenticated:
        
            has_borrowed = Purchase.objects.filter(user=self.request.user, book=book).exists()
            context['has_purchased_or_borrowed'] = has_borrowed
        else:
        
            context['has_borrowed'] = False

        context['comments'] = comments
        context['comment_form'] = comment_form
        context['stars'] = dict(RATING_CHOICES)
        return context





# class DetailPostView(DetailView):
#     model = Book
#     pk_url_kwarg = 'id'
#     template_name = 'detail_book.html'

#     def post(self, request, *args,**kwargs):
#         comment_form = forms.CommentForm(data=self.request.POST)
#         post = self.get_object()
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.save()
#         return self.get(request,*args,**kwargs)




#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comments = post.comments.all()
#         comment_form = forms.CommentForm()

#         context['comments'] = comments
#         context['comment_form'] = comment_form
#         context['stars'] = dict(RATING_CHOICES)
#         return context

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = self.get_object()
    #     comments = post.comments.all()
    #     comment_form = forms.CommentForm()

    #     context['comments'] = comments
    #     context['comment_form'] = comment_form
    #     return context


# @login_required
# def borrow(request, book_id):
#     user = request.user
#     if request.method == 'POST':
#         book = Book.objects.get(id=book_id)
#         if book.quantity != 0:
#             book.quantity -= 1
#             book.save()
#             purchase = Purchase(user=request.user, book=book, category=book.category)
#             purchase.save()

#             account = Transaction.objects.get(user=user)
#             account.balance -= book.borrowing_price
#             account.save()

#             messages.success(request, f'Thank you for purchasing {book.title}')
#             return redirect('profile')
        
#         else:
#             messages.error(request,"sorry not available")
#             return render(request, 'borrow.html', {'book': book})
            
            
#     else:
#         return render(request, 'borrow.html', {'book': Book.objects.get(id=book_id)})
    

# @login_required
# def return_book(request, purchase_id):
#     purchase = get_object_or_404(Purchase, id=purchase_id)
#     if request.user != purchase.user:
#         messages.error(request, "")
#         return redirect('profile')

#     book = purchase.book

#     if request.method == 'POST':
#         book.quantity += 1
#         book.save()
#         # purchase.return_date = datetime.date.today()
#         purchase.return_date = datetime.date.today()
#         purchase.save()

#         messages.success(request, f'Thank you for returning {book.title}')
#         return redirect('profile')

#     return render(request, 'return.html', {'purchase': purchase})
def send_borrow_email(user,subject, book, borrowing_price, balance_after_borrowing,template):
    subject = 'Book Borrowed Successfully'
    message = render_to_string(template, {
        'user': user,
        'book': book,
        'borrowing_price': borrowing_price,
        'balance_after_borrowing': balance_after_borrowing,
        })
    
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()
    print("Borrowing Email sent successfully")



@login_required
def borrow(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        if book.quantity != 0:
            
            borrowing_price = book.borrowing_price

            
            if request.user.account.balance >= borrowing_price:
                
                request.user.account.balance -= borrowing_price
                request.user.account.save()

            
                book.quantity -= 1
                book.save()

                
                purchase = Purchase(user=request.user, book=book, category=book.category, borrowing_price=borrowing_price)
                purchase.save()
                Transaction.objects.create(
                account=request.user.account,
                transaction_type=BORROW_BOOK,
                amount=borrowing_price,
                balance_after_transaction=request.user.account.balance)

                messages.success(request, f'Thank you for borrowing {book.title}')
                subject = 'Book Borrowed Successfully'
                template = 'borrow_email_template.html' 
                # send_reg_email(request.user, book.id, subject, template)
                send_borrow_email(request.user, 'SuccessFully Borrowed' , book, borrowing_price, request.user.account.balance,'borrow_email.html')

                return redirect('profile')
            else:
                messages.error(request, 'Insufficient balance to borrow the book.')
                return render(request, 'borrow.html', {'book': book})
        else:
            messages.error(request, "Sorry, the book is not available Now.")
            return render(request, 'borrow.html', {'book': book})
    else:
        return render(request, 'borrow.html', {'book': Book.objects.get(id=book_id)})
    



@login_required
def return_book(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    if request.user != purchase.user:
        messages.error(request, "ERROR 404 ")
        return redirect('profile')

    book = purchase.book

    if request.method == 'POST':
        book.quantity += 1
        book.save()
        borrowing_price = book.borrowing_price
        amount_to_add = borrowing_price
        user_account = UserBookAccount.objects.get(user=request.user)
        user_account.balance += amount_to_add
        user_account.save()
        purchase.return_date = datetime.date.today()
        purchase.save()
        Transaction.objects.create(
            account=request.user.account,
            transaction_type=RETURN_BOOK,
            amount=borrowing_price,
            balance_after_transaction=request.user.account.balance)

        messages.success(request, f'Thank you for returning {book.title}. {amount_to_add} added to your balance.')
        return redirect('profile')

    return render(request, 'return.html', {'purchase': purchase})