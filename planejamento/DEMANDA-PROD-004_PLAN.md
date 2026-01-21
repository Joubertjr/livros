# PLANEJAMENTO CANÔNICO — DEMANDA-PROD-004: PERSISTÊNCIA PROGRESSIVA E RETOMADA SEGURA

**Demanda:** DEMANDA-PROD-004_PERSISTENCIA_PROGRESSIVA_RETOMADA_SEGURA.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-21  
**Status:** ⏸️ F-1 PENDENTE APROVAÇÃO  
**Classe:** A (Execução Longa + Streaming + Persistência + Retomada)  
**Z10 Obrigatório:** ✅ SIM  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado

Para qualquer execução de resumo (PDF, livro ou texto longo):

- Todo valor cognitivo gerado pelo sistema é persistido progressivamente
- Nenhuma falha técnica, desconexão ou erro parcial faz o sistema:
  - perder trabalho já executado
  - exigir reprocessamento de etapas concluídas
- O usuário (ou sistema) consegue:
  - inspecionar o progresso já realizado
  - retomar a execução a partir do último ponto válido
  - validar partes do resumo sem esperar o fim do processamento
- O sistema consegue responder objetivamente, a qualquer momento:
  **"O que já foi feito, está salvo e é reaproveitável?"**

### 📌 Resumo do END:

**"Se o sistema produziu valor cognitivo, esse valor não se perde."**

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS — NÃO NEGOCIÁVEIS)

Estas frases são canônicas, reutilizáveis e bloqueantes:

- **Valor:** "Valor cognitivo produzido não é descartável."
- **Execução longa:** "Execução longa sem persistência progressiva é desperdício estrutural."
- **Falha:** "Falha não pode apagar história."
- **Retomada:** "Retomar não é recomeçar."
- **END-FIRST:** "END não é só o final; END é o que permanece."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## ✅ CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)

### PASS

- ✅ O sistema persiste resultados intermediários relevantes do resumo
- ✅ Progresso já executado não se perde em caso de falha
- ✅ Existe distinção clara entre:
  - processamento transitório
  - valor cognitivo persistente
- ✅ O sistema permite inspeção de resultados parciais
- ✅ Retomada não exige reprocessamento do que já foi concluído
- ✅ Execuções anteriores ficam disponíveis para consulta
- ✅ END é verificável antes do término total do processo
- ✅ Gate Z10 aplicado (execução longa + persistência)
- ✅ Gate Z11 continua PASS
- ✅ Evidência gerada em `/EVIDENCIAS/produto/`

### FAIL (AUTOMÁTICO)

- ❌ Falha apaga progresso já produzido
- ❌ Persistência só ocorre no final
- ❌ Retomar execução implica reprocessar etapas concluídas
- ❌ "Salvar tudo no final" tratado como suficiente
- ❌ Persistência validada apenas no caminho feliz
- ❌ Histórico inexistente ou inconsistente
- ❌ END só é observável no final da execução
- ❌ Qualidade tratada como opcional

---

## 🚫 DO / DON'T

### DO (Fazer)

**Durante Planejamento (F-1):**
- ✅ Criar este documento de planejamento
- ✅ Definir TODO canônico
- ✅ Definir escopo DO/DON'T
- ✅ Definir ordem de execução
- ✅ Definir critérios de FAIL
- ✅ Definir strings de prova
- ✅ Aguardar aprovação explícita ("F-1 aprovada")

**Durante Execução (após F-1 aprovada):**
- ✅ Definir o que é "valor cognitivo persistente"
- ✅ Definir pontos mínimos de persistência incremental
- ✅ Definir contrato de retomada segura
- ✅ Ajustar pipeline para respeitar o contrato
- ✅ Expor inspeção de progresso/resultados parciais
- ✅ Garantir histórico de execuções
- ✅ Gerar evidência de falha sem perda de progresso
- ✅ Validar Gates (Z10, Z11)
- ✅ Seguir TDD rigorosamente (teste antes de código)
- ✅ Aplicar Gate Z10 (provas mínimas de robustez)

### DON'T (Não Fazer)

**Durante Planejamento (F-1):**
- ❌ Executar comandos
- ❌ Criar código
- ❌ Criar testes
- ❌ "Validar rapidamente"
- ❌ Interpretar regras durante execução

