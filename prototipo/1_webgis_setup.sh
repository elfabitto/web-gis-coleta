#!/bin/bash
# Script de configuração inicial do WebGIS de Coleta de Campo

echo "🚀 Configurando projeto WebGIS..."

# Criar diretório do projeto
mkdir webgis_coleta
cd webgis_coleta

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
# venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Criar arquivo requirements.txt
cat > requirements.txt << EOF
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
Pillow==10.1.0
django-filter==23.5
python-decouple==3.8

# GeoDjango
GDAL==3.7.3
EOF

# Instalar dependências
pip install -r requirements.txt

# Criar projeto Django
django-admin startproject config .

# Criar app de coleta
python manage.py startapp coleta

echo "✅ Projeto criado com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "1. Configure o PostgreSQL + PostGIS"
echo "2. Edite config/settings.py com as configurações do banco"
echo "3. Execute: python manage.py migrate"
echo "4. Crie um superusuário: python manage.py createsuperuser"
