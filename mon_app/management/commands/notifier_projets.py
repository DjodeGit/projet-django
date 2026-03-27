from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from mon_app.models import ProjetBlog, Subscriber


class Command(BaseCommand):
    help = 'Envoie un email de notification aux abonnés pour un projet spécifique ou tous les projets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--projet-id',
            type=int,
            help='ID du projet spécifique à notifier',
        )
        parser.add_argument(
            '--tous',
            action='store_true',
            help='Notifier pour tous les projets existants',
        )

    def handle(self, *args, **options):
        projet_id = options.get('projet_id')
        tous = options.get('tous')
        
        subscribers = Subscriber.objects.filter(is_active=True)
        
        if not subscribers.exists():
            self.stdout.write(self.style.WARNING('Aucun abonné trouvé !'))
            return
        
        recipient_list = [sub.email for sub in subscribers]
        site_url = getattr(settings, 'SITE_URL', 'https://jodeanas-portfolio.onrender.com')
        
        if projet_id:
            # Envoyer pour un projet spécifique
            try:
                projet = ProjetBlog.objects.get(id=projet_id)
                self.envoyer_email(projet, recipient_list, site_url)
                self.stdout.write(self.style.SUCCESS(f'✓ Email envoyé pour le projet: {projet.titre}'))
            except ProjetBlog.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Projet avec ID {projet_id} non trouvé !'))
        
        elif tous:
            # Envoyer pour tous les projets
            projets = ProjetBlog.objects.all().order_by('-created_at')
            if not projets.exists():
                self.stdout.write(self.style.WARNING('Aucun projet trouvé !'))
                return
            
            for projet in projets:
                self.envoyer_email(projet, recipient_list, site_url)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Emails envoyés pour {projets.count()} projets à {len(recipient_list)} abonnés'))
        
        else:
            self.stdout.write(self.style.ERROR('Veuillez spécifier --projet-id ou --tous'))
            self.stdout.write(self.style.WARNING('Exemple: python manage.py notifier_projets --tous'))

    def envoyer_email(self, projet, recipient_list, site_url):
        subject = f'Nouveau projet ajouté : {projet.titre}'
        
        message = f"""
Bonjour,

Un nouveau projet a été ajouté au portfolio de MEDONJIO TENANG JODEANAS !

═══════════════════════════════════════════════════════════

Titre du projet : {projet.titre}

Description :
{projet.description}

État du projet : {projet.get_etat_display()}

Langages/Technologies : {projet.langages}

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
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur: {str(e)}'))