**Durante Execução:**
- ❌ Persistir apenas no final
- ❌ Permitir perda de progresso em caso de falha
- ❌ Exigir reprocessamento ao retomar
- ❌ Validar persistência apenas no caminho feliz
- ❌ Tratar qualidade como opcional
- ❌ Ignorar Gate Z10 (obrigatório para Classe A)
- ❌ Quebrar Gate Z11

---

## 🧱 BLOQUEIOS ESTRUTURAIS

- 🔒 F-1 obrigatório (demanda de execução longa) — **ESTE DOCUMENTO**
- 🔒 Gate Z10 obrigatório (robustez + persistência) — **Classe A**
- 🔒 Nenhuma perda de valor cognitivo é aceitável
- 🔒 END-FIRST v2 continua governando
- 🔒 Evidência obrigatória antes de declarar PASS
- 🔒 TDD obrigatório (teste antes de código)

---

## 📋 TODO CANÔNICO (F0-F9)

### F0 — Revisar Plano (BLOQUEANTE — SEM EXECUÇÃO)

**END:** Plano aprovado e pronto para execução

**DONE WHEN:**
- Checklist completo verificado
- Nenhum comando executado
- Nenhum código alterado
- Declaração explícita: "F-1 aprovada"

**PROIBIÇÕES:**
- ❌ Executar comandos
- ❌ Criar código
- ❌ "Validar rapidamente"

---

### F1 — Definir "Valor Cognitivo Persistente"

**END:** Definição clara e verificável do que constitui "valor cognitivo persistente"

**DONE WHEN:**
- Lista explícita de artefatos que são "valor cognitivo":
  - Resumos de capítulos processados
  - Coverage reports parciais
  - Pontos-chave identificados
  - Citações extraídas
  - Exemplos encontrados
  - Metadados de processamento (timestamps, chunks processados)
- Distinção clara entre:
  - Processamento transitório (logs, estados temporários)
  - Valor cognitivo persistente (resultados que não podem se perder)
- Documentação da definição criada

**PROVA:**
```bash
# Verificar que definição existe e está documentada
docker compose exec app bash -c 'test -f /app/DEMANDAS/DEMANDA-PROD-004_PERSISTENCIA_PROGRESSIVA_RETOMADA_SEGURA.md && grep -q "valor cognitivo" /app/DEMANDAS/DEMANDA-PROD-004_PERSISTENCIA_PROGRESSIVA_RETOMADA_SEGURA.md && echo "OK: definição existe" || echo "FAIL: definição não encontrada"'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Valor cognitivo produzido não é descartável."

---

### F2 — Definir Pontos Mínimos de Persistência Incremental

**END:** Pontos de checkpoint definidos onde valor cognitivo deve ser persistido

**DONE WHEN:**
- Lista de pontos de checkpoint definida:
  - Após processamento de cada capítulo
  - Após geração de coverage report parcial
  - Após identificação de pontos-chave
  - Após extração de citações
  - Após identificação de exemplos
- Frequência mínima de persistência definida (ex.: a cada capítulo, a cada 30 segundos, etc.)
- Critério de "ponto válido" definido (o que pode ser retomado)

**PROVA:**
```bash
# Verificar que pontos de checkpoint estão documentados
docker compose exec app bash -c 'grep -E "checkpoint|persistência incremental" /app/planejamento/DEMANDA-PROD-004_PLAN.md | head -5'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Execução longa sem persistência progressiva é desperdício estrutural."

---

### F3 — Definir Contrato de Retomada Segura

**END:** Contrato explícito de como o sistema retoma execução a partir de um checkpoint

**DONE WHEN:**
- Formato de checkpoint definido (estrutura de dados)
- Identificação de checkpoint válido (como detectar último checkpoint válido)
- Lógica de retomada definida:
  - Como identificar onde parou
  - Como validar que checkpoint é válido
  - Como continuar a partir do checkpoint
  - Como evitar reprocessamento
- Tratamento de checkpoint inválido/corrompido definido

