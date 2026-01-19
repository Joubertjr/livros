---
document_id: KANBAN_CANONICO
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-10
governed_by: /METODO/PILAR_ENDFIRST.md
---

# Kanban Canônico — Visibilidade sem Conversa

**Versão:** 1.0  
**Data:** 10 de Janeiro de 2026  
**Tipo:** Operacional (Processo de Visibilidade)  
**Status:** Aprovado pelo CEO

---

## 🎯 OBJETIVO

Este documento define o **Kanban canônico** do ENDFIRST Ecosystem: um sistema de visibilidade que **elimina conversa humana** como fonte de verdade sobre "o que está acontecendo".

**Regra fundamental:**
> Se não está visível no Kanban canônico, não está acontecendo.  
> Status verbal passa a ser ruído.

**Princípios aplicados:**
- **END FIRST:** Kanban serve ao resultado, não o contrário
- **OD-009:** Processo > Disciplina (sistema impede erro por design)
- **OD-011:** Entendimento sem mudança é fuga (Kanban muda comportamento agora)

---

## 📊 COLUNAS CANÔNICAS

O Kanban canônico possui **5 colunas obrigatórias** e **0 colunas opcionais**.

### 1. BACKLOG
**Definição:** Demandas que ainda não têm END explícito ou não foram priorizadas pelo CEO.

**Entrada:**
- Demanda criada no Git (`/DEMANDAS/` ou `/DEMANDAS_MANUS/`)
- Status no YAML: `draft` ou `ready`
- Sem aprovação formal do CEO

**Saída:**
- CEO aprova demanda (status → `ready`)
- CEO prioriza demanda (move para TODO)

**Responsável por mover:** CEO

**Proibições:**
- ❌ Demanda sem END explícito
- ❌ Demanda sem arquivo no Git
- ❌ Demanda "verbal" ou "em conversa"

---

### 2. TODO
**Definição:** Demandas aprovadas e priorizadas, aguardando início de execução.

**Entrada:**
- Demanda com status `ready` no Git
- END explícito documentado
- Critérios de aceitação definidos pelo CEO
- Executor designado (Cursor ou Manus)

**Saída:**
- Executor inicia execução (move para DOING)
- Primeira evidência de progresso (commit, issue, PR)

**Responsável por mover:** Executor (Cursor ou Manus)

**Proibições:**
- ❌ Demanda sem critérios de aceitação
- ❌ Demanda sem executor designado
- ❌ Demanda "quase pronta para começar"

---

### 3. DOING
**Definição:** Demandas em execução ativa, com evidência de progresso no Git.

**Entrada:**
- Executor iniciou execução
- Primeira evidência no Git (commit, issue, PR referenciando card)
- Status no YAML: `in_progress`

**Saída:**
- Todos os critérios de aceitação atingidos
- Evidência final no Git (commits, PRs, documentos)
- Executor declara conclusão (move para DONE)

**Responsável por mover:** Executor (Cursor ou Manus)

**Proibições:**
- ❌ Card em DOING sem commit/PR/issue referenciando
- ❌ Card em DOING há mais de 7 dias sem atualização (move para BLOCKED)
- ❌ Card em DOING com status verbal "quase pronto"

**Regra de rastreabilidade:**
> Todo incremento (commit/PR/issue) DEVE referenciar o card.  
> Formato: `[CARD-XXX]` ou `Refs #XXX` no título/descrição.

---

### 4. BLOCKED
**Definição:** Demandas com impedimento estrutural que impede progresso.

**Entrada:**
- Executor identifica bloqueio (dependência externa, decisão do CEO, recurso indisponível)
- Executor documenta bloqueio no card (descrição + label)
- Executor move para BLOCKED

**Saída:**
- Bloqueio resolvido (decisão do CEO, recurso disponível, dependência atendida)
- Responsável pela resolução move para TODO ou DOING

**Responsável por mover:**
- **Para BLOCKED:** Executor (Cursor ou Manus)
- **Para TODO/DOING:** CEO ou responsável pela resolução

**Proibições:**
- ❌ Card em BLOCKED sem descrição do bloqueio
- ❌ Card em BLOCKED sem responsável pela resolução
- ❌ Card em BLOCKED por "falta de tempo" (não é bloqueio estrutural)

**Regra de visibilidade:**
> CEO DEVE ver em 30s: o que está bloqueado e por quê.  
> Bloqueio sem descrição = card inválido.

---

### 5. DONE
**Definição:** Demandas concluídas, com todos os critérios de aceitação atingidos e validadas pelo CEO.

