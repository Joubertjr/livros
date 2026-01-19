---
document_id: END_FIRST_V2
type: canonical
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-19
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.1
created_at: 2026-01-19
---

# END-FIRST v2 — Planejamento como Artefato Canônico

**Versão:** 1.0  
**Data:** 19 de Janeiro de 2026  
**Status:** Canônico (Evolução do Método)  
**Autoria:** CEO (Joubert Jr) + Manus AI  
**Path Canônico:** `/METODO/END_FIRST_V2.md`

---

## 🎯 O QUE É END-FIRST v2

END-FIRST v2 é a **evolução canônica** do método END-FIRST que introduz **F-1 (Planejamento Canônico)** como estágio obrigatório e bloqueante antes de qualquer execução.

**Princípio fundamental:**
> "Planejamento é artefato de primeira classe. Executor apenas executa."

---

## 🔥 POR QUE END-FIRST v2 EXISTE

### Problema Observado (Evidência Empírica)

Durante a execução real de um projeto complexo, foi observado **retrabalho sistemático** entre:
- Arquiteto (humano)
- Executor (Cursor)
- Validações manuais repetidas

**O problema não foi:**
- ❌ Técnico
- ❌ Qualidade de código
- ❌ Execução do Cursor

**A causa raiz foi metodológica:**

O método END-FIRST atual **não trata planejamento como artefato canônico governado**, o que gera:
- Interpretação durante execução
- Endurecimento tardio de regras
- Ciclos repetidos de validação
- Overhead cognitivo e operacional

---

### Diagnóstico (Causa Raiz)

O método END-FIRST atualmente:
- Assume que "planejar" ≈ "executar"
- Não exige aprovação explícita do plano
- Não diferencia planejamento, TODO e execução
- Permite que o executor interprete regras durante a execução

**👉 Isso não escala sob carga real.**

---

## 🔒 F-1 — PLANEJAMENTO CANÔNICO (BLOQUEANTE)

### Definição

**F-1** é o estágio obrigatório de **Planejamento Canônico** que deve ser concluído e aprovado antes de qualquer execução.

**Função:**
- Transformar demanda em plano executável
- Eliminar interpretação durante execução
- Estabilizar arquitetura e governança antes de código

---

### END (Resultado Esperado de F-1)

Ao final de F-1, devem existir:

- ✅ **1 documento único de planejamento canônico**
- ✅ **1 TODO canônico derivado do plano**
- ✅ **Escopo DO / DON'T explícito**
- ✅ **Ordem de execução explícita**
- ✅ **Critérios de FAIL explícitos**
- ✅ **Strings de prova definidas** (quando aplicável)

---

### DONE WHEN (Critérios de Conclusão)

F-1 está concluída quando:

- ✅ Declaração explícita no relatório: **"F-1 aprovada"**
- ✅ Nenhum comando foi executado
- ✅ Nenhum código foi alterado
- ✅ Plano foi aprovado pelo CEO ou arquiteto responsável

---

### PROIBIÇÕES (FAIL Automático)

Durante F-1, é **estritamente proibido:**

- ❌ Executar comandos
- ❌ Criar código
- ❌ Criar automações
- ❌ "Validar rapidamente"
- ❌ Interpretar regras durante execução

**Frase canônica:**
> "F-1 é planejamento, não execução. Executar durante F-1 é FAIL automático."

---

## 🧱 REGRA GLOBAL (CANÔNICA)

> **"Planejamento é artefato de primeira classe."**

**Implicações:**

- O executor (Cursor) **apenas executa**
- Arquitetura, governança e escopo **só existem antes da F-1 aprovada**
- Interpretação acontece **durante planejamento**, não durante execução
- Retrabalho de validação é **eliminado por design**

---

## 📊 QUANDO F-1 É OBRIGATÓRIO

### F-1 é obrigatório para:

- ✅ Projetos complexos (múltiplos arquivos, múltiplas etapas)
- ✅ Mudanças estruturais no método
- ✅ Implementação de novos produtos
- ✅ Demandas com dependências entre etapas
- ✅ Demandas com critérios de FAIL não triviais

