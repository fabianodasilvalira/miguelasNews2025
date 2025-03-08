from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings  # Para acessar o modelo CustomUser

# Função para criar o grupo de jornalistas e adicionar permissões
def create_journalist_group():
    journalist_group, created = Group.objects.get_or_create(name='Journalists')
    if created:
        # Atribui permissões ao grupo (opcionalmente, adicione permissões personalizadas)
        permissions = [
            Permission.objects.get(codename='add_news'),
            Permission.objects.get(codename='change_news'),
        ]
        journalist_group.permissions.set(permissions)
        journalist_group.save()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='news', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    video = models.FileField(upload_to='news_videos/', blank=True, null=True)  # Para vídeos
    original_link = models.URLField(blank=True, null=True)  # Link original, caso a notícia tenha sido copiada
    author = models.CharField(max_length=100, blank=True, null=True)  # Autor da notícia

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)  # Relacionamento com News
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)  # Para imagens

    def __str__(self):
        return f"Imagem para {self.news.title}"

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relacionamento com CustomUser
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)  # Relacionamento com News
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.author} na notícia '{self.news.title}'"

class NewsLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relacionamento com CustomUser
    news = models.ForeignKey(News, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} curtiu {self.news.title}'
