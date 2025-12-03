from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Article,AuditLog
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages



from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article



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
            f"Un nouvel utilisateur vient de créer un compte sur le journal Focus Media.\n\n"
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
def notify_admin_on_article_action(sender, instance, created, **kwargs):
    """
    Envoie un mail HTML à l'admin quand un staff publie ou édite un article
    """
    action = "publié" if created else "modifié"

    subject = f"[Journal] Article {action}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [settings.ADMIN_EMAIL]

    # 📩 Version texte brut (fallback)
    text_content = (
        f"Bonjour,\n\n"
        f"L'article « {instance.titre} » a été {action} par "
        f"{instance.auteur.username}.\n\n"
        f"Catégorie : {instance.get_categorie_display()}\n"
        f"Lien : {instance.get_absolute_url()}\n\n"
        f"— Votre application Django"
    )

    # 🎨 Version HTML (joli)
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height:1.6; color:#333;">
        <h2 style="color:#2c3e50;">📰 Article {action}</h2>
        <p>
          Bonjour,<br><br>
          L'article <strong>« {instance.titre} »</strong> a été <strong>{action}</strong> 
          par <em>{instance.auteur.username}</em>.
        </p>
        <p>
          <strong>Catégorie :</strong> {instance.get_categorie_display()}<br>
          <strong>Lien :</strong> 
          <a href="{instance.get_absolute_url()}" style="color:#2980b9; text-decoration:none;">
            Voir l’article
          </a>
        </p>
        <hr>
        <p style="font-size:12px; color:#888;">— Votre application Django</p>
      </body>
    </html>
    """

    # Création de l’email avec les deux versions
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


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
        
        
# signals.py


@receiver(post_save, sender=Article)
def log_article_save(sender, instance, created, **kwargs):
    if created:
        action = "create"
    else:
        action = "update"
    # On suppose que l'article a un champ "auteur" = User
    AuditLog.objects.create(
        user=instance.auteur,
        article=instance,
        action=action
    )

@receiver(post_delete, sender=Article)
def log_article_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=instance.auteur,
        article=instance,
        action="delete"
    )
