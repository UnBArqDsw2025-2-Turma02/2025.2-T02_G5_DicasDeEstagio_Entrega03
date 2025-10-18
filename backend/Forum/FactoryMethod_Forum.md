<style>
    .markdown-section table {
        justify-items: center;
    }

    img{
        max-height: 300px;
        justify-items: center;
    }

</style>

# 3.1.3. Factory Method - Fórum de Tópicos

## 1. Introdução

O padrão _Factory Method_ é um dos padrões de projeto criacionais propostos pela _Gang of Four_ (GoF). Seu principal objetivo é delegar a responsabilidade de criação de objetos às subclasses, promovendo baixo acoplamento e maior flexibilidade na arquitetura do sistema.

Conforme destacado por LARMAN (2007), o _Factory Method_ pode ser compreendido como um caso particular do _Template Method_, no qual a operação primitiva é responsável pela criação de instâncias de classes concretas. Essa abordagem é amplamente utilizada no desenvolvimento de _frameworks_, pois permite que superclasses definam métodos de criação e deixem que as subclasses concretas determinem qual tipo específico de objeto será instanciado. Tal característica reforça a extensibilidade e a reutilização de código, princípios centrais da engenharia de software orientada a objetos.

## 2. Metodologia

Neste projeto, o padrão _Factory Method_ foi implementado com o objetivo de gerenciar o processo de criação de diferentes tipos de tópicos no fórum da plataforma Dicas de Estágio. O sistema suporta cinco tipos distintos de tópicos: **Vagas**, **Dúvidas**, **Experiências**, **Dicas** e **Discussões**. Todos compartilham os atributos básicos definidos no modelo `Forum`, porém são instanciados de forma especializada por meio de fábricas específicas (`TopicoVagaCreator`, `TopicoDuvidaCreator`, `TopicoExperienciaCreator`, `TopicoDicaCreator` e `TopicoDiscussaoCreator`).

A aplicação do padrão foi conduzida a partir do estudo teórico do conceito e da análise das necessidades de criação de diferentes tipos de conteúdo no fórum. A partir disso, foi elaborada uma estrutura que permite a criação padronizada e extensível de tópicos com características específicas para cada tipo.

Após a definição da arquitetura, a implementação foi realizada em três etapas:

1. Definição das classes abstratas e fábricas concretas em `backend/Forum/factories/topico_factory.py`;
2. Integração com o modelo existente `Forum` em `backend/Forum/models.py`;
3. Criação de testes automatizados para validação das regras e consistência do padrão em `backend/Forum/tests.py`.

### 3. Participantes

Os participantes da implementação deste Padrão de Projeto estão descritos na tabela abaixo:

<p style="text-align: center;">Tabela 1: Participantes da implementação do Factory Method</p>

|Matrícula | Aluno |
| -- | -- |
| [DEIXAR EM BRANCO]  |  [DEIXAR EM BRANCO] |
| [DEIXAR EM BRANCO]  |  [DEIXAR EM BRANCO] |

## 4. Aplicação do _Factory Method_

### 4.1. Modelagem UML

[ESPAÇO PARA DIAGRAMA UML - A SER CRIADO]

A estrutura implementada demonstra a relação entre as classes, destacando a dependência das subclasses criadoras (`TopicoVagaCreator`, `TopicoDuvidaCreator`, `TopicoExperienciaCreator`, `TopicoDicaCreator`, `TopicoDiscussaoCreator`) em relação à superclasse abstrata `TopicoCreator`, bem como a associação entre os criadores e o produto concreto (`Forum`).

### 4.2. Implementação

A estrutura implementada pode ser resumida da seguinte forma:

```python
class TopicoCreator(ABC):
    @abstractmethod
    def create_topico(self, user, titulo, conteudo, **kwargs):
        pass
    
    def validar_conteudo(self, titulo, conteudo):
        # Validação comum para todos os tipos
        pass
    
    def formatar_titulo(self, titulo, prefixo):
        # Formatação padrão de títulos
        pass
```

A classe `TopicoCreator` define a interface do método-fábrica (`create_topico`), que será obrigatoriamente sobrescrito nas subclasses concretas. Cada criador é responsável por instanciar um tipo específico de tópico com suas características particulares:

