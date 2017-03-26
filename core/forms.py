from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.http import JsonResponse

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        form = super(UserCreateForm, self)
        response = {'errors': '', 'response': ''}
        if self.is_valid():
            user = form.save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            response['response'] = {'status': 'success'}
            return JsonResponse(response)
        else:
            response['errors'] = form.errors
            return JsonResponse(response)
