from django import forms
from django.contrib.auth import get_user_model
from .models import Captcha
User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={"required": "Please enter a username.",
                                                                            'min_length': "Username must be at least 2 characters long.",
                                                                            'max_length': "Username must be at most 20 characters long."})
    email = forms.EmailField(
        error_messages={"required": "Please enter an email address.", "invalid": "Please enter a valid email address."})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        captcha_obj = Captcha.objects.filter(email=email, captcha=captcha).first()

        if not captcha_obj:
            raise forms.ValidationError("Invalid captcha.")
        captcha_obj.delete()
        return captcha

class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={"required": "Please enter an email address.", "invalid": "Please enter a valid email address."})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)