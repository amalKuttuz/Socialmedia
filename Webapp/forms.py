from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from api.models import *

class PostsForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["post","image"]
        widgets={
            "post":forms.Textarea(attrs={"class":"form-conotrol","row":5}),
            "image":forms.FileInput(attrs={"class":"form-select"})
        }

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()




class UserForm(forms.ModelForm):
      class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email']

class ProfileForm(forms.ModelForm):
      class Meta:
        model = Profile
        fields = ['bio']

class Commentform(forms.ModelForm):
      class Meta:
            model = Comments
            fields = ['comment','user','post']


class DeleteForm(forms.Form):
    post_id = forms.CharField(widget=forms.HiddenInput())