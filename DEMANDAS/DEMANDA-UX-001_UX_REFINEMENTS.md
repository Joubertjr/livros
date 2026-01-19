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
- Resultados apresentados de forma mais legível e orientada a leitura
- UX consistente com o valor do produto: confiança, rastreabilidade, clareza
- Usuário nunca vê IDs técnicos, hashes ou marcadores internos
- Usuário nunca fica em dúvida se o sistema está funcionando
- Nenhum elemento da UI gera a pergunta: "isso é bug ou comportamento esperado?"
- Todo bloco com conteúdo é visualmente legível sem interação oculta
- Layout se adapta ao conteúdo (altura automática)
- Leitura é possível sem scroll oculto ou descoberta acidental
- Progresso comunica atividade contínua mesmo em etapas longas

**⚠️ Importante:**
Este END não altera funcionalidade, apenas forma de apresentação e experiência.

---

## ✅ Critérios de Aceitação (Binários)

### PASS
- ✅ Usuário entende o que está vendo sem explicação externa
- ✅ Nenhum texto técnico desnecessário exposto ao usuário final
- ✅ Estados vazios e mensagens fazem sentido
- ✅ Interface continua funcional (Gate Z11 continua PASS)
- ✅ Nenhuma regressão funcional (Z0–Z11 continuam PASS)
- ✅ Evidência UX gerada (prints ou PDF em `/EVIDENCIAS/ux/`)

### FAIL (Automático)
- ❌ UX alterada sem F-1 aprovada
- ❌ UI "mais bonita" mas menos clara
- ❌ Qualquer regressão funcional
- ❌ Gate Z11 quebrado
- ❌ Correção aplicada "direto no código" sem planejamento
- ❌ Marcadores técnicos internos ([[RS:...]] ou similares) aparecem para o usuário
- ❌ IDs de chunk, hashes, referências internas ou artefatos de rastreabilidade aparecem na UI
- ❌ Blocos possuem conteúdo invisível ou cortado
- ❌ Blocos que não expandem conforme o conteúdo
- ❌ Usuário precisa usar scroll oculto para descobrir conteúdo
- ❌ Métricas exibidas confundem sem explicação contextual
- ❌ Métricas exibidas sem contexto semântico
- ❌ Progresso parece travado durante execução longa
- ❌ Usuário não sabe se o sistema está funcionando

---

## 🧠 Problemas Observados (Contexto)

Estes itens **NÃO são tarefas**, são sinais de oportunidade**:

- "Original – 0 palavras" pode confundir usuários não técnicos
- Métricas e rastreabilidade são poderosas, mas podem ser melhor explicadas
- Resultado é correto, mas pode ser mais legível
- Falta hierarquia visual clara entre:
  - resumo
  - capítulos
  - evidências
- UX atual é "engenharia-first", não "leitor-first"

### A) Ruído Técnico Vazando para Usuário Final
- O resumo exibido ao usuário contém marcadores técnicos internos como:
  `[[RS:capX:hash|chunks:Y]]`
- Esses identificadores são artefatos de rastreabilidade interna
- Usuário final **NÃO deve ver** referências técnicas ou IDs de chunk
- IDs de chunk, hashes, referências internas ou artefatos de rastreabilidade aparecem na UI

➡️ **Frase canônica:**
"Usuário final nunca deve ver IDs técnicos, hashes ou marcadores internos.
Qualquer ocorrência disso é FAIL de UX."

### B) Métricas Semanticamente Confusas
- A UI exibe "Original – 0 palavras" para capítulos
- Isso é tecnicamente verdadeiro, mas semanticamente confuso
- Usuário não consegue distinguir se é bug, erro de processamento ou comportamento esperado

➡️ **Frase canônica:**
"Métrica correta mas semanticamente ambígua é FAIL de clareza de UX."

### C) Blocos com Conteúdo Invisível ou Área Travada (BUG DE UX)
- Blocos como "Coverage & Evidence" e "Confiabilidade do Resumo":
  - Possuem conteúdo interno
  - Não expandem verticalmente conforme o conteúdo
  - Cortam informação ou exigem scroll oculto
- Usuário **NÃO consegue saber** o que existe dentro do bloco

➡️ **Frase canônica obrigatória:**
"Todo bloco com conteúdo deve expandir verticalmente conforme o conteúdo.
Conteúdo invisível, cortado ou acessível apenas por scroll oculto é FAIL."

### D) Feedback Insuficiente Durante Execuções Longas (SSE)
- Durante execuções longas (~15 minutos):
  - Progresso visual pode ficar estático (ex.: 35%)
  - Backend continua ativo via keepalive SSE
  - Usuário não sabe se o sistema travou ou está processando
- Console mostra atividade, mas UI não comunica progresso perceptível

➡️ **Frase canônica:**
"UX deve comunicar atividade contínua perceptível durante etapas longas,
mesmo quando o percentual não muda."

**⚠️ Nenhum desses pontos é bug funcional.**  
São problemas de experiência do usuário que precisam ser refinados.

---

## 🚫 DO / DON'T

### DO
- ✅ Melhorar clareza textual
- ✅ Melhorar hierarquia visual
- ✅ Melhorar feedback ao usuário
- ✅ Manter rastreabilidade explícita
- ✅ Manter todos os gates PASS

### DON'T
- ❌ Alterar pipeline
- ❌ Alterar lógica de sumarização
- ❌ "Simplificar" removendo garantias
- ❌ Refatorar backend
- ❌ Quebrar Gate Z11

---

## 🧱 Bloqueios Estruturais
- 🔒 F-1 obrigatório (demanda de produto)
- 🔒 Gate Z11 continua bloqueante
- 🔒 Nenhuma alteração sem evidência visual
- 🔒 UX ≠ estética → UX = clareza + confiança

---

## 📋 TODO Canônico (Somente Após F-1 Aprovada)
1. F-1: Planejamento Canônico (UX)
2. Definir mudanças de texto/labels
3. Definir melhorias visuais (layout, espaçamento, hierarquia)
4. Implementar mudanças mínimas
5. Gerar evidência UX obrigatória (prints ou PDF em `/EVIDENCIAS/ux/`)
6. Validar Z11 novamente (Gate Z11 continua bloqueante após qualquer alteração de UX)
7. Declarar PASS

---

## ❌ Fora de Escopo
- Novas features
- Performance
- Mudanças no modelo
- Alterações no pipeline
- Refatorações estruturais

---

## 📌 Status

**BACKLOG**

Este arquivo não autoriza execução.

Só pode ser executado após:
- Priorização explícita
- F-1 aprovada
- Ordem clara do CEO

---

## 🧭 Regra Final

**Produto já funciona.**  
Esta demanda existe para eliminar confusão, não para mudar lógica, pipeline ou garantias.
