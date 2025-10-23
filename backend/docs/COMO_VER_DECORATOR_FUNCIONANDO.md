# 🎯 Guia Prático: Ver o Decorator em Ação

## 📋 Passo a Passo para Ver o LoggingDecorator Funcionando

### Terminal 1: Servidor Django (com logs visíveis)

```bash
# 1. Ativar ambiente virtual
cd /home/mashiro/workspace/2025.2-T02_G5_DicasDeEstagio_Entrega03/backend
source .venv/bin/activate

# 2. Iniciar servidor (DEIXAR RODANDO - você verá os logs aqui)
python manage.py runserver 8001
```

**O que você verá:** O servidor rodando e esperando requisições.

---

### Terminal 2: Fazer Requisições HTTP

Abra um SEGUNDO terminal e execute:

```bash
# Ativar ambiente virtual
cd /home/mashiro/workspace/2025.2-T02_G5_DicasDeEstagio_Entrega03/backend
source .venv/bin/activate
```

Agora faça as requisições abaixo e **OBSERVE O TERMINAL 1** para ver os logs do Decorator:

#### 🔹 Teste 1: Requisição GET simples
```bash
curl http://127.0.0.1:8001/api/forum/
```

**O que o Decorator faz:**
- ✅ Loga `[REQUEST] GET /api/forum/ - User: Anonymous`
- ✅ Loga `[RESPONSE] GET /api/forum/ - Status: 200 - Time: 0.XXXs - User: Anonymous`

---

#### 🔹 Teste 2: Criar tópico usando Factory Method (endpoint com @log_request)
```bash
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Backend Django",
    "conteudo": "Procuramos desenvolvedor Django com 2 anos de experiência",
    "empresa": "Tech Corp"
  }'
```

**O que o Decorator faz:**
- ✅ Loga `[REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous`
- ✅ Loga `[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 403 - Time: 0.XXXs`
  - (Status 403 porque não está autenticado, mas o Decorator funcionou!)

---

#### 🔹 Teste 3: Listar tópicos por tipo (sem decorator = sem logs extras)
```bash
curl http://127.0.0.1:8001/api/forum/por-tipo/vaga
```

**O que acontece:**
- ⚠️ Apenas log padrão do Django (sem [REQUEST]/[RESPONSE])
- Este endpoint NÃO tem `@log_request`, então não há logs especiais

---

#### 🔹 Teste 4: Ver estatísticas (sem decorator)
```bash
curl http://127.0.0.1:8001/api/forum/estatisticas-tipos/
```

**O que acontece:**
- ⚠️ Log padrão do Django apenas
- Sem `@log_request` = sem logs customizados

---

#### 🔹 Teste 5: Endpoint que DEVE falhar (para ver log de erro)
```bash
curl http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"dados": "invalidos"}'
```

**O que o Decorator faz:**
- ✅ Loga `[REQUEST] POST /api/forum/criar-por-tipo/`
- ✅ Loga `[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 400 - Time: 0.XXXs`

---

## 🔍 Onde o @log_request está Aplicado

No arquivo `backend/Forum/views.py`, apenas estes métodos têm o decorator:

```python
class ForumViewSet(viewsets.ModelViewSet):
    
    @log_request  # ✅ TEM DECORATOR
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @log_request  # ✅ TEM DECORATOR
    @action(detail=False, methods=['post'], url_path='criar-por-tipo')
    def criar_topico_por_tipo(self, request):
        # ... código
```

**Endpoints SEM decorator (não geram logs customizados):**
- `GET /api/forum/` - list
- `GET /api/forum/{id}/` - retrieve
- `GET /api/forum/por-tipo/{tipo}/` - listar_por_tipo
- `GET /api/forum/estatisticas-tipos/` - estatisticas_tipos

---

## 📊 Exemplo de Saída Esperada no Terminal 1

Quando você fizer as requisições, verá algo assim no terminal do servidor:

```
[23/Oct/2025 19:30:15] INFO [REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous
[23/Oct/2025 19:30:15] INFO [RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 403 - Time: 0.023s - User: Anonymous
[23/Oct/2025 19:30:15] "POST /api/forum/criar-por-tipo/ HTTP/1.1" 403 58

[23/Oct/2025 19:30:20] INFO [REQUEST] GET /api/forum/ - User: Anonymous
[23/Oct/2025 19:30:20] INFO [RESPONSE] GET /api/forum/ - Status: 200 - Time: 0.145s - User: Anonymous
[23/Oct/2025 19:30:20] "GET /api/forum/ HTTP/1.1" 200 2345
```

**Compare:**
- Linhas com `[REQUEST]` e `[RESPONSE]` = **Decorator em ação** ✅
- Linhas sem esses marcadores = log padrão do Django

---

## 🎬 Demonstração Rápida (1 minuto)

```bash
# Terminal 1: Iniciar servidor
cd backend && source .venv/bin/activate && python manage.py runserver 8001

# Terminal 2: Fazer requisição decorada
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_topico": "vaga", "titulo": "Teste", "conteudo": "Conteúdo teste"}'

# Volte ao Terminal 1 e veja:
# [REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous
# [RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 403 - Time: 0.XXXs
```

---

## 🧪 Script de Teste Automatizado

Se quiser ver todos os testes de uma vez:

```bash
# No Terminal 2 (com servidor rodando no Terminal 1)
cd backend
source .venv/bin/activate

# Executar múltiplas requisições
echo "=== Teste 1: GET sem autenticação ==="
curl -s http://127.0.0.1:8001/api/forum/ | head -c 100

echo -e "\n\n=== Teste 2: POST com @log_request ==="
curl -s -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_topico": "vaga", "titulo": "Vaga Teste", "conteudo": "Conteúdo"}'

echo -e "\n\n=== Teste 3: GET tipos disponíveis ==="
curl -s http://127.0.0.1:8001/api/forum/tipos-disponiveis/ | python -m json.tool

echo -e "\n\nOBSERVE O TERMINAL DO SERVIDOR para ver os logs do Decorator!"
```

---

## ✅ Checklist de Verificação

- [ ] Terminal 1 rodando: `python manage.py runserver 8001`
- [ ] Terminal 2 pronto para comandos curl
- [ ] Executei requisição POST para `/criar-por-tipo/`
- [ ] Vi no Terminal 1 as linhas com `[REQUEST]` e `[RESPONSE]`
- [ ] Comparei com requisições sem decorator (menos logs)
- [ ] Entendi que o decorator adiciona logs automaticamente

---

## 🎓 Conclusão

O **LoggingDecorator** funciona de forma transparente:

1. **SEM modificar o código da view**
2. **Adiciona logs de REQUEST, RESPONSE e ERROR**
3. **Calcula tempo de execução automaticamente**
4. **Captura informações do usuário (email ou Anonymous)**
5. **Pode ser aplicado/removido apenas com `@log_request`**

**Isso é o padrão Decorator em ação!** 🚀
