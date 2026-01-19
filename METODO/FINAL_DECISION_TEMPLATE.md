---
document_id: FINAL_DECISION_TEMPLATE
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-08
governed_by: /METODO/ONTOLOGY_DECISIONS.md
version: 1.0
created_at: 2026-01-08
---

# FINAL DECISION TEMPLATE — Formato Padrão de Decisão Final

**Versão:** 1.0  
**Data:** 8 de Janeiro de 2026  
**Tipo:** Operacional (Tipo B)  
**Owner:** CEO (Joubert Jr)

---

## 🎯 OBJETIVO

Este documento define **como o CEO decide, de forma objetiva, se uma DEMANDA foi bem-sucedida**.

**Função:**
- Permitir decisão objetiva, repetível e auditável
- Eliminar improviso no momento do julgamento
- Garantir que decisão não muda critério
- Garantir que executor não influencia julgamento
- Garantir que resultado não vira debate

**Quem usa:** CEO  
**Quando:** Somente após entrega do executor  
**Fonte de verdade:** Critérios de aceitação já commitados

---

## 📋 FORMATO PADRÃO

### 1️⃣ IDENTIFICAÇÃO

**Campos obrigatórios:**

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| **Demanda** | ID da demanda avaliada | DEMANDA-001 |
| **Produto** | Nome do produto | LLM Orchestrator |
| **Executor** | Quem executou | cursor |
| **Spec governante** | Spec que define resultado esperado | EF-2026-001 |
| **Critérios de aceitação** | Documento com critérios | DEMANDA-001_ACCEPTANCE.md |
| **Commit avaliado** | Hash do commit de resultado | [hash] |
| **Data da avaliação** | Data do julgamento | 2026-01-08 |
| **Avaliador** | Quem decide | CEO (Joubert Jr) |

---

### 2️⃣ REGRA DE JULGAMENTO (IMUTÁVEL)

**Princípios:**
- ✅ Cada critério é binário: **PASS** / **FAIL**
- ✅ Qualquer **FAIL** elimina aprovação direta
- ❌ Não existe "quase aprovado"
- ✅ Ajuste só ocorre se arquitetura estiver correta
- ✅ Evidência é obrigatória (opinião não conta)

**Rejeição ocorre se:**
- Critério estrutural falhar
- Solução fugir do contrato
- Executor "decidir" algo não autorizado

---

### 3️⃣ AVALIAÇÃO POR CRITÉRIO

**Formato obrigatório:**

| Critério | Resultado | Evidência |
|----------|-----------|-----------|
| Critério 1 | PASS / FAIL | link / trecho / explicação curta |
| Critério 2 | PASS / FAIL | link / trecho / explicação curta |
| Critério 3 | PASS / FAIL | link / trecho / explicação curta |
| Critério 4 | PASS / FAIL | link / trecho / explicação curta |
| Critério 5 | PASS / FAIL | link / trecho / explicação curta |

**Nota:** Evidência é obrigatória. Opinião não conta.

---

### 4️⃣ VEREDITO FINAL

**Escolher exatamente um:**

---

#### ✅ APROVADO

**Condições:**
- ✅ Todos os critérios **PASS**
- ✅ Solução respeita spec
- ✅ Nenhuma decisão fora do contrato

**Ação:**
1. Registrar aprovação no Git
2. Encerrar demanda
3. Produto avança

**Proibido:**
- ❌ Aprovar com ressalvas
- ❌ Aprovar "parcialmente"
- ❌ Aprovar "com ajustes futuros"

---

#### ⚠️ AJUSTAR

**Condições:**
- ✅ Arquitetura correta
- ⚠️ Um ou mais critérios **FAIL** corrigíveis
- ✅ Nenhuma violação ontológica

**Ação:**
1. Criar lista objetiva de ajustes
2. Reabrir execução para Cursor
3. Critérios **NÃO mudam**

**Proibido:**
- ❌ Mudar critérios de aceitação
- ❌ Criar novos critérios
- ❌ Negociar o que é "sucesso"

---

#### ❌ REJEITADO

**Condições:**
- ❌ Violação estrutural
- ❌ Solução fora do contrato
- ❌ Decisão indevida do executor

**Ação:**
1. Encerrar execução atual
2. Decidir: nova demanda ou abandono
3. Registrar motivo

