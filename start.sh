#!/bin/bash

# Script para iniciar o projeto Django WebGIS

echo "🚀 Iniciando WebGIS - Coleta de Dados Geográficos"
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "✅ Ativando ambiente virtual..."
source venv/bin/activate

# Instalar/atualizar dependências
echo "📦 Verificando dependências..."
pip install -r requirements.txt -q

# Executar migrações
echo "🗄️  Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput -q

# Iniciar servidor
echo ""
echo "✅ Tudo pronto!"
echo ""
echo "🌐 Servidor Django iniciando em http://localhost:8000"
echo "📊 Admin Django em http://localhost:8000/admin/"
echo "📚 API em http://localhost:8000/api/"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo ""

python manage.py runserver 0.0.0.0:8000
