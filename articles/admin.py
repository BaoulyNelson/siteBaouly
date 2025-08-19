from django.contrib import admin
from .models import Article,Temoignage,Contact



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("titre", "categorie", "auteur", "date_publication", "active")
    list_filter = ("categorie", "date_publication", "active")
    search_fields = ("titre", "contenu")

    def get_fields(self, request, obj=None):
        fields = ["titre", "resume", "contenu", "image", "categorie", "auteur"]
        if obj and obj.categorie == "annonces":  # ✅ ajouter le champ uniquement si "annonces"
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
