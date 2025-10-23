#!/bin/bash
# Script de Demonstração do Decorator Pattern
# Execute este script EM UM TERMINAL enquanto o servidor roda em OUTRO

echo "════════════════════════════════════════════════════════════"
echo "🎯 DEMONSTRAÇÃO: Decorator Pattern - LoggingDecorator"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  CERTIFIQUE-SE de que o servidor está rodando:"
echo "   Terminal 1: cd backend && source .venv/bin/activate && python manage.py runserver 8002"
echo ""
echo "Pressione ENTER para começar os testes..."
read

PORT=8002
BASE_URL="http://127.0.0.1:$PORT"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📌 TESTE 1: Endpoint COM @log_request decorator"
echo "════════════════════════════════════════════════════════════"
echo "Endpoint: POST /api/forum/criar-por-tipo/"
echo "Decorator: ✅ SIM (@log_request aplicado)"
echo ""
echo "O QUE ESPERAR no terminal do servidor:"
echo "  [REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous"
echo "  [RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 403 - Time: 0.XXXs"
echo ""
echo "Fazendo requisição..."
echo "────────────────────────────────────────────────────────────"

curl -X POST "$BASE_URL/api/forum/criar-por-tipo/" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Backend Django",
    "conteudo": "Procuramos desenvolvedor Django experiente"
  }' \
  -w "\n\nStatus HTTP: %{http_code}\nTempo total: %{time_total}s\n"

echo ""
echo "👉 OLHE O TERMINAL DO SERVIDOR AGORA! Você deve ver:"
echo "   ✅ Linha com [REQUEST] POST /api/forum/criar-por-tipo/"
echo "   ✅ Linha com [RESPONSE] com status e tempo de execução"
echo ""
echo "Pressione ENTER para próximo teste..."
read

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📌 TESTE 2: Endpoint SEM decorator"
echo "════════════════════════════════════════════════════════════"
echo "Endpoint: GET /api/forum/"
echo "Decorator: ❌ NÃO (método list não tem @log_request)"
echo ""
echo "O QUE ESPERAR no terminal do servidor:"
echo "  Apenas log padrão do Django (sem [REQUEST]/[RESPONSE])"
echo ""
echo "Fazendo requisição..."
echo "────────────────────────────────────────────────────────────"

curl -X GET "$BASE_URL/api/forum/" \
  -H "Content-Type: application/json" \
  -w "\n\nStatus HTTP: %{http_code}\nTempo total: %{time_total}s\n" \
  | head -c 200

echo "..."
echo ""
echo "👉 OLHE O TERMINAL DO SERVIDOR AGORA! Você deve ver:"
echo "   ⚠️  Apenas: \"GET /api/forum/ HTTP/1.1\" 200 ..."
echo "   ❌ SEM as linhas [REQUEST] e [RESPONSE]"
echo ""
echo "Pressione ENTER para próximo teste..."
read

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📌 TESTE 3: Tipos disponíveis (Factory Method)"
echo "════════════════════════════════════════════════════════════"
echo "Endpoint: GET /api/forum/tipos-disponiveis/"
echo "Decorator: ❌ NÃO"
echo ""
echo "Fazendo requisição..."
echo "────────────────────────────────────────────────────────────"

curl -X GET "$BASE_URL/api/forum/tipos-disponiveis/" \
  -w "\n\nStatus HTTP: %{http_code}\n"

echo ""
echo "Pressione ENTER para próximo teste..."
read

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📌 TESTE 4: Estatísticas por tipo"
echo "════════════════════════════════════════════════════════════"
echo "Endpoint: GET /api/forum/estatisticas-tipos/"
echo "Decorator: ❌ NÃO"
echo ""
echo "Fazendo requisição..."
echo "────────────────────────────────────────────────────────────"

curl -X GET "$BASE_URL/api/forum/estatisticas-tipos/" \
  -w "\n\nStatus HTTP: %{http_code}\n"

echo ""
echo "Pressione ENTER para teste final..."
read

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📌 TESTE 5: Múltiplas requisições decoradas"
echo "════════════════════════════════════════════════════════════"
echo "Vamos fazer 3 requisições rápidas para ver múltiplos logs"
echo ""

for i in {1..3}; do
  echo "Requisição $i/3..."
  curl -s -X POST "$BASE_URL/api/forum/criar-por-tipo/" \
    -H "Content-Type: application/json" \
    -d "{\"tipo_topico\": \"duvida\", \"titulo\": \"Teste $i\", \"conteudo\": \"Conteúdo $i\"}" \
    > /dev/null
  sleep 0.5
done

echo ""
echo "👉 OLHE O TERMINAL DO SERVIDOR AGORA!"
echo "   Você deve ver 3 pares de [REQUEST]/[RESPONSE]"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ DEMONSTRAÇÃO COMPLETA"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📝 RESUMO do que você viu:"
echo ""
echo "1. Endpoints COM @log_request:"
echo "   ✅ POST /api/forum/criar-por-tipo/"
echo "   → Gera logs [REQUEST] e [RESPONSE]"
echo "   → Mostra usuário (Anonymous ou email)"
echo "   → Calcula tempo de execução automaticamente"
echo ""
echo "2. Endpoints SEM @log_request:"
echo "   ❌ GET /api/forum/"
echo "   ❌ GET /api/forum/tipos-disponiveis/"
echo "   ❌ GET /api/forum/estatisticas-tipos/"
echo "   → Apenas log padrão do Django"
echo ""
echo "3. BENEFÍCIOS do Decorator Pattern:"
echo "   • Adiciona funcionalidade SEM modificar código da view"
echo "   • Pode ser aplicado/removido facilmente"
echo "   • Reutilizável em múltiplos endpoints"
echo "   • Mantém Single Responsibility Principle"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "🎓 Para mais detalhes, veja:"
echo "   • backend/docs/COMO_VER_DECORATOR_FUNCIONANDO.md"
echo "   • backend/docs/GOF_ESTRUTURAIS_DECORATOR.md"
echo "════════════════════════════════════════════════════════════"
