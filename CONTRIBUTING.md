# Guia de Contribuição - Projeto Dicas de Estágio

Obrigado por seu interesse em contribuir com o projeto **Dicas de Estágio**! Este documento fornece diretrizes e informações sobre como você pode contribuir de forma efetiva para nosso projeto.

## Índice

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Configurando o Ambiente de Desenvolvimento](#configurando-o-ambiente-de-desenvolvimento)
- [Processo de Contribuição](#processo-de-contribuição)
- [Diretrizes de Commit](#diretrizes-de-commit)
- [Diretrizes de Pull Request](#diretrizes-de-pull-request)
- [Diretrizes de Documentação](#diretrizes-de-documentação)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Melhorias](#sugerindo-melhorias)

## Código de Conduta

Este projeto e todos os participantes estão sujeitos ao [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, espera-se que você cumpra este código. Por favor, reporte comportamentos inaceitáveis para os maintainers do projeto.

## Como Posso Contribuir?

Existem várias maneiras de contribuir com o projeto:

### 🐛 Reportando Bugs
- Verifique se o bug já foi reportado nas [Issues](../../issues)
- Crie uma nova issue usando o template de bug report
- Forneça informações detalhadas sobre como reproduzir o bug

### 💡 Sugerindo Melhorias
- Verifique se a sugestão já foi proposta nas [Issues](../../issues)
- Crie uma nova issue usando o template de feature request
- Descreva claramente a melhoria e sua justificativa

### 📝 Melhorando a Documentação
- Corrija erros de digitação
- Melhore a clareza das explicações
- Adicione exemplos práticos
- Traduza conteúdo quando necessário
- Adicione novos artefatos de documentação

### 🎨 Contribuindo com Design
- Melhore o layout e design das páginas
- Adicione diagramas e esquemas visuais
- Otimize imagens e recursos visuais
- Sugira melhorias na experiência do usuário

## Configurando o Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)
- Git

### Passos para Configuração

1. **Fork o repositório**
   ```bash
   # Clique no botão "Fork" no GitHub
   ```

2. **Clone seu fork**
   ```bash
   git clone https://github.com/<seu-usuario>/2025.2-T02_G5_DicasDeEstagio_Entrega01.git
   cd 2025.2-T02_G5_DicasDeEstagio_Entrega01
   ```

3. **Adicione o repositório original como upstream**
   ```bash
   git remote add upstream https://github.com/UnBArqDsw2025-2-Turma02/2025.2-T02_G5_DicasDeEstagio_Entrega01.git
   ```

4. **Instale as dependências do MkDocs**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute o projeto localmente**
   ```bash
   mkdocs serve
   ```
   
   O site ficará disponível em `http://127.0.0.1:8000/`

## Processo de Contribuição

### 1. Antes de Começar
- Verifique as [Issues](../../issues) abertas para evitar trabalho duplicado
- Para mudanças grandes, abra uma issue primeiro para discussão
- Certifique-se de que sua branch está atualizada com a main

### 2. Criando uma Branch
```bash
# Atualize sua branch main
git checkout main
git pull upstream main

# Crie uma nova branch com nome descritivo
git checkout -b tipo/descricao-da-mudanca
```

**Convenção de nomenclatura de branches:**
- `feature/nome-da-funcionalidade` - para novas funcionalidades
- `fix/nome-do-bug` - para correções de bugs
- `docs/nome-da-documentacao` - para mudanças na documentação
- `refactor/nome-da-refatoracao` - para refatorações de código

### 3. Fazendo as Mudanças
- Faça commits pequenos e focados
- Teste suas mudanças localmente com `mkdocs serve`
- Siga as diretrizes de estilo da documentação
- Verifique se os links internos estão funcionando

### 4. Enviando as Mudanças
```bash
# Adicione e commit suas mudanças
git add .
git commit -m "tipo: descrição clara da mudança"

# Envie para seu fork
git push origin sua-branch
```

## Diretrizes de Commit

Utilizamos o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/) para mensagens de commit:

### Formato
```
tipo(escopo): descrição

[corpo opcional]

[rodapé opcional]
```

### Tipos Permitidos
- `feat`: nova funcionalidade ou seção de documentação
- `fix`: correção de bug ou erro na documentação
- `docs`: mudanças na documentação
- `style`: mudanças de formatação/estilo
- `refactor`: reorganização da estrutura de documentação
- `chore`: mudanças em configurações, ferramentas, etc.

### Exemplos
```bash
feat(docs): adiciona seção sobre estágios remotos
fix(bpmn): corrige erro na modelagem do processo
docs: atualiza README com instruções de instalação
style: corrige formatação dos arquivos markdown
```

## Diretrizes de Pull Request

### Antes de Abrir um PR
- [ ] Certifique-se de que todas as mudanças estão funcionando
- [ ] Execute `mkdocs serve` para testar localmente
- [ ] Verifique se todos os links estão funcionando
- [ ] Confirme que está seguindo as diretrizes de documentação

### Template de PR
```markdown
## Descrição
Breve descrição das mudanças realizadas.

## Tipo de Mudança
- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova funcionalidade (mudança que adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação (mudança apenas na documentação)

## Como Foi Testado?
Descreva como você testou suas mudanças.

## Checklist
- [ ] Minha documentação segue as diretrizes de estilo do projeto
- [ ] Revisei meu próprio conteúdo
- [ ] Verifiquei se todos os links estão funcionando
- [ ] Testei localmente com `mkdocs serve`
- [ ] Minhas mudanças não quebram a estrutura da documentação
```

## Diretrizes de Documentação

### Estrutura dos Arquivos
- Use Markdown para toda a documentação
- Mantenha a estrutura de pastas existente
- Nomeie arquivos de forma clara e descritiva

### Estilo de Escrita
- Use linguagem clara e objetiva
- Inclua exemplos práticos sempre que possível
- Mantenha a formatação consistente
- Use listas para melhorar a legibilidade

### Imagens e Mídia
- Coloque imagens na pasta `docs/assets/imgs/`
- Use nomes descritivos para arquivos de imagem
- Otimize o tamanho das imagens

## Reportando Bugs

Para reportar um bug, abra uma [nova issue](../../issues/new) com as seguintes informações:

### Template de Bug Report
```markdown
**Descrição do Bug**
Uma descrição clara e concisa do que é o bug.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

**Comportamento Esperado**
Uma descrição clara do que você esperava que acontecesse.

**Screenshots**
Se aplicável, adicione screenshots para ajudar a explicar o problema.

**Ambiente**
- OS: [ex: iOS]
- Browser: [ex: chrome, safari]
- Versão: [ex: 22]

**Informações Adicionais**
Qualquer outra informação sobre o problema.
```

## Sugerindo Melhorias

Para sugerir uma melhoria, abra uma [nova issue](../../issues/new) com:

### Template de Feature Request
```markdown
**A melhoria está relacionada a um problema? Descreva.**
Uma descrição clara e concisa de qual é o problema.

**Descreva a solução que você gostaria**
Uma descrição clara e concisa do que você quer que aconteça.

**Descreva alternativas que você considerou**
Uma descrição clara e concisa de quaisquer soluções ou funcionalidades alternativas que você considerou.

**Informações Adicionais**
Qualquer outra informação ou screenshots sobre a feature request.
```

## Reconhecimento

Todas as contribuições são valorizadas e reconhecidas. Os contribuidores serão listados no arquivo CONTRIBUTORS.md (quando criado) e nos créditos da documentação.

## Precisa de Ajuda?

Se você tiver dúvidas sobre como contribuir:

1. Verifique a documentação existente
2. Procure por issues similares
3. Abra uma issue com a tag `question`
4. Entre em contato com os maintainers do projeto

---

**Obrigado por contribuir com o projeto Dicas de Estágio! 🚀**