```python
class TopicoVagaCreator(TopicoCreator):
    def create_topico(self, user, titulo, conteudo, salario=None, requisitos=None, 
                     empresa=None, tipo_vaga="Estágio", **kwargs):
        # Criação específica para tópicos de vaga
        return Forum.objects.create(...)
```

```python
class TopicoDuvidaCreator(TopicoCreator):
    def create_topico(self, user, titulo, conteudo, categoria="Geral", 
                     urgencia="Normal", tags=None, **kwargs):
        # Criação específica para tópicos de dúvida
        return Forum.objects.create(...)
```

Através dessa estrutura, o código cliente não precisa conhecer diretamente as classes específicas de cada tipo de tópico. Ele apenas interage com a factory apropriada:

```python
topico_factory = TopicoFactory()
vaga = topico_factory.create_topico('vaga', user, titulo, conteudo, ...)
```

Dessa forma, a instanciação é encapsulada dentro das fábricas concretas, permitindo a expansão do sistema para novos tipos de tópicos sem alterar o código existente.

### 4.3. Tipos de Tópicos Suportados

O sistema atualmente suporta cinco tipos de tópicos, cada um com características específicas:

#### 4.3.1. Tópicos de Vaga (`TopicoVagaCreator`)
- **Finalidade**: Publicação de oportunidades de estágio ou emprego
- **Campos específicos**: salário, requisitos, empresa, tipo_vaga
- **Formatação**: `[VAGA - {TIPO}] {título}`
- **Exemplo**: `[VAGA - ESTÁGIO] Desenvolvedor Python Júnior`

#### 4.3.2. Tópicos de Dúvida (`TopicoDuvidaCreator`)
- **Finalidade**: Perguntas sobre carreira e estágios
- **Campos específicos**: categoria, urgência, tags
- **Formatação**: `[DÚVIDA - {CATEGORIA}] {título}`
- **Exemplo**: `[DÚVIDA - ENTREVISTAS] Como me preparar para entrevista técnica?`

#### 4.3.3. Tópicos de Experiência (`TopicoExperienciaCreator`)
- **Finalidade**: Compartilhamento de experiências de estágio
- **Campos específicos**: empresa, período, área, nota_experiencia
- **Formatação**: `[EXPERIÊNCIA] {título}`
- **Exemplo**: `[EXPERIÊNCIA] Minha experiência como estagiário na empresa X`

#### 4.3.4. Tópicos de Dica (`TopicoDicaCreator`)
- **Finalidade**: Compartilhamento de dicas de carreira
- **Campos específicos**: categoria_dica, nível, aplicabilidade
- **Formatação**: `[DICA - {CATEGORIA}] {título}`
- **Exemplo**: `[DICA - PRODUTIVIDADE] Como se organizar no estágio`

#### 4.3.5. Tópicos de Discussão (`TopicoDiscussaoCreator`)
- **Finalidade**: Discussões gerais sobre temas diversos
- **Campos específicos**: tema, tipo_discussao
- **Formatação**: `[DISCUSSÃO - {TEMA}] {título}`
- **Exemplo**: `[DISCUSSÃO - TRABALHO REMOTO] Home office para estagiários`

### 4.4. Códigos na Íntegra

A seguir, estão apresentados os códigos que implementam as classes relacionadas ao _Factory Method_ para tópicos do fórum.

*`Forum/factories/topico_factory.py`*

<details>
    <summary>Clique aqui para ver o código inteiro</summary>

