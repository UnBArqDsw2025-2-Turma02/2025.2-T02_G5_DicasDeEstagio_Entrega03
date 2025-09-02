# Política de Repositório - Padrões de Branches

## 1. Política de Branches

### 1.1 Estrutura Semântica para pull request
Os requests devem seguir o formato:
```
## Descrição das Alterações
Breve descrição das modificações realizadas

## Tipo de Mudança
- [ ] Feature (nova funcionalidade)
- [ ] Fix (correção de bug)
- [ ] Docs (mudança na documentação)
- [ ] Refactor (refatoração de código)
- [ ] Test (adição/atualização de testes)

## Checklist de Validação
### Pré-requisitos
- [ ] Branch atualizada com develop/main
- [ ] Commits seguem padrão semântico

### Documentação
- [ ] README atualizado (se necessário)
- [ ] Comentários de código adicionados
- [ ] Changelog atualizado

### Revisão
- [ ] Self-review do código realizada

## Observações Adicionais
<!-- Comentários extras para os revisores -->
```

### 1.2 Proteção de Branches 
Branches protegidas (main, develop, release/*) devem ter:
- **Requer pull request antes do merge**
  - Requer review from Code Owners
- **Status checks obrigatórios**
  - Requer status checks para passar
  - Requer que as branches estejam atualizadas com base na main
  

### 1.3 Padrão de Nomenclatura
- `main`: Branch principal de produção
- `<nome_participante>`: Branch de integração e recursos
- `feature/*`: Novos recursos
- `release/*`: Preparação de releases

---

## Bibliografia

- Conventional Commits. Disponível em: https://www.conventionalcommits.org/. Acesso em: 02 set. 2025.



## Histórico de Versão
| ID | Descrição | Autor |Revisor | Data |
| -- | -- | -- | -- | -- |
| 01  |  Adição dos dados | [Víctor Moreira](https://github.com/aqela-batata-alt) | - | 02/09/25 |
