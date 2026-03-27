from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ProjetBlog, Subscriber


@receiver(post_save, sender=ProjetBlog)
def send_email_to_subscribers(sender, instance, created, **kwargs):
    """
    Envoie un email à tous les abonnés quand un projet est créé ou mis à jour.
    """
    # Récupérer tous les abonnés actifs
    subscribers = Subscriber.objects.filter(is_active=True)
    
    if subscribers.exists():
        # Récupérer l'URL du site (ou utiliser une valeur par défaut)
        site_url = getattr(settings, 'SITE_URL', 'https://jodeanas-portfolio.onrender.com')
        
        # Préparer le sujet et le message
        if created:
            subject = f'Nouveau projet ajouté : {instance.titre}'
        else:
            subject = f'Projet mis à jour : {instance.titre}'
        
        # Préparer la liste des emails
        recipient_list = [subscriber.email for subscriber in subscribers]
        
        # Préparer le message avec les détails du projet
        message = f"""
Bonjour,

Un nouveau projet a été ajouté au portfolio de MEDONJIO TENANG JODEANAS !

═══════════════════════════════════════════════════════════

Titre du projet : {instance.titre}

Description :
{instance.description}

État du projet : {instance.get_etat_display()}

Langages/Technologies : {instance.langages}

═══════════════════════════════════════════════════════════

Consultez le portfolio pour voir tous les projets :
{site_url}/projets/

Cordialement,
L'équipe Portfolio
"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            print(f"✓ Email de notification envoyé à {len(recipient_list)} abonnés")
        except Exception as e:
            print(f"✗ Erreur lors de l'envoi des emails : {str(e)}")
    else:
        print("Aucun abonné trouvé - aucun email envoyé")
