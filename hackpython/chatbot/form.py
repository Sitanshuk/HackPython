from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
	email = forms.EmailField(max_length = 254, required = True)
	password = forms.CharField(widget = forms.PasswordInput(), required = True)
	class Meta:
		model = User
		fields = ('email','password')

class SignupForm(UserCreationForm):
	email = forms.EmailField(max_length=254, required=True)
	password1=forms.CharField(widget=forms.PasswordInput(),required=True)
	password2=forms.CharField(widget=forms.PasswordInput(),required=True)
	
	class Meta:
		model = User
		fields = ('email', 'password1', 'password2')