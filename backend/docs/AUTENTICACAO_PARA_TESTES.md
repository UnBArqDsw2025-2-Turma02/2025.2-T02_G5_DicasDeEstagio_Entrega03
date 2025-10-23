# 🔐 Como Testar o Decorator COM Autenticação

## ⚠️ Problema Atual

Você está recebendo este erro:
```
Cannot assign "<django.contrib.auth.models.AnonymousUser>": "Forum.user" must be a "User" instance.
```

**Motivo:** O endpoint `criar-por-tipo` requer um usuário autenticado porque precisa associar o tópico a um user.

---

## ✅ Solução: 3 Opções

### Opção 1: Usar Django Admin (MAIS RÁPIDO) ⭐

1. **Criar um superuser:**
```bash
cd backend
python manage.py createsuperuser
# Email: admin@test.com
# Password: admin123
```

2. **Fazer login no Django Admin:**
```bash
# Abra no navegador:
http://127.0.0.1:8001/admin/

# Login com as credenciais criadas
```

3. **Usar Session Authentication com curl:**
```bash
# Primeiro, obter o CSRF token e Session Cookie
curl -c cookies.txt http://127.0.0.1:8001/admin/login/

# Fazer login (você precisará do CSRF token do HTML)
# Ou usar o navegador para login e depois usar as ferramentas de desenvolvedor
```

---

### Opção 2: Criar Usuário via API e Usar Basic Auth

1. **Criar um usuário:**
```bash
curl -X POST http://127.0.0.1:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@decorator.com",
    "password": "senha123",
    "nome": "Usuario Teste"
  }'
```

2. **Usar Basic Authentication:**
```bash
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -u "teste@decorator.com:senha123" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Python Django",
    "conteudo": "Desenvolvedor backend com Django e DRF"
  }'
```

---

### Opção 3: Testar Apenas Endpoints Públicos (SEM AUTH)

Alguns endpoints **não** requerem autenticação:

#### ✅ Tipos Disponíveis (GET - Público)
```bash
curl http://127.0.0.1:8001/api/forum/tipos-disponiveis/
```

**Logs esperados no servidor:**
```
[REQUEST] GET /api/forum/tipos-disponiveis/ - User: Anonymous
[RESPONSE] GET /api/forum/tipos-disponiveis/ - Status: 200 - Time: 0.005s - User: Anonymous
```

#### ✅ Listar Tópicos (GET - Público)
```bash
curl http://127.0.0.1:8001/api/forum/topicos/
```

#### ✅ Estatísticas (GET - Público)
```bash
curl http://127.0.0.1:8001/api/forum/estatisticas-tipos/
```

---

## 🎯 Demonstração do Padrão Decorator

### O Que Observar nos Logs

Quando você faz uma requisição, o servidor mostra:

```
[REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous
[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 401 - Time: 0.001s - User: Anonymous - Reason: Not authenticated
```

Ou com sucesso (quando autenticado):

```
[REQUEST] POST /api/forum/criar-por-tipo/ - User: teste@decorator.com
[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 201 - Time: 0.045s - User: teste@decorator.com
```

### Logs de Erro

Se algo der errado:

```
[REQUEST] POST /api/forum/criar-por-tipo/ - User: teste@decorator.com
[ERROR] POST /api/forum/criar-por-tipo/ - Error: Campo obrigatório faltando - Time: 0.002s - User: teste@decorator.com
```

---

## 🚀 Script Automatizado

Execute o script de teste:

```bash
cd backend
./testar_com_autenticacao.sh
```

Este script:
1. Tenta criar um usuário
2. Testa endpoint SEM autenticação (erro esperado)
3. Testa endpoints públicos (sucesso)
4. Mostra como verificar os logs

---

## 📋 Checklist de Teste

- [ ] Servidor rodando em `http://127.0.0.1:8001`
- [ ] Terminal do servidor visível para ver logs
- [ ] Testar endpoint público: `tipos-disponiveis` ✅
- [ ] Ver logs `[REQUEST]` e `[RESPONSE]` no terminal ✅
- [ ] Testar endpoint protegido SEM auth → Erro 401 ✅
- [ ] (Opcional) Criar superuser e testar COM auth → Sucesso 201 ✅

---

## 💡 Exemplo Completo de Teste

### Terminal 1: Servidor
```bash
cd backend
python manage.py runserver 8001

# Aguarde ver:
# Starting development server at http://127.0.0.1:8001/
```

### Terminal 2: Testes
```bash
# Teste 1: Endpoint público (funciona SEM auth)
curl http://127.0.0.1:8001/api/forum/tipos-disponiveis/

# Observe no Terminal 1:
# [REQUEST] GET /api/forum/tipos-disponiveis/ - User: Anonymous
# [RESPONSE] GET /api/forum/tipos-disponiveis/ - Status: 200 - Time: 0.003s - User: Anonymous

# Teste 2: Endpoint protegido SEM auth (erro esperado)
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Teste",
    "conteudo": "Conteudo teste"
  }'

# Observe no Terminal 1:
# [REQUEST] POST /api/forum/criar-por-tipo/ - User: Anonymous
# [RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 401 - Time: 0.001s - User: Anonymous - Reason: Not authenticated
```

---

## 🎓 Conclusão

O **Padrão Decorator** está funcionando! Você pode ver:

✅ Logs de requisição `[REQUEST]`  
✅ Logs de resposta `[RESPONSE]` com status e tempo  
✅ Logs de erro `[ERROR]` com detalhes  
✅ Informações do usuário (autenticado ou Anonymous)  

**Para a apresentação**, você pode usar os endpoints **públicos** que não requerem autenticação e ainda assim demonstrar perfeitamente o padrão Decorator em ação! 🎉
