from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
        }


# user details edit
class ProfileEditForm(forms.Form):
	user_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))
	pen_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
	bio = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), required=False)
