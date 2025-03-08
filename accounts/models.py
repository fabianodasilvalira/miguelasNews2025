from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')  # Define o papel como 'Admin' para superusuários
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Remove o campo 'username' e usa 'email' como identificador único
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[('Leitor', 'Leitor'), ('Escritor', 'Escritor'), ('Admin', 'Admin')],
        default='Leitor'
    )

    USERNAME_FIELD = 'email'  # Usa 'email' como campo de login
    REQUIRED_FIELDS = []  # Remove 'username' dos campos obrigatórios

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Verifica se o campo 'role' foi alterado
        if self.pk:  # Verifica se o usuário já existe no banco de dados
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.role != self.role:  # Se o 'role' foi alterado
                self.update_groups_based_on_role()
        else:  # Se é um novo usuário
            self.update_groups_based_on_role()

        super().save(*args, **kwargs)

    def update_groups_based_on_role(self):
        # Remove o usuário de todos os grupos
        self.groups.clear()

        # Adiciona o usuário ao grupo correspondente ao 'role'
        group_name = self.role
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)