# coleta/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django_filters.rest_framework import DjangoFilterBackend
from .models import Imovel
from .serializers import ImovelSerializer, ImovelListSerializer


class ImovelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de imóveis
    """
    queryset = Imovel.objects.filter(ativo=True).select_related('agente_coleta')
    serializer_class = ImovelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['numero_imovel', 'bairro', 'cidade', 'agente_coleta']
    
    def get_serializer_class(self):
        """
        Retorna serializer apropriado para a ação
        """
        if self.action == 'list':
            return ImovelListSerializer
        return ImovelSerializer
    
    def perform_create(self, serializer):
        """
        Define o agente de coleta ao criar
        """
        serializer.save(agente_coleta=self.request.user)
    
    @action(detail=False, methods=['get'])
    def meus_imoveis(self, request):
        """
        Retorna apenas os imóveis coletados pelo usuário autenticado
        """
        imoveis = self.queryset.filter(agente_coleta=request.user)
        serializer = self.get_serializer(imoveis, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def proximos(self, request):
        """
        Busca imóveis próximos a uma coordenada
        Query params: lat, lng, distancia (em metros, padrão 1000)
        """
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        distancia = request.query_params.get('distancia', 1000)
        
        if not lat or not lng:
            return Response(
                {'error': 'Parâmetros lat e lng são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ponto = Point(float(lng), float(lat), srid=4326)
            imoveis = self.queryset.filter(
                localizacao__distance_lte=(ponto, D(m=float(distancia)))
            ).distance(ponto).order_by('distance')
            
            serializer = self.get_serializer(imoveis, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'error': 'Coordenadas inválidas'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        Retorna estatísticas de coleta
        """
        total = self.queryset.count()
        meus = self.queryset.filter(agente_coleta=request.user).count()
        
        por_agente = {}
        for imovel in self.queryset.values('agente_coleta__username'):
            agente = imovel['agente_coleta__username']
            por_agente[agente] = por_agente.get(agente, 0) + 1
        
        return Response({
            'total_imoveis': total,
            'meus_imoveis': meus,
            'por_agente': por_agente
        })
    
    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """
        Desativa um imóvel (soft delete)
        """
        imovel = self.get_object()
        imovel.ativo = False
        imovel.save()
        return Response({'status': 'Imóvel desativado'})
