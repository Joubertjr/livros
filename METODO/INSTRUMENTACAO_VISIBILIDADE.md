---
document_id: INSTRUMENTACAO_VISIBILIDADE
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-10
governed_by: /METODO/PILAR_ENDFIRST.md
---

# Instrumentação de Visibilidade — Fonte Única de Verdade

**Versão:** 1.0  
**Data:** 10 de Janeiro de 2026  
**Tipo:** Operacional (Sistema de Visibilidade)  
**Status:** Aprovado pelo CEO

---

## 🎯 OBJETIVO

Este documento define a **instrumentação de visibilidade** do ENDFIRST Ecosystem: **como CEO vê "o que está acontecendo" em 30 segundos, sem conversa humana**.

**Regra fundamental:**
> GitHub Projects é a fonte única de verdade.  
> Se não está no Kanban, não está acontecendo.  
> Status verbal é ruído.

**Princípios aplicados:**
- **END FIRST:** Visibilidade serve ao resultado, não o contrário
- **OD-009:** Processo > Disciplina (sistema impede erro por design)
- **OD-011:** Entendimento sem mudança é fuga (visibilidade muda comportamento agora)

---

## 📊 FONTE ÚNICA DE VERDADE

### GitHub Projects (Kanban Canônico)
**URL:** https://github.com/users/Joubertjr/projects/[NÚMERO]  
**Produto:** LLM Orchestrator (DEMANDA-001)

**O que CEO vê em 30 segundos:**
1. **O que está em execução agora** (coluna DOING)
2. **O que está bloqueado e por quê** (coluna BLOCKED + descrição do bloqueio)
3. **O que falta para concluir DEMANDA-001** (coluna TODO + cards restantes)

**Formato dos cards:**
- **Título:** Nome da demanda ou incremento (ex: "INCREMENTO 3 - Integração com Keychain")
- **Descrição:** END explícito + critérios de aceitação + evidências
- **Labels:** `priority:high`, `type:bug`, `blocked:decision`, etc.
- **Assignee:** Executor (Cursor ou Manus)
- **Milestone:** Produto (ex: "LLM Orchestrator v1.0")

---

## 🔍 PERGUNTAS QUE CEO RESPONDE EM 30s

### Pergunta 1: O que está em execução agora?
**Como responder:**
1. Abrir GitHub Projects
2. Olhar coluna DOING
3. Ler títulos dos cards

**Exemplo de resposta:**
> "INCREMENTO 3 - Integração com Keychain está em execução pelo Cursor."

**Proibições:**
- ❌ Perguntar ao executor "o que você está fazendo?"
- ❌ Confiar em status verbal ("estou trabalhando nisso")
- ❌ Assumir que algo está em execução sem card em DOING

---

### Pergunta 2: O que está bloqueado e por quê?
**Como responder:**
1. Abrir GitHub Projects
2. Olhar coluna BLOCKED
3. Ler descrição do bloqueio no card

**Exemplo de resposta:**
> "INCREMENTO 2 está bloqueado porque Keychain não está disponível no macOS Sandbox. Responsável pela resolução: CEO (decisão sobre alternativa)."

**Proibições:**
- ❌ Perguntar ao executor "por que está travado?"
- ❌ Aceitar bloqueio sem descrição ("está bloqueado, não sei por quê")
- ❌ Aceitar bloqueio sem responsável pela resolução

---

### Pergunta 3: O que falta para concluir DEMANDA-001?
**Como responder:**
1. Abrir GitHub Projects
2. Contar cards em TODO + DOING + BLOCKED
3. Comparar com total de incrementos planejados

**Exemplo de resposta:**
> "Faltam 5 incrementos: 3 em TODO, 1 em DOING, 1 em BLOCKED. Total planejado: 7 incrementos. Progresso: 2/7 (28%)."

**Proibições:**
- ❌ Perguntar ao executor "quanto falta?"
- ❌ Confiar em estimativa verbal ("falta pouco")
- ❌ Assumir que algo está pronto sem card em DONE

---

## 📏 CRITÉRIOS DE VISIBILIDADE

### Critério 1: Rastreabilidade 100%
**Definição:** Todo incremento (commit/PR/issue) referencia card.

**Como validar:**
1. Abrir card no GitHub Projects
2. Clicar em "Development" (seção de PRs/issues vinculados)
3. Verificar se há commits/PRs/issues referenciando

**Formato de referência:**
- `[CARD-XXX]` no título do commit/PR/issue
- `Refs #XXX` na descrição do commit/PR/issue
- `Closes #XXX` quando incremento conclui card

