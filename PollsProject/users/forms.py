from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # make email field unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # check if user with form.email exists
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("A user with that email address already exists.")
        return email