**PROVA:**
```bash
# Verificar que contrato está documentado
docker compose exec app bash -c 'grep -E "retomada|checkpoint|resume" /app/planejamento/DEMANDA-PROD-004_PLAN.md | head -5'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Retomar não é recomeçar."
- "Falha não pode apagar história."

---

### F4 — Ajustar Pipeline para Respeitar Contrato de Persistência

**END:** Pipeline modificado para persistir valor cognitivo nos pontos definidos

**DONE WHEN:**
- Pipeline identifica pontos de checkpoint
- Pipeline persiste valor cognitivo em cada checkpoint
- Persistência é atômica (ou salva tudo ou não salva nada)
- Validação de checkpoint após persistência
- Logs de persistência gerados

**PROVA:**
```bash
# Verificar que pipeline tem lógica de persistência progressiva
docker compose exec app bash -c 'grep -E "checkpoint|persist.*progress|save.*incremental" /app/src/summarizer_robust.py | head -5'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Valor cognitivo produzido não é descartável."
- "Falha não pode apagar história."

---

### F5 — Expor Inspeção de Progresso/Resultados Parciais

**END:** Sistema expõe API/interface para inspecionar progresso e resultados parciais

**DONE WHEN:**
- Endpoint/interface para consultar progresso atual
- Endpoint/interface para consultar resultados parciais já persistidos
- Resposta inclui:
  - Status da execução (em progresso, pausada, concluída, falhou)
  - Checkpoints disponíveis
  - Resultados parciais já salvos
  - Ponto de retomada (se aplicável)

**PROVA:**
```bash
# Verificar que API expõe progresso
docker compose exec app bash -c 'grep -E "progress|partial|checkpoint" /app/src/api/routes.py | head -5'
```

**REGRAS CANÔNICAS APLICADAS:**
- "END não é só o final; END é o que permanece."

---

### F6 — Garantir Histórico de Execuções

**END:** Todas as execuções ficam disponíveis para consulta posterior

**DONE WHEN:**
- Execuções são identificadas unicamente (session_id ou equivalente)
- Histórico de execuções é consultável
- Cada execução mantém:
  - Status (concluída, em progresso, falhou, pausada)
  - Checkpoints disponíveis
  - Resultados parciais
  - Timestamp de criação e última atualização

**PROVA:**
```bash
# Verificar que histórico é consultável
docker compose exec app bash -c 'grep -E "history|execution|session" /app/src/api/routes.py | head -5'
```

**REGRAS CANÔNICAS APLICADAS:**
- "O usuário não deve perder acesso ao que o sistema já produziu para ele."

---

### F7 — Gerar Evidência de Falha sem Perda de Progresso

**END:** Sistema gera evidência de que falha não apaga progresso já persistido

**DONE WHEN:**
- Teste que simula falha durante execução longa
- Teste valida que progresso já persistido não se perde
- Teste valida que retomada não reprocessa etapas concluídas
- Evidência documentada em `/EVIDENCIAS/produto/`

**PROVA:**
```bash
# Executar teste de falha sem perda de progresso
docker compose exec app bash -c 'pytest src/tests/integration/test_persistencia_progressiva.py -v -k "test_falha_sem_perda_progresso"'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Falha não pode apagar história."
- "Retomar não é recomeçar."

---

### F8 — Validar Gate Z10 (Robustez + Persistência)

**END:** Gate Z10 validado com provas mínimas de robustez

**DONE WHEN:**
- Testes de robustez implementados:
  - Falha de conexão durante execução
  - Falha de disco durante persistência
  - Timeout durante processamento
  - Checkpoint corrompido
- Todos os testes passam (`pytest -q` = 0 failed)
- Evidência de Gate Z10 gerada

**PROVA:**
```bash
# Validar Gate Z10
docker compose exec app bash -c 'pytest src/tests/integration/test_gate_z10_persistencia_progressiva.py -q'
```

**REGRAS CANÔNICAS APLICADAS:**
- Gate Z10 é obrigatório para Classe A

---

### F9 — Validar Gate Z11 e Declarar PASS

**END:** Gate Z11 validado e demanda declarada como PASS

**DONE WHEN:**
- Gate Z11 continua PASS (interface funcional)
- Todos os critérios de aceitação atendidos
- Evidência completa gerada em `/EVIDENCIAS/produto/`
- Documentação atualizada
- Declaração explícita: "DEMANDA-PROD-004: PASS"

**PROVA:**
```bash
# Validar Gate Z11
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health | grep -q "healthy" && echo "Z11: PASS" || echo "Z11: FAIL"'
```

**REGRAS CANÔNICAS APLICADAS:**
- Gate Z11 continua bloqueante

---

## 🎯 STRINGS DE PROVA

**Comandos de Validação (executados via Docker):**

```bash
# F1: Verificar definição de valor cognitivo
docker compose exec app bash -c 'grep -q "valor cognitivo" /app/DEMANDAS/DEMANDA-PROD-004_PERSISTENCIA_PROGRESSIVA_RETOMADA_SEGURA.md && echo "F1: PASS" || echo "F1: FAIL"'

