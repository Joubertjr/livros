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

**⚠️ Nenhum desses pontos é bug.**  
São refinamentos, não correções.

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
5. Gerar evidência UX (prints/PDF)
6. Validar Z11 novamente
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
Esta demanda existe para refinar a experiência, não para "consertar".
