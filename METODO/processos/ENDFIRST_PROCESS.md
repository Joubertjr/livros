---
document_id: ENDFIRST_PROCESS
type: operational
owner: Manus (Agent)
status: approved
approved_by: CEO
approved_at: 2026-01-07
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.0
created_at: 2026-01-07
---

# ENDFIRST_PROCESS — Processo Humano de 30 Segundos

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Status:** Operacional  
**Governado por:** `/METODO/PILAR_ENDFIRST.md`  
**Path Canônico:** `/METODO/processos/ENDFIRST_PROCESS.md`

---

## 🎯 Objetivo

Este documento define o **processo humano mínimo** para aplicar o Pilar ENDFIRST em qualquer conversa, reunião ou demanda.

**Tempo esperado:** 30 segundos para iniciar, 5-15 minutos para completar v0.

---

## 🚀 Regra de Comunicação (2 Linhas)

Quando alguém te pedir algo, você responde assim:

### 1️⃣ "Beleza — vou passar isso pelo Pilar ENDFIRST."
### 2️⃣ "Me diga só a entrada bruta (sem solução)."

E você cola a entrada bruta no template, sem pensar.

**Resultado:** Você nunca mais precisa "ser bom" em definir resultado. Você só precisa capturar.

---

## 📋 Processo Passo a Passo

### Passo 1: Captura (Nível 0)
**Tempo:** 30 segundos

**Ação:**
1. Receba a entrada bruta (texto, áudio, conversa)
2. Cole no template na seção **"1️⃣ Contexto da entrada"**
3. Não corrija, não interprete, não melhore

**Resultado:** Entrada registrada.

---

### Passo 2: Transform (Nível 1 — v0)
**Tempo:** 5-15 minutos

**Ação:**
1. Responda **Pergunta 1:** O que passa a ser verdade? (3-5 verdades)
2. Responda **Pergunta 2:** Qual é o gap? (3-5 pares atual → desejado)
3. Defina **Critérios de aceitação** (3-7 critérios verificáveis)
4. Defina **Escopo** (dentro/fora)
5. Defina **Incertezas aceitáveis** (3-7 incertezas com fronteiras)
6. Declare **Pai provisório** (pode ser "TBD" com prazo de revisão)
7. Preencha **Versionamento** (v0, data, motivo)
8. Marque **Checklist mínimo** (B1, B2, B3, B5, B6, B10, B11)

**Resultado:** Spec v0 válida (pode existir oficialmente no sistema).

---

### Passo 3: Validate (Checklist Mínimo)
**Tempo:** 2 minutos

**Ação:**
Verifique se a Spec passa nos bloqueios mínimos:

- [ ] **B1** — Não é solution-first (descreve resultado, não solução)
- [ ] **B2** — É verificável (critérios testáveis)
- [ ] **B3** — Tem pai declarado (ou "TBD" com compromisso)
- [ ] **B5** — Tem escopo (dentro/fora)
- [ ] **B6** — É versionada (v0, data, motivo)
- [ ] **B10** — Incertezas explícitas (com fronteiras)
- [ ] **B11** — Passou pelo processo (Perguntas 1-2 respondidas)

**Resultado:** PASS ou FAIL.

---

### Passo 4: Emit (Saída Oficial)
**Tempo:** 1 minuto

**Ação:**
1. Se PASS → Salve como `ENDFIRST_SPEC_<ID>.md`
2. Adicione **Declaração de passagem**: "Esta ENDFIRST_SPEC está oficialmente aceita pelo sistema no Modo v0."
3. Mova para backlog oficial

**Resultado:** Spec oficialmente aceita no sistema.

---

## 🔄 Fluxo Visual

```
Entrada bruta
    ↓
[Captura] (30s)
    ↓
Entrada registrada
    ↓
[Transform] (5-15min)
    ↓
Spec v0 preenchida
    ↓
[Validate] (2min)
    ↓
PASS/FAIL
    ↓
[Emit] (1min)
    ↓
Spec oficial no sistema
```

---

## 🛡️ Proteções Anti-Paralisia

### Proteção 1: Modo v0 é suficiente
**Problema:** "Preciso responder todas as 6 perguntas antes de começar?"

**Solução:** Não. Modo v0 só exige Perguntas 1-2. O resto pode vir depois (v1).

---

### Proteção 2: Pai provisório é permitido
**Problema:** "Não sei onde isso se encaixa no portfolio."

**Solução:** Declare "TBD" com prazo de revisão. Pode existir sem pai definitivo.

---

### Proteção 3: Incertezas são permitidas
**Problema:** "Não tenho todas as respostas."

**Solução:** Liste as incertezas explicitamente com fronteiras (OK se... / NÃO OK se...).

---

### Proteção 4: Captura sem julgamento
**Problema:** "A entrada está confusa/mal escrita."

**Solução:** Capture exatamente como está. Não corrija. O ritual transforma depois.

---

## 🚫 O Que NÃO Fazer

### ❌ Não pule a captura
**Problema:** Ir direto para "definir resultado" sem registrar entrada bruta.

**Consequência:** Perde contexto original, não tem rastro de transformação.

---

### ❌ Não corrija a entrada
**Problema:** "Melhorar" a entrada antes de registrar.

**Consequência:** Perde fidelidade, não sabe o que mudou.

---

### ❌ Não finja ter respostas
**Problema:** Preencher seções sem saber, só para "completar".

**Consequência:** Spec falsa, validação quebrada, confiança perdida.

---

### ❌ Não crie Spec sem template
**Problema:** "Vou escrever do meu jeito, mais rápido."

**Consequência:** Não passa nos bloqueios, não é compatível, vira "duas verdades".

---

## 📊 Métricas de Sucesso

### Métrica 1: Tempo de captura
**Objetivo:** < 30 segundos da entrada até registro.

**Como medir:** Timestamp de recebimento → timestamp de registro.

---

### Métrica 2: Taxa de PASS v0
**Objetivo:** > 80% das Specs v0 passam no checklist mínimo na primeira tentativa.

**Como medir:** (Specs PASS / Total de Specs criadas) × 100.

---

### Métrica 3: Tempo de transformação
**Objetivo:** < 15 minutos da captura até Spec v0 válida.

**Como medir:** Timestamp de registro → timestamp de PASS.

---

### Métrica 4: Taxa de adoção
**Objetivo:** 100% das demandas passam pelo Pilar ENDFIRST antes de entrar no backlog.

**Como medir:** (Demandas com Spec / Total de demandas) × 100.

---

## 🎯 Regra Mãe (Para Colar no Topo do Chat/Equipe)

```
REGRA ENDFIRST PARA QUALQUER CONVERSA:

"Antes de discutir solução, precisamos escrever a ENDFIRST_SPEC v0. 
Se não existe spec, a demanda não existe."
```

**Isso sozinho já muda o comportamento do sistema.**

---

## 📜 Declaração Final

Este processo existe para **eliminar fricção**, não criar burocracia.

Se o processo está travando em vez de clarificando, o problema é no processo, não em você.

Reporte qualquer travamento e revisaremos o processo.

---

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Path Canônico:** `/METODO/processos/ENDFIRST_PROCESS.md`  
**Governado por:** `/METODO/PILAR_ENDFIRST.md`
