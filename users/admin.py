from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'country', 'email_verified')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('email_verified', 'country')
    readonly_fields = ('email_verification_token',)