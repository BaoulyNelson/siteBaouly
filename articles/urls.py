from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthForm


app_name = "articles"

urlpatterns = [
    # Page d'accueil
    path("", views.index, name="index"),

    # Authentification
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="auth/login.html",
            authentication_form=CustomAuthForm,
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="articles:index"),
        name="logout"
    ),
    # Déconnexion avec confirmation personnalisée
    path("logout/confirm/", views.confirmer_deconnexion, name="confirmer_deconnexion"),

    # Inscription et profil
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    # Edition du profil (ajout)
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    
    path('recherche/', views.recherche, name='recherche'),
    path("contact/", views.contact, name="contact"),
    path("temoignages/", views.temoignages, name="temoignages"),

    # Articles par catégorie et détail
    path("categorie/<str:slug>/", views.articles_par_categorie, name="articles_par_categorie"),
    path("<slug:slug>/", views.detail, name="detail"),


]
