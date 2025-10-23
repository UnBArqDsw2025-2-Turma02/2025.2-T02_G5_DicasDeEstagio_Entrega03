# 🧪 Comandos CURL para Testar Iterator + Decorator

## Token de Acesso
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjYyMzYzLCJpYXQiOjE3NjEyNTg3NjMsImp0aSI6IjY1NzE5NDZlOTY2NzRlN2RiZTZjMGM1MjIzNGE2Y2FkIiwidXNlcl9pZCI6IjE1In0.pDFqVn0syGLjEWy64CFH3uRTwjGO9-eAmaERTP8kTcA"
```

## 1️⃣ Criar Tópicos (Factory Method + Decorator)

### Criar VAGA #1
```bash
curl -X POST http://localhost:8000/api/forum/criar-decorado/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjYyMzYzLCJpYXQiOjE3NjEyNTg3NjMsImp0aSI6IjY1NzE5NDZlOTY2NzRlN2RiZTZjMGM1MjIzNGE2Y2FkIiwidXNlcl9pZCI6IjE1In0.pDFqVn0syGLjEWy64CFH3uRTwjGO9-eAmaERTP8kTcA" \
  -d '{"tipo_topico":"vaga","titulo":"Vaga Python Junior","conteudo":"Procuramos desenvolvedor Python"}'
```

### Criar DÚVIDA
```bash
curl -X POST http://localhost:8000/api/forum/criar-decorado/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjYyMzYzLCJpYXQiOjE3NjEyNTg3NjMsImp0aSI6IjY1NzE5NDZlOTY2NzRlN2RiZTZjMGM1MjIzNGE2Y2FkIiwidXNlcl9pZCI6IjE1In0.pDFqVn0syGLjEWy64CFH3uRTwjGO9-eAmaERTP8kTcA" \
  -d '{"tipo_topico":"duvida","titulo":"Como usar Django?","conteudo":"Tenho dúvidas sobre Django REST Framework"}'
```

### Criar VAGA #2
```bash
curl -X POST http://localhost:8000/api/forum/criar-decorado/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjYyMzYzLCJpYXQiOjE3NjEyNTg3NjMsImp0aSI6IjY1NzE5NDZlOTY2NzRlN2RiZTZjMGM1MjIzNGE2Y2FkIiwidXNlcl9pZCI6IjE1In0.pDFqVn0syGLjEWy64CFH3uRTwjGO9-eAmaERTP8kTcA" \
  -d '{"tipo_topico":"vaga","titulo":"Vaga de estágio","conteudo":"Estágio em desenvolvimento web"}'
```

### Criar DICA
```bash
curl -X POST http://localhost:8000/api/forum/criar-decorado/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjYyMzYzLCJpYXQiOjE3NjEyNTg3NjMsImp0aSI6IjY1NzE5NDZlOTY2NzRlN2RiZTZjMGM1MjIzNGE2Y2FkIiwidXNlcl9pZCI6IjE1In0.pDFqVn0syGLjEWy64CFH3uRTwjGO9-eAmaERTP8kTcA" \
  -d '{"tipo_topico":"dica","titulo":"Dica de carreira","conteudo":"Como criar um bom LinkedIn"}'
```

### Criar EXPERIÊNCIA
```bash
curl -X POST http://localhost:8000/api/forum/criar-decorado/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjYyMzYzLCJpYXQiOjE3NjEyNTg3NjMsImp0aSI6IjY1NzE5NDZlOTY2NzRlN2RiZTZjMGM1MjIzNGE2Y2FkIiwidXNlcl9pZCI6IjE1In0.pDFqVn0syGLjEWy64CFH3uRTwjGO9-eAmaERTP8kTcA" \
  -d '{"tipo_topico":"experiencia","titulo":"Minha experiência","conteudo":"Trabalhei como estagiário na empresa X"}'
```

---

## 2️⃣ Testar Iterator Pattern

### Listar apenas VAGAs
```bash
curl http://localhost:8000/api/forum/iterator-por-tipo/vaga/
```

### Listar apenas DÚVIDAs
```bash
curl http://localhost:8000/api/forum/iterator-por-tipo/duvida/
```

### Listar apenas DICAs
```bash
curl http://localhost:8000/api/forum/iterator-por-tipo/dica/
```

### Listar apenas EXPERIÊNCIAs
```bash
curl http://localhost:8000/api/forum/iterator-por-tipo/experiencia/
```

### Listar apenas DISCUSSÕEs
```bash
curl http://localhost:8000/api/forum/iterator-por-tipo/discussao/
```

---

## 3️⃣ Demonstrações

### Demonstração da integração Factory + Iterator
```bash
curl http://localhost:8000/api/forum/demonstracao-minima/
```

### Ver tipos disponíveis
```bash
curl http://localhost:8000/api/forum/tipos-disponiveis/
```

---

## 4️⃣ Deletar Tópico (Decorator Pattern)

### Deletar tópico (soft delete) - substitua {id} pelo ID do tópico
```bash
curl -X DELETE http://localhost:8000/api/forum/deletar-decorado/1/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjYyMzYzLCJpYXQiOjE3NjEyNTg3NjMsImp0aSI6IjY1NzE5NDZlOTY2NzRlN2RiZTZjMGM1MjIzNGE2Y2FkIiwidXNlcl9pZCI6IjE1In0.pDFqVn0syGLjEWy64CFH3uRTwjGO9-eAmaERTP8kTcA"
```

---

## 📊 O que esperar:

### No Terminal do Servidor (logs do Decorator):
```
INFO [REQUEST] POST /api/forum/criar-decorado/ - User: teste@iterator.com
INFO [RESPONSE] POST /api/forum/criar-decorado/ - Status: 201 - Time: 0.045s - User: teste@iterator.com
```

### Na Resposta do Iterator:
```json
{
  "tipo_topico": "vaga",
  "total_encontrado": 2,
  "topicos": [
    {
      "id": 1,
      "titulo": "[VAGA - ESTÁGIO] Vaga Python Junior",
      "conteudo": "Procuramos desenvolvedor Python",
      "user": "teste@iterator.com"
    }
  ],
  "implementacao": {
    "padrao_usado": "Iterator Pattern (Versão Mínima)",
    "iterator_type": "TopicoPorTipoIterator"
  }
}
```

---

## ✅ Padrões GoF Demonstrados:

1. 🏭 **Factory Method** - Cria tópicos com formatação padronizada
2. 🎨 **Decorator** - Registra logs de requisições automaticamente
3. 🔄 **Iterator** - Navega pelos tópicos filtrados por tipo

**Copie e cole cada comando no terminal para testar!** 🚀
