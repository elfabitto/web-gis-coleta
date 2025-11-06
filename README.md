# 📍 WebGIS - Coleta de Dados Geográficos de Imóveis

Um aplicativo Django completo para coleta, visualização e gerenciamento de dados geográficos de imóveis em campo, com suporte a mapas interativos e API REST.

## 🎯 Funcionalidades

- **Coleta de Dados em Campo**: Formulário intuitivo para coleta de informações de imóveis
- **Mapa Interativo**: Visualização de pontos coletados em tempo real com Leaflet.js
- **API REST**: Endpoints completos para CRUD de imóveis
- **Ações Customizadas**: Busca de imóveis próximos, estatísticas de coleta
- **Admin Django**: Interface administrativa com suporte a mapas
- **Autenticação**: Controle de acesso baseado em usuários
- **Responsivo**: Funciona em navegadores e dispositivos móveis

## 📋 Requisitos do Sistema

- Python 3.10+
- pip (gerenciador de pacotes Python)
- SQLite (incluído no Python) ou PostgreSQL + PostGIS (para produção)

## 🚀 Instalação Rápida

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd django_webgis
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Executar migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Criar superusuário
```bash
python manage.py createsuperuser
```

### 7. Coletar arquivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 8. Executar servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## 📚 Estrutura do Projeto

```
django_webgis/
├── config/                 # Configurações do Django
│   ├── settings.py        # Configurações principais
│   ├── urls.py            # Rotas da aplicação
│   └── wsgi.py            # Configuração WSGI
├── coleta/                # Aplicação principal
│   ├── models.py          # Modelo Imovel
│   ├── views.py           # ViewSet da API
│   ├── serializers.py     # Serializers
│   ├── admin.py           # Configuração do admin
│   └── migrations/        # Migrações do banco de dados
├── templates/             # Templates HTML
├── static/                # Arquivos estáticos (CSS, JS, imagens)
├── media/                 # Arquivos de upload (fotos de imóveis)
├── manage.py              # Script de gerenciamento do Django
└── requirements.txt       # Dependências do projeto
```

## 🔌 API REST Endpoints

### Autenticação
- `POST /api-auth/login/` - Login
- `POST /api-auth/logout/` - Logout

### Imóveis
- `GET /api/imoveis/` - Listar todos os imóveis
- `POST /api/imoveis/` - Criar novo imóvel
- `GET /api/imoveis/{id}/` - Obter detalhes de um imóvel
- `PUT /api/imoveis/{id}/` - Atualizar um imóvel
- `DELETE /api/imoveis/{id}/` - Deletar um imóvel
- `GET /api/imoveis/meus_imoveis/` - Listar imóveis do usuário autenticado
- `GET /api/imoveis/proximos/?lat=-1.4558&lng=-48.4902&distancia=2000` - Buscar imóveis próximos
- `GET /api/imoveis/estatisticas/` - Obter estatísticas de coleta
- `POST /api/imoveis/{id}/desativar/` - Desativar um imóvel

## 📝 Exemplo de Requisição

### Criar um novo imóvel
```bash
curl -X POST http://localhost:8000/api/imoveis/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "numero_imovel": "12345",
    "numero_hidrometro": "HM-98765",
    "endereco": "Rua das Flores, 123",
    "bairro": "Centro",
    "cidade": "Belém",
    "latitude": -1.4558,
    "longitude": -48.4902,
    "observacoes": "Casa em bom estado"
  }'
```

### Buscar imóveis próximos
```bash
curl -X GET "http://localhost:8000/api/imoveis/proximos/?lat=-1.4558&lng=-48.4902&distancia=2000" \
  -H "Authorization: Token YOUR_TOKEN"
```

## 🔐 Segurança em Produção

1. **Gerar SECRET_KEY seguro:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

2. **Configurar HTTPS:**
```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

3. **Configurar CORS:**
```python
CORS_ALLOWED_ORIGINS = [
    "https://seudominio.com",
]
```

4. **Usar variáveis de ambiente:**
```bash
export SECRET_KEY="sua-chave-secreta"
export DEBUG=False
export DB_NAME="webgis_db"
export DB_USER="postgres"
export DB_PASSWORD="sua_senha"
export DB_HOST="localhost"
export DB_PORT="5432"
```

## 🐘 Migrar para PostgreSQL + PostGIS

### 1. Instalar PostgreSQL e PostGIS
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib postgis

# macOS
brew install postgresql postgis
```

### 2. Criar banco de dados
```bash
sudo -u postgres psql
CREATE DATABASE webgis_db;
\c webgis_db
CREATE EXTENSION postgis;
\q
```

### 3. Atualizar settings.py
```python
# Descomente a configuração do PostgreSQL em settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'webgis_db',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Aplicar migrações
```bash
python manage.py migrate
```

## 🐳 Deploy com Docker

### Dockerfile
```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgis/postgis:14-3.3
    environment:
      POSTGRES_DB: webgis_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=False
      - DB_HOST=db
      - SECRET_KEY=sua-chave-secreta

volumes:
  postgres_data:
```

### Executar
```bash
docker-compose up -d
```

## 📱 PWA (Progressive Web App)

O projeto pode ser convertido em um PWA adicionando:

1. **manifest.json** - Metadados da aplicação
2. **service-worker.js** - Cache offline
3. **Ícones** - Para instalação em dispositivos

## 🧪 Testes

```bash
python manage.py test
```

## 📊 Monitoramento

```bash
# Ver logs do Django
python manage.py runserver --verbosity 3

# Ver logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

- **Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Leaflet.js**: https://leafletjs.com/
- **PostGIS**: https://postgis.net/documentation/

## ✅ Checklist de Deploy

- [ ] PostgreSQL + PostGIS instalado e configurado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Migrações aplicadas
- [ ] Superusuário criado
- [ ] Arquivos estáticos coletados
- [ ] Variáveis de ambiente configuradas
- [ ] HTTPS configurado (produção)
- [ ] Backup configurado
- [ ] Monitoramento ativo

---

**Desenvolvido com ❤️ para coleta de dados geográficos**
