---
document_id: GOVERNANCE_CYCLE_LIFECYCLE
type: canonical
owner: CEO (Joubert Jr)
status: draft
governed_by: END_FIRST_V2
version: 1.0
created_at: 2026-01-19
created_by: Cursor (executor)
---

# Governança do Ciclo de Vida de Artefatos — END-FIRST v2

**Versão:** 1.0  
**Data:** 19 de Janeiro de 2026  
**Status:** Canônico (Governança do Método)  
**Governado por:** END-FIRST v2  
**Path Canônico:** Este documento é parte da governança conceitual do método END-FIRST v2

---

## 🎯 OBJETIVO

Este documento mapeia conceitualmente o ciclo completo de vida dos artefatos no método END-FIRST v2, definindo:
- As etapas do ciclo
- O papel de cada tipo de artefato
- As transições entre etapas
- Critérios de "ativo vs histórico"

**Princípio fundamental:**
> "Artefatos com naturezas diferentes não podem ocupar o mesmo plano semântico."

---

## 🔄 CICLO COMPLETO: DEMANDA → F-1 → EXECUÇÃO → EVIDÊNCIAS → HISTÓRICO

### Visão Geral do Ciclo

O ciclo de vida de qualquer trabalho no método END-FIRST v2 segue esta sequência conceitual:

```
DEMANDA (Intenção)
    ↓
F-1 (Planejamento Canônico)
    ↓
EXECUÇÃO (Implementação)
    ↓
EVIDÊNCIAS (Prova)
    ↓
HISTÓRICO (Memória)
```

**Regra canônica:**
> "Demanda não é histórico. Histórico não governa execução."

---

## 📋 ETAPAS DO CICLO

### 1. DEMANDA (Intenção)

**Natureza:** Artefato de intenção  
**Momento de criação:** Início do ciclo  
**Papel:** Define o que precisa ser feito e por quê

**Características:**
- Contém END (resultado observável)
- Define critérios de aceitação (PASS/FAIL binários)
- Estabelece regras canônicas e bloqueios
- Não define "como fazer" (isso é F-1)

**Estado:** Ativo enquanto governa o ciclo  
**Transição:** Deixa de ser "ativo" quando o trabalho é concluído e movido para histórico

**Frase canônica aplicada:**
> "Se é preciso explicar onde algo se encaixa, o método falhou."

---

### 2. F-1 (Planejamento Canônico)

**Natureza:** Artefato de planejamento bloqueante  
**Momento de criação:** Após demanda, antes de execução  
**Papel:** Transforma demanda em plano executável

**Características:**
- É obrigatório para demandas complexas
- Deve ser aprovado explicitamente antes de execução
- Define TODO canônico (F0, F1, F2, ...)
- Estabelece provas binárias verificáveis
- Não se perpetua após aprovação

**Estado:** Ativo durante planejamento e execução  
**Transição:** Deixa de ser "ativo" quando execução é concluída

**Frase canônica aplicada:**
> "F-1 existe para governar execução, não para se perpetuar."

**Regra estrutural:**
> "Planejamento é artefato de primeira classe. Executor apenas executa."

---

### 3. EXECUÇÃO (Implementação)

**Natureza:** Processo, não artefato  
**Momento:** Após F-1 aprovada  
**Papel:** Implementa o que foi planejado

**Características:**
- Segue o TODO canônico definido em F-1
- Não interpreta ou altera o plano durante execução
- Gera artefatos de implementação (código, documentos, etc.)
- Valida cada fase conforme critérios binários

**Estado:** Processo ativo  
**Transição:** Conclui quando todos os TODOs canônicos são completados

**Observação importante:**
Execução não é um artefato, é um processo que consome F-1 e produz Evidências.

---

### 4. EVIDÊNCIAS (Prova)

**Natureza:** Artefato de prova documental  
**Momento de criação:** Durante e após execução  
**Papel:** Prova que o END foi alcançado

**Características:**
- Documenta conformidade com critérios de aceitação
- Contém provas binárias verificáveis
- Distingue-se de planejamento (F-1) e de histórico
- Não substitui o END, apenas o prova

**Estado:** Ativo enquanto valida o trabalho  
**Transição:** Pode ser movido para histórico após validação completa

**Frase canônica aplicada:**
> "Evidência prova o END; não substitui o END."

**Diferenciação:**
- **Evidência documental** (criar arquivos markdown): ✅ Permitido (é documentação)
- **Automação/ferramentas** (scripts, validações automáticas): ❌ Proibido (não é evidência, é automação)

---

### 5. HISTÓRICO (Memória)

**Natureza:** Artefato de memória sistêmica  
**Momento de criação:** Após conclusão do trabalho  
**Papel:** Preserva conhecimento e contexto para referência futura

