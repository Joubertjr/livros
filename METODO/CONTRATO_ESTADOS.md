---
document_id: CONTRATO_ESTADOS
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-10
governed_by: /METODO/PILAR_ENDFIRST.md
---

# Contrato de Estados — Quem Move o Quê

**Versão:** 1.0  
**Data:** 10 de Janeiro de 2026  
**Tipo:** Operacional (Contrato de Responsabilidades)  
**Status:** Aprovado pelo CEO

---

## 🎯 OBJETIVO

Este documento define o **contrato de estados** do Kanban canônico: **quem move o quê**, **quando**, e **por quê**.

**Regra fundamental:**
> Cada papel (CEO/Manus/Cursor) tem autoridade exclusiva sobre movimentações específicas.  
> Ninguém move card fora da sua autoridade.

**Princípios aplicados:**
- **OD-009:** Processo > Disciplina (sistema impede erro por design)
- **OD-011:** Entendimento sem mudança é fuga (contrato muda comportamento agora)
- **ROLES_AND_RESPONSIBILITIES:** Papéis institucionais, não pessoais

---

## 👥 PAPÉIS E AUTORIDADES

### CEO (Joubert Jr)
**Autoridade:**
- Aprovar/rejeitar demandas (BACKLOG → TODO ou rejeitar)
- Priorizar demandas (reordenar TODO)
- Validar resultados (DONE → TODO se não atende END)
- Resolver bloqueios estratégicos (BLOCKED → TODO/DOING)

**Proibições:**
- ❌ Mover card de TODO → DOING (executor decide quando inicia)
- ❌ Mover card de DOING → DONE (executor declara conclusão)
- ❌ Criar demanda sem END explícito

---

### Manus (Agent)
**Autoridade:**
- Executar demandas de especificação/clareza (TODO → DOING → DONE)
- Documentar decisões ontológicas (criar ODs)
- Atualizar governança documental (APPROVAL_LOG, templates)
- Declarar bloqueio em demandas Manus (DOING → BLOCKED)

**Proibições:**
- ❌ Aprovar demandas (só CEO aprova)
- ❌ Executar código técnico de produtos (responsabilidade do Cursor)
- ❌ Mover card de outra pessoa sem autorização

---

### Cursor (Agent)
**Autoridade:**
- Executar demandas técnicas de produtos (TODO → DOING → DONE)
- Criar incrementos (commits, PRs, issues)
- Declarar bloqueio técnico (DOING → BLOCKED)
- Referenciar cards em todo incremento (obrigatório)

**Proibições:**
- ❌ Aprovar demandas (só CEO aprova)
- ❌ Alterar END ou critérios de aceitação (imutável durante execução)
- ❌ Mover card sem evidência no Git (commit/PR/issue)

---

## 🔄 TRANSIÇÕES DE ESTADO

### BACKLOG → TODO
**Quem move:** CEO  
**Quando:** Demanda aprovada e priorizada  
**Pré-condições:**
- Demanda tem END explícito
- Demanda tem critérios de aceitação
- Demanda tem executor designado
- Arquivo existe no Git (`/DEMANDAS/` ou `/DEMANDAS_MANUS/`)

**Pós-condições:**
- Status no YAML: `ready`
- Card está em TODO
- Executor sabe que pode iniciar

**Proibições:**
- ❌ Mover para TODO sem END explícito
- ❌ Mover para TODO sem executor designado

---

### TODO → DOING
**Quem move:** Executor (Manus ou Cursor)  
**Quando:** Executor inicia execução  
**Pré-condições:**
- Demanda está em TODO
- Executor tem clareza sobre END e critérios de aceitação
- Não há bloqueio conhecido

**Pós-condições:**
- Status no YAML: `in_progress`
- Card está em DOING
- Primeira evidência no Git (commit/PR/issue referenciando card)

**Proibições:**
- ❌ Mover para DOING sem primeira evidência no Git
- ❌ Mover para DOING sem entender END

---

