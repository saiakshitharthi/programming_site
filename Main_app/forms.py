from django import forms
from . import models
from django.contrib.auth.models import User
class ProblemForm(forms.ModelForm):
    class Meta:
        model = models.Problems
        exclude = ['Number_of_submissions','Number_of_accepted',]
class SolutionForm(forms.ModelForm):
    class Meta:
        model = models.Submissions
        exclude = ['user','accepted','problem']
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password']
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = models.User_info
        exclude = ['user','points']
class FriendsForm(forms.Form):
    make_friend = forms.BooleanField()