### F-1 é opcional para:

- ❌ Demandas simples (1 arquivo, 1 etapa, escopo claro)
- ❌ Correções triviais (typo, formatação)
- ❌ Atualizações de documentação sem impacto estrutural

**Regra de decisão:**
> Se há dúvida se F-1 é necessário, F-1 é necessário.

---

## 🔄 FLUXO END-FIRST v2

### Fluxo Completo (com F-1)

```
DEMANDA → F-1 (Planejamento) → APROVAÇÃO → CARD → EXECUÇÃO → EVIDÊNCIA → JULGAMENTO
```

### Detalhamento de F-1

1. **Input:** DEMANDA com END explícito
2. **Processo:**
   - Criar documento de planejamento
   - Definir TODO canônico
   - Definir escopo DO / DON'T
   - Definir ordem de execução
   - Definir critérios de FAIL
   - Definir strings de prova (se aplicável)
3. **Output:** Plano aprovado com declaração "F-1 aprovada"
4. **Bloqueio:** Execução só inicia após aprovação explícita

---

## 📦 ESTRUTURA DO DOCUMENTO DE PLANEJAMENTO (F-1)

### Template Mínimo

```markdown
# PLANEJAMENTO CANÔNICO — [NOME DA DEMANDA]

## END (da demanda original)
[Copiar END da demanda]

## TODO CANÔNICO
- [ ] Etapa 1: [descrição objetiva]
- [ ] Etapa 2: [descrição objetiva]
- [ ] Etapa N: [descrição objetiva]

## ESCOPO

### DO (fazer)
- ✅ [ação 1]
- ✅ [ação 2]

### DON'T (não fazer)
- ❌ [ação proibida 1]
- ❌ [ação proibida 2]

## ORDEM DE EXECUÇÃO
1. [Etapa 1]
2. [Etapa 2]
3. [Etapa N]

## CRITÉRIOS DE FAIL
- ❌ [condição que invalida execução]
- ❌ [condição que invalida execução]

## STRINGS DE PROVA (quando aplicável)
- `[string esperada no output]`
- `[string esperada no log]`

## APROVAÇÃO
**Status:** [PENDENTE / APROVADO]
**Aprovado por:** [nome]
**Data:** [YYYY-MM-DD]

**Declaração:** "F-1 aprovada"
```

---

## 🎯 IMPACTO ESPERADO

Após END-FIRST v2:

- ✅ **Zero retrabalho de validação**
- ✅ **Zero interpretação durante execução**
- ✅ **Cursor atua como executor literal**
- ✅ **Arquitetura e governança ficam estáveis**
- ✅ **Redução drástica de overhead cognitivo**
- ✅ **Método passa a escalar para projetos complexos**

---

## 🧠 INTEGRAÇÃO COM MÉTODO ATUAL

### Relação com ODs Existentes

**OD-007 (END é pré-condição absoluta)**
- F-1 **reforça** OD-007: planejamento tem END próprio

**OD-009 (Processo > Disciplina)**
- F-1 **implementa** OD-009: bloqueio estrutural elimina dependência de "lembrar de planejar"

**OD-010 (RESULT é primeira classe)**
- F-1 **aplica** OD-010: planejamento é resultado verificável, não processo

**OD-011 (Metacognição fora do caminho crítico)**
- F-1 **resolve** OD-011: interpretação acontece em F-1, não durante execução

**OD-012 (nova):** Planejamento é artefato de primeira classe
- F-1 **cristaliza** OD-012: planejamento tem END, DONE WHEN, FAIL

---

### Relação com Pilar ENDFIRST

END-FIRST v2 **não substitui** o Pilar ENDFIRST.

**Pilar ENDFIRST:**
- Transforma intenção difusa → resultado explícito (ENDFIRST_SPEC)
- Ritual de 6 perguntas + 11 bloqueios

**END-FIRST v2 (F-1):**
- Transforma demanda → plano executável
- Bloqueio antes de execução

