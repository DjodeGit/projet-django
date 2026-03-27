from django.urls import path
from  .views import index,about,projet,contact,projet,subscribe
from mon_app import views

urlpatterns = [
    path('',index , name='index'),
    path('about/',about,name='about'),
    path('projet/',projet,name='projet'),
    path('contact/', contact,name='contact'),
    path('projets/', projet, name='projet'),
    path('subscribe/', subscribe, name='subscribe'),
]
