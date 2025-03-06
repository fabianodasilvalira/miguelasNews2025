from django.contrib import admin
from .models import Category, News, NewsImage, NewsLike

# Inline para imagens associadas à notícia
class NewsImageInline(admin.TabularInline):  # Você pode usar `StackedInline` se preferir
    model = NewsImage
    extra = 1  # Número de campos de imagem adicionais exibidos
    fields = ['image']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published_date', 'author']  # Campos a exibir na lista de notícias
    search_fields = ['title', 'content']  # Permite buscar por título e conteúdo
    list_filter = ['category']  # Filtro por categoria
    inlines = [NewsImageInline]  # Adiciona a possibilidade de incluir imagens diretamente no News Admin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  # Campos a exibir na lista de categorias
    search_fields = ['name']

class NewsLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at')  # Exibe essas colunas na lista de curtidas
    list_filter = ('created_at', 'news')  # Filtros por data e notícia
    search_fields = ('user__username', 'news__title')  # Pesquisa por nome de usuário e título da notícia

# Registrar modelos no admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsLike, NewsLikeAdmin)  # Agora registra corretamente o modelo NewsLike
