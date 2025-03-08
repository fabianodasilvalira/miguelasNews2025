from django.test import TestCase
from django.contrib.auth.models import Group

from accounts.models import CustomUser
from .models import Category, News

class CustomUserTests(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.assertEqual(user.role, 'Leitor')

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(email='admin@example.com', password='password123')
        self.assertEqual(superuser.role, 'Admin')

class NewsTests(TestCase):
    def test_create_news(self):
        category = Category.objects.create(name='Test Category', description='Test Description')
        user = CustomUser.objects.create_user(email='author@example.com', password='password123')
        news = News.objects.create(title='Test News', content='Test Content', category=category, author=user)
        self.assertEqual(news.author, user)