### DOING → BLOCKED
**Quem move:** Executor (Manus ou Cursor)  
**Quando:** Bloqueio estrutural impede progresso  
**Pré-condições:**
- Card está em DOING
- Bloqueio é estrutural (não é "falta de tempo")
- Executor documenta bloqueio no card

**Pós-condições:**
- Card está em BLOCKED
- Descrição do bloqueio está no card
- Responsável pela resolução está identificado (CEO, Manus, Cursor, ou externo)

**Proibições:**
- ❌ Mover para BLOCKED sem descrição do bloqueio
- ❌ Mover para BLOCKED por "falta de tempo" (não é bloqueio estrutural)

---

### BLOCKED → TODO/DOING
**Quem move:** Responsável pela resolução (CEO, Manus, Cursor)  
**Quando:** Bloqueio resolvido  
**Pré-condições:**
- Bloqueio foi resolvido (decisão tomada, recurso disponível, dependência atendida)
- Executor confirma que pode prosseguir

**Pós-condições:**
- Card está em TODO (se precisa reiniciar) ou DOING (se continua)
- Descrição do bloqueio permanece no card (histórico)

**Proibições:**
- ❌ Mover para TODO/DOING sem resolver bloqueio
- ❌ Apagar descrição do bloqueio (histórico deve permanecer)

---

### DOING → DONE
**Quem move:** Executor (Manus ou Cursor)  
**Quando:** Todos os critérios de aceitação atingidos  
**Pré-condições:**
- Todos os critérios de aceitação atingidos
- Evidência final no Git (commits, PRs, documentos)
- Executor declara conclusão

**Pós-condições:**
- Status no YAML: `done`
- Card está em DONE
- CEO pode validar resultado (opcional: validação implícita)

**Proibições:**
- ❌ Mover para DONE sem evidência no Git
- ❌ Mover para DONE com critérios de aceitação não atingidos
- ❌ Mover para DONE "quase pronto" (não existe "quase DONE")

---

### DONE → TODO (Revalidação)
**Quem move:** CEO  
**Quando:** Resultado não atende END  
**Pré-condições:**
- CEO valida resultado
- Resultado não atende END ou critérios de aceitação
- CEO documenta motivo da rejeição

**Pós-condições:**
- Card está em TODO
- Motivo da rejeição está documentado no card
- Executor sabe o que precisa corrigir

**Proibições:**
- ❌ Rejeitar sem documentar motivo
- ❌ Rejeitar por "não gostei" (motivo deve ser objetivo)

---

## 📋 ENTRADA E SAÍDA POR PAPEL

### Cursor (Executor Técnico)

**Entrada (o que Cursor recebe):**
- Demanda em TODO com status `ready`
- END explícito documentado
- Critérios de aceitação congelados (imutável durante execução)
- Arquivo `/DEMANDAS/DEMANDA-XXX.md` no Git
- Arquivo `/DEMANDAS/DEMANDA-XXX_RESULT.md` (resultado esperado)
- Arquivo `/DEMANDAS/DEMANDA-XXX_ACCEPTANCE.md` (critérios do CEO)

**Saída (o que Cursor entrega):**
- Commits incrementais (cada commit referencia card)
- PRs (cada PR referencia card)
- Issues (cada issue referencia card)
- Evidência dos critérios de aceitação (testes, screenshots, logs)
- Card em DONE quando todos os critérios atingidos

**Proibições:**
- ❌ Iniciar execução sem END explícito
- ❌ Criar commit sem referenciar card
- ❌ Declarar DONE sem evidência dos critérios

---

### Manus (Executor de Especificação)

**Entrada (o que Manus recebe):**
- Demanda em TODO com status `ready`
- END explícito documentado
- Escopo definido (o que está dentro/fora)
- Arquivo `/DEMANDAS_MANUS/DEMANDA_MANUS-XXX.md` no Git

**Saída (o que Manus entrega):**
- Documentos Markdown governados (YAML frontmatter completo)
- Decisões ontológicas (ODs) se aplicável
- Atualizações de governança (APPROVAL_LOG, templates)
- Card em DONE quando todos os entregáveis criados e aprovados

