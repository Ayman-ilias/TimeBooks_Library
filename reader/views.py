from typing import Any
from django.shortcuts import render, redirect
from .import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from posts.models import post
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from books.views import Purchase
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives


def send_email(user,subject, template):
    message = render_to_string(template, {
        'user' : user,
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


def send_reg_email(user,account_id,subject, template):
    message = render_to_string(template, {
        'user' : user,
        'account_id' : account_id
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()
    print("registration Email sent successfully")




def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            
            account_id = user.account.id 
            
            send_reg_email(user, account_id, 'Registration Successful', 'registration_email.html')
            
            messages.success(request, 'Registered successfully and Logged In the TimeBooks Library')
            return redirect('home')
    else:
        register_form = forms.RegistrationForm()

    return render(request, 'user_registration.html', {'form': register_form})


# class UserRegistrationView(FormView):
#     template_name = 'user_registration.html'
#     form_class = RegistrationForm
#     success_url = reverse_lazy('home')
#     def form_valid(self,form):
#         user = form.save()
#         login(self.request, user)
#         account_no=user.account.account_no
#         send_reg_email(self.request.user,account_no, "Account Registration", "accounts/registration_email.html")
#         return super().form_valid(form)



class UserLoginView(LoginView):
    template_name='user_login.html'
    # success_url=reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')
    

    def form_valid(self, form):
        messages.success(self.request,'Logged In Successfully ツ ')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request,' Invalid Information ( ˘︹˘ ) ')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context    
    
 

# @login_required
# def profile(request):
#     return render(request, 'profile.html')

@login_required
def profile(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'profile.html', {'purchases': purchases})
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeuserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated successfully')
            return redirect('edit_profile')
    else:
        profile_form = forms.ChangeuserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': profile_form})

def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'PassWord Updated Successfully')
            send_email(request.user, "PassWord Change", "pass_change_email.html")
            update_session_auth_hash(request,form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request,"Logged out successfully")
    return redirect('user_login')
    

def test(request):
    return render(request,'register.html')

