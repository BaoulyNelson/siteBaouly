from django.contrib import admin
from .models import Article,Temoignage,Contact,NewsletterSubscriber
from .models import MembreEquipe

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("titre", "categorie", "auteur", "date_publication", "active")
    list_filter = ("categorie", "date_publication", "active")
    search_fields = ("titre", "contenu")

    def get_fields(self, request, obj=None):
        fields = ["titre", "contenu", "image", "categorie", "auteur"]
        if obj and obj.categorie == "annonces":
            fields.append("active")
        return fields


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "sujet", "date")
    search_fields = ("nom", "email", "sujet")


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ("nom", "date", "approuve")
    list_filter = ("approuve", "date")
    search_fields = ("nom", "message")
    actions = ["approuver"]

    def approuver(self, request, queryset):
        queryset.update(approuve=True)




@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "date_subscribed")   # colonnes affichées dans la liste
    search_fields = ("email",)                    # barre de recherche
    ordering = ("-date_subscribed",)              # tri par défaut : plus récents en premier
    list_filter = ("date_subscribed",)            # filtre par date dans la sidebar
    
    
    

@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "role", "ordre", "est_actif")
    list_editable = ("ordre", "est_actif")
    search_fields = ("prenom", "nom", "role")


admin.site.site_header = "Mon Journal - Administration"
admin.site.site_title = "Mon Journal"
admin.site.index_title = "Bienvenue dans l'espace d'administration"