```python
from abc import ABC, abstractmethod
from django.utils import timezone
from ..models import Forum


class TopicoCreator(ABC):
    
    @abstractmethod
    def create_topico(self, user, titulo, conteudo, **kwargs):
        pass
    
    def validar_conteudo(self, titulo, conteudo):
        if not titulo or len(titulo.strip()) < 5:
            raise ValueError("Título deve ter pelo menos 5 caracteres")
        
        if not conteudo or len(conteudo.strip()) < 10:
            raise ValueError("Conteúdo deve ter pelo menos 10 caracteres")
        
        return True
    
    def formatar_titulo(self, titulo, prefixo):
        titulo_limpo = titulo.strip()
        if not titulo_limpo.startswith(f"[{prefixo}]"):
            return f"[{prefixo}] {titulo_limpo}"
        return titulo_limpo


class TopicoVagaCreator(TopicoCreator):
    def create_topico(self, user, titulo, conteudo, salario=None, requisitos=None, 
                     empresa=None, tipo_vaga="Estágio", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"VAGA - {tipo_vaga.upper()}")
        
        conteudo_enriquecido = conteudo
        
        if empresa:
            conteudo_enriquecido += f"\n\n**Empresa:** {empresa}"
        
        if salario:
            conteudo_enriquecido += f"\n**Salário:** {salario}"
        
        if requisitos:
            conteudo_enriquecido += f"\n**Requisitos:** {requisitos}"
        
        conteudo_enriquecido += f"\n\n**Tipo de Vaga:** {tipo_vaga}"
        conteudo_enriquecido += f"\n**Publicado em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDuvidaCreator(TopicoCreator):
    def create_topico(self, user, titulo, conteudo, categoria="Geral", 
                     urgencia="Normal", tags=None, **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"DÚVIDA - {categoria.upper()}")
        
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n**Categoria:** {categoria}"
        conteudo_enriquecido += f"\n**Urgência:** {urgencia}"
        
        if tags:
            tags_str = ", ".join(tags) if isinstance(tags, list) else tags
            conteudo_enriquecido += f"\n**Tags:** {tags_str}"
        
        if urgencia.lower() == "alta":
            conteudo_enriquecido += f"\n\n**URGENTE:** Preciso de ajuda rapidamente!"
        
        conteudo_enriquecido += f"\n\n**Pergunta feita em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Aguardando respostas da comunidade...**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoExperienciaCreator(TopicoCreator):
    def create_topico(self, user, titulo, conteudo, empresa=None, periodo=None, 
                     area=None, nota_experiencia=None, **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, "EXPERIÊNCIA")
        
        conteudo_enriquecido = conteudo
        
        if empresa:
            conteudo_enriquecido += f"\n\n**Empresa:** {empresa}"
        
        if periodo:
            conteudo_enriquecido += f"\n**Período:** {periodo}"
        
        if area:
            conteudo_enriquecido += f"\n**Área:** {area}"
        
        if nota_experiencia:
            estrelas = "*" * int(nota_experiencia)
            conteudo_enriquecido += f"\n**Avaliação:** {estrelas} ({nota_experiencia}/5)"
        
        conteudo_enriquecido += f"\n\n**Compartilhado em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Compartilhe sua experiência também!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDicaCreator(TopicoCreator):
    def create_topico(self, user, titulo, conteudo, categoria_dica="Carreira", 
                     nivel="Iniciante", aplicabilidade="Geral", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"DICA - {categoria_dica.upper()}")
        
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n**Categoria:** {categoria_dica}"
        conteudo_enriquecido += f"\n**Nível:** {nivel}"
        conteudo_enriquecido += f"\n**Aplicabilidade:** {aplicabilidade}"
        
        if nivel.lower() == "iniciante":
            conteudo_enriquecido += f"\n\n**Perfeito para quem está começando!**"
        elif nivel.lower() == "avançado":
            conteudo_enriquecido += f"\n\n**Para quem já tem experiência!**"
        
        conteudo_enriquecido += f"\n\n**Dica compartilhada em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Ajudou? Deixe um comentário!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDiscussaoCreator(TopicoCreator):
    def create_topico(self, user, titulo, conteudo, tema="Geral", 
                     tipo_discussao="Aberta", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"DISCUSSÃO - {tema.upper()}")
        
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n**Tema:** {tema}"
        conteudo_enriquecido += f"\n**Tipo:** {tipo_discussao}"
        
        conteudo_enriquecido += f"\n\n**Discussão iniciada em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Participe! Queremos ouvir sua opinião!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoFactory:
    
    _creators = {
        'vaga': TopicoVagaCreator(),
        'duvida': TopicoDuvidaCreator(),
        'experiencia': TopicoExperienciaCreator(),
        'dica': TopicoDicaCreator(),
        'discussao': TopicoDiscussaoCreator(),
    }
    
    @classmethod
    def get_creator(cls, tipo_topico):
        creator = cls._creators.get(tipo_topico.lower())
        if not creator:
            raise ValueError(f"Tipo de tópico '{tipo_topico}' não suportado. "
                           f"Tipos disponíveis: {list(cls._creators.keys())}")
        return creator
    
    @classmethod
    def create_topico(cls, tipo_topico, user, titulo, conteudo, **kwargs):
        creator = cls.get_creator(tipo_topico)
        return creator.create_topico(user, titulo, conteudo, **kwargs)
    
    @classmethod
    def get_tipos_disponiveis(cls):
        return {
            'vaga': {
                'nome': 'Vaga de Estágio/Emprego',
                'descricao': 'Para publicar oportunidades de estágio ou emprego',
                'campos_extras': ['salario', 'requisitos', 'empresa', 'tipo_vaga'],
                'exemplo': 'Vaga para desenvolvedor Python júnior'
            },
            'duvida': {
                'nome': 'Dúvida sobre Estágios',
                'descricao': 'Para fazer perguntas sobre estágios e carreira',
                'campos_extras': ['categoria', 'urgencia', 'tags'],
                'exemplo': 'Como me preparar para entrevista técnica?'
            },
            'experiencia': {
                'nome': 'Compartilhar Experiência',
                'descricao': 'Para compartilhar experiências de estágio',
                'campos_extras': ['empresa', 'periodo', 'area', 'nota_experiencia'],
                'exemplo': 'Minha experiência como estagiário na empresa X'
            },
            'dica': {
                'nome': 'Dica de Carreira',
                'descricao': 'Para compartilhar dicas úteis sobre carreira',
                'campos_extras': ['categoria_dica', 'nivel', 'aplicabilidade'],
                'exemplo': 'Como criar um LinkedIn profissional'
            },
            'discussao': {
                'nome': 'Discussão Geral',
                'descricao': 'Para iniciar discussões sobre temas diversos',
                'campos_extras': ['tema', 'tipo_discussao'],
                'exemplo': 'O que vocês acham do home office para estagiários?'
            }
        }
```
</details>

