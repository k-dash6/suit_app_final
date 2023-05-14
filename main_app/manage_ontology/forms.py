from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username',)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddElements(forms.Form):
    subject_name = forms.CharField(max_length=100, required=False)
    predicat_name = forms.CharField(max_length=100, required=False)
    object_name = forms.CharField(max_length=100, required=False)


class ReturnRandom(forms.Form):
    property = forms.CharField(max_length=100, required=False)
    obj = forms.CharField(max_length=100, required=False)


class DeleteElements(forms.Form):
    element_name = forms.CharField(max_length=100, required=False)


class DeleteOneElement(forms.Form):
    subject_name = forms.CharField(max_length=100, required=False)
    predicat_name = forms.CharField(max_length=100, required=False)
    object_name = forms.CharField(max_length=100, required=False)
