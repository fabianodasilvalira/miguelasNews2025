from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Certifique-se de que o caminho do modelo esteja correto


# Customizando o UserAdmin para exibir a role do CustomUser
class CustomUserAdmin(UserAdmin):
    # Define os campos a serem exibidos na lista de usuários no Admin
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined', 'last_login')  # Adiciona 'role'

    # Define filtros adicionais na listagem de usuários
    list_filter = ('role', 'is_active')  # Permite filtrar usuários por role e status ativo

    # Define os campos exibidos na tela de detalhes do usuário
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )

    # Define os campos que podem ser editados diretamente na lista de usuários
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )


# Registra o CustomUser no Django Admin com a customização
admin.site.register(CustomUser, CustomUserAdmin)
