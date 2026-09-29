from django.contrib.admin import ModelAdmin, StackedInline, display, register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import Autor, Categoria, Compra, Editora, ItensCompra, Livro, User


@register(Autor)
class AutorAdmin(ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'email')
    list_filter = ('nome',)
    ordering = ('nome', 'email')
    list_per_page = 10


@register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    list_filter = ('descricao',)
    ordering = ('descricao',)
    list_per_page = 10


class ItensCompraInline(StackedInline):
    model = ItensCompra
    extra = 1  # Quantidade de itens adicionais


@register(Compra)
class CompraAdmin(ModelAdmin):
    list_display = ('usuario', 'status', 'total_formatado', 'data_relativa')
    search_fields = ('usuario', 'status')
    list_filter = ('usuario', 'status', 'data')
    ordering = ('usuario', 'status', 'data')
    list_per_page = 10
    inlines = [ItensCompraInline]
    readonly_fields = ('total_formatado', 'data')

    @display(description='Data', ordering='data')
    def data_relativa(self, obj):
        days_per_month = 30
        months_per_year = 12
        agora = timezone.localtime()
        data = timezone.localtime(obj.data)
        diff_days = (agora - data).days

        if diff_days == 0:
            return 'Hoje'
        if diff_days == 1:
            return 'Ontem'
        if diff_days < days_per_month:
            return f'Há {diff_days} dias'

        total_months = diff_days // days_per_month

        if total_months < months_per_year:
            return (
                'Há 1 mês'
                if total_months == 1
                else f'Há {total_months} meses'
            )

        years = total_months // months_per_year
        months = total_months % months_per_year

        if months == 0:
            return 'Há 1 ano' if years == 1 else f'Há {years} anos'

        years_text = '1 ano' if years == 1 else f'{years} anos'
        months_text = '1 mês' if months == 1 else f'{months} meses'

        return f'Há {years_text} e {months_text}'

    @display(description="Total")
    def total_formatado(self, obj):
        """Exibe R$ 123.45 em vez de 123.45."""
        return f"R$ {obj.total:.2f}"


@register(Editora)
class EditoraAdmin(ModelAdmin):
    list_display = ('nome', 'email', 'cidade')
    search_fields = ('nome', 'email', 'cidade')
    list_filter = ('nome', 'email', 'cidade')
    ordering = ('nome', 'email', 'cidade')
    list_per_page = 10


@register(Livro)
class LivroAdmin(ModelAdmin):
    list_display = ('titulo', 'editora', 'categoria', 'preco', 'quantidade')
    search_fields = ('titulo', 'editora__nome', 'categoria__descricao')
    list_filter = ('editora', 'categoria')
    ordering = ('titulo', 'editora', 'categoria')
    list_per_page = 25


@register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ('id',)
    list_display = ('email', 'name')
    search_fields = ('email', 'name', 'groups__name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'foto',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'foto',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )


# admin.site.register(models.Autor)
# admin.site.register(models.Categoria)
# admin.site.register(models.Editora)
# admin.site.register(models.Livro)
# admin.site.register(models.User, UserAdmin)
