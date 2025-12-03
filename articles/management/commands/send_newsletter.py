from django.core.management.base import BaseCommand
from django.conf import settings
from articles.models import Article, NewsletterSubscriber
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    help = "Envoie les dernières actualités aux abonnés de la newsletter"

    def handle(self, *args, **kwargs):
        subscribers = NewsletterSubscriber.objects.all()
        latest_articles = Article.objects.filter(active=True).order_by('-date_publication')[:5]

        if not latest_articles.exists():
            self.stdout.write("Aucun article actif trouvé.")
            return

        site_url = "https://focusmedia.pythonanywhere.com/"  # adapte à ton domaine

        html_content = render_to_string("newsletter/newsletter.html", {
            "articles": latest_articles,
            "site_url": site_url
        })

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(
                subject="Nos dernières actualités 📰",
                body="Vous ne pouvez pas voir ce mail ? Activez le HTML.",  # fallback texte
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            self.stdout.write(f"Email envoyé à {subscriber.email}")

        self.stdout.write(self.style.SUCCESS("✅ Newsletter envoyée à tous les abonnés."))
