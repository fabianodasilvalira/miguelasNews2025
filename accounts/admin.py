# admin.py do seu app accounts
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Ou o nome correto do seu modelo

admin.site.register(CustomUser, UserAdmin)