**Entrada:**
- Todos os critérios de aceitação atingidos
- Evidência final no Git (commits, PRs, documentos)
- Executor declara conclusão
- CEO valida resultado (opcional: pode ser validação implícita)

**Saída:**
- Não há saída (DONE é estado final)

**Responsável por mover:** Executor (Cursor ou Manus) + validação do CEO

**Proibições:**
- ❌ Card em DONE sem evidência no Git
- ❌ Card em DONE com critérios de aceitação não atingidos
- ❌ Card em DONE "quase pronto" (não existe "quase DONE")

**Regra de validação:**
> CEO pode mover de DONE para TODO se resultado não atende END.  
> Isso não é "retrabalho" — é validação estrutural.

---

## 🤖 AUTOMAÇÕES ESTRUTURAIS

### Automação 1: Rastreabilidade Obrigatória
**Gatilho:** Commit/PR/Issue criado  
**Ação:** Verificar se referencia card (`[CARD-XXX]` ou `Refs #XXX`)  
**Falha:** Bloquear merge/push até referência ser adicionada

**Implementação:** GitHub Actions (futuro) ou validação manual (agora)

---

### Automação 2: Detecção de Estagnação
**Gatilho:** Card em DOING há mais de 7 dias sem atualização  
**Ação:** Mover para BLOCKED automaticamente + notificar executor  
**Falha:** N/A (automação preventiva)

**Implementação:** GitHub Actions (futuro) ou revisão manual semanal (agora)

---

### Automação 3: Sincronização de Status
**Gatilho:** Status no YAML do arquivo Git muda  
**Ação:** Atualizar card no Kanban automaticamente  
**Falha:** Alertar inconsistência (status no Git ≠ status no Kanban)

**Implementação:** GitHub Actions (futuro) ou atualização manual (agora)

---

## 🚫 PROIBIÇÕES ABSOLUTAS

### Proibição 1: Status Inventado
❌ **Proibido:** Criar colunas além das 5 canônicas (BACKLOG/TODO/DOING/BLOCKED/DONE)  
✅ **Permitido:** Usar labels para contexto adicional (ex: `priority:high`, `type:bug`)

**Razão:** Colunas extras criam ambiguidade ("Em Revisão" = DOING ou DONE?)

---

### Proibição 2: Status Verbal
❌ **Proibido:** Usar conversa humana como fonte de verdade sobre progresso  
✅ **Permitido:** Conversa para clarificar bloqueios (mas bloqueio deve estar documentado no card)

**Razão:** Status verbal não é auditável, não é rastreável, não é fonte única de verdade.

---

### Proibição 3: Card sem Evidência
❌ **Proibido:** Card em DOING sem commit/PR/issue referenciando  
✅ **Permitido:** Card em TODO sem evidência (ainda não iniciou)

**Razão:** DOING sem evidência = status inventado.

---

### Proibição 4: Dependência de Disciplina
❌ **Proibido:** Processo que depende de "lembrar de atualizar Kanban"  
✅ **Permitido:** Processo que impede merge/push sem referência ao card

**Razão:** OD-009 (disciplina humana é falha de design).

---

## 📏 CRITÉRIOS DE VALIDAÇÃO

**Este Kanban está correto quando:**
- [ ] CEO abre GitHub Projects e em 30s sabe: o que está em execução, o que está bloqueado, o que falta
- [ ] Todo card em DOING tem commit/PR/issue referenciando
- [ ] Todo card em BLOCKED tem descrição do bloqueio + responsável pela resolução
- [ ] Nenhum card está em coluna inventada (além das 5 canônicas)
- [ ] Status verbal é ignorado (Kanban é fonte única de verdade)

**Responsável pela validação:** CEO  
**Frequência:** Semanal (ou sempre que CEO abrir GitHub Projects)

---

## 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/CONTRATO_ESTADOS.md` (quem move o quê, entrada/saída por papel)
- `/METODO/INSTRUMENTACAO_VISIBILIDADE.md` (como CEO vê estado sem conversa)
- `/METODO/EXECUTION_MODEL.md` (modelo de execução: CEO autoriza, Manus especifica, Cursor executa)
- `/METODO/PILAR_ENDFIRST.md` (princípios fundacionais)
- `/METODO/ONTOLOGY_DECISIONS.md` (OD-009, OD-011)

---

**Versão:** 1.0  
**Data:** 10 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Declaração do CEO:** "A partir deste commit, 'o que está acontecendo' não é mais uma pergunta. Se não está visível no Kanban canônico, não está acontecendo. Status verbal passa a ser ruído."