# F2: Verificar pontos de checkpoint
docker compose exec app bash -c 'grep -q "checkpoint" /app/planejamento/DEMANDA-PROD-004_PLAN.md && echo "F2: PASS" || echo "F2: FAIL"'

# F3: Verificar contrato de retomada
docker compose exec app bash -c 'grep -q "retomada" /app/planejamento/DEMANDA-PROD-004_PLAN.md && echo "F3: PASS" || echo "F3: FAIL"'

# F4: Verificar pipeline modificado
docker compose exec app bash -c 'grep -q "checkpoint\|persist.*progress" /app/src/summarizer_robust.py && echo "F4: PASS" || echo "F4: FAIL"'

# F5: Verificar API de progresso
docker compose exec app bash -c 'grep -q "progress\|partial" /app/src/api/routes.py && echo "F5: PASS" || echo "F5: FAIL"'

# F6: Verificar histórico
docker compose exec app bash -c 'grep -q "history\|execution" /app/src/api/routes.py && echo "F6: PASS" || echo "F6: FAIL"'

# F7: Executar teste de falha
docker compose exec app bash -c 'pytest src/tests/integration/test_persistencia_progressiva.py -v -k "test_falha_sem_perda_progresso"'

# F8: Validar Gate Z10
docker compose exec app bash -c 'pytest src/tests/integration/test_gate_z10_persistencia_progressiva.py -q'

# F9: Validar Gate Z11
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health | grep -q "healthy" && echo "Z11: PASS" || echo "Z11: FAIL"'
```

**Strings Esperadas:**
- F1-F6: `PASS` (definições e implementações existem)
- F7: Teste passa sem perda de progresso
- F8: `0 failed` (Gate Z10 validado)
- F9: `Z11: PASS` (Gate Z11 continua funcional)

---

## 🎯 APROVAÇÃO

**Status:** ⏸️ PENDENTE DE APROVAÇÃO

**Checklist de Aprovação:**
- [x] TODO canônico existe (F0-F9)
- [x] Escopo DO/DON'T explícito
- [x] Ordem de execução definida
- [x] Critérios de FAIL listados
- [x] Strings de prova definidas
- [x] Nenhum comando foi executado durante F-1
- [x] Nenhum código foi criado durante F-1
- [x] Gate Z10 identificado como obrigatório (Classe A)
- [x] Frases canônicas referenciadas

**Aguardando:**
- [ ] Declaração explícita: **"F-1 aprovada"**
- [ ] Aprovação do CEO ou arquiteto responsável

---

## 📌 NOTAS

**Regra Crítica:**
> "F-1 é planejamento, não execução. Executar durante F-1 é FAIL automático."

**Bloqueio Estrutural:**
> "Esta demanda requer F-1 (Planejamento Canônico). Sem F-1 aprovada, não posso executar."

**Classe A - Z10 Obrigatório:**
> "Demandas Classe A (Execução Longa + Streaming + Persistência + Retomada) exigem obrigatoriamente Gate Z10 (Qualidade de Produto) com provas mínimas de robustez."

**Relação com Outras Demandas:**
- **DEMANDA-PROD-003** (Persistência Confiável): Garante que quando salvar, salve corretamente. Esta demanda (PROD-004) garante que salve progressivamente.
- **DEMANDA-PROD-002** (Persistência Histórico): Garante histórico. Esta demanda (PROD-004) garante que histórico seja construído progressivamente.

---

**Documento criado:** 2026-01-21  
**Última atualização:** 2026-01-21  
**Governado por:** END-FIRST v2
