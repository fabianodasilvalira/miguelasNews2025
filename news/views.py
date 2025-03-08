from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from django.contrib.auth.models import Group
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from .models import News, Category, Comment, NewsLike
from .serializers import NewsSerializer, CategorySerializer, CommentSerializer, UserCreateSerializer

# Permissões Personalizadas
class IsReader(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Leitor').exists()

class IsWriter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Escritor').exists() or request.user.is_superuser
        )

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Admin').exists() or request.user.is_superuser
        )

# ViewSet para Notícias
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-published_date')
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsWriter | IsAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# View para Listar e Criar Categorias
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

# View para Detalhes, Atualização e Exclusão de Categorias
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

# View para Listar e Criar Comentários
class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsReader]

    def perform_create(self, serializer):
        news_id = self.request.data.get('news')
        if news_id:
            try:
                news = News.objects.get(id=news_id)
                serializer.save(user=self.request.user, news=news)
            except News.DoesNotExist:
                raise serializers.ValidationError("Notícia não encontrada.")
        else:
            raise serializers.ValidationError("Campo 'news' é obrigatório.")

# View para Detalhes, Atualização e Exclusão de Comentários
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsReader]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and obj.user != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar/excluir este comentário.")
        return obj

# View para Curtir/Descurtir Notícias
class NewsLikeToggle(APIView):
    permission_classes = [IsReader]

    def post(self, request, news_id, *args, **kwargs):
        user = request.user
        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            return Response({"detail": "Notícia não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        like, created = NewsLike.objects.get_or_create(user=user, news=news)

        if not created:
            like.delete()
            return Response({"detail": "Curtida removida."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Notícia curtida."}, status=status.HTTP_201_CREATED)

# View para Criar Usuários (Leitores)
@api_view(['POST'])
def create_user(request):
    data = request.data.copy()
    data['role'] = 'Leitor'

    serializer = UserCreateSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()  # Salva o usuário no banco de dados
        group = Group.objects.get(name='Leitor')
        user.groups.add(group)  # Agora o usuário tem um ID e pode ser adicionado ao grupo
        return Response({
            'message': 'Leitor criado com sucesso!',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_user_escritor_admin(request):
    data = request.data.copy()
    role = data.get('role', 'Leitor')

    if role not in ['Admin', 'Escritor', 'Leitor']:
        return Response({"detail": "Role inválido. Aceito apenas: 'Admin', 'Escritor' ou 'Leitor'."},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = UserCreateSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()  # Salva o usuário no banco de dados
        group = Group.objects.get(name=role)
        user.groups.add(group)  # Agora o usuário tem um ID e pode ser adicionado ao grupo
        return Response({
            'message': 'Usuário criado com sucesso!',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)