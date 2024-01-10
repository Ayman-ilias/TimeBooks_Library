from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import  GENDER_TYPE,UserBookAccount,UserInfo

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    country = forms.CharField(max_length=100)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    city = forms.CharField(max_length= 100)
    mobile_number = forms.DecimalField(max_digits=12, decimal_places=2)
    

    class Meta:
        model = User
        fields = ['username' ,'first_name' , 'last_name','email', 'password1','password2', 'gender', 'birth_date','mobile_number','city','country']
    


    def save(self, commit=True):
        our_user = super().save(commit=False) # ami database e data save korbo na ekhn
        if commit == True:
            our_user.save() # user model e data save korlam
            # account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            # postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            # street_address = self.cleaned_data.get('street_address')
            
            UserInfo.objects.create(
                user = our_user,
                # postal_code = postal_code,
                country = country,
                city = city,
                # street_address = street_address
            )
            UserBookAccount.objects.create(
                user = our_user,
                # account_type  = account_type,
                gender = gender,
                birth_date =birth_date,
                account_id = 900000+ our_user.id
            )
        return our_user




class ChangeuserForm(UserChangeForm):
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    mobile_number = forms.DecimalField(max_digits=12, decimal_places=2)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    password= None


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'mobile_number', 'city', 'country']
        exclude = ['password']