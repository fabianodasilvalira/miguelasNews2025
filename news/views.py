import logging
from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers

# Configuração do logger
logger = logging.getLogger(__name__)

from .models import Category, News, NewsImage, Comment, NewsLike
from .serializers import CategorySerializer, NewsSerializer, CommentSerializer, UserCreateSerializer


# Permissão customizada para leitores autenticados
class IsReader(BasePermission):
    """
    Permissão personalizada para garantir que o usuário esteja autenticado
    e possa interagir com as notícias (curtir, comentar, etc.)
    """
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        return request.user.is_authenticated


# Permissão customizada para jornalistas ou administradores
class IsJournalistOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Permite apenas administradores ou jornalistas
        return request.user.is_staff or request.user.groups.filter(name='Journalists').exists()


# ViewSet para News (Notícias)
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsJournalistOrAdmin]

    def perform_create(self, serializer):
        # Aqui, o autor da notícia é o usuário logado
        serializer.save(author=self.request.user)


# View para listar e criar categorias
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Define permissões diferentes para GET e POST.
        - GET: Acesso público.
        - POST: Acesso apenas para usuários autenticados.
        """
        if self.request.method == 'POST':
            # Para o método POST, exige autenticação
            return [IsAuthenticated()]
        return []  # Para o método GET, acesso público

    def perform_create(self, serializer):
        logger.info("Criando uma nova categoria.")
        serializer.save()
        logger.info("Categoria criada com sucesso.")

    def get(self, request, *args, **kwargs):
        # Log que imprime quando entra na rota de categorias
        logger.info("Entrou na rota GET /categories/")
        return super().get(request, *args, **kwargs)


# View para detalhes, atualização e exclusão de categorias
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# View para listar e criar notícias
class NewsListCreate(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_permissions(self):
        """
        Define permissões diferentes para GET e POST.
        - GET: Acesso público.
        - POST: Acesso apenas para usuários autenticados.
        """
        if self.request.method == 'POST':
            # Para o método POST, exige autenticação
            return [IsAuthenticated()]
        return []  # Para o método GET, acesso público

    def perform_create(self, serializer):
        logger.info("Iniciando criação de notícia.")

        # Verificando os dados recebidos
        category_id = self.request.data.get('category', None)
        logger.debug(f"Dados recebidos: {self.request.data}")
        logger.debug(f"Arquivos recebidos: {self.request.FILES}")

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                news = serializer.save(category=category)
                logger.info(f"Notícia criada: {news.title}")

                # Verificando imagens na requisição
                images = self.request.FILES.getlist('images')
                if images:
                    logger.info(f"{len(images)} imagem(s) recebida(s) para a notícia.")
                    for image in images:
                        NewsImage.objects.create(news=news, image=image)
                        logger.info(f"Imagem associada: {image.name}")
                else:
                    logger.info("Nenhuma imagem enviada.")

            except Category.DoesNotExist:
                logger.error(f"Categoria com ID {category_id} não encontrada.")
                return Response({"error": "Categoria não encontrada."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error("Campo 'category' não encontrado na requisição.")
            return Response({"error": "O campo 'category' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)


# View para detalhes, atualização e exclusão de notícias
class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


# View para listar e criar comentários
class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsReader]  # Apenas leitores autenticados podem comentar

    def perform_create(self, serializer):
        # O campo 'news' da requisição será usado diretamente
        news_id = self.request.data.get('news', None)  # Use 'news' em vez de 'news_id'

        if news_id:
            try:
                # Aqui, verificamos se a notícia existe com o ID fornecido
                news = News.objects.get(id=news_id)
                serializer.save(news=news)  # Atribui a notícia à criação do comentário
            except News.DoesNotExist:
                raise serializers.ValidationError("Notícia não encontrada.")
        else:
            raise serializers.ValidationError("Campo 'news' é obrigatório.")


# View para detalhes, atualização e exclusão de comentários
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# View para curtir ou descurtir notícias
class NewsLikeToggle(APIView):
    permission_classes = [IsReader]  # Apenas leitores autenticados podem interagir

    def post(self, request, news_id, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            return Response({"detail": "Notícia não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        like, created = NewsLike.objects.get_or_create(user=user, news=news)

        if not created:
            like.delete()  # Remove a curtida se já existe
            return Response({"detail": "Curtida removida."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Notícia curtida."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_user(request):
    """
    Permite que qualquer pessoa se cadastre como leitor.
    """
    data = request.data.copy()
    data['role'] = 'leitor'  # Define automaticamente como leitor

    serializer = UserCreateSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Leitor criado com sucesso!',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Apenas usuários logados podem cadastrar escritores/admins
def create_user_escritor_admin(request):
    """
    Permite que um administrador crie usuários com as roles 'escritor' ou 'admin'.
    Somente um administrador pode criar usuários 'admin' ou 'escritor'.
    """
    # Verifica se o usuário autenticado é um administrador
    if not request.user.is_superuser:
        return Response({"detail": "Apenas administradores podem criar usuários 'admin' ou 'escritor'."},
                        status=status.HTTP_403_FORBIDDEN)

    # Copia os dados do request
    data = request.data.copy()

    # Obtém o role do novo usuário (padrão é 'leitor', mas pode ser 'escritor' ou 'admin')
    role = data.get('role', 'leitor')

    # Valida se o role informado é válido
    if role not in ['leitor', 'escritor', 'admin']:
        return Response({"detail": "Role inválido. Apenas 'leitor', 'escritor' ou 'admin' são permitidos."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Cria o serializer para validar e salvar os dados
    serializer = UserCreateSerializer(data=data)

    if serializer.is_valid():
        # Salva o usuário com a role especificada
        user = serializer.save(role=role)

        return Response({
            'message': 'Usuário criado com sucesso!',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


