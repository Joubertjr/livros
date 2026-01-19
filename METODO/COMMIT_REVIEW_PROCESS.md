---
document_id: COMMIT_REVIEW_PROCESS
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-08
governed_by: /METODO/ROLES_AND_RESPONSIBILITIES.md
---

# Processo de Revisão de Commits

**Versão:** 1.0  
**Data:** 8 de Janeiro de 2026  
**Tipo:** Operacional (Processo)  
**Status:** Aprovado pelo CEO

---

## 🎯 OBJETIVO

Este documento define o **processo oficial de revisão de commits** no ENDFIRST Ecosystem.

**Função:**
> Garantir que todo commit seja revisado, classificado e aprovado antes de ser considerado válido.

**Princípio:**
> Commit não revisado = risco sistêmico.

---

## 👥 PAPÉIS NA REVISÃO

### CEO (Joubert Jr)
- **Responsabilidade:** Autoridade final de aprovação
- **Ação:** Dá veredito final (aprova ou rejeita)
- **Não faz:** Revisão técnica detalhada

### Manus (Agent AI)
- **Responsabilidade:** Executor da revisão e relator
- **Ação:** Analisa commit, aplica checklist, escreve parecer
- **Não faz:** Nunca aprova sozinho

### Cursor (AI Code Editor)
- **Responsabilidade:** Não participa da revisão de governança
- **Ação:** Nenhuma (apenas executa código)
- **Não faz:** Não revisa, não aprova, não valida governança

---

## 🔄 FLUXO CORRETO (5 PASSOS)

### Passo 1: Commit é Feito e Enviado
**Responsável:** Manus ou Cursor  
**Ação:** `git commit` + `git push`

**Resultado:** Commit aparece no GitHub

---

### Passo 2: CEO Solicita Revisão
**Responsável:** CEO  
**Ação:** Pergunta ao Manus:

```
"Fiz esse commit: https://github.com/Joubertjr/endfirst-ecosystem/commit/[HASH]
O que você acha? Está ok?"
```

**Resultado:** Revisão é iniciada

---

### Passo 3: Manus Executa Revisão
**Responsável:** Manus  
**Ação:** Abre commit no navegador e analisa:

**Checklist obrigatório:**
- [ ] **Diff linha por linha** (mudanças fazem sentido?)
- [ ] **Mensagem de commit** (estruturada? clara?)
- [ ] **Arquivos afetados** (escopo correto?)
- [ ] **YAML frontmatter** (válido? completo?)
- [ ] **APPROVAL_LOG.md** (atualizado? sem TBD?)
- [ ] **Estatísticas** (totais corretos?)
- [ ] **Referências** (links não quebrados?)
- [ ] **Governança** (conforme ENDFIRST_DOCUMENT_GOVERNANCE?)
- [ ] **Histórico** (mudanças registradas?)

**Ferramenta:** `COMMIT_GOVERNANCE_CHECKLIST.md`

**Resultado:** Parecer estruturado

---

### Passo 4: Manus Entrega Veredito
**Responsável:** Manus  
**Ação:** Entrega parecer no formato:

```markdown
## COMMIT: [HASH]
**STATUS:** ✅ CONFORME | ⚠️ QUASE | ❌ NÃO CONFORME

### Análise

**Diff:**
- ✅ ok / ❌ problema X

**Mensagem:**
- ✅ ok / ❌ problema Y

**Governança:**
- ✅ ok / ❌ violação Z

**Risco atual:**
- 🟢 Baixo / 🟡 Médio / 🔴 Alto

### Decisão Recomendada
- Manter como está
- Documentar como legado
- Criar correção (novo commit)

### Justificativa
(Explicação estrutural da recomendação)
```

**Resultado:** CEO tem parecer completo

---

### Passo 5: CEO Dá Aprovação Final
**Responsável:** CEO  
**Ação:** Decide:

- ✅ **Aprovar** → Commit vira oficial
- ⚠️ **Aprovar com ressalvas** → Commit vira legado
- ❌ **Rejeitar** → Criar commit de correção

**Resultado:** Status final do commit é definido

---

## 📋 FORMATO CANÔNICO DO PARECER

Todo parecer de revisão DEVE seguir este formato:

```markdown
# REVISÃO DE COMMIT — [HASH]

**Data:** [YYYY-MM-DD]  
**Commit:** [HASH]  
**Link:** https://github.com/Joubertjr/endfirst-ecosystem/commit/[HASH]  
**Revisor:** Manus (Agent AI)  
**Checklist:** COMMIT_GOVERNANCE_CHECKLIST.md

---

## 📋 CHECKLIST DE CONFORMIDADE

### ✅ 1. Diff Linha por Linha
**Status:** ✅ CONFORME / ⚠️ RESSALVAS / ❌ NÃO CONFORME

**Verificação:**
(Análise detalhada)

**Resultado:** (Conclusão)

---

### ✅ 2. Mensagem de Commit
**Status:** ✅ CONFORME / ⚠️ RESSALVAS / ❌ NÃO CONFORME

**Verificação:**
(Análise detalhada)

**Resultado:** (Conclusão)

---

(... repetir para todos os 9 itens do checklist)

---

## 📊 VEREDITO FINAL

**Status:** ✅ CONFORME / ⚠️ CONFORME COM RESSALVAS / ❌ NÃO CONFORME

**Risco atual:** 🟢 Baixo / 🟡 Médio / 🔴 Alto

**Decisão recomendada:**
- [ ] Manter como está
- [ ] Documentar como legado
- [ ] Criar correção (novo commit)

**Justificativa:**
(Explicação estrutural)

---

**Versão:** 1.0  
**Data:** [YYYY-MM-DD]  
**Revisado por:** Manus (Agent AI)  
**Aprovado por:** (aguardando CEO)
```

