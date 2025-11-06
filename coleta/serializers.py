"""
Serializers para a API REST do WebGIS de Coleta
"""

from rest_framework import serializers
from .models import Imovel


class ImovelSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Imovel
    Retorna dados em formato JSON para integração com mapas
    """
    
    agente_nome = serializers.CharField(source='agente_coleta.username', read_only=True)
    
    class Meta:
        model = Imovel
        fields = [
            'id',
            'numero_imovel',
            'numero_hidrometro',
            'endereco',
            'bairro',
            'cidade',
            'latitude',
            'longitude',
            'observacoes',
            'foto',
            'agente_coleta',
            'agente_nome',
            'data_coleta',
            'data_atualizacao',
            'ativo'
        ]
        read_only_fields = ['id', 'data_coleta', 'data_atualizacao']
    
    def create(self, validated_data):
        """
        Cria um novo imóvel com coordenadas
        """
        # Define o agente de coleta como o usuário autenticado
        if 'agente_coleta' not in validated_data:
            validated_data['agente_coleta'] = self.context['request'].user
        
        return super().create(validated_data)


class ImovelListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de imóveis
    """
    
    agente_nome = serializers.CharField(source='agente_coleta.username', read_only=True)
    
    class Meta:
        model = Imovel
        fields = [
            'id',
            'numero_imovel',
            'endereco',
            'latitude',
            'longitude',
            'agente_nome',
            'data_coleta',
            'foto'
        ]
