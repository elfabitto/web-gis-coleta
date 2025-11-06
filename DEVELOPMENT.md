# 🛠️ Guia de Desenvolvimento - WebGIS Coleta

## Configuração do Ambiente de Desenvolvimento

### 1. Pré-requisitos
- Python 3.10+
- Git
- VSCode ou IDE de sua preferência
- Postman ou Insomnia (para testar API)

### 2. Setup Inicial

```bash
# Clonar repositório
git clone <seu-repositorio>
cd django_webgis

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env

# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## Estrutura de Arquivos

```
django_webgis/
├── config/
│   ├── __init__.py
│   ├── settings.py          # Configurações do projeto
│   ├── urls.py              # Rotas principais
│   ├── asgi.py              # Configuração ASGI
│   └── wsgi.py              # Configuração WSGI
├── coleta/
│   ├── migrations/          # Migrações do banco de dados
│   ├── __init__.py
│   ├── admin.py             # Configuração do admin
│   ├── apps.py              # Configuração da app
│   ├── models.py            # Modelos de dados
│   ├── serializers.py       # Serializers da API
│   ├── views.py             # ViewSets da API
│   ├── urls.py              # Rotas da app
│   └── tests.py             # Testes unitários
├── templates/               # Templates HTML
├── static/                  # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── media/                   # Arquivos de upload
│   └── imoveis/
├── manage.py                # Script de gerenciamento
├── requirements.txt         # Dependências
├── .env                     # Variáveis de ambiente
├── .env.example             # Exemplo de .env
├── README.md                # Documentação principal
├── API_DOCUMENTATION.md     # Documentação da API
└── DEVELOPMENT.md           # Este arquivo
```

## Desenvolvimento de Features

### 1. Criar uma Nova Feature

```bash
# Criar branch
git checkout -b feature/nome-da-feature

# Fazer alterações
# ...

# Testar
python manage.py test

# Commit
git add .
git commit -m "feat: descrição da feature"

# Push
git push origin feature/nome-da-feature
```

### 2. Adicionar um Novo Campo ao Modelo

```python
# coleta/models.py
class Imovel(models.Model):
    # ... campos existentes ...
    novo_campo = models.CharField(
        max_length=100,
        verbose_name='Novo Campo',
        blank=True,
        null=True
    )
```

Depois:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Criar um Novo Serializer

```python
# coleta/serializers.py
class NovoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = ['id', 'numero_imovel', 'endereco']
```

### 4. Adicionar um Novo Endpoint

```python
# coleta/views.py
class ImovelViewSet(viewsets.ModelViewSet):
    # ... código existente ...
    
    @action(detail=False, methods=['get'])
    def novo_endpoint(self, request):
        """Descrição do novo endpoint"""
        # Implementação
        return Response({'resultado': 'sucesso'})
```

## Testes

### Executar Todos os Testes
```bash
python manage.py test
```

### Executar Testes de uma App Específica
```bash
python manage.py test coleta
```

### Executar um Teste Específico
```bash
python manage.py test coleta.tests.ImovelTestCase.test_criar_imovel
```

### Exemplo de Teste
```python
# coleta/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Imovel

class ImovelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.imovel = Imovel.objects.create(
            numero_imovel='12345',
            endereco='Rua Teste, 123',
            latitude=-1.4558,
            longitude=-48.4902,
            agente_coleta=self.user
        )
    
    def test_criar_imovel(self):
        self.assertEqual(self.imovel.numero_imovel, '12345')
    
    def test_string_representation(self):
        self.assertEqual(str(self.imovel), 'Imóvel 12345 - Rua Teste, 123')
```

## Debugging

### Usar o Django Shell
```bash
python manage.py shell

# Dentro do shell
from coleta.models import Imovel
imoveis = Imovel.objects.all()
for imovel in imoveis:
    print(imovel)
```

### Usar o Debugger do VSCode

Crie `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver"],
            "django": true
        }
    ]
}
```

### Logs

```python
# coleta/views.py
import logging

logger = logging.getLogger(__name__)

class ImovelViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info(f"Criando novo imóvel: {request.data}")
        return super().create(request, *args, **kwargs)
```

## Performance

### Otimizar Queries

```python
# Ruim
imoveis = Imovel.objects.all()
for imovel in imoveis:
    print(imovel.agente_coleta.username)  # N+1 query

# Bom
imoveis = Imovel.objects.select_related('agente_coleta')
for imovel in imoveis:
    print(imovel.agente_coleta.username)  # 1 query
```

### Usar Índices

```python
# coleta/models.py
class Imovel(models.Model):
    # ... campos ...
    
    class Meta:
        indexes = [
            models.Index(fields=['numero_imovel']),
            models.Index(fields=['data_coleta']),
            models.Index(fields=['agente_coleta']),
        ]
```

## Segurança

### Validação de Entrada

```python
# coleta/serializers.py
class ImovelSerializer(serializers.ModelSerializer):
    def validate_latitude(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude deve estar entre -90 e 90")
        return value
    
    def validate_longitude(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude deve estar entre -180 e 180")
        return value
```

### Permissões

```python
# coleta/views.py
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class ImovelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        # Apenas admins podem deletar
        if not request.user.is_staff:
            raise PermissionDenied("Apenas administradores podem deletar imóveis")
        return super().destroy(request, *args, **kwargs)
```

## Integração Contínua

### GitHub Actions

Crie `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test
```

## Linting e Formatação

### Instalar Ferramentas
```bash
pip install flake8 black isort
```

### Executar Linting
```bash
flake8 coleta/
```

### Formatar Código
```bash
black coleta/
isort coleta/
```

## Documentação

### Gerar Documentação Automática
```bash
pip install drf-spectacular

# Adicionar em settings.py
INSTALLED_APPS = [
    # ...
    'drf_spectacular',
]

# Adicionar em urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
```

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'django'"
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Erro: "django.db.utils.OperationalError: no such table"
```bash
# Executar migrações
python manage.py migrate
```

### Erro: "CORS error"
```python
# Verificar settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]
```

### Erro: "Permission denied" ao fazer upload
```bash
# Verificar permissões
chmod -R 755 media/
```

## Recursos Úteis

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/topics/db/models/best-practices/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

**Happy coding! 🚀**
