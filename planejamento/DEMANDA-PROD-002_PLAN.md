# PLANEJAMENTO CANÔNICO — DEMANDA-PROD-002: PERSISTÊNCIA, HISTÓRICO E FEEDBACK

**Demanda:** DEMANDA-PROD-002_PERSISTENCIA_HISTORICO_FEEDBACK.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-19  
**Status:** F-1 PENDENTE DE APROVAÇÃO  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para um usuário final:**
- Todo processo de resumo executado é persistido
- O usuário pode consultar resumos passados
- Cada resumo possui:
  - Identificador único
  - Nome/título definido
  - Data/hora de execução
  - Tipo de processo usado (ex.: estratégia A, B, experimental)
- É possível comparar diferentes execuções de resumo
- O usuário pode:
  - Registrar feedback, dúvida, erro ou sugestão
  - Ver claramente que sua solicitação foi recebida
  - Ver quando e como houve resposta

**Para o sistema:**
- Todos os dados do processo (input, estratégia, eventos, outputs) ficam armazenados
- Diferentes tipos de pipeline de resumo podem coexistir
- Feedback do usuário fica vinculado ao resumo específico
- Respostas posteriores (IA ou humano) ficam rastreadas
- Nenhuma informação gerada durante o processo se perde

**⚠️ Importante:**
Este END não define UI específica nem implementação técnica, apenas comportamento observável.

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS — NÃO NEGOCIÁVEIS)

Estas frases são canônicas, reutilizáveis e bloqueantes:

- **Persistência:** "Processo que não deixa rastro não é produto, é experimento descartável."
- **Comparabilidade:** "Se não posso comparar execuções, não posso evoluir o sistema."
- **Feedback:** "Feedback sem rastreabilidade é ruído."
- **Histórico:** "O usuário não deve perder acesso ao que o sistema já produziu para ele."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## ✅ Critérios de Aceitação (Binários)

### PASS

- ✅ Resumos permanecem acessíveis após execução
- ✅ Cada execução é identificável e consultável
- ✅ Diferentes pipelines de resumo são distinguíveis
- ✅ Usuário consegue revisar resumos antigos
- ✅ Usuário consegue registrar feedback facilmente
- ✅ Sistema consegue responder ou registrar resposta ao feedback
- ✅ Feedback e resposta ficam associados ao resumo correto
- ✅ Nada depende de memória temporária ou sessão ativa
- ✅ Interface continua funcional (Gate Z11 permanece PASS)
- ✅ Nenhuma regressão funcional (Z0–Z11 continuam PASS)
- ✅ Evidência gerada (documentação e provas em `/EVIDENCIAS/`)

### FAIL (AUTOMÁTICO)

- ❌ Resumo se perde ao recarregar a página
- ❌ Não há como distinguir dois resumos diferentes
- ❌ Usuário não sabe se seu feedback foi visto
- ❌ Processos diferentes se misturam sem rastreabilidade
- ❌ Histórico depende de logs internos ou console
- ❌ Feedback não é associado a nada concreto
- ❌ UX alterada sem F-1 aprovada
- ❌ Qualquer regressão funcional
- ❌ Gate Z11 quebrado
- ❌ Correção aplicada direto no código sem planejamento

---

## 🚫 DO / DON'T

### DO (fazer)

- ✅ Persistir dados do processo
- ✅ Tratar resumo como artefato de produto
- ✅ Separar processos de resumo por tipo
- ✅ Facilitar feedback do usuário
- ✅ Manter rastreabilidade completa
- ✅ Manter todos os gates PASS

### DON'T (não fazer)

- ❌ Resolver só com UI temporária
- ❌ Depender de sessão ativa
- ❌ Misturar execuções diferentes
- ❌ Ignorar feedback do usuário
- ❌ Tratar isso como "log técnico"
- ❌ Alterar pipeline de sumarização
- ❌ "Simplificar" removendo garantias
- ❌ Refatorar backend sem necessidade
- ❌ Quebrar Gate Z11

---

## 🧱 Bloqueios Estruturais

- 🔒 F-1 obrigatório (demanda de produto complexa) — **ESTE DOCUMENTO**
- 🔒 Não executar sem definição clara de modelo de dados
- 🔒 Não executar sem decisão explícita de escopo
- 🔒 Gate Z11 continua bloqueante
- 🔒 Nenhuma alteração sem evidência visual
- 🔒 Persistência = produto, não experimento

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

### F1 — Definir Modelo de Dados de Persistência

**END:** Modelo de dados definido e documentado (schema)

