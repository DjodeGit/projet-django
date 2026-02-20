from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ProjetBlog, Subscriber

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
    
    # Check if email already exists
    if Subscriber.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'Cette adresse email est déjà abonnée.'}, status=400)
    
    # Create new subscriber
    subscriber = Subscriber.objects.create(email=email)
    
    # Send confirmation email
    try:
        send_mail(
            subject='Abonnement à la Newsletter - Portfolio',
            message=f'Bonjour,\n\nMerci de vous être abonné à ma newsletter ! Vous recevrez désormais des mises à jour sur mes nouveaux projets et actualités.\n\nCordialement,\nMEDONJIO TENANG JODEANAS',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return JsonResponse({'success': True, 'message': 'Merci ! Votre abonnement a été confirmé. Consultez votre email.'})
    except Exception as e:
        print("Erreur envoi email:", str(e))
        return JsonResponse({'success': True, 'message': 'Abonnement créé ! (Email de confirmation non envoyé)'})

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

def contact(request):
    success = False  # par défaut

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
                send_mail(
                    subject=f"Message depuis le portfolio : {subject}",
                    message=email_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                success = True
            except Exception as e:
                print("Erreur envoi email :", str(e))  # pour voir dans la console
                # Tu peux laisser success = False (c'est déjà le cas)
        # else: on laisse success = False si champs vides

    # Toujours renvoyer success dans le contexte, même sur GET ou erreur
    return render(request, 'contact.html', {'success': success})