# coleta/serializers.py

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from .models import Imovel


class ImovelSerializer(GeoFeatureModelSerializer):
    """
    Serializer GeoJSON para o modelo Imovel
    """
    
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    agente_nome = serializers.CharField(source='agente_coleta.username', read_only=True)
    
    class Meta:
        model = Imovel
        geo_field = 'localizacao'
        fields = [
            'id',
            'numero_imovel',
            'numero_hidrometro',
            'endereco',
            'bairro',
            'cidade',
            'localizacao',
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
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        if latitude and longitude:
            validated_data['localizacao'] = Point(longitude, latitude, srid=4326)
        
        # Define o agente de coleta como o usuário autenticado
        if 'agente_coleta' not in validated_data:
            validated_data['agente_coleta'] = self.context['request'].user
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Atualiza um imóvel existente
        """
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        if latitude and longitude:
            validated_data['localizacao'] = Point(longitude, latitude, srid=4326)
        
        return super().update(instance, validated_data)


class ImovelListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de imóveis
    """
    
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
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
    
    def get_latitude(self, obj):
        return obj.latitude
    
    def get_longitude(self, obj):
        return obj.longitude
