from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
from captcha.fields import CaptchaField


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255, required=False)
    profile = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'profile','password1','password2']


class ForgetPassword(forms.Form):
    username = forms.CharField(required=True)
    Email = forms.EmailField(required=True)


class Edit_info(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255, required=False)
    profile = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'profile']


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Old Password")
    new_password_1 = forms.CharField(widget=forms.PasswordInput, required=True, label="New Password")
    new_password_2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password_1 = cleaned_data.get("new_password_1")
        new_password_2 = cleaned_data.get("new_password_2")

        if new_password_1 and new_password_2 and new_password_1 != new_password_2:
            raise forms.ValidationError("New passwords don't match.")

        return cleaned_data


class user_login_form(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()
