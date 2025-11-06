# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from coleta.views import ImovelViewSet

# Router da API
router = DefaultRouter()
router.register(r'imoveis', ImovelViewSet, basename='imovel')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('coleta.urls')),  # URLs do frontend
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# coleta/urls.py

from django.urls import path
from . import views_frontend

app_name = 'coleta'

urlpatterns = [
    path('', views_frontend.mapa_view, name='mapa'),
    path('formulario/', views_frontend.formulario_view, name='formulario'),
]
