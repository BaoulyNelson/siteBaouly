from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthForm

from django.views.generic import TemplateView
app_name = "articles"

urlpatterns = [
    # Page d'accueil
    path("", views.index, name="index"),

    # Authentification
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
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
    
    # Changer de mot de passe
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Réinitialisation du mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    # Confirmation de réinitialisation de mot de passe
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Page de confirmation après la réinitialisation du mot de passe
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Inscription et profil
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    # Edition du profil (ajout)
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    
    path('recherche/', views.recherche, name='recherche'),
    path('recherche/', views.recherche, name='search'),
    path("contact/", views.contact, name="contact"),
    path("temoignages/", views.temoignages, name="temoignages"),
    
    path('qui-sommes-nous/', views.about_us, name='about_us'),
    path('publicite/', views.advertising, name='advertising'),
    path('carrieres/', views.careers, name='careers'),
    path('mentions-legales/', views.legal_notice, name='legal_notice'),
    path('politique-confidentialite/', views.privacy_policy, name='privacy_policy'),
    path('cookies/', views.cookies_policy, name='cookies_policy'),
    path("subscribe/", views.subscribe, name="subscribe"),
    
    # --- Dashboard Staff (dans le même fichier) ---
    path("dashboard/articles/", views.ArticleDashboardListView.as_view(), name="articles_list"),
    path("dashboard/articles/new/", views.ArticleCreateView.as_view(), name="article_create"),
    path("dashboard/articles/<slug:slug>/edit/", views.ArticleUpdateView.as_view(), name="article_edit"),
    path("dashboard/articles/<slug:slug>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("googlef954842a7ede02af.html",TemplateView.as_view(template_name="googlef954842a7ede02af.html"),name="google_verify",
),
    # Articles par catégorie et détail
    path("categorie/<str:slug>/", views.articles_par_categorie, name="articles_par_categorie"),
    path("<slug:slug>/", views.detail, name="detail"),


]
