---
document_id: COMMIT_GOVERNANCE_CHECKLIST
type: operational
owner: Manus (Agent)
status: approved
approved_by: CEO
approved_at: 2026-01-08
governed_by: /METODO/ENDFIRST_DOCUMENT_GOVERNANCE.md
---

# Commit Governance Checklist

**Versão:** 1.3  
**Data:** 10 de Janeiro de 2026  
**Governado por:** ENDFIRST_DOCUMENT_GOVERNANCE.md  
**Status:** Operacional (Aprovado pelo CEO)

---

## 🎯 OBJETIVO

Este checklist **impede commits "quase conformes"** que passam tecnicamente mas quebram governança silenciosamente.

**Regra:**
> Todo commit que altera documentos governados DEVE passar por este checklist antes de ser considerado CONFORME.

---

## ✅ CHECKLIST OBRIGATÓRIO

Antes de considerar um commit **CONFORME com governança**, verifique:

### Verificações Básicas

- [ ] **Este commit altera documentos governados?**
  - Se SIM → Continuar checklist
  - Se NÃO → Checklist não se aplica

- [ ] **Isso exige disciplina humana para não dar errado? (OD-009)**
  - Se SIM → ❌ REJEITADO
  - Se NÃO → ✅ Pode seguir
  - Nota: Se a única defesa do processo é "as pessoas vão tomar cuidado", o processo está errado

- [ ] **Que comportamento pequeno muda agora por causa disso? (OD-011)**
  - Sem resposta concreta → ❌ REJEITADO
  - Se exigir disciplina humana → ❌ REJEITADO (OD-009)
  - Se mudança é "mais tarde" → ❌ REJEITADO
  - Se mudança é observável agora → ✅ Pode seguir
  - Nota: Se algo "faz sentido" mas não muda nada, é fuga sofisticada

- [ ] **Isso exige metacognição humana no caminho crítico? (OD-011 estendida)**
  - Se SIM → ❌ REJEITADO
  - Se NÃO → ✅ Pode seguir

- [ ] **APPROVAL_LOG.md foi atualizado NESTE commit?**
  - Aprovações devem estar no mesmo commit que as mudanças
  - Não pode haver commit de documentos sem atualização do log

- [ ] **Nenhuma entrada contém `commit: TBD`**
  - `TBD` é PROIBIDO (ver APPROVAL_LOG_RULES.md)
  - Toda entrada deve ter hash real

- [ ] **O hash deste commit aparece no APPROVAL_LOG.md**
  - Commits de aprovação devem referenciar a si mesmos
  - Rastreabilidade deve ser bidirecional

### Verificações de Consistência

- [ ] **A contagem total de documentos foi recalculada**
  - Contar arquivos .md no repositório
  - Atualizar estatísticas em APPROVAL_LOG.md
  - Total deve bater com realidade (não fantasma)

- [ ] **YAML frontmatter e APPROVAL_LOG estão sincronizados**
  - `status` no YAML = `status` no log
  - `approved_by` no YAML = `approved_by` no log
  - `approved_at` no YAML = `approved_at` no log
  - `governed_by` no YAML = `governed_by` no log

- [ ] **Justificativa de aprovação está explícita**
  - Coluna `reason` no APPROVAL_LOG preenchida
  - Justificativa é estrutural (não cosmética)
  - Motivo da aprovação é auditável

### Verificações de Rastreabilidade

- [ ] **Histórico de mudanças foi atualizado**
  - Evento registrado em APPROVAL_LOG.md
  - Data, evento e responsável preenchidos

- [ ] **Commits anteriores não foram alterados**
  - Não reescrever histórico (no rebase/force push)
  - Correções devem ser novos commits

---

## 📜 DECLARAÇÃO DE CONFORMIDADE

Após completar o checklist, declare:

**Status do commit:**
- [ ] ✅ **CONFORME** — Todos os itens verificados, commit pode ser considerado aprovado
- [ ] ❌ **NÃO CONFORME** — Um ou mais itens falharam, commit precisa de correção

---

## 🚫 REGRA DE BLOQUEIO

**Se este checklist não fecha → o commit NÃO pode ser considerado aprovado.**

Commits não conformes devem ser:
1. Corrigidos com novo commit (preferencial)
2. Ou revertidos (se impacto crítico)

**Nunca:**
- ❌ Ignorar checklist ("depois eu corrijo")
- ❌ Aprovar parcialmente ("quase conforme")
- ❌ Deixar TBD para "preencher depois"

---

## 🔄 QUANDO USAR ESTE CHECKLIST

**Use este checklist quando:**
- Criar novo documento governado
- Aprovar documento retroativamente
- Atualizar APPROVAL_LOG.md
- Corrigir metadados de documentos
- Fazer qualquer commit que afete governança

**Não use quando:**
- Commit não afeta documentos governados
- Mudanças são apenas de código (não docs)
- Commit é puramente técnico (build, config)

---

## 📊 EXEMPLO DE USO

### Cenário: Aprovar 3 documentos retroativamente

**Commit:** `178e186`

**Checklist:**
- [x] Altera documentos governados? → SIM (TEMPLATE_DEMANDA, DEMANDA_001)
- [x] APPROVAL_LOG atualizado? → SIM (no mesmo commit)
- [ ] Nenhum TBD? → ❌ NÃO (4 entradas com TBD)
- [ ] Hash aparece no log? → ❌ NÃO (TBD em vez de 178e186)
- [ ] Contagem recalculada? → ❌ NÃO (17 em vez de 14)
- [x] YAML sincronizado? → SIM
- [x] Justificativa explícita? → SIM

**Status:** ❌ NÃO CONFORME (3 itens falharam)

**Ação:** Criar commit de correção (`4b8957a`)

---

### Cenário: Commit de correção

**Commit:** `4b8957a`

**Checklist:**
- [x] Altera documentos governados? → SIM (APPROVAL_LOG.md)
- [x] APPROVAL_LOG atualizado? → SIM (corrige TBD e contagem)
- [x] Nenhum TBD? → SIM (todos substituídos por hashes)
- [x] Hash aparece no log? → SIM (4b8957a registrado)
- [x] Contagem recalculada? → SIM (14 documentos)
- [x] YAML sincronizado? → SIM
- [x] Justificativa explícita? → SIM

**Status:** ✅ CONFORME (todos os itens verificados)

---

## 🧠 POR QUE ESTE CHECKLIST EXISTE

**Problema identificado:**
- Commits passavam tecnicamente mas quebravam governança
- TBD, contagens fantasma, inconsistências silenciosas
- Correções retroativas frequentes

**Solução:**
- Checklist obrigatório antes de declarar conformidade
- Impede estados intermediários inválidos
- Torna governança autoexplicativa

**Resultado esperado:**
- ❌ TBD nunca mais aparece
- ❌ Contagem fantasma não acontece
- ✅ Governança vira verificável
- ✅ Novos colaboradores não quebram o sistema

---

## 📚 DOCUMENTOS RELACIONADOS

- **ENDFIRST_DOCUMENT_GOVERNANCE.md** — Governança canônica
- **APPROVAL_LOG.md** — Log de aprovações
- **APPROVAL_LOG_RULES.md** — Regras anti-TBD

---

**Versão:** 1.0  
**Criado:** 8 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Status:** Operacional
