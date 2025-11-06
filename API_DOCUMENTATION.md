# 📚 Documentação da API REST - WebGIS Coleta

## Visão Geral

A API REST do WebGIS fornece endpoints para gerenciar imóveis, coordenadas geográficas e dados de coleta em campo.

## Base URL

```
http://localhost:8000/api/
```

## Autenticação

A API utiliza autenticação por sessão Django. Para usar os endpoints protegidos:

1. Faça login em `/api-auth/login/`
2. Use o cookie de sessão nas requisições subsequentes

### Exemplo de Login
```bash
curl -X POST http://localhost:8000/api-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }' \
  -c cookies.txt
```

## Endpoints

### 1. Listar Imóveis

**GET** `/api/imoveis/`

Retorna uma lista paginada de todos os imóveis ativos.

#### Query Parameters
- `page` (int): Número da página (padrão: 1)
- `numero_imovel` (string): Filtrar por número do imóvel
- `bairro` (string): Filtrar por bairro
- `cidade` (string): Filtrar por cidade
- `agente_coleta` (int): Filtrar por ID do agente

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/imoveis/?bairro=Centro&page=1" \
  -b cookies.txt
```

#### Resposta (200 OK)
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/imoveis/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "numero_imovel": "12345",
      "numero_hidrometro": "HM-98765",
      "endereco": "Rua das Flores, 123",
      "bairro": "Centro",
      "cidade": "Belém",
      "latitude": -1.4558,
      "longitude": -48.4902,
      "observacoes": "Casa em bom estado",
      "foto": "http://localhost:8000/media/imoveis/2024/11/foto.jpg",
      "agente_coleta": 1,
      "agente_nome": "admin",
      "data_coleta": "2024-11-06T10:30:00Z",
      "data_atualizacao": "2024-11-06T10:30:00Z",
      "ativo": true
    }
  ]
}
```

### 2. Criar Imóvel

**POST** `/api/imoveis/`

Cria um novo registro de imóvel.

#### Body (JSON)
```json
{
  "numero_imovel": "12345",
  "numero_hidrometro": "HM-98765",
  "endereco": "Rua das Flores, 123",
  "bairro": "Centro",
  "cidade": "Belém",
  "latitude": -1.4558,
  "longitude": -48.4902,
  "observacoes": "Casa em bom estado",
  "foto": null,
  "ativo": true
}
```

#### Exemplo de Requisição
```bash
curl -X POST http://localhost:8000/api/imoveis/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
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

#### Resposta (201 Created)
```json
{
  "id": 1,
  "numero_imovel": "12345",
  "numero_hidrometro": "HM-98765",
  "endereco": "Rua das Flores, 123",
  "bairro": "Centro",
  "cidade": "Belém",
  "latitude": -1.4558,
  "longitude": -48.4902,
  "observacoes": "Casa em bom estado",
  "foto": null,
  "agente_coleta": 1,
  "agente_nome": "admin",
  "data_coleta": "2024-11-06T10:30:00Z",
  "data_atualizacao": "2024-11-06T10:30:00Z",
  "ativo": true
}
```

### 3. Obter Detalhes do Imóvel

**GET** `/api/imoveis/{id}/`

Retorna os detalhes completos de um imóvel específico.

#### Exemplo de Requisição
```bash
curl -X GET http://localhost:8000/api/imoveis/1/ \
  -b cookies.txt
```

#### Resposta (200 OK)
```json
{
  "id": 1,
  "numero_imovel": "12345",
  "numero_hidrometro": "HM-98765",
  "endereco": "Rua das Flores, 123",
  "bairro": "Centro",
  "cidade": "Belém",
  "latitude": -1.4558,
  "longitude": -48.4902,
  "observacoes": "Casa em bom estado",
  "foto": "http://localhost:8000/media/imoveis/2024/11/foto.jpg",
  "agente_coleta": 1,
  "agente_nome": "admin",
  "data_coleta": "2024-11-06T10:30:00Z",
  "data_atualizacao": "2024-11-06T10:30:00Z",
  "ativo": true
}
```

### 4. Atualizar Imóvel

**PUT** `/api/imoveis/{id}/`

Atualiza todos os campos de um imóvel.

#### Exemplo de Requisição
```bash
curl -X PUT http://localhost:8000/api/imoveis/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "numero_imovel": "12345",
    "numero_hidrometro": "HM-98765",
    "endereco": "Rua das Flores, 456",
    "bairro": "Centro",
    "cidade": "Belém",
    "latitude": -1.4558,
    "longitude": -48.4902,
    "observacoes": "Casa reformada",
    "ativo": true
  }'
```

#### Resposta (200 OK)
```json
{
  "id": 1,
  "numero_imovel": "12345",
  "numero_hidrometro": "HM-98765",
  "endereco": "Rua das Flores, 456",
  "bairro": "Centro",
  "cidade": "Belém",
  "latitude": -1.4558,
  "longitude": -48.4902,
  "observacoes": "Casa reformada",
  "foto": null,
  "agente_coleta": 1,
  "agente_nome": "admin",
  "data_coleta": "2024-11-06T10:30:00Z",
  "data_atualizacao": "2024-11-06T11:00:00Z",
  "ativo": true
}
```

### 5. Atualização Parcial

**PATCH** `/api/imoveis/{id}/`

Atualiza apenas os campos fornecidos.

#### Exemplo de Requisição
```bash
curl -X PATCH http://localhost:8000/api/imoveis/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "observacoes": "Casa reformada"
  }'
```

### 6. Deletar Imóvel

**DELETE** `/api/imoveis/{id}/`

Remove um imóvel do banco de dados.

#### Exemplo de Requisição
```bash
curl -X DELETE http://localhost:8000/api/imoveis/1/ \
  -b cookies.txt