**DONE WHEN:**
- Schema de dados definido (Pydantic ou equivalente)
- Campos obrigatórios identificados:
  - Identificador único (resumo_id)
  - Nome/título
  - Data/hora de execução
  - Tipo de pipeline/estratégia
  - Input (texto ou referência a arquivo)
  - Output (resumo completo)
  - Metadados do processo (coverage_report, addendum_metrics, etc.)
- Documentação do schema criada
- Decisão sobre formato de armazenamento (JSON, SQLite, etc.)

**PROVA:**
```bash
# Verificar que schema existe
docker compose exec app bash -c 'test -f /app/src/schemas/summary_storage.py && echo "OK: schema existe" || echo "FAIL: schema não existe"'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Processo que não deixa rastro não é produto, é experimento descartável."

---

### F2 — Definir Modelo de Identificação de Resumo

**END:** Sistema de identificação único e consultável definido

**DONE WHEN:**
- Formato de `resumo_id` definido (UUID, hash, sequencial, etc.)
- Estratégia de geração de ID documentada
- Garantia de unicidade estabelecida
- Formato de consulta definido (API endpoint)

**PROVA:**
```bash
# Verificar que modelo de ID está documentado
docker compose exec app bash -c 'grep -E "resumo_id|summary_id" /app/src/schemas/summary_storage.py | head -3'
```

**REGRAS CANÔNICAS APLICADAS:**
- "O usuário não deve perder acesso ao que o sistema já produziu para ele."

---

### F3 — Definir Diferenciação de Pipelines de Resumo

**END:** Sistema permite distinguir diferentes tipos de pipeline/estratégia

**DONE WHEN:**
- Campo `pipeline_type` ou equivalente definido no schema
- Valores possíveis documentados (ex.: "robust", "standard", "experimental")
- Estratégia de versionamento de pipeline definida
- API permite filtrar por tipo de pipeline

**PROVA:**
```bash
# Verificar que schema inclui tipo de pipeline
docker compose exec app bash -c 'grep -E "pipeline|strategy|type" /app/src/schemas/summary_storage.py | head -3'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Se não posso comparar execuções, não posso evoluir o sistema."

---

### F4 — Implementar Persistência de Resumos

**END:** Resumos são persistidos automaticamente após execução

**DONE WHEN:**
- Módulo de persistência implementado
- Resumos salvos após conclusão do pipeline
- Dados completos do processo armazenados
- Nenhum resumo se perde após execução
- Persistência não depende de sessão ativa

**PROVA:**
```bash
# Verificar que resumo foi persistido após execução
docker compose exec app bash -c 'ls -la /app/volumes/summaries/ 2>/dev/null | head -5 || echo "Verificar estrutura de persistência"'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Processo que não deixa rastro não é produto, é experimento descartável."
- "Nenhum resumo pode existir apenas em memória"

---

### F5 — Implementar API de Histórico

**END:** Usuário pode consultar resumos passados via API

**DONE WHEN:**
- Endpoint `/api/summaries` ou equivalente implementado
- Endpoint permite listar resumos (com paginação se necessário)
- Endpoint permite buscar resumo por ID
- Endpoint permite filtrar por tipo de pipeline
- Resposta inclui metadados (ID, nome, data, tipo)

**PROVA:**
```bash
# Verificar que endpoint de histórico existe e responde
docker compose exec app bash -c 'curl -s http://localhost:8000/api/summaries | head -20'
```

**REGRAS CANÔNICAS APLICADAS:**
- "O usuário não deve perder acesso ao que o sistema já produziu para ele."

---

### F6 — Implementar Sistema de Feedback

**END:** Usuário pode registrar feedback vinculado a resumo específico

**DONE WHEN:**
- Schema de feedback definido (resumo_id, tipo, mensagem, data)
- Endpoint `/api/summaries/{resumo_id}/feedback` implementado
- Feedback persistido e vinculado ao resumo correto
- Usuário vê confirmação de recebimento

**PROVA:**
```bash
# Verificar que endpoint de feedback existe
docker compose exec app bash -c 'curl -s -X POST http://localhost:8000/api/summaries/test-id/feedback -H "Content-Type: application/json" -d "{\"type\":\"doubt\",\"message\":\"test\"}" 2>&1 | head -5'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Feedback sem rastreabilidade é ruído."
- "Feedback do usuário deve estar ligado a um artefato concreto"

---

### F7 — Implementar Sistema de Respostas ao Feedback

**END:** Sistema pode registrar resposta ao feedback (IA ou humano)

**DONE WHEN:**
- Schema de resposta definido (feedback_id, resposta, autor, data)
- Endpoint para registrar resposta implementado
- Resposta vinculada ao feedback correto
- Usuário pode ver resposta quando disponível

