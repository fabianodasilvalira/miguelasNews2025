from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet, CategoryListCreate, CategoryDetail,
    CommentListCreate, CommentDetail, NewsLikeToggle,
    create_user, create_user_escritor_admin
)

# Configuração do Router para NewsViewSet
router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    # Endpoint para obtenção e refresh de tokens JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URLs para Category (categorias de notícias)
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),

    # URLs para Comentários
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),

    # URL para curtir/descurtir uma notícia
    path('news/<int:news_id>/like/', NewsLikeToggle.as_view(), name='news-like-toggle'),

    # URLs para criação de usuários
    path('users/register/', create_user, name='register-reader'),
    path('users/admin/create/', create_user_escritor_admin, name='register-admin-or-writer'),

    # Inclui as URLs geradas pelo Router
    path('', include(router.urls)),
]

# Serve arquivos de mídia em ambiente de desenvolvimento (modo DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)