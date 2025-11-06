# 📚 Guia Completo de Instalação - WebGIS de Coleta de Campo

## 🖥️ Requisitos do Sistema

### Windows
- Python 3.10 ou superior
- PostgreSQL 14+ com PostGIS
- Git
- VSCode

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib postgis
```

---

## 📦 Instalação Passo a Passo

### 1️⃣ Instalar PostgreSQL + PostGIS

#### Windows:
1. Baixar PostgreSQL: https://www.postgresql.org/download/windows/
2. Durante instalação, marcar **PostGIS** no Stack Builder
3. Anotar senha do usuário `postgres`

#### Linux:
```bash
sudo apt install postgresql postgresql-contrib postgis
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2️⃣ Criar Banco de Dados

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco de dados
CREATE DATABASE webgis_db;

# Conectar ao banco
\c webgis_db

# Habilitar PostGIS
CREATE EXTENSION postgis;

# Verificar instalação
SELECT PostGIS_Version();

# Sair
\q
```

### 3️⃣ Configurar Projeto Python

```bash
# Criar diretório do projeto
mkdir webgis_coleta
cd webgis_coleta

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Criar requirements.txt
cat > requirements.txt << EOF
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-gis==1.0
django-cors-headers==4.3.1
django-filter==23.5
psycopg2-binary==2.9.9
Pillow==10.1.0
python-decouple==3.8
gunicorn==21.2.0
EOF

# Instalar dependências
pip install -r requirements.txt
```

### 4️⃣ Criar Projeto Django

```bash
# Criar projeto
django-admin startproject config .

# Criar app de coleta
python manage.py startapp coleta

# Criar diretórios necessários
mkdir -p templates static media
mkdir -p media/imoveis
```

### 5️⃣ Configurar Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=True

DB_NAME=webgis_db
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=5432
```

### 6️⃣ Aplicar Migrações

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 7️⃣ Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 8️⃣ Executar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

---

## 🚀 Deploy em Produção

### Opção 1: Deploy com Docker

Criar `Dockerfile`:

```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar projeto
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Criar `docker-compose.yml`:

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
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=False
      - DB_HOST=db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - media_volume:/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

Executar:
```bash
docker-compose up -d
```

### Opção 2: Deploy no Heroku

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Criar app
heroku create nome-do-seu-app

# Adicionar buildpacks
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-geo-buildpack.git

# Adicionar PostgreSQL com PostGIS
heroku addons:create heroku-postgresql:mini

# Configurar variáveis
heroku config:set SECRET_KEY=sua-chave-secreta
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Executar migrações
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 📱 Configurar PWA (Progressive Web App)

### 1. Criar `manifest.json`:

```json
{
  "name": "WebGIS Coleta de Campo",
  "short_name": "WebGIS",
  "description": "Aplicativo de coleta de dados geográficos",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 2. Criar `service-worker.js`:

```javascript
const CACHE_NAME = 'webgis-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

---

## 🔧 Troubleshooting

### Erro: "GDAL não encontrado"
```bash
# Windows - Instalar OSGeo4W
# https://trac.osgeo.org/osgeo4w/

# Linux
sudo apt install gdal-bin libgdal-dev
```

### Erro: "PostGIS não encontrado"
```bash
# Verificar extensão
sudo -u postgres psql -d webgis_db -c "SELECT PostGIS_Version();"
```

### Erro de Permissão no Media
```bash
# Linux
sudo chown -R $USER:$USER media/
chmod -R 755 media/
```

---

## 📊 Monitoramento e Logs

```bash
# Ver logs do Django
python manage.py runserver --verbosity 3

# Ver logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Ver logs do Docker
docker-compose logs -f
```

---

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

---

## 📞 Suporte

- Django: https://docs.djangoproject.com/
- GeoDjango: https://docs.djangoproject.com/en/4.2/ref/contrib/gis/
- Leaflet: https://leafletjs.com/
- PostGIS: https://postgis.net/documentation/

---

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

**Boa sorte com seu projeto! 🚀**