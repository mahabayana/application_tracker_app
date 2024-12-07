from django import forms
from .models import Application, User_Person


#application form - to keep track of applications 
class ApplicationForm(forms.ModelForm):   
    class Meta:
        model = Application
        fields = ['company', 'position', 'date_applied', 'status', 'skills']

#user form defaulted to mahab and mahab@example.com- myself single user 
class UserForm(forms.ModelForm):
    class Meta:
        model = User_Person
        fields = ['name', 'email']


