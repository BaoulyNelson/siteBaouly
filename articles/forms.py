# articles/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, Temoignage


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "nom d'utilisateur",
            "autocomplete": "username",
            "id": "email",
            "class": "text-input"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Mot de passe",
            "autocomplete": "current-password",
            "class": "text-input"
        })
    )




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "placeholder": "Adresse e-mail",
        "autocomplete": "email",
        "class": "text-input",
        "id": "email"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Nom d’utilisateur",
        "autocomplete": "username",
        "class": "text-input",
        "id": "username"
    }))
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={
        "placeholder": "Mot de passe",
        "autocomplete": "new-password",
        "class": "text-input"
    }))
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirmer le mot de passe",
        "autocomplete": "new-password",
        "class": "text-input"
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet e-mail existe déjà.")
        return email
    
    
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "placeholder": "Adresse e-mail",
        "autocomplete": "email",
        "class": "text-input",
        "id": "email"
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "placeholder": "Prénom",
        "class": "text-input"
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "placeholder": "Nom",
        "class": "text-input"
    }))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un compte avec cet e-mail existe déjà.")
        return email



class ContactForm(forms.ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Votre nom",
        "class": "text-input",
        "autocomplete": "name",
        "id": "nom"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Votre email",
        "class": "text-input",
        "autocomplete": "email",
        "id": "email"
    }))
    sujet = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Sujet",
        "class": "text-input",
        "id": "sujet"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Votre message",
        "class": "text-input",
        "rows": 5,
        "id": "message"
    }))

    class Meta:
        model = Contact
        fields = ["nom", "email", "sujet", "message"]


class TemoignageForm(forms.ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Votre nom",
        "class": "text-input",
        "autocomplete": "name",
        "id": "nom"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Votre témoignage",
        "class": "text-input",
        "rows": 5,
        "id": "message"
    }))

    class Meta:
        model = Temoignage
        fields = ["nom", "message"]
