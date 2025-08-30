# articles/context_processors.py
from django.db.models import Count
from .models import Article  # adapte l'import selon ton app
from django.contrib.auth import get_user_model
from articles.models import NewsletterSubscriber,Temoignage,MembreEquipe,Contact  # adapte si nécessaire
from django.core.cache import cache

User = get_user_model()

def dashboard_stats(request):
    # cache pour éviter de frapper la DB à chaque requête
    stats = cache.get('dashboard_stats')
    if not stats:
        stats = {
            'total_articles': Article.objects.count(),
            'total_users': User.objects.count(),
            'total_testimonials': Temoignage.objects.count(),
            'total_subscribers': NewsletterSubscriber.objects.count(),
            'total_equipes': MembreEquipe.objects.count(),   # <-- nouveau compteur
            'total_contacts': Contact.objects.count(),   # <-- nouveau compteur

      
        }
        # expire au bout de 60s (ajuste selon besoin)
        cache.set('dashboard_stats', stats, 60)
    return stats
