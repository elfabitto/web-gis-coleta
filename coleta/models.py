"""
Modelos para o aplicativo de coleta de dados geográficos de imóveis
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Imovel(models.Model):
    """
    Modelo para armazenar dados de imóveis coletados em campo
    """
    
    # Informações básicas
    numero_imovel = models.CharField(
        max_length=50,
        verbose_name='Número do Imóvel',
        help_text='Identificação única do imóvel'
    )
    
    numero_hidrometro = models.CharField(
        max_length=50,
        verbose_name='Número do Hidrômetro',
        blank=True,
        null=True
    )
    
    # Endereço
    endereco = models.CharField(
        max_length=500,
        verbose_name='Endereço Completo'
    )
    
    bairro = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    cidade = models.CharField(
        max_length=100,
        default='',
        blank=True
    )
    
    # Coordenadas geográficas (latitude e longitude)
    latitude = models.FloatField(
        verbose_name='Latitude',
        help_text='Latitude do imóvel (ex: -1.4558)'
    )
    
    longitude = models.FloatField(
        verbose_name='Longitude',
        help_text='Longitude do imóvel (ex: -48.4902)'
    )
    
    # Observações
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações de Campo'
    )
    
    # Foto
    foto = models.ImageField(
        upload_to='imoveis/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Foto do Imóvel'
    )
    
    # Metadados
    agente_coleta = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Agente de Coleta',
        related_name='imoveis_coletados'
    )
    
    data_coleta = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data/Hora da Coleta'
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name='Registro Ativo'
    )
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-data_coleta']
        indexes = [
            models.Index(fields=['numero_imovel']),
            models.Index(fields=['data_coleta']),
        ]
    
    def __str__(self):
        return f'Imóvel {self.numero_imovel} - {self.endereco}'
    
    def get_coordenadas(self):
        """Retorna coordenadas formatadas"""
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }
    
    def get_distancia_para(self, lat, lng):
        """
        Calcula a distância aproximada entre este imóvel e outro ponto
        Usa a fórmula de Haversine para cálculo aproximado
        """
        from math import radians, cos, sin, asin, sqrt
        
        lon1, lat1, lon2, lat2 = map(radians, [self.longitude, self.latitude, lng, lat])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Raio da Terra em km
        return c * r * 1000  # Retorna em metros
