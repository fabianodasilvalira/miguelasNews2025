from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Ajuste para exibir o 'email' no lugar de 'username'
    list_display = ('email', 'role', 'is_staff')

    # Ajuste para os campos de edição no Admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),
    )

    # Ajuste para os campos na tela de adição
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )

    # Define a ordenação por 'email' em vez de 'username'
    ordering = ('email',)

    # Especifica que o 'username' não será usado
    def get_username(self, obj):
        return obj.email  # Retorna o e-mail no lugar do 'username'

    get_username.short_description = 'Username'  # A descrição será 'Username', mas vai retornar o email
