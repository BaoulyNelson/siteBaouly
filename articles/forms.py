# articles/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, Temoignage,NewsletterSubscriber
from .models import Article


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



class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Votre email",
            "class": "w-full px-3 py-2 rounded-l-md focus:outline-none text-gray-900 bg-white border border-gray-300",
            "autocomplete": "email",
            "id": "newsletter-email"
        })
    )

    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("ℹ️ Cette adresse est déjà inscrite à la newsletter.")
        return email





class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["titre", "resume", "contenu", "image", "categorie", "active"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Titre de l'article"}),
            "resume": forms.Textarea(attrs={"class": "block w-full rounded-md p-2 border", "rows": 3, "placeholder": "Résumé"}),
            "contenu": forms.Textarea(attrs={"class": "block w-full rounded-md p-2 border", "rows": 10, "placeholder": "Contenu (Markdown/HTML selon ton usage)"}),
            "categorie": forms.Select(attrs={"class": "block w-full rounded-md p-2 border"}),
            "active": forms.CheckboxInput(attrs={"class": "h-4 w-4"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionnel : labels francisés
        self.fields["titre"].label = "Titre"
        self.fields["resume"].label = "Résumé (facultatif)"
        self.fields["contenu"].label = "Contenu"
        self.fields["image"].label = "Image de couverture"
        self.fields["categorie"].label = "Catégorie"
        self.fields["active"].label = "Publier (actif)"


from django import forms
from .models import MembreEquipe

class MembreEquipeForm(forms.ModelForm):
    class Meta:
        model = MembreEquipe
        fields = [
            "prenom",
            "nom",
            "role",
            "bio",
            "image",
            "linkedin",
            "twitter",
            "github",
            "couleur",
            "est_actif",
            "ordre",
        ]
        widgets = {
            "prenom": forms.TextInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Prénom"}),
            "nom": forms.TextInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Nom"}),
            "role": forms.TextInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Rôle dans l’équipe"}),
            "bio": forms.Textarea(attrs={"class": "block w-full rounded-md p-2 border", "rows": 4, "placeholder": "Brève biographie"}),
            "linkedin": forms.URLInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Lien LinkedIn"}),
            "twitter": forms.URLInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Lien Twitter/X"}),
            "github": forms.URLInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Lien GitHub"}),
            "couleur": forms.TextInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Classe Tailwind (ex: bg-indigo-500)"}),
            "ordre": forms.NumberInput(attrs={"class": "block w-full rounded-md p-2 border", "placeholder": "Ordre d’affichage"}),
            "est_actif": forms.CheckboxInput(attrs={"class": "h-4 w-4"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels francisés
        self.fields["prenom"].label = "Prénom"
        self.fields["nom"].label = "Nom"
        self.fields["role"].label = "Rôle"
        self.fields["bio"].label = "Biographie"
        self.fields["image"].label = "Photo de profil"
        self.fields["linkedin"].label = "Profil LinkedIn"
        self.fields["twitter"].label = "Profil Twitter/X"
        self.fields["github"].label = "Profil GitHub"
        self.fields["couleur"].label = "Couleur (fond avatar)"
        self.fields["ordre"].label = "Ordre"
        self.fields["est_actif"].label = "Actif (affiché sur le site)"
