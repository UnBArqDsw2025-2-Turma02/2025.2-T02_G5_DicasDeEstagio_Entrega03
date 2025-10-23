# 🔐 Guia Rápido de Autenticação JWT

## ✅ Configuração Completa

O projeto já está configurado com JWT (JSON Web Tokens) usando `rest_framework_simplejwt`.

---

## 📍 Endpoints Disponíveis

### 1. Registrar Novo Usuário
```bash
curl -X POST http://127.0.0.1:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@teste.com",
    "password": "senha123",
    "nome": "Usuario Teste"
  }'
```

**Resposta (201 Created):**
```json
{
  "user": {
    "id": 1,
    "email": "usuario@teste.com",
    "nome": "Usuario Teste"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 2. Login (obter tokens)
```bash
curl -X POST http://127.0.0.1:8001/api/auth/token/obtain/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@teste.com",
    "password": "senha123"
  }'
```

**Resposta (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 3. Usar Token em Requisições Autenticadas

#### Criar Tópico COM Autenticação
```bash
# Substitua SEU_TOKEN_AQUI pelo token 'access' recebido
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Python Django",
    "conteudo": "Desenvolvedor backend com Django e DRF"
  }'
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "titulo": "[VAGA] Vaga Python Django",
  "conteudo": "Desenvolvedor backend com Django e DRF",
  "user": {
    "id": 1,
    "email": "usuario@teste.com",
    "nome": "Usuario Teste"
  },
  "data_criacao": "2025-10-23T20:40:00Z",
  "visualizacoes": 0
}
```

---

### 4. Renovar Token (Refresh)
Tokens de acesso expiram em 60 minutos. Use o refresh token para obter um novo:

```bash
curl -X POST http://127.0.0.1:8001/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "SEU_REFRESH_TOKEN_AQUI"
  }'
```

**Resposta (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 🎯 Teste Completo (Passo a Passo)

### Terminal 1: Servidor
```bash
cd backend
python manage.py runserver 8001
```

### Terminal 2: Testes

#### Passo 1: Registrar usuário
```bash
curl -X POST http://127.0.0.1:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "decorator@teste.com",
    "password": "senha123",
    "nome": "Teste Decorator"
  }'
```

**Copie o token `access` da resposta!**

#### Passo 2: Criar tópico COM autenticação
```bash
# Cole seu token no lugar de SEU_TOKEN_AQUI
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Python",
    "conteudo": "Desenvolvedor backend"
  }'
```

**Logs esperados no Terminal 1:**
```
[REQUEST] POST /api/forum/criar-por-tipo/ - User: decorator@teste.com
[RESPONSE] POST /api/forum/criar-por-tipo/ - Status: 201 - Time: 0.045s - User: decorator@teste.com
```

#### Passo 3: Testar endpoint público (SEM token)
```bash
curl http://127.0.0.1:8001/api/forum/tipos-disponiveis/
```

**Logs esperados no Terminal 1:**
```
[REQUEST] GET /api/forum/tipos-disponiveis/ - User: Anonymous
[RESPONSE] GET /api/forum/tipos-disponiveis/ - Status: 200 - Time: 0.003s - User: Anonymous
```

---

## 🔧 Configurações JWT

Definidas em `core/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Token expira em 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh token expira em 7 dias
    'ROTATE_REFRESH_TOKENS': True,                   # Gera novo refresh ao usar
    'AUTH_HEADER_TYPES': ('Bearer',),                # Tipo: Bearer Token
}
```

---

## 🐛 Troubleshooting

### Erro: "Authentication credentials were not provided"
**Solução:** Certifique-se de incluir o header:
```bash
-H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Erro: "Token is invalid or expired"
**Solução:** Use o endpoint de refresh para obter novo token:
```bash
curl -X POST http://127.0.0.1:8001/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "SEU_REFRESH_TOKEN"}'
```

### Erro: "CSRF cookie not set"
**Solução:** Já corrigido! Usamos `@method_decorator(csrf_exempt)` nos ViewSets.

---

## 📚 Script Automatizado

Use o script de teste completo:

```bash
cd backend
./testar_com_autenticacao.sh
```

---

## ✅ Resumo para Apresentação

1. **Registrar usuário** → Obter tokens (access + refresh)
2. **Usar token** → Fazer requisições autenticadas
3. **Ver logs** → [REQUEST] e [RESPONSE] no terminal do servidor
4. **Padrão Decorator** → Logging automático funcionando! 🎉

---

## 🎓 Exemplo Completo com Variáveis

```bash
# 1. Registrar e capturar token
RESPONSE=$(curl -s -X POST http://127.0.0.1:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "password": "senha123",
    "nome": "Usuario Teste"
  }')

# 2. Extrair token
TOKEN=$(echo $RESPONSE | grep -o '"access":"[^"]*"' | cut -d'"' -f4)

# 3. Usar token para criar tópico
curl -X POST http://127.0.0.1:8001/api/forum/criar-por-tipo/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tipo_topico": "vaga",
    "titulo": "Vaga Python Django",
    "conteudo": "Desenvolvedor backend"
  }'
```

---

## 🎉 Pronto!

Agora você pode:
- ✅ Criar usuários
- ✅ Fazer login e obter JWT tokens
- ✅ Fazer requisições autenticadas
- ✅ Ver o padrão Decorator em ação nos logs!
