from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article,Temoignage,NewsletterSubscriber
from .forms import RegistrationForm, EditProfileForm,ContactForm,TemoignageForm,MembreEquipeForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .forms import NewsletterForm
from django.contrib.auth.models import User
from django.urls import reverse
# yourapp/views.py
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Article
from .forms import ArticleForm
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from django.utils.html import strip_tags
from django.http import JsonResponse
from .models import MembreEquipe
from .models import AuditLog
from .utils import log_action
from django.contrib.admin.models import ADDITION, CHANGE

def index(request):
    a_la_une = Article.objects.filter(categorie="une").order_by("-date_publication").first()
    a_la_minute = Article.objects.filter(categorie="minute").order_by("-date_publication")[:10]
    # autres = Article.objects.exclude(categorie="une").order_by("-date_publication")[:20]
    autres = (Article.objects.exclude(categorie__in=["une", "annonces"]).order_by("-date_publication")[:20])
    populaires = Article.objects.exclude(categorie="annonces").order_by("-date_publication")[:10]
    annonces = Article.objects.filter(categorie="annonces").order_by("-date_publication")[:10]
    temoignages = Temoignage.objects.filter(approuve=True).order_by("-date")[:10]

    # Préparation de l'image pour OpenGraph (page d'accueil)
    absolute_image_url = None
    if a_la_une and a_la_une.image:
        absolute_image_url = request.build_absolute_uri(a_la_une.image.url)

    return render(request, "index.html", {
        "a_la_une": a_la_une,
        "a_la_minute": a_la_minute,
        "autres": autres,
        "populaires": populaires,
        "annonces": annonces,
        "temoignages": temoignages,
        "absolute_image_url": absolute_image_url,  # ✅ envoyé au template
    })



def articles_par_categorie(request, slug):
    # Récupérer les articles de cette catégorie
    articles = Article.objects.filter(categorie=slug).order_by("-date_publication")

    # Obtenir le label lisible depuis CATEGORIES
    label = dict(Article.CATEGORIES).get(slug, slug)

    return render(request, "articles/categorie.html", {
        "articles": articles,
        "categorie": label,  # Affichage lisible (ex: "Sport")
        "slug": slug,        # Valeur brute (ex: "sport")
    })




def audit_log_list(request):
    logs = AuditLog.objects.select_related("user", "article").order_by("-timestamp")
    return render(request, "admin/audit_logs.html", {"logs": logs})


def detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    # URL absolue de l'image pour OpenGraph
    absolute_image_url = request.build_absolute_uri(article.image.url) if article.image else None

    # Articles similaires (même catégorie, sauf l'article actuel, limité à 3)
    related_articles = Article.objects.filter(
        categorie=article.categorie
    ).exclude(id=article.id).order_by('-date_publication')[:3]

    # Choisir le template selon le rôle
    template = "dashboard/article_detail.html" if request.user.is_authenticated and request.user.is_staff else "articles/detail.html"

    return render(request, template, {
        "article": article,
        "absolute_image_url": absolute_image_url,
        "related_articles": related_articles
    })



def about_us(request):
    membres = MembreEquipe.objects.filter(est_actif=True).order_by("ordre")
    return render(request, "partials/about_us.html", {"membres_equipe": membres})


    
# Mixins pour restreindre l'accès aux staffs
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
    
class ListeEquipeView(ListView):
    model = MembreEquipe
    template_name = "dashboard/equipe/liste.html"
    context_object_name = "membres_equipe"

    def get_queryset(self):
        return MembreEquipe.objects.filter(est_actif=True).order_by("ordre")
    
class MembreEquipeCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = MembreEquipe
    form_class = MembreEquipeForm
    template_name = "dashboard/equipe/form.html"
    success_url = reverse_lazy("articles:liste-equipe")
    
    def form_valid(self, form):
        # affecter l'auteur automatiquement
        form.instance.auteur = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "✅ L'equipe a été créé avec succès !")
        return response

class MembreEquipeUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = MembreEquipe
    form_class = MembreEquipeForm
    template_name = "dashboard/equipe/form.html"
    success_url = reverse_lazy("articles:liste-equipe")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "✏️ L'equipe a été mis à jour avec succès !")
        return response
    



