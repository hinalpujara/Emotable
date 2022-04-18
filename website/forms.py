from pyexpat import model
from tkinter import Widget
from attr import attr
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField
from django.db.models import fields
from .models import GENDER_CHOICES, Post, Profile

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control round_border',
            'placeholder': 'Password',
        }
))

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'First name'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'Last name'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'Email'}
    ))
    username = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control round_border',
            'placeholder': 'Password',
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control round_border',
            'placeholder': 'Confirm password',
        }))

    class Meta:
        model = User
        fields = ['first_name','last_name','email',"username",'password1','password2']

class ProfileRegisterForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.TextInput(
        attrs={
            'type': 'date',
            'class':'form-control round_border',
            'placeholder':'Birth date'
        }
    ))

    gender = forms.CharField(widget=forms.Select(
        choices=GENDER_CHOICES,
        attrs={
            'class':'form-control round_border',
            'placeholder':'Gender'
        }))



    class Meta:
        model = Profile
        fields = ["birth_date","gender"]

class PostContent(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Post
        fields = ["content"]

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'First name'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'Last name'}))
    
    username = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class': 'form-control round_border', 'placeholder': 'Username'}))
    
    
    class Meta:
        model = User
        fields = ['first_name','last_name',"username"]
 

class ProfileUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.TextInput(
        attrs={
            'type': 'date',
            'class':'form-control round_border',
            'placeholder':'Birth date'
        }
    ))
    gender = forms.CharField(widget=forms.Select(
        choices=GENDER_CHOICES,
        attrs={
            'class':'form-control round_border',
            'placeholder':'Gender'
        }))

    bio =  forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control round_border', 'placeholder': 'Bio',"rows":3, "cols":10}
    ))
    profile_picture = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['birth_date', 'gender', 'bio','profile_picture']

