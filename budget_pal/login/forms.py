from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# para incluir el mail en registro

class NuevoRegistro(UserCreationForm):

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def save(self, commit=True):
		user = super(NuevoRegistro, self).save(commit=False)
		if commit:
			user.save()
		return user
	