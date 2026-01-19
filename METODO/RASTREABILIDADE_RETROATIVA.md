---
document_id: RASTREABILIDADE_RETROATIVA
type: operational
owner: Manus (Agent)
status: approved
approved_by: CEO
approved_at: 2026-01-11
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.0
created_at: 2026-01-11
---

# RASTREABILIDADE RETROATIVA — Commits do Cursor

**Versão:** 1.0  
**Data:** 11 de Janeiro de 2026  
**Decisão do CEO:** 2026-01-11

---

## 🎯 CONTEXTO

**Situação:** Cursor executou 3 commits técnicos (bba18f6, b1909e9, 4da9497) antes da criação das regras de rastreabilidade Kanban (CURSOR_INSTRUCTIONS.md, Issue #8, tripla garantia A+B+C).

**Problema:** Commits não referenciam cards do GitHub Projects (`Refs #X`) e cards não foram movidos (TODO/DOING/DONE).

**Decisão do CEO:**
> "Os commits técnicos do Cursor são aceitos com ajuste de rastreabilidade, pois ocorreram antes do bloqueio estrutural. A tripla garantia está aprovada e torna esse tipo de erro impossível daqui pra frente."

---

## 📋 COMMITS AFETADOS

### 1. Commit `bba18f6` — Critério 1 (Envio para 1-4 LLMs)

**Mensagem original:**
```
docs(evidencias): prova do Critério 1 + decisão técnica temporária
```

**Rastreabilidade retroativa:**
- **Card associado:** #4 (INCREMENTO 3 - Envio simultâneo para múltiplas LLMs)
- **Critério atendido:** Critério 1 (Sistema executável + envio para 1-4 LLMs)
- **Status técnico:** ✅ APROVADO (checklist reprodutível, evidência válida)
- **Status de governança:** ⚠️ AJUSTADO (rastreabilidade adicionada retroativamente)

**Referência correta:**
```
Refs #4
```

---

### 2. Commit `b1909e9` — Critério 2 (Visualização Lado a Lado)

**Mensagem original:**
```
feat(ui): INCREMENTO 4 - layout lado a lado fixo (Critério 2)
```

**Rastreabilidade retroativa:**
- **Card associado:** #5 (INCREMENTO 4 - Seleção de melhor resposta + validação cruzada automática)
- **Critério atendido:** Critério 2 (Visualização lado a lado)
- **Nota:** Commit diz "INCREMENTO 4" mas card #5 é "INCREMENTO 4" (numeração correta)
- **Status técnico:** ✅ APROVADO (checklist reprodutível, layout implementado corretamente)
- **Status de governança:** ⚠️ AJUSTADO (rastreabilidade adicionada retroativamente)

**Referência correta:**
```
Refs #5
```

---

### 3. Commit `4da9497` — Critério 3 (Seleção de Melhor Resposta)

**Mensagem original:**
```
feat(ui): INCREMENTO 5 - seleção de melhor resposta (Critério 3)
```

**Rastreabilidade retroativa:**
- **Card associado:** #5 (INCREMENTO 4 - Seleção de melhor resposta + validação cruzada automática)
- **Critério atendido:** Critério 3 (Seleção de melhor resposta)
- **Nota:** Commit diz "INCREMENTO 5" mas card #5 é "INCREMENTO 4" (inconsistência de numeração)
- **Status técnico:** ✅ APROVADO (checklist reprodutível, múltiplos indicadores visuais)
- **Status de governança:** ⚠️ AJUSTADO (rastreabilidade adicionada retroativamente, numeração mantida como está)

**Referência correta:**
```
Refs #5
```

---

## 🔒 DECISÃO ESTRUTURAL

**Regra aplicada:** Não reescrever história. Corrigir rastreabilidade para frente.

**Motivo:**
- Commits já foram pushed
- Código e evidências técnicas estão corretos
- Violação de processo ocorreu ANTES do bloqueio estrutural (tripla garantia)
- Reescrever histórico (amend/rebase) é proibido após push

**Solução:**
- Criar documento de rastreabilidade retroativa (este arquivo)
- Atualizar cards no GitHub Projects para refletir estado real (DONE)
- Registrar exceção pré-regra

---

## 📊 ESTADO DOS CARDS (CORREÇÃO)

### Card #4 (INCREMENTO 3)
- **Título:** INCREMENTO 3 - Envio simultâneo para múltiplas LLMs
- **Status antes:** TODO
- **Status correto:** DONE
- **Motivo:** Commit `50d9023` (implementação) + `bba18f6` (evidência) existem
- **Ação:** Mover de TODO → DONE

### Card #5 (INCREMENTO 4)
- **Título:** INCREMENTO 4 - Seleção de melhor resposta + validação cruzada automática
- **Status antes:** TODO
- **Status correto:** DONE (parcial: Critério 2 + Critério 3 concluídos)
- **Motivo:** Commits `b1909e9` (layout lado a lado) + `4da9497` (seleção) existem
- **Ação:** Mover de TODO → DONE
- **Nota:** Validação cruzada automática (Critério 5) ainda não implementada

---

## ⚠️ EXCEÇÃO PRÉ-REGRA

**Declaração formal:**

Este documento registra uma **exceção pré-regra** para 3 commits do Cursor (bba18f6, b1909e9, 4da9497) que ocorreram ANTES da criação das regras de rastreabilidade Kanban.

**Condições da exceção:**
1. ✅ Código e evidências técnicas corretos
2. ✅ Critérios de aceitação atendidos
3. ✅ Checklist reprodutível por terceiros
4. ⚠️ Rastreabilidade ausente (corrigida retroativamente neste documento)
5. ⚠️ Cards não movidos (corrigidos após este documento)

**Lei ativa a partir de agora:**
- **Tripla garantia (A+B+C):** CURSOR_INSTRUCTIONS.md + PROMPT_CURSOR.md (stub) + Issue #8
- **Regra absoluta:** Todo commit DEVE referenciar card (`Refs #X`)
- **Fluxo obrigatório:** TODO → DOING (início) → DONE (fim)
- **Sem exceções futuras:** Cursor não pode alegar desconhecimento

---

## 🔒 LEI OPERACIONAL (ATIVA)

**Frase canônica:**
> "Cursor não executa sem card. Manus não executa sem demanda. CEO não cria card. O sistema impede atalhos por design."

**Contratos:**
- **Cursor:** "Sem card, eu não executo. Mesmo que pareça óbvio."
- **Manus:** "Sem DEMANDA_MANUS e card, eu não trabalho."
- **CEO:** "Eu decido. Eu não opero Kanban."

**Fluxo único:**
```
DEMANDA → CARD → EXECUÇÃO → EVIDÊNCIA → JULGAMENTO
```

**Proibido:**
- ❌ "Já que estou aqui..."
- ❌ "Bug pequeno"
- ❌ Execução invisível
- ❌ Status narrativo

---

## 📜 DECLARAÇÃO DO CEO (REGISTRADA)

> "Os commits técnicos do Cursor são aceitos com ajuste de rastreabilidade, pois ocorreram antes do bloqueio estrutural. A tripla garantia está aprovada e torna esse tipo de erro impossível daqui pra frente."

**Data:** 2026-01-11  
**Decisão:** ACEITO COM AJUSTE (sem reverter código)

---

**Governado por:** `/METODO/PILAR_ENDFIRST.md`  
**Path Canônico:** `/METODO/RASTREABILIDADE_RETROATIVA.md`
