from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from .models import Category, News, NewsImage, Comment, NewsLike, Sponsor
from rest_framework import serializers



# Serializer para Categoria
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color']

# Serializer para Imagens de Notícias
class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image']

# Serializer para Comentários
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'news', 'created_at']
        read_only_fields = ['user', 'created_at']

# Serializer para Curtidas em Notícias
class NewsLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLike
        fields = ['id', 'user', 'news', 'created_at']


# Serializer para Patrocinador
class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'logo', 'website', 'start_date', 'end_date', 'description']

# Serializer para Notícia
class NewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # Comentários relacionados à notícia
    likes = NewsLikeSerializer(many=True, read_only=True)  # Curtidas relacionadas à notícia
    images = NewsImageSerializer(many=True, read_only=True)  # Imagens relacionadas à notícia
    category = CategorySerializer(read_only=True)  # Categoria da notícia
    like_count = serializers.SerializerMethodField()  # Campo calculado para quantidade de curtidas
    comment_count = serializers.SerializerMethodField()  # Campo calculado para quantidade de comentários
    sponsors = SponsorSerializer(many=True, read_only=True)  # Patrocinadores relacionados à notícia

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'published_date', 'category', 'views', 'video', 'original_link', 'author',
            'images', 'category', 'comments', 'likes', 'like_count', 'comment_count', 'highlight', 'sponsors'
        ]

    def get_like_count(self, obj):
        # Retorna a quantidade de curtidas para a notícia
        return NewsLike.objects.filter(news=obj).count()

    def get_comment_count(self, obj):
        # Retorna a quantidade de comentários para a notícia
        return Comment.objects.filter(news=obj).count()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']  # Inclua todos os campos necessários

    def validate_role(self, value):
        if value not in ['Leitor', 'Escritor', 'Admin']:
            raise ValidationError("Role inválido. Aceito apenas: 'Leitor', 'Escritor' ou 'Admin'.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'Leitor')  # Se role não for fornecido, usa 'Leitor' por padrão
        )
        return user  # Retorna o usuário salvo


