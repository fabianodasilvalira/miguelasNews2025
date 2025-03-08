from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import User, Group
from .models import Category, News, NewsImage, NewsLike

# Inline para imagens associadas à notícia
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ['image']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published_date', 'author']  # Adicionado 'author'
    search_fields = ['title', 'content']
    list_filter = ['category']
    inlines = [NewsImageInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class NewsLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at')
    list_filter = ('created_at', 'news')
    search_fields = ('user__username', 'news__title')

# Registrar modelos no admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsLike, NewsLikeAdmin)

# Registrar apenas o modelo User (Group já está registrado pelo Django)
admin.site.register(User)

# Desregistrar o GroupAdmin padrão
admin.site.unregister(Group)

# Registrar o GroupAdmin personalizado
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    list_display = ['name', 'get_users']
    search_fields = ['name']

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])
    get_users.short_description = 'Usuários'