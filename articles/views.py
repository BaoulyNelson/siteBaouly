from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article,Temoignage
from .forms import RegistrationForm, EditProfileForm,ContactForm,TemoignageForm
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .forms import NewsletterForm
from .models import NewsletterSubscriber
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


def index(request):
    a_la_une = Article.objects.filter(categorie="une").order_by("-date_publication").first()
    a_la_minute = Article.objects.filter(categorie="minute").order_by("-date_publication")[:10]
    autres = Article.objects.exclude(categorie="une").order_by("-date_publication")[:20]
    populaires = Article.objects.exclude(categorie="annonces").order_by("-date_publication")[:6]
    annonces = Article.objects.filter(categorie="annonces").order_by("-date_publication")[:3]
    temoignages = Temoignage.objects.filter(approuve=True).order_by("-date")[:3]  # les 3 derniers témoignages

    return render(request, "index.html", {
        "a_la_une": a_la_une,
        "a_la_minute": a_la_minute,
        "autres": autres,
        "populaires": populaires,
        "annonces": annonces,
        "temoignages": temoignages,  # ✅ ajout
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




def detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.user.is_authenticated and request.user.is_staff:
        template = "dashboard/article_detail.html"
    else:
        template = "articles/detail.html"

    return render(request, template, {"article": article})
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
        # option: staff voit tous; si tu veux restreindre à ses propres articles, filter(auteur=self.request.user)
        return Article.objects.all().order_by("-date_publication")

class ArticleCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboard/article_form.html"
    success_url = reverse_lazy("articles:articles_list")

    def form_valid(self, form):
        # affecter l'auteur automatiquement
        form.instance.auteur = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboard/article_form.html"
    success_url = reverse_lazy("articles:articles_list")

class ArticleDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Article
    template_name = "dashboard/article_detail.html"
    context_object_name = "article"
    
    
    
def register(request):
    if request.user.is_authenticated:
        return redirect("articles:index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Ajouter un message de succès
            messages.success(request, "Inscription réussie ! Bienvenue sur Mon Journal.")
            return redirect("articles:index")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})



@login_required
def profile(request):
    return render(request, "registration/profile.html", {"user": request.user})


def confirmer_deconnexion(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Vous avez été déconnecté avec succès.")
        return redirect("articles:index")
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




def about_us(request):
    return render(request, "partials/about_us.html")

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

from django.db.models import Q

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

