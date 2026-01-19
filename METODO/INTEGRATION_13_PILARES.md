---
document_id: INTEGRATION_13_PILARES
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-07
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.0
created_at: 2026-01-07
---

# INTEGRAÇÃO — Pilar ENDFIRST vs 13 Pilares

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Governado por:** PILAR_ENDFIRST.md  
**Status:** Operacional (Aprovado pelo CEO)

---

## 🎯 OBJETIVO

Este documento resolve o conflito entre dois sistemas metodológicos que coexistiam no repositório:

1. **Sistema Antigo:** "13 Pilares ENDFIRST" (criado em 04/01/2026)
2. **Sistema Novo:** "Pilar ENDFIRST" (criado em 07/01/2026)

**Decisão CEO:**
> Pilar ENDFIRST governa tudo. "13 Pilares" vira backlog/conteúdo futuro, não verdade atual.

---

## 📊 ESTADO ANTES DA INTEGRAÇÃO

### Sistema Antigo (04/01/2026)

**Conceito:** "13 Pilares ENDFIRST"  
**Descrição:** Método operacional para gestão de projetos baseado em 13 pilares fundamentais.

**Pilares:**
1. Pilar 0: Resultado Esperado
2. Pilar 1: Obstáculos
3. Pilar 1.5: Modelos Mentais
4. Pilar 2: Recursos
5. Pilar 3: Calibração
6. Pilar 3.5: Gestão de Projetos
7. Pilar 4: Caminho Reverso
8. Pilar 5: Validação Externa
9. Pilar 6: Execução
10. Pilar 6.5: Processos
11. Pilar 7: Aprendizados
12. Pilar 8: Comunicação
13. Pilar 11: Comunicação Eficaz

**Template:** `TEMPLATE_DEMANDA.md` (baseado em 8 pilares: 0-8)

**Documentos:**
- `README.md` (raiz) — Define ecossistema baseado em 13 pilares
- `TEMPLATE_DEMANDA.md` — Template de demanda com 8 pilares
- `DEMANDA_001_DOCUMENTAR_13_PILARES.md` — Demanda para documentar os 13 pilares

**Status:** Criado antes do Pilar ENDFIRST existir.

---

### Sistema Novo (07/01/2026)

**Conceito:** "Pilar ENDFIRST" (meta-pilar)  
**Descrição:** Sistema de tradução governada de intenção difusa → resultado explícito, verificável e versionável.

**Mecanismo:** 6 Perguntas + 11 Bloqueios (B1-B11)

**Template:** `ENDFIRST_SPEC.md`

**Documentos:**
- `PILAR_ENDFIRST.md` — Fonte soberana de verdade
- `ENDFIRST_SPEC.md` — Template oficial
- `ENDFIRST_SPEC_EF-2026-001.md` — Exemplo real (LLM Orchestrator)
- `ENDFIRST_PROCESS.md` — Processo humano de 30 segundos
- `DEMANDA-001_LLM_ORCHESTRATOR.md` — Demanda oficial

**Status:** Criado e validado pelo CEO (Declaração Final de Passagem).

---

## 🔗 RELAÇÃO ENTRE OS SISTEMAS

### Decisão Estrutural

**Pilar ENDFIRST governa tudo.**

**Relação:**
- **Pilar ENDFIRST** → Define **COMO** criar especificações (meta-pilar, soberano)
- **13 Pilares** → Define **O QUE** incluir nas demandas (método operacional, subordinado)

**Hierarquia:**
```
PILAR_ENDFIRST.md (meta-pilar, soberano)
    ↓ governa
ENDFIRST_SPEC.md (template de especificação)
    ↓ pode usar
TEMPLATE_DEMANDA.md (template operacional com 8 pilares)
    ↓ cria
DEMANDA_XXX.md (demandas operacionais)
```

---

## 📋 CONSEQUÊNCIAS PRÁTICAS

### 1. Template de Demandas

**`TEMPLATE_DEMANDA.md` continua válido** para demandas operacionais.

**Quando usar:**
- Demandas táticas (implementação, execução)
- Demandas que já têm resultado claro
- Demandas dentro de escopo conhecido

**Exemplo:** "Implementar Pilar 0 - Resultado Esperado" (demanda tática)

---

### 2. ENDFIRST_SPEC

**`ENDFIRST_SPEC.md` é obrigatório** para demandas estratégicas.

**Quando usar:**
- Demandas estratégicas (novos produtos, novos processos)
- Demandas com resultado ambíguo
- Demandas que impactam governança

