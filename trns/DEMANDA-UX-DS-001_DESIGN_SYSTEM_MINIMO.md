---
demanda_id: DEMANDA-UX-DS-001
title: Design System Mínimo + Component Library (Anti-Retrabalho)
type: UX
altera_funcionalidade: sim
exige_f1: sim
status: backlog
created_at: 2026-01-19
created_by: CEO (Joubert Jr)
executor: Cursor
---

# DEMANDA-UX-DS-001 — DESIGN SYSTEM MÍNIMO + COMPONENT LIBRARY (Anti-Retrabalho)

**Tipo:** Infra de UI / UX Sistêmica  
**Método:** END-FIRST v2  
**Status:** BACKLOG (NÃO EXECUTAR)  
**Sistema:** CoverageSummarizer / livros  
**Projeto:** https://github.com/Joubertjr/livros

⸻

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para qualquer tela do produto (incluindo CoverageSummarizer):**
- Existe um Design System mínimo no repo com:
  - Tokens de spacing, tipografia, cores (incluindo estados), radius e sombras
  - Regras explícitas de uso ("não inventar valores soltos")
- Existe uma biblioteca de componentes base reutilizáveis:
  - Button, Input, Card, Badge/Tag de status, Alert, Progress, Accordion/Collapse, Table/List
- Qualquer nova UI passa a ser composição de componentes, não CSS ad-hoc
- UI final fica consistente e previsível (reduz "atrito de UI" e retrabalho)
- O sistema continua respeitando as regras canônicas:
  - Scroll interno proibido
  - Legibilidade imediata
  - Sem ruído técnico para usuário final
  - Progresso perceptível

**⚠️ Importante:**
Este END NÃO exige "ficar bonito"; exige consistência sistêmica.

**Resultado esperado do sistema:**

> UI consistente e previsível através de Design System mínimo e biblioteca de componentes reutilizáveis, eliminando retrabalho e decisões subjetivas por tela.

⸻

## 🚫 Regras Canônicas

**Design System:**
> "Sem tokens, todo pixel vira debate."

**Composição:**
> "Tela não é CSS novo: tela é composição."

**Consistência:**
> "Consistência remove opinião do loop."

**Valores:**
> "Se um valor foi inventado 'no olho', o método falhou."

**Scroll (GLOBAL):**
> "Scroll interno é PROIBIDO. Conteúdo invisível ou cortado é BUG estrutural."

**Legibilidade (GLOBAL):**
> "Se o usuário não vê o conteúdo imediatamente, o produto falhou."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

⸻

## ✅ Critérios de Aceitação (Binários)

### PASS

- ✅ Tokens definidos e usados (spacing/typo/colors/radius/shadow)
- ✅ Componentes base existem e são reutilizados
- ✅ Nenhum valor "mágico" fora dos tokens nos componentes/telas alteradas
- ✅ Estados (hover/focus/disabled/loading/error/success) definidos nos componentes
- ✅ UI final fica consistente e previsível
- ✅ Nova UI é composição de componentes, não CSS ad-hoc
- ✅ Gate Z11 permanece PASS
- ✅ Gate Z12 permanece PASS (se aplicável)
- ✅ Gate Z13 aplicável e satisfazível (UI/UX sistêmica)
- ✅ Evidência gerada (prints ou doc em `/EVIDENCIAS/ux/`)
- ✅ Nenhuma regressão funcional (Z0–Z11 continuam PASS)

### FAIL (AUTOMÁTICO)

- ❌ Componentes criados mas telas continuam "CSS solto"
- ❌ Tokens existem mas não são usados
- ❌ Valores mágicos espalhados
- ❌ Inconsistência entre botões/cards/inputs
- ❌ Regressão em Z11/Z12/Z13
- ❌ Scroll interno reaparece
- ❌ UX alterada sem F-1 aprovada
- ❌ Qualquer regressão funcional
- ❌ Gate Z11 quebrado
- ❌ Correção aplicada direto no código sem planejamento

⸻

## 🧠 Problemas Observados (Evidência — Não São Tarefas)

**Contexto (não tarefas):**

Problema real observado: retrabalho e fricção ao refinar UI, porque cada tela vira decisão subjetiva.

**Causa raiz identificada:**

> UI atual depende de decisões subjetivas por tela, gerando retrabalho e inconsistência. Falta contrato técnico reutilizável (Design System + Component Library).

**Isso impede:**
- Evolução rápida de UI
- Consistência visual
- Redução de retrabalho
- Escalabilidade de novas telas

⸻

## 🚫 DO / DON'T

### DO (fazer)

- ✅ Criar tokens e impor uso
- ✅ Criar componentes base reutilizáveis
- ✅ Priorizar acessibilidade (focus visível, contraste mínimo, navegação teclado)
- ✅ Auditar telas existentes para migrar minimamente
- ✅ Manter todos os gates PASS
- ✅ Manter regras canônicas de UX (scroll interno proibido, legibilidade imediata)

### DON'T (não fazer)

- ❌ Redesenhar produto inteiro
- ❌ Refatorar backend
- ❌ Criar 20 variações de botão
- ❌ Inserir scroll interno em qualquer lugar
- ❌ Alterar pipeline de sumarização
- ❌ "Simplificar" removendo garantias
- ❌ Quebrar Gate Z11

⸻

## 🧱 Bloqueios Estruturais

- 🔒 F-1 obrigatório (demanda de UX sistêmica complexa)
- 🔒 Gate Z11 continua bloqueante
- 🔒 Gate Z12 continua bloqueante (se aplicável)
- 🔒 Gate Z13 aplicável e bloqueante (UI/UX sistêmica)
- 🔒 Nenhuma alteração sem evidência visual
- 🔒 Scroll interno = BUG estrutural (não negociável)
- 🔒 Tokens devem ser impostos, não opcionais

⸻

## 📋 TODO Canônico (Somente Após F-1 Aprovada)

1. F-1: Planejamento Canônico (Design System + Component Library)
2. Definir tokens (spacing/typo/colors/radius/shadow)
3. Definir componentes base (lista mínima: Button, Input, Card, Badge, Alert, Progress, Accordion, Table)
4. Implementar componentes com tokens
5. Migrar 1 tela piloto (CoverageSummarizer) para composição
6. Auditar telas existentes para migração mínima
7. Garantir ausência total de scroll interno
8. Gerar evidência antes/depois (prints ou doc)
9. Validar Gate Z11
10. Validar Gate Z12 (se aplicável)
11. Validar Gate Z13 (UI/UX sistêmica)
12. Validar suite verde (pytest -q = 0 failed)
13. Declarar PASS

⸻

## ❌ Fora de Escopo

**Esta demanda NÃO inclui:**

- ❌ Design "bonito" subjetivo
- ❌ Novas features de produto
- ❌ Performance
- ❌ Mudanças de pipeline
- ❌ Redesign completo do produto
- ❌ 20 variações de cada componente
- ❌ Refatorações estruturais do backend

⸻

## 📌 Status

**BACKLOG (NÃO EXECUTAR)**

Este arquivo não autoriza execução. Só pode ser executado após:
- Priorização explícita
- F-1 aprovada
- Ordem clara do CEO

⸻

## 🧭 Regra Final (Canônica)

> "Sem biblioteca de componentes, UI vira retrabalho infinito."

⸻

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Path Canônico:** `/DEMANDAS/DEMANDA-UX-DS-001_DESIGN_SYSTEM_MINIMO.md`  
**Template:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`