def equipe_json(request):
    """Endpoint JSON si tu veux charger la liste côté client via fetch."""
    qs = MembreEquipe.objects.filter(est_actif=True).order_by("ordre")
    donnees = [{
        "nom_complet": f"{m.prenom} {m.nom}".strip(),
        "prenom": m.prenom,
        "nom": m.nom,
        "role": m.role,
        "bio": m.bio,
        "image": m.image.url if m.image else None,
        "initiales": m.initiales,
        "couleur": m.couleur,
        "linkedin": m.linkedin,
        "twitter": m.twitter,
        "github": m.github,
    } for m in qs]
    return JsonResponse(donnees, safe=False, json_dumps_params={"ensure_ascii": False})


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        # rediriger vers login si pas connecté, sinon 403 (ou custom)
        if not self.request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(self.request.get_full_path())
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Accès réservé au personnel.")

# Liste des articles du dashboard (pour le staff)
class ArticleDashboardListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Article
    template_name = "dashboard/articles_list.html"
    context_object_name = "articles"
    paginate_by = 20

    def get_queryset(self):
        # le staff voit tous les articles ; tu peux filtrer si tu veux
        return Article.objects.all().order_by("-date_publication")



class ArticleCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboard/article_form.html"
    success_url = reverse_lazy("articles:articles_list")

    def form_valid(self, form):
        # affecter l'auteur automatiquement
        form.instance.auteur = self.request.user
        response = super().form_valid(form)

        # logger l’action
        log_action(
            user=self.request.user,
            obj=self.object,
            action_flag=ADDITION,
            message="Article créé via le dashboard"
        )

        messages.success(self.request, "✅ L'article a été créé avec succès !")
        return response


class ArticleUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboard/article_form.html"
    success_url = reverse_lazy("articles:articles_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        # logger l’action
        log_action(
            user=self.request.user,
            obj=self.object,
            action_flag=CHANGE,
            message="Article mis à jour via le dashboard"
        )

        messages.success(self.request, "✏️ L'article a été mis à jour avec succès !")
        return response

    
    
class ArticleDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Article
    template_name = "dashboard/article_detail.html"
    context_object_name = "article"
    
    
    
def register(request):
    # Empêcher un utilisateur déjà connecté de voir la page d'inscription
    if request.user.is_authenticated:
        return redirect("articles:index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur
            user = form.save()

            # Connecter l'utilisateur immédiatement après inscription
            login(request, user)

            # Ajouter un flag pour signaler que c'est une inscription
            request.session["from_register"] = True

            # Message de succès pour l'inscription
            messages.success(request, "✅ Inscription réussie ! Bienvenue sur le Journal Le Baouly.")

            return redirect("articles:index")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "registration/profile.html", {"user": request.user})


def confirmer_deconnexion(request):
    if request.method == "POST":
        # L'utilisateur a confirmé, on le déconnecte
        logout(request)
        messages.success(request, "Vous avez été déconnecté avec succès.")
        return redirect("articles:index")  # Ou une autre page après déconnexion

    # Si c'est un GET (ou si l'utilisateur n'a pas confirmé), on affiche la confirmation
    return render(request, "registration/confirmer_deconnexion.html")

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect("articles:profile")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "registration/edit_profile.html", {"form": form})




def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "contact/contact_success.html")
        
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})



@login_required
def temoignages(request):
    if request.method == "POST":
        form = TemoignageForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "temoignages/confirmation.html")
    else:
        form = TemoignageForm()

    liste = Temoignage.objects.filter(approuve=True).order_by("-date")
    return render(request, "temoignages/temoignages.html", {"form": form, "temoignages": liste})






def advertising(request):
    return render(request, "partials/advertising.html")

def careers(request):
    return render(request, "partials/careers.html")


def legal_notice(request):
    return render(request, "partials/legal_notice.html")

def privacy_policy(request):
    return render(request, "partials/privacy_policy.html")

def cookies_policy(request):
    return render(request, "partials/cookies_policy.html")

def subscribe(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            # envoyer email de bienvenue
            send_mail(
                "Bienvenue dans notre newsletter 🎉",
                "Merci de vous être abonné ! Vous recevrez bientôt nos actualités.",
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                fail_silently=True,
            )
            messages.success(request, "✅ Merci ! Votre adresse a bien été enregistrée.")
        else:
            # Django affichera le message d’erreur du form (email déjà inscrit ou invalide)
            messages.error(request, form.errors.get("email")[0])

        next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse("home")
        return redirect(next_url)

    return redirect("index")



# views.py


def recherche(request):
    query = request.GET.get('q', '')  # récupère le mot-clé
    results = []

    if query:
        results = Article.objects.filter(
            Q(titre__icontains=query) |
            Q(contenu__icontains=query) |
            Q(resume__icontains=query) |
            Q(categorie__icontains=query) |
            Q(auteur__username__icontains=query)  # 🔑 recherche par nom d'utilisateur
        ).order_by('-date_publication')

    return render(request, 'search/recherche.html', {
        'query': query,
        'results': results
    })