**Exemplo:** "Criar sistema de governança documental" (demanda estratégica)

---

### 3. Documentação dos 13 Pilares

**Status:** Backlog futuro (não verdade atual).

**O que significa:**
- Os 13 pilares **existem conceitualmente**
- Mas **não estão documentados oficialmente** ainda
- `DEMANDA_001_DOCUMENTAR_13_PILARES.md` permanece no backlog
- Quando for executada, deve passar pelo Pilar ENDFIRST primeiro

**Ação futura:**
1. Criar ENDFIRST_SPEC para "Documentar 13 Pilares"
2. Validar com CEO (Declaração Final de Passagem)
3. Implementar documentação
4. Cada pilar vira documento oficial

---

## 🎯 REGRAS DE USO

### Regra 1: Pilar ENDFIRST é soberano

**Toda demanda estratégica** deve passar pelo Pilar ENDFIRST antes de entrar no sistema.

**Bloqueio:** Não pode criar demanda estratégica sem ENDFIRST_SPEC.

---

### Regra 2: Template de Demanda é subordinado

**`TEMPLATE_DEMANDA.md`** pode ser usado para demandas táticas, mas:
- Não substitui ENDFIRST_SPEC para demandas estratégicas
- Não governa outros documentos
- É um template operacional, não canônico

---

### Regra 3: 13 Pilares são conteúdo, não método

**Os 13 pilares** são conteúdo a ser documentado, não o método de documentação.

**Método de documentação:** Pilar ENDFIRST (6 Perguntas + 11 Bloqueios)

---

## 📊 MAPEAMENTO: 8 Pilares → ENDFIRST_SPEC

Como os "8 pilares" do `TEMPLATE_DEMANDA.md` se mapeiam para o `ENDFIRST_SPEC.md`:

| Pilar (Template Antigo) | Pergunta/Bloqueio (ENDFIRST_SPEC) |
|-------------------------|------------------------------------|
| Pilar 0: Resultado Esperado | Pergunta 2: Resultado estrutural (5 verdades) |
| Pilar 1: Obstáculos | Pergunta 2: Formas de falha |
| Pilar 2: Recursos | Pergunta 6: Dependências |
| Pilar 3: Calibração | Pergunta 2: Gap (estado atual vs desejado) |
| Pilar 4: Caminho Reverso | Pergunta 4: Critérios de aceitação |
| Pilar 5: Validação Externa | Pergunta 11: Declaração Final de Passagem |
| Pilar 6: Execução | (Fora do escopo da Spec — vira DEMANDA depois) |
| Pilar 7: Aprendizados | (Fora do escopo da Spec — vira retrospectiva depois) |
| Pilar 8: Comunicação | Pergunta 9: Alinhamento hierárquico |

**Observação:** ENDFIRST_SPEC é mais rigoroso (11 bloqueios vs 8 pilares).

---

## 🚫 O QUE NÃO FAZER

### ❌ Não criar "dois sistemas paralelos"

**Errado:** Usar ENDFIRST_SPEC para alguns projetos e TEMPLATE_DEMANDA para outros sem critério claro.

**Certo:** Usar ENDFIRST_SPEC para estratégico, TEMPLATE_DEMANDA para tático.

---

### ❌ Não ignorar sistema antigo

**Errado:** Deletar `TEMPLATE_DEMANDA.md` e `DEMANDA_001`.

**Certo:** Manter templates antigos, mas subordinados ao Pilar ENDFIRST.

---

### ❌ Não fingir que 13 Pilares estão documentados

**Errado:** Referenciar "Pilar 3.5" como se estivesse documentado oficialmente.

**Certo:** Referenciar conceito de "Gestão de Projetos" e adicionar nota: "(Pilar 3.5 — a documentar)".

---

## 📜 DECLARAÇÃO FINAL

**Este documento resolve o conflito entre os dois sistemas.**

**Decisão CEO:**
> Pilar ENDFIRST governa tudo. "13 Pilares" vira backlog/conteúdo futuro, não verdade atual.

**Consequências:**
- ✅ ENDFIRST_SPEC é obrigatório para demandas estratégicas
- ✅ TEMPLATE_DEMANDA continua válido para demandas táticas
- ✅ Documentação dos 13 Pilares permanece no backlog
- ✅ Não há mais "dois sistemas" — há hierarquia clara

**Status:** Integração completa e aprovada.

---

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Próximo passo:** Atualizar README raiz para refletir esta integração
