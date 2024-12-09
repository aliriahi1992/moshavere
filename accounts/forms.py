from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm



class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'full_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # هش کردن رمز عبور
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="شماره موبایل")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