---

## 🚫 ANTI-PADRÕES (PROIBIDOS)

### ❌ Revisão sem Checklist
**Proibido:** Revisar commit sem aplicar COMMIT_GOVERNANCE_CHECKLIST

**Motivo:** Perde itens críticos

**Consequência:** Revisão inválida

---

### ❌ Auto-aprovação
**Proibido:** Manus aprovar commit que fez

**Motivo:** Conflito de interesse

**Consequência:** Aprovação inválida

---

### ❌ Aprovação sem Parecer
**Proibido:** CEO aprovar sem ler parecer de Manus

**Motivo:** Perde contexto técnico

**Consequência:** Risco sistêmico

---

### ❌ Cursor em Revisão
**Proibido:** Cursor participar de revisão de governança

**Motivo:** Papel errado

**Consequência:** Decisão inválida

---

### ❌ Commit não Revisado
**Proibido:** Commit existir sem status de revisão

**Motivo:** Risco sistêmico desconhecido

**Consequência:** Governança incompleta

---

## 🎯 CLASSIFICAÇÃO DE COMMITS

### ✅ CONFORME
**Definição:** Commit atende 100% do checklist

**Ação:** Manter como está

**Risco:** 🟢 Baixo

---

### ⚠️ CONFORME COM RESSALVAS
**Definição:** Commit tem problemas menores ou é legado pré-governança

**Ação:** Documentar como legado, não corrigir

**Risco:** 🟡 Médio (aceitável)

**Exemplo:** Commits anteriores à criação da governança formal

---

### ❌ NÃO CONFORME
**Definição:** Commit viola regras críticas

**Ação:** Criar commit de correção imediata

**Risco:** 🔴 Alto (inaceitável)

**Exemplo:** TBD presente, contagem fantasma, referências quebradas

---

## 📊 MÉTRICAS DE SAÚDE

### Commits Revisados
**Meta:** 100% dos commits têm status de revisão

**Cálculo:** `(commits revisados / commits totais) * 100`

**Status atual:** Verificar em APPROVAL_LOG.md

---

### Taxa de Conformidade
**Meta:** >80% dos commits CONFORMES

**Cálculo:** `(commits conformes / commits revisados) * 100`

**Interpretação:**
- **>80%:** 🟢 Sistema saudável
- **60-80%:** 🟡 Atenção necessária
- **<60%:** 🔴 Sistema em risco

---

### Tempo de Revisão
**Meta:** <24h entre commit e revisão

**Cálculo:** `data_revisao - data_commit`

**Interpretação:**
- **<24h:** 🟢 Rápido
- **24-72h:** 🟡 Aceitável
- **>72h:** 🔴 Lento (risco de acúmulo)

---

## 🔄 REVISÃO DE COMMITS HISTÓRICOS

### Escopo
**Todos os commits existentes devem ser revisados**, incluindo:
- Commits recentes (pós-governança)
- Commits antigos (pré-governança)
- Commits de correção
- Commits de merge

**Regra:** Nada fica "não revisado".

---

### Processo para Commits Antigos

1. **Identificar commits pré-governança**
   - Commits antes de 30a7081 (Governança v1.0)

2. **Revisar usando checklist atual**
   - Aplicar COMMIT_GOVERNANCE_CHECKLIST.md
   - Mesmo que commit seja anterior à criação do checklist

3. **Classificar adequadamente**
   - ✅ CONFORME (se atende checklist)
   - ⚠️ CONFORME COM RESSALVAS (legado)
   - ❌ NÃO CONFORME (se viola regras críticas)

4. **Documentar decisão**
   - Registrar status em documento de revisão
   - Justificar classificação (especialmente "legado")

5. **Não reescrever história**
   - Commits antigos não são corrigidos
   - São apenas classificados e documentados

**Objetivo:** Tornar estado atual 100% compreendido, não reescrever passado.

---

## 📜 DECLARAÇÃO

**Todo commit tem status de revisão explícito.**

**Nenhum commit é "autoaprovado".**

**Manus recomenda. CEO decide.**

---

**Versão:** 1.0  
**Data:** 8 de Janeiro de 2026  
**Aprovado por:** CEO  
**Governado por:** /METODO/ROLES_AND_RESPONSIBILITIES.md
