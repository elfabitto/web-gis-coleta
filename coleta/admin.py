"""
Configuração do Django Admin para o aplicativo de coleta
"""

from django.contrib import admin
from .models import Imovel


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):  # <<<< Mudou de GISModelAdmin para ModelAdmin
    """
    Administração de imóveis
    """
    
    list_display = [
        'numero_imovel',
        'endereco',
        'bairro',
        'agente_coleta',
        'data_coleta',
        'ativo'
    ]
    
    list_filter = [
        'ativo',
        'agente_coleta',
        'bairro',
        'cidade',
        'data_coleta'
    ]
    
    search_fields = [
        'numero_imovel',
        'numero_hidrometro',
        'endereco',
        'bairro',
        'observacoes'
    ]
    
    readonly_fields = ['data_coleta', 'data_atualizacao']
    
    fieldsets = (
        ('Identificação', {
            'fields': ('numero_imovel', 'numero_hidrometro')
        }),
        ('Endereço', {
            'fields': ('endereco', 'bairro', 'cidade')
        }),
        # Localização comentada temporariamente (campo GIS)
        # ('Localização', {
        #     'fields': ('localizacao',)
        # }),
        ('Informações Adicionais', {
            'fields': ('observacoes', 'foto')
        }),
        ('Metadados', {
            'fields': ('agente_coleta', 'data_coleta', 'data_atualizacao', 'ativo'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Define o agente de coleta ao salvar pelo admin
        """
        if not change:  # Se está criando
            obj.agente_coleta = request.user
        super().save_model(request, obj, form, change)