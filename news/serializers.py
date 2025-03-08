from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import CustomUser
from .models import Category, News, NewsImage, Comment, NewsLike
from django.contrib.auth.models import User


# Serializer para Categoria
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# Serializer para Imagens de Notícias
class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image']


# Serializer para Comentários
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'news', 'created_at']


# Serializer para Curtidas em Notícias
class NewsLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLike
        fields = ['id', 'user', 'news', 'created_at']


# Serializer para Notícia
class NewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = NewsLikeSerializer(many=True, read_only=True)  # Para incluir as curtidas
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'published_date', 'category', 'views', 'video', 'original_link', 'author', 'images', 'comments', 'likes']


CustomUser = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']  # Inclui os campos necessários

    def create(self, validated_data):
        # Define a role padrão como 'leitor', caso não seja enviada
        role = validated_data.get('role', 'leitor')

        # Criação do usuário com hash da senha
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )
        return user

    def to_representation(self, instance):
        """
        Remove a senha antes de retornar os dados do usuário.
        """
        data = super().to_representation(instance)
        data.pop('password', None)  # Remove a senha dos dados retornados
        return data