```

#### Resposta (204 No Content)
```
(sem corpo)
```

### 7. Meus Imóveis

**GET** `/api/imoveis/meus_imoveis/`

Retorna apenas os imóveis coletados pelo usuário autenticado.

#### Exemplo de Requisição
```bash
curl -X GET http://localhost:8000/api/imoveis/meus_imoveis/ \
  -b cookies.txt
```

#### Resposta (200 OK)
```json
[
  {
    "id": 1,
    "numero_imovel": "12345",
    "endereco": "Rua das Flores, 123",
    "latitude": -1.4558,
    "longitude": -48.4902,
    "agente_nome": "admin",
    "data_coleta": "2024-11-06T10:30:00Z",
    "foto": null
  }
]
```

### 8. Imóveis Próximos

**GET** `/api/imoveis/proximos/?lat={latitude}&lng={longitude}&distancia={metros}`

Busca imóveis dentro de uma distância especificada de uma coordenada.

#### Query Parameters (Obrigatórios)
- `lat` (float): Latitude do ponto de referência
- `lng` (float): Longitude do ponto de referência
- `distancia` (float): Distância em metros (padrão: 1000)

#### Exemplo de Requisição
```bash
curl -X GET "http://localhost:8000/api/imoveis/proximos/?lat=-1.4558&lng=-48.4902&distancia=2000" \
  -b cookies.txt
```

#### Resposta (200 OK)
```json
[
  {
    "id": 1,
    "numero_imovel": "12345",
    "endereco": "Rua das Flores, 123",
    "latitude": -1.4558,
    "longitude": -48.4902,
    "agente_nome": "admin",
    "data_coleta": "2024-11-06T10:30:00Z",
    "foto": null
  },
  {
    "id": 2,
    "numero_imovel": "12346",
    "endereco": "Rua das Flores, 456",
    "latitude": -1.4560,
    "longitude": -48.4905,
    "agente_nome": "admin",
    "data_coleta": "2024-11-06T10:35:00Z",
    "foto": null
  }
]
```

#### Erros
- **400 Bad Request**: Se `lat` ou `lng` não forem fornecidos
- **400 Bad Request**: Se as coordenadas forem inválidas

### 9. Estatísticas de Coleta

**GET** `/api/imoveis/estatisticas/`

Retorna estatísticas gerais de coleta de imóveis.

#### Exemplo de Requisição
```bash
curl -X GET http://localhost:8000/api/imoveis/estatisticas/ \
  -b cookies.txt
```

#### Resposta (200 OK)
```json
{
  "total_imoveis": 25,
  "meus_imoveis": 10,
  "por_agente": {
    "admin": 15,
    "agente1": 10
  }
}
```

### 10. Desativar Imóvel

**POST** `/api/imoveis/{id}/desativar/`

Desativa um imóvel (soft delete) sem removê-lo do banco de dados.

#### Exemplo de Requisição
```bash
curl -X POST http://localhost:8000/api/imoveis/1/desativar/ \
  -b cookies.txt
```

#### Resposta (200 OK)
```json
{
  "status": "Imóvel desativado"
}
```

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 204 | No Content - Requisição bem-sucedida sem conteúdo |
| 400 | Bad Request - Requisição inválida |
| 401 | Unauthorized - Autenticação necessária |
| 403 | Forbidden - Acesso negado |
| 404 | Not Found - Recurso não encontrado |
| 500 | Internal Server Error - Erro no servidor |

## Tratamento de Erros

### Erro de Validação (400)
```json
{
  "numero_imovel": ["Este campo é obrigatório."],
  "latitude": ["Certifique-se de que este valor é menor ou igual a 90."]
}
```

### Erro de Autenticação (401)
```json
{
  "detail": "As credenciais de autenticação não foram fornecidas."
}
```

### Erro de Permissão (403)
```json
{
  "detail": "Você não tem permissão para executar esta ação."
}
```

### Erro de Recurso Não Encontrado (404)
```json
{
  "detail": "Não encontrado."
}
```

## Paginação

A listagem de imóveis é paginada com 100 itens por página.

### Exemplo de Resposta Paginada
```json
{
  "count": 250,
  "next": "http://localhost:8000/api/imoveis/?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtros

Você pode filtrar os resultados usando query parameters:

```bash
# Filtrar por bairro
curl -X GET "http://localhost:8000/api/imoveis/?bairro=Centro" \
  -b cookies.txt

# Filtrar por número do imóvel
curl -X GET "http://localhost:8000/api/imoveis/?numero_imovel=12345" \
  -b cookies.txt

# Combinar filtros
curl -X GET "http://localhost:8000/api/imoveis/?bairro=Centro&cidade=Belém" \
  -b cookies.txt
```

## Upload de Fotos

Para fazer upload de uma foto ao criar ou atualizar um imóvel, use `multipart/form-data`:

```bash
curl -X POST http://localhost:8000/api/imoveis/ \
  -b cookies.txt \
  -F "numero_imovel=12345" \
  -F "endereco=Rua das Flores, 123" \
  -F "latitude=-1.4558" \
  -F "longitude=-48.4902" \
  -F "foto=@/caminho/para/foto.jpg"
```

## Rate Limiting

Atualmente, não há limite de taxa implementado. Isso pode ser adicionado no futuro.

## Versionamento

A API está na versão 1.0. Futuras versões podem ser acessadas via `/api/v2/`, etc.

## Suporte

Para dúvidas ou problemas, consulte a documentação do Django REST Framework:
https://www.django-rest-framework.org/
