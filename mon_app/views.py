from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ProjetBlog, Subscriber
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

def projet(request):
    projets = ProjetBlog.objects.all().order_by('-created_at')
    return render(request,'projet.html', {'projets': projets})

@require_POST
@csrf_exempt
def subscribe(request):
    email = request.POST.get('email', '').strip()
    
    if not email:
        return JsonResponse({'success': False, 'message': 'Veuillez entrer une adresse email.'}, status=400)
    
    # Validate email format
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return JsonResponse({'success': False, 'message': 'Veuillez entrer une adresse email valide.'}, status=400)
    
    # Check if email already exists
    if Subscriber.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'Cette adresse email est déjà abonnée.'}, status=400)
    
    # Create new subscriber
    subscriber = Subscriber.objects.create(email=email)
    
    # Try to send confirmation email
    try:
        # Check if email is configured
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning("Email not configured - skipping confirmation email")
            return JsonResponse({'success': True, 'message': 'Merci ! Votre abonnement a été confirmé (sans email de confirmation).'})
        
        send_mail(
            subject='Abonnement à la Newsletter - Portfolio',
            message=f'Bonjour,\n\nMerci de vous être abonné à ma newsletter ! Vous recevrez désormais des mises à jour sur mes nouveaux projets et actualités.\n\nCordialement,\nMEDONJIO TENANG JODEANAS',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return JsonResponse({'success': True, 'message': 'Merci ! Votre abonnement a été confirmé. Consultez votre email.'})
    except Exception as e:
        logger.error(f"Email error: {str(e)}")
        # Still return success since subscriber was created
        return JsonResponse({'success': True, 'message': 'Abonnement créé ! (Email de confirmation non envoyé)'})

def contact(request):
    success = False
    error_message = None

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:
            email_content = (
                f"Nom: {name}\n"
                f"Email: {email}\n"
                f"Sujet: {subject}\n\n"
                f"Message:\n{message}"
            )

            try:
                # Check if email is configured
                if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                    logger.warning("Email not configured - cannot send message")
                    error_message = "Le système d'envoi d'emails n'est pas configuré. Veuillez me contacter directement par email."
                else:
                    send_mail(
                        subject=f"Message depuis le portfolio : {subject}",
                        message=email_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.EMAIL_HOST_USER],
                        fail_silently=False,
                    )
                    success = True
            except Exception as e:
                logger.error(f"Email error: {str(e)}")
                error_message = f"Une erreur est survenue lors de l'envoi du message. Erreur: {str(e)}"
        else:
            error_message = "Veuillez remplir tous les champs."

    return render(request, 'contact.html', {'success': success, 'error_message': error_message})
