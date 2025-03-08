from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import create_user, create_user_escritor_admin  # Certifique-se de importar a função correta

from .views import (
    NewsListCreate, NewsDetail, CategoryListCreate, CategoryDetail,
    CommentListCreate, CommentDetail, NewsLikeToggle,
)

# Definição das URLs


urlpatterns = [
    # Endpoint para obtenção e refresh de tokens JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URLs para Category (categorias de notícias)
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),  # Lista e cria categorias
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),  # Detalha, atualiza e deleta uma categoria

    # URLs para News (notícias)
    path('news/', NewsListCreate.as_view(), name='news-list-create'),  # Lista e cria notícias
    path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),  # Detalha, atualiza e deleta uma notícia

    # URLs para Comentários
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),

    # URL para curtir/descurtir uma notícia
    path('news/<int:news_id>/like/', NewsLikeToggle.as_view(), name='news-like-toggle'),

    path('users/register/', create_user, name='register-reader'),  # cadastrar como leitor
    path('users/admin/create/', create_user_escritor_admin, name='register-admin-or-writer'), # riar escritores/admins
]

# Serve arquivos de mídia em ambiente de desenvolvimento (modo DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
