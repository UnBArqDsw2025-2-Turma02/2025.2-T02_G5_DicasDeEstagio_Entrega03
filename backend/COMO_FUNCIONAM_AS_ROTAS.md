# 🎯 Como as Rotas Funcionam no Django REST Framework

## ❓ Sua Dúvida: "Onde estão as rotas?"

**Resposta:** As rotas são **criadas automaticamente** pelo Django REST Framework quando você:
1. Registra um ViewSet no router
2. Usa o decorator `@action`

## 📚 Explicação Técnica

### 1. Registro no Router (urls.py)

```python
routers = routers.DefaultRouter()
routers.register(r'forum', ForumViewSet)  # ← Cria TODAS as rotas automaticamente
```

Este `register` cria **automaticamente**:

| Método HTTP | URL | Função no ViewSet |
|-------------|-----|-------------------|
| GET | `/api/forum/` | `list()` |
| POST | `/api/forum/` | `create()` |
| GET | `/api/forum/{id}/` | `retrieve()` |
| PUT | `/api/forum/{id}/` | `update()` |
| DELETE | `/api/forum/{id}/` | `destroy()` |

### 2. Decorator @action Cria Rotas Extras

Cada `@action` no seu ViewSet **cria automaticamente uma rota nova**:

#### Exemplo 1:
```python
@action(detail=False, methods=['post'], url_path='criar-por-tipo')
def criar_topico_por_tipo(self, request):
    pass
```

**Rota criada automaticamente:**
- `POST /api/forum/criar-por-tipo/`

#### Exemplo 2:
```python
@action(detail=False, methods=['get'], url_path='tipos-disponiveis')
def tipos_disponiveis(self, request):
    pass
```

**Rota criada automaticamente:**
- `GET /api/forum/tipos-disponiveis/`

#### Exemplo 3:
```python
@action(detail=False, methods=['get'], url_path='por-tipo/(?P<tipo>[^/.]+)')
def listar_por_tipo(self, request, tipo=None):
    pass
```

**Rota criada automaticamente:**
- `GET /api/forum/por-tipo/{tipo}/`
- Ex: `GET /api/forum/por-tipo/vaga/`

## ✅ Todas as Rotas Disponíveis no Seu Projeto

### ForumViewSet (`/api/forum/`):

| Método | URL | Tem @log_request? | Função |
|--------|-----|-------------------|--------|
| GET | `/api/forum/` | ❌ | Listar todos os tópicos |
| POST | `/api/forum/` | ✅ (via perform_create) | Criar tópico |
| GET | `/api/forum/{id}/` | ❌ | Ver um tópico |
| PUT | `/api/forum/{id}/` | ❌ | Atualizar tópico |
| DELETE | `/api/forum/{id}/` | ❌ | Deletar tópico |
| GET | `/api/forum/{id}/comentarios/` | ❌ | Ver comentários |
| POST | `/api/forum/criar-por-tipo/` | ✅ | Criar via Factory |
| GET | `/api/forum/tipos-disponiveis/` | ❌ | Listar tipos |
| GET | `/api/forum/por-tipo/{tipo}/` | ❌ | Filtrar por tipo |
| GET | `/api/forum/estatisticas-tipos/` | ❌ | Estatísticas |
| GET | `/api/forum/iterator-por-tipo/{tipo}/` | ❌ | Iterator pattern |
| GET | `/api/forum/demonstracao-minima/` | ❌ | Demo Iterator |

### ComentarioForumViewSet (`/api/comentarios/`):

| Método | URL | Tem @log_request? | Função |
|--------|-----|-------------------|--------|
| GET | `/api/comentarios/` | ❌ | Listar comentários |
| POST | `/api/comentarios/` | ❌ | Criar comentário |
| GET | `/api/comentarios/{id}/` | ❌ | Ver comentário |
| GET | `/api/comentarios/{id}/respostas/` | ❌ | Ver respostas |
| GET | `/api/comentarios/navegar-por-tipo/{tipo}/` | ❌ | Iterator |
| GET | `/api/comentarios/{id}/comentarios-arvore/` | ❌ | Árvore |
| GET | `/api/comentarios/paginado-avancado/` | ❌ | Paginação |
| GET | `/api/comentarios/demonstracao-padroes/` | ❌ | Demo padrões |

## 🧪 Como Testar as Rotas

### Passo 1: Iniciar Servidor
```bash
cd backend
source .venv/bin/activate
python manage.py runserver 8001
```

### Passo 2: Testar Rotas (outro terminal)

```bash
# Rota SEM decorator (log padrão)
curl http://127.0.0.1:8001/api/forum/tipos-disponiveis/

# Rota COM decorator (gera [REQUEST] e [RESPONSE])
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_topico": "vaga", "titulo": "Teste", "conteudo": "Teste"}'
```

### Passo 3: Ver Logs no Terminal do Servidor

No terminal onde o servidor está rodando, você verá:

**COM @log_request:**
```
[REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous
[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 403 - Time: 0.023s
```

**SEM @log_request:**
```
"GET /api/forum/tipos-disponiveis/ HTTP/1.1" 200 345
```

## 💡 Resumo

1. **Você NÃO precisa adicionar rotas manualmente em urls.py**
2. **O `routers.register()` cria as rotas automaticamente**
3. **Cada `@action` adiciona uma rota extra automaticamente**
4. **O `@log_request` é aplicado nos MÉTODOS, não nas rotas**
5. **As rotas JÁ EXISTEM e ESTÃO FUNCIONANDO agora mesmo**

## 🎯 Teste Rápido Agora

Execute isso EM UM TERMINAL com servidor rodando EM OUTRO:

```bash
# Terminal 1: Servidor
cd backend && source .venv/bin/activate && python manage.py runserver 8001

# Terminal 2: Teste
curl http://127.0.0.1:8001/api/forum/tipos-disponiveis/
```

Se retornar JSON com tipos disponíveis, **as rotas estão funcionando**! ✅
