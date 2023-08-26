from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Select category"

    class Meta:
        model = Item
        exclude = ("user", "slug")
        fields = [
            "user",
            "title",
            "slug",
            "content",
            "photo",
            "link",
            "is_published",
            "cat",
        ]
        widgets = {
            "user": forms.HiddenInput(),
            "slug": forms.HiddenInput(),
            "title": forms.TextInput(),
            "content": forms.Textarea(
                attrs={"id": "comment", "name": "comment"}
            ),
            "cat": forms.Select(),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 200:
            raise ValidationError("Length exceeds 200 characters")

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput())
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"type": "email"})
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"type": "password"})
    )
    password2 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"type": "password"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Login")
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"type": "password"})
    )


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        max_length=125,
        widget=forms.TextInput(attrs={"class": "input"}),
    )
    last_name = forms.CharField(
        label="First Name",
        max_length=125,
        widget=forms.TextInput(attrs={"class": "input"}),
    )
    email = forms.EmailField(
        label="Email", widget=forms.TextInput(attrs={"class": "input", "type": "email"})
    )
    content = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={"class": "input01", "row": 3})
    )

    class Meta:
        model = FeedBack
        exclude = ("user",)
        fields = [
            "user",
            "first_name",
            "last_name",
            "email",
            "content",
        ]
        widgets = {
            "user": forms.HiddenInput(),
        }
