from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'reply')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')

# Register your models here.
