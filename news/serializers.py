from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, News, NewsImage, Comment, NewsLike


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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user