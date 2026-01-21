# ORDENS AO CURSOR — EXECUÇÃO DEMANDA-PROD-004

**Data:** 2026-01-21  
**Status:** ✅ ATIVO  
**F-1:** APROVADA (2026-01-21 - CEO)

---

## 🚦 AUTORIZAÇÃO FORMAL

**"Cursor: a DEMANDA-PROD-004 está com F-1 APROVADA.
Execute estritamente o TODO F0–F9 do planejamento canônico.
Não pule fases.
Não implemente nada fora do escopo.
Toda prova deve ser registrada conforme definido."**

---

## 📋 TODO CANÔNICO (F0-F9)

### F0 — Revisar Plano (BLOQUEANTE — SEM EXECUÇÃO)

**END:** Plano aprovado e pronto para execução

**DONE WHEN:**
- Checklist completo verificado
- Nenhum comando executado
- Nenhum código alterado
- Declaração explícita: "F-1 aprovada" ✅

**STATUS:** ✅ COMPLETA — F-1 aprovada e pronta para execução F1-F9

---

### F1 — Definir "Valor Cognitivo Persistente"

**END:** Definição clara e verificável do que constitui "valor cognitivo persistente"

**AÇÃO:**
- Lista explícita de artefatos que são "valor cognitivo"
- Distinção clara entre processamento transitório e valor persistente
- Documentação da definição

**PROVA:** Verificar que definição existe e está documentada

---

### F2 — Definir Pontos Mínimos de Persistência Incremental

**END:** Pontos de checkpoint definidos onde valor cognitivo deve ser persistido

**AÇÃO:**
- Lista de pontos de checkpoint
- Frequência mínima de persistência
- Critério de "ponto válido"

**PROVA:** Verificar que pontos de checkpoint estão documentados

---

### F3 — Definir Contrato de Retomada Segura

**END:** Contrato explícito de como o sistema retoma execução a partir de um checkpoint

**AÇÃO:**
- Formato de checkpoint
- Identificação de checkpoint válido
- Lógica de retomada
- Tratamento de checkpoint inválido

**PROVA:** Verificar que contrato está documentado

---

### F4 — Ajustar Pipeline para Respeitar Contrato de Persistência

**END:** Pipeline modificado para persistir valor cognitivo nos pontos definidos

**AÇÃO:**
- Pipeline identifica pontos de checkpoint
- Pipeline persiste valor cognitivo em cada checkpoint
- Persistência é atômica
- Validação de checkpoint após persistência

**PROVA:** Verificar que pipeline tem lógica de persistência progressiva

---

### F5 — Expor Inspeção de Progresso/Resultados Parciais

**END:** Sistema expõe API/interface para inspecionar progresso e resultados parciais

**AÇÃO:**
- Endpoint/interface para consultar progresso
- Endpoint/interface para consultar resultados parciais
- Resposta inclui status, checkpoints, resultados parciais

**PROVA:** Verificar que API expõe progresso

---

### F6 — Garantir Histórico de Execuções

**END:** Todas as execuções ficam disponíveis para consulta posterior

**AÇÃO:**
- Execuções identificadas unicamente
- Histórico consultável
- Cada execução mantém status, checkpoints, resultados, timestamps

**PROVA:** Verificar que histórico é consultável

---

### F7 — Gerar Evidência de Falha sem Perda de Progresso

**END:** Sistema gera evidência de que falha não apaga progresso já persistido

**AÇÃO:**
- Teste que simula falha durante execução longa
- Teste valida que progresso não se perde
- Teste valida que retomada não reprocessa
- Evidência documentada

**PROVA:** Executar teste de falha sem perda de progresso

---

### F8 — Validar Gate Z10 (Robustez + Persistência)

**END:** Gate Z10 validado com provas mínimas de robustez

**AÇÃO:**
- Testes de robustez implementados
- Todos os testes passam
- Evidência de Gate Z10 gerada

**PROVA:** Validar Gate Z10

---

### F9 — Validar Gate Z11 e Declarar PASS

**END:** Gate Z11 validado e demanda declarada como PASS

**AÇÃO:**
- Gate Z11 continua PASS
- Todos os critérios de aceitação atendidos
- Evidência completa gerada
- Declaração explícita: "DEMANDA-PROD-004: PASS"

**PROVA:** Validar Gate Z11

---

## 🚫 REGRAS OBRIGATÓRIAS

- ❌ Não pular fases
- ❌ Não implementar fora do escopo
- ❌ Não executar sem prova registrada
- ✅ Seguir TDD rigorosamente (teste antes de código)
- ✅ Aplicar Gate Z10 (obrigatório para Classe A)
- ✅ Manter Gate Z11 PASS

---

## 📌 STATUS ATUAL

**F-1:** ✅ APROVADA  
**Próxima Fase:** F1 (Definir "Valor Cognitivo Persistente")  
**Executor:** Cursor  
**Método:** END-FIRST v2

---

**Documento criado:** 2026-01-21  
**Última atualização:** 2026-01-21  
**Governado por:** END-FIRST v2
