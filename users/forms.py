import re
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Librarian


from .models import Librarian


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Email"}),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Password"}),
    )

    class Meta:
        fields = ("email", "password")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not Librarian.objects.filter(email=email).exists():
            raise ValidationError(_("User with that email does not exist"))

        return email


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter First Name"}),
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Last Name"}),
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Email"}),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Password"}),
    )

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Repeat Password"}),
    )

    class Meta:
        model = Librarian
        fields = ["first_name", "last_name", "email", "password", "repeat_password"]

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        
        if not re.match(r"^[A-Za-z\s]+$", first_name):
            raise ValidationError(_("First name should only contain letters and spaces."))

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if not re.match(r"^[A-Za-z\s]+$", last_name):
            raise ValidationError(_("Last name should only contain letters and spaces."))  

        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Librarian.objects.filter(email=email).exists():
            raise ValidationError(_("Email already exists"))

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return password

    def clean_repeat_password(self):
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("repeat_password")

        if password != repeat_password:
            raise ValidationError(_("Passwords do not match"))

        return repeat_password