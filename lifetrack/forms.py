from django import forms
from django.contrib.auth.models import User
from lifetrack.models import *

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model=User
		fields=('username','first_name','password')
		labels={'first_name':'Name'}

class ListForm(forms.ModelForm):
	class Meta:
		model=HabitList
		fields=('name','freq')
