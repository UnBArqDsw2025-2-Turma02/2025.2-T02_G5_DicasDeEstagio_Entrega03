
# Política de Repositório - Padrões de Commits

## 1. Padrões de Commits
### 1.1 Estrutura Semântica
Os commits devem seguir o formato:
```
<tipo>[escopo opcional]: <descrição breve>

[corpo opcional]

[rodapé opcional]
```
**Exemplos**:
- `feat: adiciona autenticação JWT`
- `fix(core): corrige loop infinito na linha 50`
- `docs: atualiza guia de instalação`

### 1.2 Tipos de Commit 
| Tipo        | Descrição                                                                 |
|-------------|---------------------------------------------------------------------------|
| feat        | Novo recurso (relacionado ao MINOR do versionamento semântico)            |
| fix         | Correção de bug (relacionado ao PATCH do versionamento semântico)         |
| docs        | Alterações na documentação                                                |
| test        | Adição/ajuste de testes                                                   |
| refactor    | Refatoração sem mudança de funcionalidade                                 |
| perf        | Melhorias de performance                                                  |
| build       | Mudanças em dependências ou ferramentas de build                          |
| ci          | Mudanças na configuração de CI/CD                                         |
| chore       | Tarefas administrativas (ex: atualizar .gitignore)                        |
| cleanup     | Limpeza de código (remoção de código comentado/obsoleto)                  |
| remove      | Remoção de arquivos ou funcionalidades                                    |



---

## Bibliografia

- Conventional Commits. Disponível em: https://www.conventionalcommits.org/. Acesso em: 02 set. 2025.




## Histórico de Versão
| ID | Descrição | Autor |Revisor | Data |
| -- | -- | -- | -- | -- |
| 01  |  Adição dos dados | [Víctor Moreira](https://github.com/aqela-batata-alt) | - | 02/09/25 |
