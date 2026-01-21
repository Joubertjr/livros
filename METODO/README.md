---
document_id: README_METODO
type: example
owner: Manus (Agent)
status: approved
approved_by: CEO
approved_at: 2026-01-07
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.0
created_at: 2026-01-07
---

# METODO — Núcleo Operacional ENDFIRST

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Status:** Operacional

---

## 🎯 O que é este diretório

Este diretório contém o **núcleo operacional do Pilar ENDFIRST** — o sistema de tradução governada de **intenção difusa** → **resultado explícito, verificável e versionável**.

**Regra fundamental:**

> "Antes de discutir solução, precisamos escrever a ENDFIRST_SPEC v0.  
> Se não existe spec, a demanda não existe."

---

## 📂 Estrutura de Arquivos

```
/METODO/
├── PILAR_ENDFIRST.md              # Fonte soberana de verdade
├── README.md                       # Este arquivo
├── templates/
│   └── ENDFIRST_SPEC.md           # Template oficial para criar specs
├── examples/
│   └── ENDFIRST_SPEC_EF-2026-001_LLM_ORCHESTRATOR.md  # Exemplo real
├── processos/
│   └── ENDFIRST_PROCESS.md        # Processo humano de 30 segundos
└── ontologia/
    └── (vazio — criar só quando B7 bloquear repetidamente)
```

---

## 🚀 Como Iniciar uma Demanda

### Passo 1: Captura (30 segundos)
1. Copie o template: `/METODO/templates/ENDFIRST_SPEC.md`
2. Cole a entrada bruta na seção **"1️⃣ Contexto da entrada"**
3. Não corrija, não interprete, não melhore

### Passo 2: Transform (5-15 minutos)
1. Responda **Pergunta 1:** O que passa a ser verdade? (3-5 verdades)
2. Responda **Pergunta 2:** Qual é o gap? (3-5 pares atual → desejado)
3. Defina **Critérios de aceitação** (3-7 critérios verificáveis)
4. Defina **Escopo** (dentro/fora)
5. Defina **Incertezas aceitáveis** (3-7 incertezas com fronteiras)
6. Declare **Pai provisório** (pode ser "TBD" com prazo de revisão)

### Passo 3: Validate (2 minutos)
Verifique se a Spec passa nos bloqueios mínimos:
- [ ] **B1** — Não é solution-first
- [ ] **B2** — É verificável
- [ ] **B3** — Tem pai declarado
- [ ] **B5** — Tem escopo
- [ ] **B6** — É versionada
- [ ] **B10** — Incertezas explícitas
- [ ] **B11** — Passou pelo processo

### Passo 4: Emit (1 minuto)
Se PASS → Salve como `ENDFIRST_SPEC_<ID>.md` e mova para backlog oficial.

---

## 📖 Documentos Canônicos

### 1. PILAR_ENDFIRST.md
**O que é:** Fonte soberana de verdade sobre o Pilar ENDFIRST.

**Contém:**
- Definição formal
- Ritual de 6 perguntas
- 11 bloqueios (B1-B11)
- 7 anti-resultados
- 4 serviços (Intake, Transform, Validate, Emit)
- 4 níveis de aplicação (Captura, v0, v1, Automação)
- Governança soberana

**Quando consultar:** Qualquer dúvida sobre o método.

---

### 2. templates/ENDFIRST_SPEC.md
**O que é:** Template oficial para criar especificações.

**Contém:**
- 2 modos (v0: mínimo para existir, v1: completo para executar)
- 15 seções mapeando 6 perguntas e 11 bloqueios
- Checklist de validação
- Declaração de passagem

**Quando usar:** Sempre que criar uma nova demanda.

---

### 3. examples/ENDFIRST_SPEC_EF-2026-001_LLM_ORCHESTRATOR.md
**O que é:** Exemplo real de aplicação do template.

**Contém:**
- Entrada bruta capturada
- Transformação em resultado estruturado
- Validação contra bloqueios
- Status: PASS (Modo v0)

**Quando consultar:** Para ver como aplicar o template na prática.

---

### 4. processos/ENDFIRST_PROCESS.md
**O que é:** Guia passo a passo para humanos.

**Contém:**
- Processo de 30 segundos
- Regra de comunicação (2 linhas)
- Proteções anti-paralisia
- Métricas de sucesso

**Quando consultar:** Para lembrar o fluxo operacional.

---

## 🛡️ Proteções Anti-Paralisia

### ✅ Modo v0 é suficiente
Você não precisa responder todas as 6 perguntas antes de começar. Modo v0 só exige Perguntas 1-2.

### ✅ Pai provisório é permitido
Você não precisa saber onde isso se encaixa no portfolio. Declare "TBD" com prazo de revisão.

### ✅ Incertezas são permitidas
Você não precisa ter todas as respostas. Liste as incertezas explicitamente com fronteiras (OK se... / NÃO OK se...).

### ✅ Captura sem julgamento
Você não precisa "melhorar" a entrada. Capture exatamente como está.

---

## 🔒 Hierarquia de Documentos

Em caso de conflito ou ambiguidade:

1. **`PILAR_ENDFIRST.md`** prevalece (fonte soberana)
2. **`templates/ENDFIRST_SPEC.md`** segue o Pilar
3. **`processos/ENDFIRST_PROCESS.md`** segue o Pilar
4. **`ontologia/`** segue o Pilar (quando existir)

---

## 📊 Níveis de Aplicação

### Nível 0: Captura
Entrada bruta registrada (sem estrutura formal).

### Nível 1: Spec v0 válida
Mínimo para existir oficialmente no sistema (Perguntas 1-2, checklist mínimo).

### Nível 2: Spec executável
Completa para permitir execução (Perguntas 1-6, checklist completo).

### Nível 3: Automação
Schema JSON, CLI, integração com GitHub Projects (futuro).

---

## 🚫 O Que NÃO Fazer

### ❌ Não pule a captura
Ir direto para "definir resultado" sem registrar entrada bruta.

### ❌ Não corrija a entrada
"Melhorar" a entrada antes de registrar.

### ❌ Não finja ter respostas
Preencher seções sem saber, só para "completar".

### ❌ Não crie Spec sem template
"Vou escrever do meu jeito, mais rápido."

---

## 📜 Declaração Final

**Este diretório é a fonte soberana de verdade sobre o Pilar ENDFIRST.**

Qualquer conflito, ambiguidade ou dúvida deve ser resolvida consultando `/METODO/PILAR_ENDFIRST.md`.

Se esse documento não responde, a resposta ainda não existe oficialmente.

---

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Path Canônico:** `/METODO/README.md`  
**Governado por:** `/METODO/PILAR_ENDFIRST.md`