**Proibições:**
- ❌ Criar documento sem YAML frontmatter
- ❌ Criar documento "que faz sentido" mas não muda comportamento (OD-011)
- ❌ Declarar DONE sem aprovação do CEO

---

### CEO (Aprovador e Validador)

**Entrada (o que CEO recebe):**
- Demanda em BACKLOG (para aprovar/rejeitar)
- Card em DONE (para validar resultado)
- Card em BLOCKED (para resolver bloqueio estratégico)

**Saída (o que CEO entrega):**
- Demanda aprovada (BACKLOG → TODO)
- Demanda rejeitada (BACKLOG → removida)
- Resultado validado (DONE permanece)
- Resultado rejeitado (DONE → TODO com motivo documentado)
- Bloqueio resolvido (BLOCKED → TODO/DOING)

**Proibições:**
- ❌ Aprovar demanda sem END explícito
- ❌ Rejeitar resultado sem documentar motivo
- ❌ Resolver bloqueio sem comunicar executor

---

## 🚫 PROIBIÇÕES ABSOLUTAS

### Proibição 1: Mover Card Fora da Autoridade
❌ **Proibido:** Manus mover card de Cursor, Cursor mover card de Manus, qualquer um aprovar demanda (só CEO aprova)  
✅ **Permitido:** Executor mover próprio card dentro das transições autorizadas

**Razão:** Autoridade é institucional, não pessoal. Cada papel tem responsabilidade exclusiva.

---

### Proibição 2: Mover Card sem Evidência
❌ **Proibido:** Mover de TODO → DOING sem primeira evidência no Git, mover de DOING → DONE sem evidência dos critérios  
✅ **Permitido:** Mover de BACKLOG → TODO sem evidência (ainda não iniciou)

**Razão:** Estado sem evidência = status inventado (viola OD-009).

---

### Proibição 3: Alterar END Durante Execução
❌ **Proibido:** Executor alterar END ou critérios de aceitação enquanto card está em DOING  
✅ **Permitido:** CEO alterar END (mas deve mover card para TODO e notificar executor)

**Razão:** END é contrato. Alterar END durante execução quebra rastreabilidade.

---

### Proibição 4: Status Verbal
❌ **Proibido:** Usar conversa humana para comunicar progresso ("estou trabalhando nisso", "quase pronto")  
✅ **Permitido:** Conversa para clarificar bloqueios (mas bloqueio deve estar documentado no card)

**Razão:** Status verbal não é auditável, não é rastreável, não é fonte única de verdade.

---

## 📏 CRITÉRIOS DE VALIDAÇÃO

**Este contrato está sendo seguido quando:**
- [ ] Nenhum card é movido fora da autoridade do papel
- [ ] Todo card em DOING tem evidência no Git (commit/PR/issue)
- [ ] Todo card em BLOCKED tem descrição do bloqueio + responsável
- [ ] Nenhum END é alterado durante execução sem mover card para TODO
- [ ] Status verbal é ignorado (Kanban é fonte única de verdade)

**Responsável pela validação:** CEO  
**Frequência:** Semanal (ou sempre que CEO abrir GitHub Projects)

---

## 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/KANBAN_CANONICO.md` (definição de colunas, regras, automações)
- `/METODO/INSTRUMENTACAO_VISIBILIDADE.md` (como CEO vê estado sem conversa)
- `/METODO/EXECUTION_MODEL.md` (modelo de execução: CEO autoriza, Manus especifica, Cursor executa)
- `/METODO/ROLES_AND_RESPONSIBILITIES.md` (papéis: CEO/Manus/Cursor)
- `/METODO/PILAR_ENDFIRST.md` (princípios fundacionais)

---

**Versão:** 1.0  
**Data:** 10 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Mudança comportamental:** A partir deste commit, ninguém move card fora da sua autoridade. Sistema impede erro por design.