## 5. Verificação e Validação

A validação da implementação foi realizada por meio de testes unitários no Django (`backend/Forum/tests.py`), abrangendo:

- Criação de instâncias de cada tipo de tópico pelas respectivas fábricas;
- Garantia de que `TopicoCreator` não pode ser instanciada diretamente (por ser abstrata);
- Testes de integridade para campos obrigatórios (_ValueError_);
- Testes de validação de conteúdo mínimo;
- Testes de formatação correta de títulos;
- Testes de funcionalidade da classe `TopicoFactory`.

### 5.1. Resultados dos Testes

Os testes implementados cobrem os seguintes cenários:

#### 5.1.1. Testes de Criação por Tipo
- `test_criar_topico_vaga`: Valida criação de tópicos de vaga com campos específicos
- `test_criar_topico_duvida`: Valida criação de tópicos de dúvida com categorização
- `test_criar_topico_experiencia`: Valida criação de tópicos de experiência com avaliação
- `test_criar_topico_dica`: Valida criação de tópicos de dica com níveis
- `test_criar_topico_discussao`: Valida criação de tópicos de discussão temática

#### 5.1.2. Testes de Validação
- `test_tipo_topico_inexistente`: Verifica tratamento de tipos não suportados
- `test_validacao_titulo_curto`: Valida rejeição de títulos muito curtos
- `test_validacao_conteudo_curto`: Valida rejeição de conteúdo insuficiente

#### 5.1.3. Testes de Formatação
- `test_formatacao_titulo_com_prefixo`: Verifica adição correta de prefixos
- `test_titulo_ja_com_prefixo`: Evita duplicação de prefixos

### 5.2. Passo-a-passo de execução dos testes

**5.2.1. Navegar para o diretório do projeto**

```bash
cd /home/cerq/Documentos/arqEntrega03/2025.2-T02_G5_DicasDeEstagio_Entrega03/backend
```

**5.2.2. Ativar o ambiente virtual (se necessário)**

```bash
source ../.venv/bin/activate
```

**5.2.3. Executar os testes do Factory Method**

