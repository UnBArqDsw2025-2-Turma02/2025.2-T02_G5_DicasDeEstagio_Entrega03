# 🎯 ROTAS DISPONÍVEIS - Como Testar o Decorator

## 📋 Rotas do ForumViewSet (Base: `/api/forum/`)

### ✅ ROTAS COM @log_request (VÃO GERAR LOGS)

#### 1. **POST /api/forum/criar-por-tipo/** ✅
```bash
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Desenvolvedor Python",
    "conteudo": "Descrição da vaga aqui"
  }'
```

**O que você verá no servidor:**
```
[REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous
[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 403 - Time: 0.XXXs - User: Anonymous
```

---

### ⚠️ ROTAS SEM @log_request (Logs padrão do Django apenas)

#### 2. **GET /api/forum/** (listar todos)
```bash
curl http://127.0.0.1:8001/api/forum/
```

#### 3. **GET /api/forum/{id}/** (ver um tópico)
```bash
curl http://127.0.0.1:8001/api/forum/1/
```

#### 4. **GET /api/forum/tipos-disponiveis/**
```bash
curl http://127.0.0.1:8001/api/forum/tipos-disponiveis/
```

#### 5. **GET /api/forum/por-tipo/{tipo}/**
```bash
curl http://127.0.0.1:8001/api/forum/por-tipo/vaga/
```

#### 6. **GET /api/forum/estatisticas-tipos/**
```bash
curl http://127.0.0.1:8001/api/forum/estatisticas-tipos/
```

#### 7. **GET /api/forum/iterator-por-tipo/{tipo}/**
```bash
curl http://127.0.0.1:8001/api/forum/iterator-por-tipo/vaga/
```

#### 8. **GET /api/forum/demonstracao-minima/**
```bash
curl http://127.0.0.1:8001/api/forum/demonstracao-minima/
```

---

## 🚀 TESTE PRÁTICO AGORA

### Passo 1: Iniciar Servidor (Terminal 1)
```bash
cd /home/mashiro/workspace/2025.2-T02_G5_DicasDeEstagio_Entrega03/backend
source .venv/bin/activate
python manage.py runserver 8001
```

### Passo 2: Fazer Requisição (Terminal 2)
```bash
# Teste a ÚNICA rota com @log_request
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_topico": "vaga", "titulo": "Teste Decorator", "conteudo": "Testando"}'
```

### Passo 3: Ver Logs no Terminal 1
Você deve ver:
```
[REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous
[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 403 - Time: 0.023s - User: Anonymous
```

**Status 403 é esperado** porque não está autenticado. O importante é ver os logs `[REQUEST]` e `[RESPONSE]` - isso prova que o Decorator está funcionando! ✅

---

## 💡 VAMOS ADICIONAR MAIS DECORATORS?

Se você quer ver o decorator funcionando em MAIS endpoints, podemos adicionar `@log_request` em outros métodos. Por exemplo:

```python
@log_request  # ADICIONAR AQUI
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

@log_request  # ADICIONAR AQUI  
def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    instance.visualizacoes += 1
    instance.save(update_fields=['visualizacoes'])
    serializer = self.get_serializer(instance)
    return Response(serializer.data)
```

Quer que eu adicione o decorator em mais endpoints?
