from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# para incluir el mail en registro

class NuevoRegistro(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ["username", "email", "password"]

	# def save(self, commit=True):
	# 	user = super(NuevoRegistro, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user
