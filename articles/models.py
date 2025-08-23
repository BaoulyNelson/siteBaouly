from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Article(models.Model):
    CATEGORIES = [
        ("une", "À la une"),
        ("minute", "À la minute"),
        ("annonces", "Annonces"),
        ("culture", "Culture"),
        ("economie", "Économie"),
        ("emploi", "Emploi"),
        ("editorial", "Éditorial"),
        ("international", "International"),
        ("national", "National"),
        ("opinions", "Opinions"),
        ("societe", "Société"),
        ("sport", "Sport"),
    ]

    titre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)

    resume = models.TextField(blank=True, null=True)
    contenu = models.TextField()
    active = models.BooleanField(default=True)  # ✅ actif/inactif
    image = models.ImageField(upload_to="articles/%Y/%m/%d/", blank=True, null=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default="une")
    date_publication = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articles"
    )
    
    class Meta:
        ordering = ["-date_publication"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        # si slug vide, le générer à partir du titre
        if not self.slug:
            base = slugify(self.titre)[:240]
            slug = base
            # éviter collisions simples (ajouter -1, -2 si nécessaire)
            i = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:detail", args=[self.slug])



class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet}"


class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)  # ✅ tu valides dans l’admin

    def __str__(self):
        return f"Témoignage de {self.nom}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email