**PROVA:**
```bash
# Verificar que endpoint de resposta existe
docker compose exec app bash -c 'curl -s -X POST http://localhost:8000/api/feedback/test-id/responses -H "Content-Type: application/json" -d "{\"response\":\"test response\"}" 2>&1 | head -5'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Feedback sem rastreabilidade é ruído."

---

### F8 — Expor Histórico e Feedback na UI

**END:** Usuário pode acessar histórico e feedback via interface

**DONE WHEN:**
- UI exibe lista de resumos passados
- UI permite visualizar resumo específico
- UI permite registrar feedback
- UI exibe feedback e respostas quando disponíveis
- Gate Z11 continua PASS

**PROVA:**
```bash
# Verificar Gate Z11
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1 && curl -s http://localhost:8000/api/health'
```

**REGRAS CANÔNICAS APLICADAS:**
- "O usuário não deve perder acesso ao que o sistema já produziu para ele."
- "Scroll interno é PROIBIDO" (se aplicável à UI de histórico)

---

### F9 — Gerar Evidência e Validar Gates

**END:** Evidência gerada e todos os gates validados

**DONE WHEN:**
- Arquivo `EVIDENCIAS/persistencia_historico_feedback_proof.md` criado
- Documenta:
  - Modelo de dados implementado
  - API de histórico funcional
  - Sistema de feedback funcional
  - Exemplos de uso
- Gate Z11: PASS
- Suite verde: `pytest -q` = 0 failed

**PROVA:**
```bash
# Verificar evidência
docker compose exec app bash -c 'test -f /app/EVIDENCIAS/persistencia_historico_feedback_proof.md && echo "OK" || echo "FAIL"'

# Validar gates
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health && pytest -q 2>&1 | tail -1'
```

---

## 🔍 ANÁLISE DO ESTADO ATUAL

### Sistema Atual

**Observações:**
- `ProgressTracker` gerencia sessões temporárias (TTL: 1 hora)
- `session_id` é UUID gerado a cada execução
- Resultados armazenados apenas em memória durante sessão
- Não há persistência permanente de resumos
- Não há histórico consultável
- Não há sistema de feedback

**Gap identificado:**
- Resumos se perdem após TTL da sessão
- Não há como revisar execuções passadas
- Não há como comparar diferentes execuções
- Não há como registrar feedback vinculado a resumo

---

## 📊 STRINGS DE PROVA (Comandos Docker)

### F1 — Schema:
```bash
docker compose exec app bash -c 'test -f /app/src/schemas/summary_storage.py && echo "OK" || echo "FAIL"'
```

### F2 — Modelo de ID:
```bash
docker compose exec app bash -c 'grep -E "resumo_id|summary_id" /app/src/schemas/summary_storage.py | head -3'
```

### F3 — Tipo de Pipeline:
```bash
docker compose exec app bash -c 'grep -E "pipeline|strategy" /app/src/schemas/summary_storage.py | head -3'
```

### F4 — Persistência:
```bash
docker compose exec app bash -c 'ls -la /app/volumes/summaries/ 2>/dev/null | head -5'
```

### F5 — API Histórico:
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/api/summaries | head -20'
```

### F6 — API Feedback:
```bash
docker compose exec app bash -c 'curl -s -X POST http://localhost:8000/api/summaries/test-id/feedback -H "Content-Type: application/json" -d "{\"type\":\"doubt\",\"message\":\"test\"}"'
```

### F7 — API Respostas:
```bash
docker compose exec app bash -c 'curl -s -X POST http://localhost:8000/api/feedback/test-id/responses -H "Content-Type: application/json" -d "{\"response\":\"test\"}"'
```

### F8 — Gate Z11:
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health'
```

### F9 — Evidência e Suite:
```bash
docker compose exec app bash -c 'test -f /app/EVIDENCIAS/persistencia_historico_feedback_proof.md && pytest -q 2>&1 | tail -1'
```

---

## 🚨 CRITÉRIOS DE FAIL

### FAIL Automático se:
- ❌ Resumo se perde após execução
- ❌ Não há identificação única de resumo
- ❌ Histórico depende de sessão ativa
- ❌ Feedback não vinculado a resumo
- ❌ Gate Z11 quebra
- ❌ Regressão funcional
- ❌ Execução sem F-1 aprovada

---

## 📌 Status

**F-1 PENDENTE DE APROVAÇÃO**

Este planejamento **NÃO autoriza execução**.

Só pode ser executado após:
- Revisão completa do planejamento
- Aprovação explícita: **"F-1 APROVADA"**
- Ordem clara do CEO

---

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Path Canônico:** `/planejamento/DEMANDA-PROD-002_PLAN.md`  
**Demanda:** `/DEMANDAS/DEMANDA-PROD-002_PERSISTENCIA_HISTORICO_FEEDBACK.md`
