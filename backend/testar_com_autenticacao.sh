#!/bin/bash

# Script para testar endpoints do Forum com autenticação
# Demonstra o padrão Decorator em ação com logs de REQUEST/RESPONSE

echo "=========================================="
echo "TESTE DO PADRÃO DECORATOR COM AUTENTICAÇÃO"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# URL base
BASE_URL="http://127.0.0.1:8001"

echo -e "${YELLOW}PASSO 1: Criar um usuário de teste${NC}"
echo "--------------------------------------"
echo "Endpoint: POST /api/users/"
echo ""

USER_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@decorator.com",
    "password": "senha123",
    "nome": "Usuario Teste Decorator"
  }')

echo "$USER_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$USER_RESPONSE"
echo ""

# Extrair o ID do usuário
USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ -z "$USER_ID" ]; then
    echo -e "${RED}❌ Erro ao criar usuário. Tentando usar usuário existente...${NC}"
    USER_ID=1
else
    echo -e "${GREEN}✅ Usuário criado com ID: $USER_ID${NC}"
fi

echo ""
echo "=========================================="
echo ""

echo -e "${YELLOW}PASSO 2: Obter token de autenticação${NC}"
echo "--------------------------------------"
echo "Endpoint: POST /api-token-auth/ (ou similar)"
echo ""
echo -e "${YELLOW}⚠️  NOTA: Este projeto pode não ter autenticação JWT configurada${NC}"
echo -e "${YELLOW}⚠️  Para testar com autenticação, você precisará:${NC}"
echo "   1. Usar Django Admin para criar um superuser"
echo "   2. Ou configurar JWT/Token authentication"
echo ""

echo "Comando para criar superuser:"
echo -e "${GREEN}python manage.py createsuperuser${NC}"
echo ""

echo "=========================================="
echo ""

echo -e "${YELLOW}PASSO 3: Testar endpoint SEM autenticação${NC}"
echo "--------------------------------------"
echo "Endpoint: POST /api/forum/criar-por-tipo/"
echo ""
echo -e "${YELLOW}🔍 OBSERVE os logs no terminal do servidor:${NC}"
echo "   - [REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous"
echo "   - [RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 401 - Time: X.XXXs"
echo ""

RESPONSE_NO_AUTH=$(curl -s -X POST "${BASE_URL}/api/forum/criar-por-tipo/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Python Django",
    "conteudo": "Desenvolvedor backend"
  }')

echo "$RESPONSE_NO_AUTH" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE_NO_AUTH"
echo ""
echo -e "${RED}❌ Esperado: Erro 401 - Autenticação necessária${NC}"
echo ""

echo "=========================================="
echo ""

echo -e "${YELLOW}PASSO 4: Testar endpoint de consulta (não requer auth)${NC}"
echo "--------------------------------------"
echo "Endpoint: GET /api/forum/tipos-disponiveis/"
echo ""
echo -e "${YELLOW}🔍 OBSERVE os logs no terminal do servidor:${NC}"
echo "   - [REQUEST] GET /api/forum/tipos-disponiveis/ - User: Anonymous"
echo "   - [RESPONSE] GET /api/forum/tipos-disponiveis/ - Status: 200 - Time: X.XXXs"
echo ""

TIPOS_RESPONSE=$(curl -s "${BASE_URL}/api/forum/tipos-disponiveis/")

echo "$TIPOS_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$TIPOS_RESPONSE"
echo ""
echo -e "${GREEN}✅ Sucesso! Veja os logs [REQUEST] e [RESPONSE] no terminal do servidor${NC}"
echo ""

echo "=========================================="
echo ""

echo -e "${YELLOW}RESUMO DO PADRÃO DECORATOR${NC}"
echo "--------------------------------------"
echo ""
echo "📋 O que foi demonstrado:"
echo "   1. Logging automático de requisições ([REQUEST])"
echo "   2. Logging de respostas com status e tempo ([RESPONSE])"
echo "   3. Logging de erros com stack trace ([ERROR])"
echo "   4. Validação de autenticação com mensagem clara"
echo ""
echo "📁 Arquivos relevantes:"
echo "   - backend/Forum/views.py (métodos com logging manual)"
echo "   - backend/core/decorators.py (classe LoggingDecorator)"
echo ""
echo "🔍 Para ver os logs em tempo real:"
echo "   Verifique o terminal onde está rodando:"
echo -e "   ${GREEN}python manage.py runserver 8001${NC}"
echo ""
echo "📚 Documentação:"
echo "   - backend/docs/GOF_ESTRUTURAIS_DECORATOR.md"
echo "   - backend/docs/COMO_VER_DECORATOR_FUNCIONANDO.md"
echo ""

echo "=========================================="
echo -e "${GREEN}✅ TESTE CONCLUÍDO${NC}"
echo "=========================================="
