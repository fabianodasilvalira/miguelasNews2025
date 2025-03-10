from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Salva o usuário antes de retornar
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')  # Define o papel como 'Admin' para superusuários

        if password is None:
            raise ValueError('O superusuário precisa de uma senha')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove o campo username
    email = models.EmailField(unique=True)  # Usa email como identificador único
    role = models.CharField(
        max_length=20,
        choices=[('Leitor', 'Leitor'), ('Escritor', 'Escritor'), ('Admin', 'Admin')],
        default='Leitor'
    )

    USERNAME_FIELD = 'email'  # Define email como campo de identificação
    REQUIRED_FIELDS = []  # Remove 'username' dos campos obrigatórios

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Salva o usuário primeiro para garantir que o id seja atribuído
        super().save(*args, **kwargs)

        # Atualiza os grupos com base no 'role'
        self.update_groups_based_on_role()

    def update_groups_based_on_role(self):
        # Remove o usuário de todos os grupos
        self.groups.clear()

        # Adiciona o usuário ao grupo correspondente ao 'role'
        group_name = self.role
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)
