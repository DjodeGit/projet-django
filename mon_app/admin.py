from django.contrib import admin
from .models import ProjetBlog, Subscriber

# Register your models here.
@admin.register(ProjetBlog)
class ProjetBlogAdmin(admin.ModelAdmin):
    list_display = ('titre', 'etat', 'created_at', 'updated_at')
    list_filter = ('etat', 'created_at')
    search_fields = ('titre', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    ordering = ('-created_at',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
