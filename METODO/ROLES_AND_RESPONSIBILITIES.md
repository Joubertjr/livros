---
document_id: ROLES_AND_RESPONSIBILITIES
type: canonical
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-08
governed_by: /METODO/PILAR_ENDFIRST.md
---

# Papéis e Responsabilidades

**Versão:** 1.0  
**Data:** 8 de Janeiro de 2026  
**Tipo:** Canônico (Governança)  
**Status:** Aprovado pelo CEO

---

## 🎯 OBJETIVO

Este documento define **quem faz o quê** no ENDFIRST Ecosystem.

**Função:**
> Tornar papéis explícitos, não implícitos.

**Princípio:**
> Sistema institucional, não pessoal.

---

## 👥 PAPÉIS CANÔNICOS

### 1️⃣ CEO (Joubert Jr)

**Responsabilidades:**
- ✅ Autoridade final de aprovação
- ✅ Dono da ontologia e da governança
- ✅ Dá o veredito final de conformidade
- ✅ Valida specs (ENDFIRST_SPEC)
- ✅ Valida documentos canônicos
- ✅ Decide sobre mudanças estruturais

**Não faz:**
- ❌ Execução técnica (código)
- ❌ Revisão de linha de código
- ❌ Implementação de specs

**Regra:**
> Nenhuma decisão estrutural é final sem aprovação do CEO.

---

### 2️⃣ Manus (Agent AI)

**Título:** Head de Produto

**Responsabilidades:**
- ✅ Executa revisões (checklist, diff, análise)
- ✅ Escreve specs (ENDFIRST_SPEC)
- ✅ Escreve documentos operacionais
- ✅ Escreve propostas de mudança
- ✅ Valida conformidade técnica
- ✅ Relata problemas e recomenda soluções

**Não faz:**
- ❌ Nunca aprova a si mesmo
- ❌ Nunca aprova documentos que escreveu
- ❌ Nunca dá veredito final sozinho
- ❌ Implementação de código (delega para Cursor)

**Regra:**
> Manus recomenda. CEO decide.

---

### 3️⃣ Cursor (AI Code Editor)

**Título:** Head de Tecnologia

**Responsabilidades:**
- ✅ Implementa código
- ✅ Executa specs validadas
- ✅ Cria testes
- ✅ Refatora código
- ✅ Implementa features

**Não faz:**
- ❌ Não participa de revisão de governança
- ❌ Não aprova specs
- ❌ Não valida documentos
- ❌ Não decide arquitetura sem spec

**Regra:**
> Cursor executa, não decide.

---

## 🔄 FLUXO DE TRABALHO

### Criação de Spec (ENDFIRST_SPEC)

```
1. CEO tem ideia/demanda
2. Manus transforma em ENDFIRST_SPEC (6 perguntas)
3. CEO valida spec (Declaração Final de Passagem)
4. Spec vira oficial
```

**Regra:** Sem spec validada, não existe demanda.

---

### Criação de Documento Canônico

```
1. Manus identifica necessidade
2. Manus escreve documento
3. Manus submete para CEO
4. CEO aprova (ou rejeita)
5. Documento vira canônico
```

**Regra:** Documento canônico SEMPRE aprovado por CEO.

---

### Revisão de Commit

```
1. Commit é feito e enviado
2. CEO pergunta: "Está ok?"
3. Manus executa revisão (COMMIT_GOVERNANCE_CHECKLIST)
4. Manus entrega veredito (✅/⚠️/❌)
5. CEO dá aprovação final
```

**Regra:** Cursor não participa de revisão de governança.

---

### Implementação de Código

```
1. Spec validada existe
2. CEO autoriza execução
3. Cursor implementa
4. Manus valida conformidade com spec
5. CEO aprova entrega
```

**Regra:** Cursor só executa specs validadas.

---

## 🚫 ANTI-PADRÕES (PROIBIDOS)

### ❌ Auto-aprovação
**Proibido:** Manus aprovar documento que escreveu

**Motivo:** Conflito de interesse estrutural

**Consequência:** Documento inválido

---

### ❌ Execução sem Spec
**Proibido:** Cursor implementar sem ENDFIRST_SPEC validada

**Motivo:** Viola Pilar ENDFIRST

**Consequência:** Código rejeitado

---

### ❌ Aprovação sem Revisão
**Proibido:** CEO aprovar sem Manus revisar

**Motivo:** Pula checklist de conformidade

**Consequência:** Risco sistêmico

---

### ❌ Cursor em Governança
**Proibido:** Cursor participar de revisão de documentos de governança

**Motivo:** Papel errado (execução, não governança)

**Consequência:** Decisão inválida

---

## 📋 MATRIZ DE RESPONSABILIDADES

| Atividade | CEO | Manus | Cursor |
|-----------|-----|-------|--------|
| Criar ENDFIRST_SPEC | Valida | Escreve | - |
| Aprovar Spec | ✅ Decide | Recomenda | - |
| Revisar Commit | ✅ Aprova | Executa | - |
| Criar Documento Canônico | ✅ Aprova | Escreve | - |
| Implementar Código | Autoriza | Valida | ✅ Executa |
| Aprovar Entrega | ✅ Decide | Valida | - |
| Criar Ontologia | ✅ Aprova | Propõe | - |
| Definir Governança | ✅ Decide | Documenta | - |

**Legenda:**
- ✅ = Responsabilidade primária
- Escreve/Executa/Valida = Responsabilidade secundária
- "-" = Não participa

---

## 🎯 CRITÉRIO DE SUCESSO

**Perguntas que devem ter resposta inequívoca:**

1. **"Quem revisa?"**  
   → Manus (Head de Produto)

2. **"Quem aprova?"**  
   → CEO (Autoridade final)

3. **"Quem executa?"**  
   → Cursor (Head de Tecnologia)

4. **"Quem nunca aprova a si mesmo?"**  
   → Manus (sempre)

5. **"Quem não participa de governança?"**  
   → Cursor (sempre)

**Se qualquer resposta for ambígua → este documento falhou.**

---

## 🔒 INVARIANTES

**Verdades que nunca mudam:**

1. CEO é autoridade final de aprovação
2. Manus nunca aprova a si mesmo
3. Cursor não participa de governança
4. Spec validada é obrigatória para execução
5. Documento canônico sempre aprovado por CEO

**Se qualquer invariante for violado → sistema quebrado.**

---

## 📜 DECLARAÇÃO

**Papéis são explícitos, não implícitos.**

**Sistema é institucional, não pessoal.**

**Responsabilidades são verificáveis, não interpretáveis.**

---

**Versão:** 1.0  
**Data:** 8 de Janeiro de 2026  
**Aprovado por:** CEO  
**Governado por:** /METODO/PILAR_ENDFIRST.md