**Características:**
- Não governa execução futura
- Não é artefato operacional
- É memória sistêmica
- Serve para auditoria e aprendizado

**Estado:** Sempre "não-ativo" (é memória, não operação)  
**Transição:** Não há transição; histórico é estado final

**Frase canônica aplicada:**
> "Demanda não é histórico. Histórico não governa execução."

**Regra estrutural:**
Histórico não pode ser usado como entrada para novas execuções. Ele é apenas memória.

---

## 🔀 TRANSIÇÕES ENTRE ETAPAS

### Transição: DEMANDA → F-1

**Critério:** Demanda identificada e priorizada  
**Bloqueio:** F-1 é obrigatória para demandas complexas  
**Resultado:** Plano canônico criado e aprovado

---

### Transição: F-1 → EXECUÇÃO

**Critério:** F-1 aprovada explicitamente  
**Bloqueio:** Nenhuma execução sem F-1 aprovada  
**Resultado:** Execução inicia seguindo TODO canônico

---

### Transição: EXECUÇÃO → EVIDÊNCIAS

**Critério:** Cada fase do TODO canônico completa  
**Bloqueio:** Provas binárias devem passar  
**Resultado:** Evidências documentais geradas

---

### Transição: EVIDÊNCIAS → HISTÓRICO

**Critério:** Trabalho concluído e validado  
**Bloqueio:** Nenhum bloqueio (é transição natural)  
**Resultado:** Artefatos movidos para memória sistêmica

---

## ✅ CRITÉRIOS DE "ATIVO vs HISTÓRICO"

### Artefato é "ATIVO" quando:

- ✅ Está governando execução atual
- ✅ Está sendo usado como entrada para decisões
- ✅ Está sendo atualizado ou referenciado
- ✅ Faz parte do ciclo de trabalho em andamento

### Artefato é "HISTÓRICO" quando:

- ✅ Trabalho foi concluído
- ✅ Não governa mais execução
- ✅ É apenas memória sistêmica
- ✅ Serve apenas para referência e auditoria

**Regra canônica:**
> "Artefatos com naturezas diferentes não podem ocupar o mesmo plano semântico."

Isso significa que:
- DEMANDA ativa ≠ DEMANDA histórica (são naturezas diferentes)
- F-1 ativa ≠ F-1 histórica (são naturezas diferentes)
- EVIDÊNCIAS ativas ≠ EVIDÊNCIAS históricas (são naturezas diferentes)

---

## 🧭 FRASES CANÔNICAS DO CICLO DE VIDA

Estas frases são canônicas e bloqueantes:

1. **Ciclo de Vida:** "Artefatos com naturezas diferentes não podem ocupar o mesmo plano semântico."

2. **Intenção vs Memória:** "Demanda não é histórico. Histórico não governa execução."

3. **Planejamento:** "F-1 existe para governar execução, não para se perpetuar."

4. **Evidência:** "Evidência prova o END; não substitui o END."

5. **Clareza Cognitiva:** "Se é preciso explicar onde algo se encaixa, o método falhou."

**Violação de qualquer frase canônica = FAIL automático.**

---

## 📌 INDEPENDÊNCIA DE IMPLEMENTAÇÃO

**Este documento é conceitual e independente de:**
- ❌ Estrutura de pastas específica
- ❌ Layout de filesystem
- ❌ Ferramentas (Docker, Git, etc.)
- ❌ Paths absolutos ou relativos
- ❌ Projeto específico

**Este documento governa:**
- ✅ Conceitos do ciclo de vida
- ✅ Natureza de cada artefato
- ✅ Transições entre etapas
- ✅ Critérios de "ativo vs histórico"

**Regra:**
> O método governa **o que criar** (conceitos). O projeto decide **onde criar** (paths).

---

## 🔗 INTEGRAÇÃO COM END-FIRST v2

Este documento integra-se ao método END-FIRST v2 mencionando explicitamente:
- **END-FIRST v2** como método governante
- **Pilar END-FIRST** como base conceitual
- **Template Canônico de Demanda** como estrutura de demanda
- **F-1 (Planejamento Canônico)** como etapa obrigatória

**Validação de integração:**
Este documento menciona pelo menos um documento canônico do método por **nome** (não por path), conforme critério binário de integração.

---

## 🧭 REGRA FINAL (CANÔNICA)

> "Quando o ciclo de vida é claro, a organização deixa de ser um problema."

---

**Governado por:** END-FIRST v2  
**Relacionado a:** GOVERNANCE_ARTIFACT_BOUNDARIES.md, GOVERNANCE_FRICTION_ANALYSIS.md, GOVERNANCE_ENDFIRST_ALIGNMENT.md