**Exemplo:**
```
[CARD-003] feat: integra Keychain para armazenamento seguro de API keys

Refs #3
```

**Proibições:**
- ❌ Commit sem referência ao card
- ❌ PR sem referência ao card
- ❌ Issue sem referência ao card

---

### Critério 2: Estado Binário
**Definição:** Estado do card é binário (está ou não está em coluna X).

**Como validar:**
1. Abrir GitHub Projects
2. Verificar se card está em exatamente 1 coluna (BACKLOG, TODO, DOING, BLOCKED, ou DONE)
3. Verificar se estado no YAML do arquivo Git bate com coluna do Kanban

**Proibições:**
- ❌ Card em múltiplas colunas
- ❌ Card "quase em DONE" (não existe "quase")
- ❌ Estado no Git diferente do estado no Kanban

---

### Critério 3: Bloqueio Documentado
**Definição:** Todo card em BLOCKED tem descrição do bloqueio + responsável pela resolução.

**Como validar:**
1. Abrir card em BLOCKED
2. Ler descrição do bloqueio
3. Verificar se responsável pela resolução está identificado

**Formato de descrição de bloqueio:**
```
**Bloqueio:** Keychain não está disponível no macOS Sandbox.
**Responsável pela resolução:** CEO (decisão sobre alternativa: usar arquivo criptografado ou aguardar suporte ao Keychain).
**Data do bloqueio:** 2026-01-10
```

**Proibições:**
- ❌ Card em BLOCKED sem descrição
- ❌ Card em BLOCKED sem responsável
- ❌ Card em BLOCKED por "falta de tempo" (não é bloqueio estrutural)

---

## 🚫 PROIBIÇÕES ABSOLUTAS

### Proibição 1: Status Verbal como Fonte de Verdade
❌ **Proibido:** Perguntar "o que você está fazendo?" ou "quanto falta?"  
✅ **Permitido:** Perguntar "por que o card está em BLOCKED?" (para clarificar bloqueio documentado)

**Razão:** Status verbal não é auditável, não é rastreável, não é fonte única de verdade.

---

### Proibição 2: Assumir Progresso sem Evidência
❌ **Proibido:** Assumir que algo está em execução sem card em DOING  
✅ **Permitido:** Assumir que algo está em execução SE card está em DOING + tem commits referenciando

**Razão:** Progresso sem evidência = status inventado (viola OD-009).

---

### Proibição 3: Aceitar Bloqueio sem Descrição
❌ **Proibido:** Card em BLOCKED sem descrição do bloqueio + responsável  
✅ **Permitido:** Card em BLOCKED com descrição completa (bloqueio + responsável + data)

**Razão:** Bloqueio sem descrição impede CEO de resolver (viola END da DEMANDA_MANUS-002).

---

### Proibição 4: Confiar em Estimativa Verbal
❌ **Proibido:** Aceitar "falta pouco" ou "quase pronto" como resposta  
✅ **Permitido:** Contar cards em TODO/DOING/BLOCKED para calcular progresso objetivo

**Razão:** Estimativa verbal é subjetiva, não é auditável, não é fonte única de verdade.

---

## 📋 CHECKLIST DE VISIBILIDADE (CEO)

**Antes de perguntar "o que está acontecendo?", CEO DEVE:**
- [ ] Abrir GitHub Projects
- [ ] Olhar coluna DOING (o que está em execução)
- [ ] Olhar coluna BLOCKED (o que está travado)
- [ ] Contar cards em TODO/DOING/BLOCKED (o que falta)
- [ ] Verificar se há cards sem evidência (commit/PR/issue)
- [ ] Verificar se há cards em BLOCKED sem descrição

**Se todas as perguntas forem respondidas em 30s → visibilidade está correta.**  
**Se alguma pergunta não puder ser respondida → sistema falhou (viola END da DEMANDA_MANUS-002).**

---

## 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/KANBAN_CANONICO.md` (definição de colunas, regras, automações)
- `/METODO/CONTRATO_ESTADOS.md` (quem move o quê, entrada/saída por papel)
- `/METODO/EXECUTION_MODEL.md` (modelo de execução: CEO autoriza, Manus especifica, Cursor executa)
- `/METODO/PILAR_ENDFIRST.md` (princípios fundacionais)
- `/METODO/ONTOLOGY_DECISIONS.md` (OD-009, OD-011)

---

**Versão:** 1.0  
**Data:** 10 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Mudança comportamental:** A partir deste commit, CEO não pergunta "o que está acontecendo?" — CEO abre GitHub Projects e vê em 30s.
