from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
	username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'help_text':' '}))	

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].label = 'Password'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].label = 'Confirm Password'


