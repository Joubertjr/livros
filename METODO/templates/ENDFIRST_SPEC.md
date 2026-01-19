---
document_id: ENDFIRST_SPEC
type: canonical
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-07
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.0
created_at: 2026-01-07
---

# ENDFIRST_SPEC — Template Canônico

**Status:** Template Oficial  
**Versão:** v0 (instância)  
**Governado por:** `/METODO/PILAR_ENDFIRST.md`  
**Path Canônico:** `/METODO/templates/ENDFIRST_SPEC.md`  
**Uso obrigatório:** ✅ SIM

---

## 📊 MODOS DE USO

Este template possui **2 modos** para evitar burocracia e paralisia por perfeição.

### 🟢 Modo v0 (Mínimo para existir)

**Objetivo:** Criar Spec que pode existir oficialmente no sistema.

**Seções obrigatórias:**
- ✅ 0️⃣ Metadados
- ✅ 1️⃣ Contexto da entrada (captura bruta)
- ✅ 2️⃣ Resultado estrutural esperado (Pergunta 1)
- ✅ 3️⃣ Gap atual → desejado (Pergunta 2)
- ✅ 8️⃣ Critérios de aceitação
- ✅ 9️⃣ Escopo e fora de escopo
- ✅ 7️⃣ Incertezas aceitáveis
- ✅ 1️⃣1️⃣ Alinhamento hierárquico (pode ser "TBD" com compromisso)
- ✅ 1️⃣4️⃣ Versionamento v0
- ✅ 1️⃣5️⃣ Declaração final de passagem
- ✅ 🔒 Checklist mínimo (B1, B2, B3, B5, B6, B10, B11)

**Quando usar:** Demanda oficial que ainda não será executada imediatamente.

---

### 🔵 Modo v1 (Completo para executar)

**Objetivo:** Completar Spec para permitir execução.

**Seções adicionais:**
- ✅ 4️⃣ Validação de percepção (Pergunta 3)
- ✅ 5️⃣ Formas de falha (Pergunta 4)
- ✅ 6️⃣ Anti-resultados (Pergunta 5)
- ✅ 🔟 Dependências e pré-condições
- ✅ 1️⃣2️⃣ Ontologia e termos críticos
- ✅ 1️⃣3️⃣ Anti-gaming / Integridade
- ✅ 🔒 Checklist completo (B1–B11)

**Quando usar:** Antes de mover para execução (backlog → em progresso).

---

### ⚠️ Regra de Progressão

**Obrigatório:**
- Toda Spec começa no Modo v0
- Não pode executar sem passar pelo Modo v1
- Pode ficar em v0 indefinidamente (desde que explícito)

**Proibido:**
- Ir direto para execução sem completar v1
- Fingir que está em v1 quando está em v0

---

## 0️⃣ METADADOS (OBRIGATÓRIO)

```yaml
spec_id: ________
version: v0
status: draft
criada_em: YYYY-MM-DD
criada_por: ________
pilar: ________
modo: v0
```

---

## 1️⃣ CONTEXTO DA ENTRADA (CAPTURA BRUTA)

### Entrada original (texto livre):

```
[Cole aqui a entrada bruta, sem correção ou interpretação]
```

### Fonte da entrada:
- [ ] Conversa
- [ ] Documento
- [ ] Áudio transcrito
- [ ] Ideia solta
- [ ] Outro: _______

---

## 2️⃣ RESULTADO ESTRUTURAL ESPERADO

**(Pergunta 1 — Pilar ENDFIRST)**

**Se isso der certo, o que passa a ser verdade?**

- [ ] **Verdade 1:** ________
- [ ] **Verdade 2:** ________
- [ ] **Verdade 3:** ________
- [ ] **Verdade 4:** ________
- [ ] **Verdade 5:** ________

---

## 3️⃣ GAP ATUAL → DESEJADO

**(Pergunta 2)**

### Estado Atual (o que não é verdade hoje)

- ❌ ________
- ❌ ________
- ❌ ________
- ❌ ________
- ❌ ________

### Estado Desejado (o que deveria ser verdade)

- ✅ ________
- ✅ ________
- ✅ ________
- ✅ ________
- ✅ ________

---

## 4️⃣ VALIDAÇÃO DE PERCEPÇÃO

**(Pergunta 3 — Pilar ENDFIRST)**

**Quem percebe o sucesso? (4 níveis)**

### Nível Técnico (sistema/infraestrutura)
- ________

### Nível Operacional (usuário direto)
- ________

### Nível Tático (time/área)
- ________

### Nível Estratégico (organização/negócio)
- ________

⚠️ **Modo v0:** Pode ser preenchido depois (v1).

---

## 5️⃣ FORMAS DE FALHA

**(Pergunta 4 — Pilar ENDFIRST)**

**Como isso pode falhar?**

| Forma de Falha | Como Detectar | Como Prevenir |
|----------------|---------------|---------------|
| ________ | ________ | ________ |
| ________ | ________ | ________ |
| ________ | ________ | ________ |

⚠️ **Modo v0:** Pode ser preenchido depois (v1).

---

## 6️⃣ ANTI-RESULTADOS

**(Pergunta 5 — Pilar ENDFIRST)**

**O que NÃO pode acontecer (mesmo se critérios técnicos passarem)?**

- ❌ ________
- ❌ ________
- ❌ ________
- ❌ ________
- ❌ ________

⚠️ **Modo v0:** Pode ser preenchido depois (v1).

