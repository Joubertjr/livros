# DEMANDA-UX-001 — UX REFINEMENTS (CoverageSummarizer / livros)

**Tipo:** Produto / UX  
**Método:** END-FIRST v2  
**Status:** BACKLOG (NÃO EXECUTAR)  
**Projeto:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado (UX Refinada)

Para um usuário final acessando `http://localhost:8000/`:
- Interface claramente compreensível sem contexto técnico
- Nenhum rótulo ambíguo ou confuso
- Feedback visual claro de estados:
  - carregando
  - sucesso
  - erro
- Resultados apresentados de forma legível e orientada à leitura
- UX consistente com o valor do produto: confiança, rastreabilidade e clareza
- Usuário **NUNCA** vê:
  - IDs técnicos
  - hashes
  - marcadores internos
  - artefatos de engenharia
- Todo conteúdo é imediatamente visível
- Layout expande verticalmente conforme o conteúdo
- Scroll interno é proibido
- Progresso comunica atividade contínua perceptível, mesmo em etapas longas
- Nenhum elemento da UI gera dúvida do tipo: "isso é bug ou comportamento esperado?"

**⚠️ Importante:**
Este END não altera funcionalidade, apenas forma de apresentação e experiência.

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS — NÃO NEGOCIÁVEIS)

Estas frases são canônicas, reutilizáveis e bloqueantes:

### Legibilidade
"Se o usuário não vê o conteúdo imediatamente, o produto falhou."

### Scroll
"Scroll interno é bug estrutural, não escolha de UX."

### Ruído Técnico
"Usuário final nunca deve ver artefatos internos de engenharia."

### Progresso
"UX deve comunicar atividade contínua perceptível durante etapas longas, mesmo quando o percentual não muda."

### Semântica
"Métrica correta mas semanticamente ambígua é FAIL de UX."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## 🚫 REGRA CANÔNICA — LEGIBILIDADE (NÃO NEGOCIÁVEL)

**Scroll interno é PROIBIDO.**
- Nenhum componente da UI pode usar scroll interno
- Todo bloco deve expandir verticalmente conforme o conteúdo
- Conteúdo oculto, cortado ou acessível apenas via scroll é BUG de produto

Scroll interno, overflow oculto ou "ver mais" para descobrir conteúdo não são UX refinements.

---

## ✅ CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)

### PASS
- ✅ Usuário entende o que está vendo sem explicação externa
- ✅ Nenhum texto técnico desnecessário exposto ao usuário final
- ✅ Nenhum identificador técnico interno visível ([[RS:...]], hashes, IDs, chunks, markers)
- ✅ Todo conteúdo visível sem scroll interno
- ✅ Blocos expandem automaticamente conforme o conteúdo
- ✅ Estados vazios e mensagens fazem sentido
- ✅ Progresso comunica atividade contínua durante execuções longas
- ✅ Interface continua funcional (Gate Z11 permanece PASS)
- ✅ Nenhuma regressão funcional (Z0–Z11 continuam PASS)
- ✅ Evidência UX gerada (prints ou PDF em `/EVIDENCIAS/ux/`)

### FAIL (AUTOMÁTICO)
- ❌ UX alterada sem F-1 aprovada
- ❌ UI "mais bonita" porém menos clara
- ❌ Qualquer regressão funcional
- ❌ Gate Z11 quebrado
- ❌ Correção aplicada direto no código sem planejamento
- ❌ Marcadores técnicos internos visíveis ao usuário final
- ❌ Conteúdo oculto, cortado ou acessível apenas via scroll interno
- ❌ Usuário precisa "descobrir" que existe conteúdo escondido
- ❌ Métricas corretas porém semanticamente confusas sem explicação
- ❌ Progresso parece travado durante execução longa
- ❌ Usuário não sabe se o sistema está funcionando

---

## 🧠 PROBLEMAS OBSERVADOS (EVIDÊNCIA — NÃO SÃO TAREFAS)

### A) Vazamento de Ruído Técnico
- Resumo exibe marcadores como `[[RS:capX:hash|chunks:Y]]`
- São artefatos de rastreabilidade interna
- Usuário final **NÃO deve vê-los**

➡️ **Regra canônica aplicada:**
"Usuário final nunca deve ver artefatos internos de engenharia."

---

### B) Métrica Semanticamente Confusa
- UI exibe "Original – 0 palavras"
- Tecnicamente correto, semanticamente confuso
- Usuário não sabe se é bug ou comportamento esperado

➡️ **Regra canônica aplicada:**
"Métrica correta mas semanticamente ambígua é FAIL de UX."

---

### C) Conteúdo Invisível / Blocos Travados (BUG)
- Blocos como "Coverage & Evidence" possuem conteúdo
- Área não expande
- Conteúdo fica invisível ou cortado

➡️ **Regra canônica aplicada:**
"Scroll interno é bug estrutural."

---

### D) Feedback Insuficiente em Execuções Longas
- Execuções longas (~15 min)
- Percentual fica parado (ex.: 35%)
- Backend ativo via SSE keepalive
- UI não comunica atividade perceptível

➡️ **Regra canônica aplicada:**
"UX deve comunicar atividade contínua perceptível mesmo quando o percentual não muda."

---

## 🚫 DO / DON'T

### DO
- ✅ Melhorar clareza textual
- ✅ Melhorar hierarquia visual
- ✅ Melhorar feedback perceptível ao usuário
- ✅ Manter rastreabilidade interna, sem vazar para UI
- ✅ Manter todos os gates PASS

### DON'T
- ❌ Alterar pipeline
- ❌ Alterar lógica de sumarização
- ❌ "Simplificar" removendo garantias
- ❌ Refatorar backend
- ❌ Introduzir scroll interno
- ❌ Quebrar Gate Z11

---

## 🧱 BLOQUEIOS ESTRUTURAIS
- 🔒 F-1 obrigatório (demanda de produto)
- 🔒 Gate Z11 continua bloqueante
- 🔒 Nenhuma alteração sem evidência visual
- 🔒 UX ≠ estética → UX = clareza + confiança
- 🔒 Scroll interno = BUG estrutural

---

## 📋 TODO CANÔNICO (SOMENTE APÓS F-1 APROVADA)
1. F-1: Planejamento Canônico (UX)
2. Definir mudanças de texto e labels
3. Definir melhorias visuais (layout, espaçamento, hierarquia)
4. Implementar mudanças mínimas
5. Garantir ausência total de scroll interno
6. Gerar evidência UX (prints/PDF)
7. Validar Gate Z11 novamente
8. Declarar PASS

---

## ❌ FORA DE ESCOPO
- Novas features
- Performance
- Mudanças no modelo
- Alterações no pipeline
- Refatorações estruturais

---

## 📌 STATUS

**BACKLOG**

Este arquivo **NÃO autoriza execução**.

Só pode ser executado após:
- Priorização explícita
- F-1 aprovada
- Ordem clara do CEO

---

## 🧭 REGRA FINAL

**Produto já funciona.**  
Esta demanda existe para eliminar confusão, não para mudar lógica.

**"Se o usuário precisa rolar um bloco para descobrir conteúdo, o produto falhou."**
