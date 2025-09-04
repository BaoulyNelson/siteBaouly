from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Article
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages


@receiver(user_logged_in)
def welcome_user(sender, request, user, **kwargs):
    # Si l'utilisateur vient de s'inscrire, on évite un doublon
    if request.session.pop("from_register", False):
        return

    messages.success(request, f"👋 Bonjour {user.username}, heureux de vous retrouver parmi nous 🌟")




@receiver(post_save, sender=User)
def notify_admin_on_new_user(sender, instance, created, **kwargs):
    if created:
        subject = "Nouvel utilisateur enregistré"
        message = (
            f"Bonjour,\n\n"
            f"Un nouvel utilisateur vient de créer un compte sur le journal Le Baouly.\n\n"
            f"👤 Nom d'utilisateur : {instance.username}\n"
            f"📧 Adresse e-mail : {instance.email or 'Non renseignée'}\n\n"
            f"Merci de vérifier et d’assurer le suivi si nécessaire.\n\n"
            f"— Votre application Django"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

@receiver(post_save, sender=Article)
def notify_new_article(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "articles",
            {
                "type": "article_posted",
                "message": f"📰 Nouvel article : {instance.titre}"
            }
        )