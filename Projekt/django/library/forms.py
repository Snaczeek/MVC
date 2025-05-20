from django import forms
from django.forms import DateInput, NumberInput, PasswordInput, Select, TextInput, widgets
from .models import Book, Author, Borrow
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'author': Select(attrs={'class': 'form-control'}),
            'year': NumberInput(attrs={'class': 'form-control'}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_date']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'birth_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