---

## 7️⃣ INCERTEZAS ACEITÁVEIS

**(Pergunta 6 — Pilar ENDFIRST)**

**Quais incertezas são permitidas neste momento?**

- 🟡 **Incerteza 1:** ________
  - ✅ **OK se:** ________
  - ❌ **NÃO OK se:** ________

- 🟡 **Incerteza 2:** ________
  - ✅ **OK se:** ________
  - ❌ **NÃO OK se:** ________

- 🟡 **Incerteza 3:** ________
  - ✅ **OK se:** ________
  - ❌ **NÃO OK se:** ________

---

## 8️⃣ CRITÉRIOS DE ACEITAÇÃO (VERIFICABILIDADE)

**(Bloqueio B2)**

**Como saber objetivamente que o resultado foi atingido?**

- [ ] **Critério 1:** ________
- [ ] **Critério 2:** ________
- [ ] **Critério 3:** ________
- [ ] **Critério 4:** ________
- [ ] **Critério 5:** ________
- [ ] **Critério 6:** ________
- [ ] **Critério 7:** ________

---

## 9️⃣ ESCOPO E FORA DE ESCOPO

**(Bloqueio B5)**

### Dentro do escopo

- ✔️ ________
- ✔️ ________
- ✔️ ________
- ✔️ ________
- ✔️ ________

### Fora do escopo

- ❌ ________
- ❌ ________
- ❌ ________
- ❌ ________
- ❌ ________

---

## 🔟 DEPENDÊNCIAS E PRÉ-CONDIÇÕES

**(Bloqueio B4)**

### Dependências técnicas:
- **Dependência 1:** ________
- **Dependência 2:** ________

### Dependências organizacionais:
- **Dependência 1:** ________
- **Dependência 2:** ________

### Dependências de dados:
- **Dependência 1:** ________
- **Dependência 2:** ________

⚠️ **Modo v0:** Pode ser preenchido depois (v1).

---

## 1️⃣1️⃣ ALINHAMENTO HIERÁRQUICO

**(Bloqueios B3 e B4)**

### Pai declarado:
- **Portfolio / Program / Project:** ________

⚠️ **Modo v0:** Pode ser `TBD` (a definir) desde que:
- Exista intenção explícita de encaixe
- Prazo de revisão definido (ex: "revisar em 2 semanas")

### Como este resultado contribui para o pai:

(1–3 frases objetivas)

⚠️ **Modo v0:** Pode ser "a definir" se pai ainda não existe.

---

## 1️⃣2️⃣ ONTOLOGIA E TERMOS CRÍTICOS

**(Bloqueio B7)**

### Termos que precisam de definição explícita:

- **Termo 1:** ________
- **Termo 2:** ________
- **Termo 3:** ________

⚠️ **Modo v0:** Pode ser preenchido depois (v1).

---

## 1️⃣3️⃣ ANTI-GAMING / INTEGRIDADE

**(Bloqueio B8)**

**Como evitar que critérios sejam "passados" sem resultado real?**

- ________
- ________
- ________

⚠️ **Modo v0:** Pode ser preenchido depois (v1).

---

## 1️⃣4️⃣ VERSIONAMENTO E HISTÓRICO

**(Bloqueio B6)**

### Histórico de versões

- **v0** — criação inicial (YYYY-MM-DD)
  - **Motivo:** ________
  - **Impacto esperado:** ________

⚠️ **Mudanças sem registro são proibidas.**

---

## 1️⃣5️⃣ DECLARAÇÃO FINAL DE PASSAGEM

**Você reconhece esta Spec como o resultado que quer perseguir agora?**

- [ ] ✅ **Sim** → A Spec passou pelo Pilar ENDFIRST
- [ ] ❌ **Não** → Voltar para Pergunta 2

---

## 🔒 CHECKLIST DE VALIDAÇÃO

### Modo v0 (Mínimo para existir)

- [ ] **B1** — Não é solution-first (descreve resultado, não solução)
- [ ] **B2** — É verificável (critérios testáveis)
- [ ] **B3** — Tem pai declarado (ou "TBD" com compromisso)
- [ ] **B5** — Tem escopo (dentro/fora)
- [ ] **B6** — É versionada (v0, motivo, impacto)
- [ ] **B10** — Incertezas explícitas (com fronteiras)
- [ ] **B11** — Passou pelo processo (Perguntas 1-2 respondidas)

### Modo v1 (Completo para executar)

- [ ] **B4** — Dependências explícitas
- [ ] **B7** — Ontologia clara (termos definidos)
- [ ] **B8** — Tem anti-gaming
- [ ] **B9** — Tem anti-resultados
- [ ] **B11** — Passou pelo processo (Perguntas 1-6 respondidas)

### Resultado da validação:
- [ ] ✅ **PASS (Modo v0)**
- [ ] ✅ **PASS (Modo v1)**
- [ ] ❌ **FAIL** — Motivos: ________

---

## 📤 SAÍDA OFICIAL

### Status: ________

**Esta ENDFIRST_SPEC está oficialmente aceita pelo sistema no Modo ________.**

**Próximos passos:**
1. ________
2. ________
3. ________

---

**Versão:** v0  
**Data:** YYYY-MM-DD  
**Governado por:** `/METODO/PILAR_ENDFIRST.md`  
**Path Canônico:** `/METODO/templates/ENDFIRST_SPEC.md`  
**Modo:** 🟢 v0 (Mínimo para existir)