**Relação:**
```
Pilar ENDFIRST → DEMANDA → F-1 (Planejamento) → EXECUÇÃO
```

---

## 📌 EXEMPLOS PRÁTICOS

### Exemplo 1: Demanda Simples (F-1 opcional)

**DEMANDA:** Corrigir typo em README.md

**Análise:**
- 1 arquivo
- 1 etapa
- Escopo trivial
- Sem dependências

**Decisão:** F-1 não necessário (fluxo direto: DEMANDA → CARD → EXECUÇÃO)

---

### Exemplo 2: Demanda Complexa (F-1 obrigatório)

**DEMANDA:** Implementar END-FIRST v2

**Análise:**
- 5 documentos impactados
- Múltiplas etapas
- Escopo complexo
- Dependências entre documentos

**Decisão:** F-1 obrigatório

**F-1 criado:**
- TODO canônico com 5 etapas
- Escopo DO/DON'T explícito
- Ordem de execução definida
- Critérios de FAIL listados
- Aprovação explícita: "F-1 aprovada"

---

## 🚨 BLOQUEIOS E VALIDAÇÕES

### Bloqueio Estrutural

**Cursor (executor) deve verificar:**
1. Demanda é complexa?
2. Existe documento de F-1?
3. F-1 foi aprovado? (declaração "F-1 aprovada")

**Se F-1 é necessário e não existe:**
> "Esta demanda requer F-1 (Planejamento Canônico). Sem F-1 aprovada, não posso executar."

---

### Validação de F-1

**Checklist de aprovação:**
- [ ] TODO canônico existe
- [ ] Escopo DO/DON'T explícito
- [ ] Ordem de execução definida
- [ ] Critérios de FAIL listados
- [ ] Nenhum comando foi executado durante F-1
- [ ] Nenhum código foi criado durante F-1
- [ ] Declaração "F-1 aprovada" presente

---

## 📜 EVIDÊNCIA

Esta evolução nasce de **uso real do método**, com múltiplos ciclos de retrabalho documentados durante:
- Endurecimento tardio de regras
- Redefinição de escopo
- Validações repetidas

**Não é opinião. É evidência empírica.**

---

## 🎯 FRASE CANÔNICA

> **"Planejamento é artefato de primeira classe. Executor apenas executa."**

---

## 📝 TEMPLATE CANÔNICO DE DEMANDA

### Relação entre F-1 e Template Canônico

**Template Canônico de Demanda:**
- Define estrutura obrigatória de toda demanda
- 11 seções obrigatórias
- Frases canônicas explícitas
- Regra de UX canônica (scroll interno proibido)

**F-1 (Planejamento Canônico):**
- Transforma demanda (já no template) em plano executável
- Obrigatório para demandas complexas
- Opcional para demandas simples

**Fluxo completo:**
```
Demanda (Template Canônico) → F-1 (Planejamento) → Execução
```

### Bloqueio Estrutural

**Regra:**
> Demandas fora do template são FAIL estrutural.

**Bloqueios:**
- 🔒 Manus não aceita demandas fora do template
- 🔒 Cursor não executa demandas fora do template
- 🔒 CEO não revisa demandas que não sigam o template

**Documento canônico:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`

---

## 📜 DECLARAÇÃO DO CEO

Reconheço esta evolução como canônica e obrigatória para o método ENDFIRST.

END-FIRST v2 passa a governar:
- Execução de demandas complexas
- Separação entre planejamento e execução
- Bloqueio estrutural de interpretação durante execução

**Status:** CANÔNICO  
**Aplicação:** Imediata para demandas complexas  
**Versão:** 1.1

**Histórico de mudanças:**
- v1.0 (2026-01-19): Versão inicial (F-1 Planejamento Canônico)
- v1.1 (2026-01-19): Adicionada seção Template Canônico de Demanda

---

**Governado por:** `/METODO/PILAR_ENDFIRST.md`  
**Path Canônico:** `/METODO/END_FIRST_V2.md`  
**Refs:** #12
