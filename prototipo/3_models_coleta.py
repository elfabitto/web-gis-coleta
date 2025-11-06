# coleta/models.py

from django.contrib.gis.db import models
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
    
    # Coordenadas geográficas (SRID 4326 = WGS84)
    localizacao = models.PointField(
        srid=4326,
        verbose_name='Localização (Lat/Lng)',
        help_text='Coordenadas geográficas do imóvel'
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
    
    @property
    def latitude(self):
        """Retorna latitude do ponto"""
        return self.localizacao.y if self.localizacao else None
    
    @property
    def longitude(self):
        """Retorna longitude do ponto"""
        return self.localizacao.x if self.localizacao else None
    
    def get_coordenadas(self):
        """Retorna coordenadas formatadas"""
        if self.localizacao:
            return {
                'latitude': self.latitude,
                'longitude': self.longitude
            }
        return None