**Proibido:**
- ❌ Rejeitar por "gosto pessoal"
- ❌ Rejeitar sem evidência
- ❌ Rejeitar por mudança de critério

---

### 5️⃣ DECLARAÇÃO FINAL DO CEO

**Texto obrigatório (sempre explícito):**

> "Resultado avaliado contra critérios previamente definidos.  
> Decisão tomada sem alteração de contrato."

**Assinatura:**
- CEO: Joubert Jr
- Data: YYYY-MM-DD

---

## 🔒 PROIBIÇÕES EXPLÍCITAS

### Durante o julgamento

- ❌ **Mudar critérios de aceitação** após entrega
- ❌ **Criar novos critérios** não declarados antes
- ❌ **Negociar o que é "sucesso"** com executor
- ❌ **Aprovar com ressalvas** não previstas
- ❌ **Reinterpretar critérios** para "ajudar" resultado
- ❌ **Decidir por "gosto pessoal"** ou opinião
- ❌ **Julgar sem evidência** objetiva

### Após o julgamento

- ❌ **Reverter decisão** sem justificativa ontológica
- ❌ **Reavaliar resultado** sem mudança de critério formal
- ❌ **Criar exceções** não previstas no template

---

## 🎯 GARANTIAS DO SISTEMA

Este formato garante que:

| Garantia | Como |
|----------|------|
| ❌ Execução não influencia decisão | Critérios existem antes da entrega |
| ❌ Critério não muda depois da entrega | Imutabilidade explícita |
| ❌ Carisma técnico não vence contrato | Evidência objetiva obrigatória |
| ✅ Decisão é rastreável | Tudo no Git |
| ✅ Sistema escala | Template reutilizável |
| ✅ Conflito vira dado, não ruído | Binário: PASS/FAIL |

---

## 🔄 LOOP COMPLETO DO ENDFIRST

**Fechado:**

```
resultado esperado → execução → julgamento → decisão
```

**Documentos envolvidos:**

| Documento | Papel |
|-----------|-------|
| **ENDFIRST_SPEC** | Define RESULTADO ESPERADO |
| **DEMANDA-XXX** | Define O QUE fazer |
| **DEMANDA-XXX_ACCEPTANCE.md** | Define O QUE é sucesso |
| **EXECUTION_MODEL.md** | Define QUEM executa |
| **FINAL_DECISION_TEMPLATE.md** | Define COMO julgar |

Cada um resolve um eixo diferente.  
Nenhuma sobreposição. Nenhuma ambiguidade.

---

## 📋 EXEMPLO DE USO

### Contexto
- Demanda: DEMANDA-001
- Critérios: DEMANDA-001_ACCEPTANCE.md
- Executor: Cursor
- Resultado: Commit [hash]

### Passo a passo

1. **CEO lê resultado** (commit do Cursor)
2. **CEO abre DEMANDA-001_ACCEPTANCE.md** (critérios)
3. **CEO preenche tabela** (critério × evidência)
4. **CEO decide** (✅ APROVADO / ⚠️ AJUSTAR / ❌ REJEITADO)
5. **CEO registra decisão no Git**
6. **Decisão é final** (sem renegociação)

---

## 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/ONTOLOGY_DECISIONS.md` (OD-006: Execução é responsabilidade da Tecnologia)
- `/METODO/EXECUTION_MODEL.md` (Modelo de execução)
- `/METODO/ENDFIRST_DOCUMENT_GOVERNANCE.md` (Governança documental)
- `/METODO/PILAR_ENDFIRST.md` (Meta-pilar)

---

## 📜 DECLARAÇÃO DO CEO

> "Se a decisão final não estiver no Git, o sistema ainda depende de pessoas.  
> Este template fecha o último elo do loop de governança."

**Data:** 2026-01-08  
**Responsável:** CEO (Joubert Jr)

---

## 📊 HISTÓRICO DE VERSÕES

| Versão | Data | Mudança | Responsável |
|--------|------|---------|-------------|
| 1.0 | 2026-01-08 | Criação do template padrão | CEO (Joubert Jr) |

---

**Versão:** 1.0  
**Criado:** 8 de Janeiro de 2026  
**Criado por:** CEO (Joubert Jr)  
**Aprovado por:** CEO (Joubert Jr)  
**Status:** Operacional (Tipo B)
