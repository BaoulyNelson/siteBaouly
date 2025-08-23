from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


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