```bash
python manage.py test Forum.tests.TopicoFactoryTestCase -v 2
```

**5.2.4. Executar comando de demonstração**

```bash
python manage.py test_topico_factory --criar-exemplos
```

Ao executar os testes, o Django cria um banco de dados temporário e verifica se as fábricas e validações funcionam conforme o esperado, garantindo que o padrão _Factory Method_ foi corretamente aplicado para os tópicos do fórum.

## 6. Integração com API REST

O padrão _Factory Method_ foi integrado com a API REST do Django através de endpoints específicos no `ForumViewSet`:

### 6.1. Endpoints Disponíveis

#### 6.1.1. POST `/api/forum/criar_topico_por_tipo/`
Cria um novo tópico usando o Factory Method:

```json
{
    "tipo_topico": "vaga",
    "titulo": "Desenvolvedor Python",
    "conteudo": "Vaga para desenvolvedor Python júnior",
    "salario": "R$ 2.500,00",
    "requisitos": "Python, Django",
    "empresa": "Tech Corp",
    "tipo_vaga": "Estágio"
}
```

#### 6.1.2. GET `/api/forum/tipos_disponiveis/`
Retorna informações sobre todos os tipos de tópicos disponíveis.

#### 6.1.3. GET `/api/forum/listar_por_tipo/?tipo=vaga`
Lista tópicos filtrados por tipo específico.

#### 6.1.4. GET `/api/forum/estatisticas_tipos/`
Retorna estatísticas de uso dos diferentes tipos de tópicos.

## 7. Vídeo de explicação

[ESPAÇO PARA VÍDEO - A SER CRIADO]

## 8. Justificativas e Senso Crítico

A escolha do padrão _Factory Method_ se mostrou adequada para este contexto, pois:

- **Organização por tipo**: Cada tipo de tópico possui características específicas que são tratadas de forma padronizada;
- **Extensibilidade**: Facilita a adição de novos tipos de tópicos sem modificar o código existente;
- **Validação consistente**: Garante que todos os tópicos passem pelas mesmas validações básicas;
- **Formatação automática**: Aplica formatação específica conforme o tipo de tópico;
- **Reutilização de código**: Evita duplicação de lógica de criação.

Em termos arquiteturais, a adoção do _Factory Method_ contribuiu para:

- **Baixo acoplamento**: O cliente não precisa conhecer as classes específicas de cada tipo;
- **Alta coesão**: Cada factory tem responsabilidade única e bem definida;
- **Testabilidade**: Cada tipo pode ser testado isoladamente;
- **Manutenibilidade**: Mudanças em um tipo não afetam os outros.

### 8.1. Benefícios Específicos para Fóruns

- **Categorização automática**: Títulos são automaticamente categorizados com prefixos;
- **Enriquecimento de conteúdo**: Cada tipo adiciona informações específicas relevantes;
- **Validação específica**: Diferentes tipos podem ter validações particulares no futuro;
- **Métricas diferenciadas**: Permite análise separada de diferentes tipos de conteúdo.

### 8.2. Limitações e Considerações

Como limitação, observa-se que:

- O número de classes criadoras cresce conforme novos tipos são adicionados;
- Cada tipo requer manutenção individual de sua lógica específica;
- A complexidade pode aumentar se os tipos tiverem muitas variações.

Entretanto, essas limitações são compensadas pela clareza, organização e manutenibilidade do código resultante.

## 9. Conclusão

A implementação do padrão _Factory Method_ para o sistema de tópicos do fórum garantiu uma estrutura organizacional robusta e extensível para a plataforma Dicas de Estágio. O padrão possibilitou a criação padronizada de diferentes tipos de conteúdo, cada um com suas características específicas, mantendo a consistência e facilitando futuras expansões.

A aplicação do padrão foi acompanhada de implementação completa em Python/Django, integração com API REST, testes automatizados abrangentes e documentação detalhada, assegurando sua correta funcionalidade e aderência aos princípios da engenharia de software orientada a objetos.

O sistema resultante oferece uma base sólida para o crescimento do fórum, permitindo a adição de novos tipos de tópicos de forma organizada e mantendo a qualidade e consistência do conteúdo publicado.
