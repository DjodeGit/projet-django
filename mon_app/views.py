from django.shortcuts import render
from .models import ProjetBlog

# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request,'about.html')
def projet(request):
    return render(request,'projet.html')
def contact(request):
    return render(request,'contact.html')


