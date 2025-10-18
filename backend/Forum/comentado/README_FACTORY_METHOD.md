# Factory Method para Tópicos do Fórum - Projeto Dicas de Estágio

## 📋 Resumo da Implementação

Este documento apresenta a implementação do **padrão Factory Method** aplicado à criação de diferentes tipos de tópicos no fórum do projeto "Dicas de Estágio".

## 🎯 Tipos de Tópicos Implementados

### 1. 📢 **VAGA** - Oportunidades de Estágio/Emprego
- **Prefixo**: `[VAGA - ESTÁGIO]` ou `[VAGA - CLT]`
- **Campos específicos**: `salario`, `requisitos`, `empresa`, `tipo_vaga`
- **Exemplo**: Vagas de desenvolvedor, designer, marketing, etc.

### 2. ❓ **DÚVIDA** - Perguntas sobre Carreira
- **Prefixo**: `[DÚVIDA - CATEGORIA]`
- **Campos específicos**: `categoria`, `urgencia`, `tags`
- **Exemplo**: Dúvidas sobre entrevistas, preparação, documentos

### 3. 📖 **EXPERIÊNCIA** - Compartilhamento de Vivências
- **Prefixo**: `[EXPERIÊNCIA]`
- **Campos específicos**: `empresa`, `periodo`, `area`, `nota_experiencia`
- **Exemplo**: Relatos de estágios, experiências em empresas

### 4. 💡 **DICA** - Conselhos de Carreira
- **Prefixo**: `[DICA - CATEGORIA]`
- **Campos específicos**: `categoria_dica`, `nivel`, `aplicabilidade`
- **Exemplo**: Dicas de produtividade, networking, currículo

### 5. 🗣️ **DISCUSSÃO** - Debates Gerais
- **Prefixo**: `[DISCUSSÃO - TEMA]`
- **Campos específicos**: `tema`, `tipo_discussao`
- **Exemplo**: Debates sobre home office, mercado de trabalho

## 🚀 Como Usar

### 1. Via Código Python

```python
from Forum.factories.topico_factory import TopicoFactory

# Criar tópico de vaga
topico_vaga = TopicoFactory.create_topico(
    tipo_topico='vaga',
    user=usuario,
    titulo='Desenvolvedor Python Júnior',
    conteudo='Descrição da vaga...',
    salario='R$ 3.000,00',
    empresa='Tech Corp',
    tipo_vaga='Estágio'
)

# Criar tópico de dúvida
topico_duvida = TopicoFactory.create_topico(
    tipo_topico='duvida',
    user=usuario,
    titulo='Como me preparar para entrevista?',
    conteudo='Preciso de ajuda...',
    categoria='Entrevistas',
    urgencia='Alta'
)
```

### 2. Via API REST

#### Criar Tópico por Tipo
```bash
POST /api/forum/criar-por-tipo/
Content-Type: application/json

{
    "tipo_topico": "vaga",
    "titulo": "Desenvolvedor Python",
    "conteudo": "Vaga para desenvolvedor...",
    "salario": "R$ 3.000",
    "empresa": "Tech Corp",
    "tipo_vaga": "Estágio"
}
```

#### Listar Tipos Disponíveis
```bash
GET /api/forum/tipos-disponiveis/
```

#### Listar Tópicos por Tipo
```bash
GET /api/forum/por-tipo/vaga/
GET /api/forum/por-tipo/duvida/
```

#### Ver Estatísticas
```bash
GET /api/forum/estatisticas-tipos/
```

### 3. Via Comando Django

```bash
# Mostrar tipos disponíveis
python manage.py test_topico_factory

# Criar exemplos de todos os tipos
python manage.py test_topico_factory --criar-exemplos

# Criar apenas um tipo específico
python manage.py test_topico_factory --tipo=vaga

# Limpar tópicos criados pelo factory
python manage.py test_topico_factory --limpar
```

## 🧪 Executando os Testes

```bash
# Executar todos os testes do Forum
python manage.py test Forum

# Executar apenas testes do Factory Method
python manage.py test Forum.tests.TopicoFactoryTestCase

# Com verbosidade
python manage.py test Forum.tests.TopicoFactoryTestCase -v 2
```

## 📁 Estrutura dos Arquivos

```
backend/Forum/
├── factories/
│   ├── __init__.py
│   └── topico_factory.py          # Implementação do Factory Method
├── management/
│   └── commands/
│       └── test_topico_factory.py  # Comando para testar
├── models.py                       # Modelo Forum existente
├── views.py                        # Views com endpoints do Factory
├── tests.py                        # Testes unitários
└── exemplo_topico_factory_usage.py # Exemplos de uso
```

## ✅ Vantagens da Implementação

1. **Extensibilidade**: Fácil adicionar novos tipos de tópicos
2. **Consistência**: Cada tipo tem formatação e campos específicos
3. **Manutenibilidade**: Lógica de criação centralizada
4. **Validação**: Validações específicas para cada tipo
5. **Rastreabilidade**: Fácil identificar e filtrar por tipo

## 🔧 Próximos Passos Sugeridos

1. **Interface Frontend**: Criar formulários específicos para cada tipo
2. **Notificações**: Sistema de notificações baseado no tipo
3. **Moderação**: Regras de moderação específicas por tipo
4. **Gamificação**: Sistema de pontos baseado no tipo de contribuição
5. **Relatórios**: Dashboards com métricas por tipo de tópico

## 🎯 Casos de Uso Reais

- **Estudantes** podem criar dúvidas e compartilhar experiências
- **Empresas** podem publicar vagas de forma estruturada
- **Estagiários** podem dar dicas e relatar experiências
- **Moderadores** podem criar discussões temáticas
- **Sistema** pode categorizar e filtrar automaticamente

## 🏆 Benefícios para o Projeto

O Factory Method aplicado aos tópicos do fórum traz organização, estrutura e facilita a manutenção do código, permitindo que o projeto "Dicas de Estágio" tenha um fórum mais organizado e funcional para todos os usuários.
