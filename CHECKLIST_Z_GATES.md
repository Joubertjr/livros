# Checklist Completo — Gates Z0 → Z11 (GO/NO-GO)

## Regras Globais (valem para TODOS os gates)

- Cada gate só é "DONE" se terminar com `pytest -q` 100% verde
- Proibido chamar OpenAI de verdade nos testes (usar mocks/stubs)
- Cada gate precisa entregar prova: teste(s) + asserts (não texto)
- Se mudar contrato/schema no meio: parar e propor diff, não "ajustar no código"

---

## Gate Z0 — Testes RED (falhas esperadas)

**Objetivo:** provar que o sistema falha quando deveria falhar.

**Regra Crítica:** Z0 nunca bloqueia suite; deve ficar xfail por design.

### Checklist

- [x] Existem testes que falham por design (ex: "resumo impossível" / falta de marcador)
- [x] Os testes descrevem claramente por que falham
- [x] Testes marcados como `@pytest.mark.xfail` com reason: "Gate Z0 = RED tests (falham por design). Não contam como failure."
- [x] Critério de PASS do Z0 = testes existem e são xfail/RED por design

### Prova Exigida

- [x] `pytest -q` verde no final do gate (Z0 não bloqueia suite)
- [x] Arquivo(s) de teste presentes em `src/tests/integration/` ou `unit/`
- [x] Testes marcados como xfail (não contam como failure)

### Artifacts Esperados

- Arquivos: `src/tests/integration/test_gate_z0_impossible_summary.py`
- Comando de prova: `pytest src/tests/integration/test_gate_z0_impossible_summary.py -q`

### Artifacts Esperados

- `src/tests/integration/test_gate_z0_impossible_summary.py`

### Comando de Prova

```bash
pytest src/tests/integration/test_gate_z0_impossible_summary.py -q
```

---

## Gate Z1 — Quality Gate lendo coverage_report.json (fonte única)

**Objetivo:** quality gate não recalcula nada, só valida arquivo.

### Checklist

- [ ] `validate_from_coverage_report(path)` implementado
- [ ] Se o arquivo não existe → FAIL
- [ ] Se JSON inválido → FAIL
- [ ] Se `overall_coverage_percentage != 100.0` → FAIL
- [ ] Se `missing_critical_item_ids` não vazio em qualquer capítulo → FAIL
- [ ] Se `total_chapters != chapters_processed` → FAIL

### Prova Exigida

- [ ] Testes usando fixtures (`coverage_report_100.json`, `coverage_report_99.json`)
- [ ] `pytest -q` verde

### Artifacts Esperados

- Arquivos: `src/tests/unit/test_quality_gate_from_coverage_report.py`, `src/tests/fixtures/coverage_report_*.json`
- Comando de prova: `pytest src/tests/unit/test_quality_gate_from_coverage_report.py -q`

### Artifacts Esperados

- `src/quality_gate.py` (método `validate_from_coverage_report`)
- `src/tests/unit/test_quality_gate_from_coverage_report.py`
- `src/tests/fixtures/coverage_report_100.json`
- `src/tests/fixtures/coverage_report_99.json`

### Comando de Prova

```bash
pytest src/tests/unit/test_quality_gate_from_coverage_report.py -q
```

---

## Gate Z2 — Auditoria determinística + anti-fraude

**Objetivo:** provar auditoria 100% determinística e resistente a marcador fake.

### Checklist

- [ ] Regex do marcador implementada
- [ ] Marcador faltando → FAIL
- [ ] Marcador presente mas chunks vazios → FAIL
- [ ] Marcador presente mas chunk referenciado não está em `source_chunks` → FAIL (anti-fraude)
- [ ] Marcador presente + chunks válidos → PASS
- [ ] Auditoria retorna lista clara de:
  - [ ] `missing_markers`
  - [ ] `invalid_markers` (ou equivalente)

### Prova Exigida

- [ ] Teste explícito de fraude (marcador aponta chunks errados)
- [ ] `pytest -q` verde

### Artifacts Esperados

- Arquivos: `src/recall_auditor.py`, `src/tests/unit/test_recall_auditor.py`
- Comando de prova: `pytest src/tests/unit/test_recall_auditor.py -q`

### Artifacts Esperados

- `src/recall_auditor.py`
- `src/tests/unit/test_recall_auditor.py`

### Comando de Prova

```bash
pytest src/tests/unit/test_recall_auditor.py -q
```

---

## Gate Z3 — IDs imutáveis (hash + normalização)

**Objetivo:** IDs determinísticos, estáveis e reproduzíveis.

### Checklist

- [ ] Função de normalização determinística
- [ ] Hash (SHA256 curto) gerado do conteúdo normalizado
- [ ] Mesmo conteúdo (mesma normalização) → mesmo `item_id`
- [ ] Mudança mínima no conteúdo → `item_id` diferente
- [ ] `item_id` segue padrão `RS:cap{N}:{hash6}`

### Prova Exigida

- [ ] Testes de estabilidade e "mudança mínima"
- [ ] `pytest -q` verde

### Artifacts Esperados

- Arquivos: `src/recall_set.py` (funções `normalize_content`, `generate_item_id`), `src/tests/unit/test_item_id_immutability.py`
- Comando de prova: `pytest src/tests/unit/test_item_id_immutability.py -q`

### Artifacts Esperados

- `src/recall_set.py` (funções `normalize_content`, `generate_item_id`)
- `src/tests/unit/test_item_id_immutability.py`

### Comando de Prova

```bash
pytest src/tests/unit/test_item_id_immutability.py -q
```

---

## Gate Z4 — Recall Set com hard cap 12 (determinístico)

**Objetivo:** nunca passar de 12 críticos, e cortar sempre igual.

### Checklist

- [ ] Se críticos > 12 → reduzir para 12
- [ ] Ordem de prioridade determinística (ex: freq > posição > markers)
- [ ] Resultado sempre igual com mesma entrada (sem aleatoriedade)
- [ ] `criticality_reason` é enum (sem texto livre)

### Prova Exigida

- [ ] Teste que gera >12 críticos e garante corte determinístico
- [ ] `pytest -q` verde

### Artifacts Esperados

- Arquivos: `src/recall_set.py` (função `generate_recall_set`, enum `CriticalityReason`), `src/tests/unit/test_recall_set_hard_cap.py`
- Comando de prova: `pytest src/tests/unit/test_recall_set_hard_cap.py -q`

### Artifacts Esperados

- `src/recall_set.py` (função `generate_recall_set` com hard cap)
- `src/tests/unit/test_recall_set_hard_cap.py`

### Comando de Prova

```bash
pytest src/tests/unit/test_recall_set_hard_cap.py -q
```

---

## Gate Z5 — Pipeline no chapter_summarizer (com regeneração)

**Objetivo:** capítulo → chunks → extrações → recall set → resumo → auditoria → regeneração.

### Checklist

- [ ] Chapter é chunkado (`chunk_ids` consistentes)
- [ ] Extração por chunk é chamada (mock)
- [ ] Recall set é gerado (hard cap respeitado)
- [ ] Resumo exige marcadores com ancoragem
- [ ] Rodar auditoria determinística
- [ ] Se falhar → regenerar até max 3
- [ ] Após 3 falhas → erro explícito

### Prova Exigida (TESTES)

- [ ] Teste: tentativa 1 falha (sem marcador) → regenera
- [ ] Teste: tentativa 2 falha (fraude/ancoragem inválida) → regenera
- [ ] Teste: tentativa 3 passa → retorna sucesso
- [ ] Assert: `regeneration_count` correto
- [ ] `pytest -q` verde

### Artifacts Esperados

- Arquivos: `src/chapter_summarizer.py` (método `summarize_chapter_robust`), `src/tests/integration/test_pipeline_regeneration.py`, `src/tests/integration/test_gate_z5_1_regeneration_antifraud.py`
- Comando de prova: `pytest src/tests/integration/test_pipeline_regeneration.py src/tests/integration/test_gate_z5_1_regeneration_antifraud.py -q`

### Artifacts Esperados

- `src/chapter_summarizer.py` (método `summarize_chapter_robust`)
- `src/exceptions.py` (classe `CoverageError`)
- `src/tests/integration/test_pipeline_regeneration.py`
- `src/tests/integration/test_gate_z5_1_regeneration_antifraud.py`

### Comando de Prova

```bash
pytest src/tests/integration/test_pipeline_regeneration.py src/tests/integration/test_gate_z5_1_regeneration_antifraud.py -q
```

---

## Gate Z6 — Evidence Generator (gera evidências + coverage_report.json)

**Objetivo:** evidência é artefato canônico, auditável.

### Checklist

**Arquivos obrigatórios:**
- [ ] `EVIDENCIAS/coverage_report.json`
- [ ] `EVIDENCIAS/extractions_<timestamp>.json`
- [ ] `EVIDENCIAS/report.md`

**Regras:**
- [ ] `coverage_report.json` tem 1 linha por item crítico com:
  - [ ] `covered`
  - [ ] `marker_found`
  - [ ] `chunks_validated`
- [ ] Totalizadores batem:
  - [ ] `total_critical_items == total_covered`
  - [ ] `overall_coverage_percentage == 100.0` quando PASS

### Prova Exigida

- [ ] Teste que valida estrutura + campos obrigatórios
- [ ] Teste que falha se faltar 1 item crítico
- [ ] `pytest -q` verde

### Artifacts Esperados

- Arquivos: `src/evidence_generator_robust.py`, `src/tests/unit/test_evidence_generator_gate_z6.py`
- Arquivos gerados: `EVIDENCIAS/coverage_report.json`, `EVIDENCIAS/extractions_*.json`, `EVIDENCIAS/report.md`
- Comando de prova: `pytest src/tests/unit/test_evidence_generator_gate_z6.py -q`

### Artifacts Esperados

- `src/evidence_generator_robust.py`
- `src/schemas/coverage_report.py`
- `src/tests/unit/test_evidence_generator_gate_z6.py`
- `EVIDENCIAS/coverage_report.json` (gerado pelos testes)
- `EVIDENCIAS/extractions_*.json` (gerado pelos testes)
- `EVIDENCIAS/report.md` (gerado pelos testes)

### Comando de Prova

```bash
pytest src/tests/unit/test_evidence_generator_gate_z6.py -q
```

---

## Gate Z7 — Summarizer integração final (orquestra tudo)

**Objetivo:** pipeline completo, sem "meio resultado".

### Checklist

- [ ] Summarizer chama pipeline robusto
- [ ] Gera evidências
- [ ] Chama Quality Gate (lendo só `coverage_report`)
- [ ] Se quality gate FAIL → levanta exceção clara e não retorna resumo
- [ ] Se PASS → retorna resultado final

### Prova Exigida

- [ ] Teste happy-path (PASS)
- [ ] Teste fail-path (coverage 99% → exception)
- [ ] `pytest -q` verde

### Artifacts Esperados

- Arquivos: `src/summarizer_robust.py`, `src/tests/integration/test_summarizer_gate_z7.py`
- Arquivos gerados: `EVIDENCIAS/coverage_report.json` (validado pelo Quality Gate)
- Comando de prova: `pytest src/tests/integration/test_summarizer_gate_z7.py -q`

### Artifacts Esperados

- `src/summarizer_robust.py`
- `src/tests/integration/test_summarizer_gate_z7.py`
- `EVIDENCIAS/coverage_report.json` (gerado pelo pipeline)

### Comando de Prova

```bash
pytest src/tests/integration/test_summarizer_gate_z7.py -q
```

---

## Gate Z8 — Prova real (fim-a-fim com livro de verdade)

**Objetivo:** comprovar no mundo real.

### Checklist

- [ ] Rodar com um PDF real
- [ ] Pasta `EVIDENCIAS/` completa gerada
- [ ] `overall_coverage_percentage == 100.0`
- [ ] Nenhum capítulo com:
  - [ ] `processed_chunks < total_chunks`
  - [ ] `missing_critical_item_ids` não vazio

### Prova Exigida

- [ ] Anexar `EVIDENCIAS/coverage_report.json` gerado
- [ ] Anexar `EVIDENCIAS/report.md`
- [ ] Log da execução (stdout) mostrando PASS final

### Artifacts Esperados

- Arquivos gerados: `EVIDENCIAS/coverage_report.json` (com `overall_coverage_percentage == 100.0`), `EVIDENCIAS/report.md`, `EVIDENCIAS/extractions_*.json`
- Comando de prova: Execução real com livro PDF + validação manual dos artifacts

### Artifacts Esperados

- `EVIDENCIAS/coverage_report.json` (gerado com livro real)
- `EVIDENCIAS/extractions_*.json` (gerado com livro real)
- `EVIDENCIAS/report.md` (gerado com livro real)
- Log de execução completo

### Comando de Prova

```bash
# Executar pipeline completo com livro real
python3 -m src.main --file <livro.pdf>
# Verificar evidências geradas
cat EVIDENCIAS/coverage_report.json | jq '.overall_coverage_percentage, .passed'
```

---

## Gate Z9 — API + Frontend Observability

**Objetivo:** Provar que API e frontend expõem observabilidade sem quebrar compatibilidade.

### Checklist

- [ ] Z9.0: Schema aceita campos opcionais (coverage_report, addendum_metrics)
- [ ] Z9.1: API retorna coverage_report quando disponível
- [ ] Z9.2: UI renderiza métricas sem quebrar quando ausentes
- [ ] Z9.3: Docker funciona end-to-end e gera evidências

### Prova Exigida

- [ ] Teste unitário: `test_api_schema_gate_z9.py` valida campos opcionais
- [ ] Teste de integração: `test_api_gate_z9.py` valida retorno de coverage_report
- [ ] Smoke test de UI: página não quebra sem coverage_report
- [ ] Evidências Docker confirmadas

### Artifacts Esperados

- `src/tests/unit/test_api_schema_gate_z9.py`
- `src/tests/integration/test_api_gate_z9.py`
- `EVIDENCIAS/gate_z9_2_ui_smoke_test.md`
- `EVIDENCIAS/gate_z9_3_docker_proof.md`

### Comando de Prova

```bash
pytest src/tests/unit/test_api_schema_gate_z9.py src/tests/integration/test_api_gate_z9.py -q
```

---

## Gate Z10 — Code Quality (TDD + Clean Code)

**Objetivo:** Garantir que código novo ou alterado atende aos padrões de TDD e Clean Code.

### Checklist

- [ ] Z10.0: Código novo ou alterado tem testes correspondentes
- [ ] Z10.1: Testes falham antes da implementação (ou são RED/xfail por design)
- [ ] Z10.2: Funções são pequenas e coesas (≤50 linhas, preferencialmente ≤40)
- [ ] Z10.3: Nomes de funções/variáveis explicam intenção, não implementação
- [ ] Z10.4: Nenhuma regra de negócio está duplicada
- [ ] Z10.5: Nenhuma lógica crítica está implícita ou "mágica"
- [ ] Z10.6: Não existem TODOs, HACKs ou comentários de desculpa
- [ ] Z10.7: Código é legível em sequência (humano novo consegue entender)
- [ ] Z10.8: Frontend e backend permanecem desacoplados
- [ ] Z10.9: `pytest -q` passa (0 failed)
- [ ] Z10.10: A implementação parte do resultado final esperado (END-FIRST), não da conveniência técnica
- [ ] **Z10.11: Testes de integração end-to-end cobrem fluxos críticos (NOVO - OBRIGATÓRIO)**
- [ ] **Z10.12: Cenários de erro e recuperação são testados (NOVO - OBRIGATÓRIO)**

### Z10.A — Heurísticas Objetivas (Validação Manual Obrigatória)

Heurísticas objetivas (validação manual), com prova via comandos no Docker:

- [ ] **Funções > 50 linhas** → FAIL (justificar exceção se necessário)
- [ ] **Arquivo > 400 linhas** → Justificar ou refatorar
- [ ] **Duplicação óbvia (copy/paste)** → FAIL (extrair função comum)
- [ ] **RED não documentado como "por design"** → FAIL (é dívida técnica)
- [ ] **TODO|HACK|FIXME no código** → FAIL (remover ou justificar)
- [ ] **Fluxo crítico sem teste de integração end-to-end** → FAIL (criar teste obrigatório)
- [ ] **Cenário de erro não testado** → FAIL (criar teste obrigatório)

**Exceção para Função > 50 linhas (Canônica)**:

Permitido SOMENTE se:
- Função for **adapter/wrapper** sem regra de negócio
- Tiver **teste cobrindo o comportamento** completo
- **Justificativa registrada** no relatório final + evidência

### Comando de Prova

```bash
# Suite completa de testes
docker compose exec app bash -c 'pytest -q'

# Testes de integração E2E
docker compose exec app bash -c 'pytest src/tests/integration/test_api_process_e2e.py src/tests/integration/test_sse_robustness.py src/tests/integration/test_error_recovery.py -v'

# Validação completa Gate Z10
make check-code-quality
```

### Z10.B — Testes de Integração End-to-End (OBRIGATÓRIO)

**Regra Crítica:** Testes unitários isolados NÃO são suficientes. Fluxos críticos DEVEM ter testes de integração.

**Fluxos críticos que DEVEM ter testes de integração:**
- [x] Upload → Processamento → SSE streaming → Result retrieval (happy path)
- [x] Erro durante processamento → Sessão preservada → Result retorna erro estruturado
- [x] SSE interrompido → Recuperação via /api/result funciona
- [x] Sessão não encontrada após erro → Tratamento adequado (não 404 silencioso)

**Testes obrigatórios implementados:**
- ✅ `test_api_process_e2e.py` - Fluxo completo end-to-end (3 testes)
- ✅ `test_sse_robustness.py` - Robustez de SSE e recuperação (4 testes)
- ✅ `test_error_recovery.py` - Recuperação de erros (5 testes)

**Comando de validação:**
```bash
# Todos os testes E2E
pytest src/tests/integration/test_api_process_e2e.py src/tests/integration/test_sse_robustness.py src/tests/integration/test_error_recovery.py -v

# Via Makefile
make test-e2e
```

### Z10.C — Processo TDD Obrigatório (NOVO)

**Regra Crítica:** TDD não é opcional. Teste primeiro, código depois.

**Processo obrigatório:**
1. **RED:** Teste escrito e falha (antes de qualquer código)
2. **GREEN:** Implementação mínima (apenas para teste passar)
3. **REFACTOR:** Clean Code (refatorar mantendo testes passando)

**Documentação:**
- `METODO/TDD_PROCESS.md` - Processo TDD canônico completo

**Validação:**
- [ ] Teste escrito antes de código
- [ ] Teste falha antes da implementação
- [ ] Teste passa após implementação
- [ ] Testes de erro existem
- [ ] Testes de integração para fluxos críticos

**Comando de validação:**
```bash
# Verificar que testes existem para código novo
pytest src/tests/ -v --collect-only | grep test_

# Validar processo TDD
# (validação manual - verificar que teste foi escrito antes)
```

### Z10.D — Análise Estática Automática (NOVO)

**Regra Crítica:** Clean Code deve ser validado automaticamente, não apenas manualmente.

**Ferramentas configuradas:**
- ✅ `flake8` - Estilo e erros básicos
- ✅ `pylint` - Análise de qualidade
- ✅ `mypy` - Verificação de tipos (opcional)
- ✅ `scripts/check_code_quality.sh` - Script de validação completa

**Validações automáticas:**
- [ ] Funções < 50 linhas (ou justificada)
- [ ] Sem TODOs/HACKs/FIXMEs
- [ ] Sem duplicação óbvia
- [ ] Estilo de código consistente

**Comando de validação:**
```bash
# Validação completa (Gate Z10)
make check-code-quality

# Ou individualmente:
flake8 src/
pylint src/
```

**Configuração:**
- `.flake8` - Configuração Flake8
- `pylintrc` - Configuração Pylint
- `.mypy.ini` - Configuração MyPy (opcional)

### Critérios de FAIL

Gate Z10 FALHA se:
- "Funciona mas está feio"
- "Depois a gente refatora"
- "Não deu tempo de escrever teste"
- Função >50 linhas sem justificativa (exceto wrapper/adapter documentado)
- Lógica implícita ou "mágica"
- Regra de negócio duplicada
- RED não documentado como "por design"
- Implementação parte de conveniência técnica, não do resultado final (viola END-FIRST)
- **Fluxo crítico sem teste de integração end-to-end (NOVO)**
- **Cenário de erro não testado em integração (NOVO)**

**Regra Crítica:** Gate Z10 falhou = PR bloqueado, mesmo com coverage 100%.

**Regra Canônica Atualizada:**
> "Teste unitário sem teste de integração é código isolado, não sistema funcional."

---

## Gate Z11 — END-USER SMOKE / FRONTEND

**Objetivo:** Garantir que a experiência observável do usuário final está funcional antes de declarar qualquer gate como PASS.

**Regra Crítica:** Se a UI estiver quebrada para o usuário final, o sistema DEVE falhar estruturalmente antes de qualquer correção.

### Checklist

- [ ] Z11.0: HTML acessível em `http://localhost:8000/` (retorna HTML válido, não 404/500)
- [ ] Z11.1: CSS acessível em `/static/css/style.css` (HTTP 200, não 404)
- [ ] Z11.2: JS acessível em `/static/js/app.js` (HTTP 200, não 404)
- [ ] Z11.3: Favicon acessível (se existir) (HTTP 200 ou 204, não 404)
- [ ] Z11.4: API Health responde corretamente (`/api/health` retorna `{"status":"healthy"}`)
- [ ] Z11.5: Nenhum recurso estático referenciado no HTML retorna 404
- [ ] Z11.6: Evidência canônica gerada com outputs dos comandos

### Prova Exigida

**Comandos Obrigatórios (executados via Docker):**

```bash
# 1. HTML acessível
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -5'

# 2. CSS acessível (código HTTP 200)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/style.css'

# 3. JS acessível (código HTTP 200)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/js/app.js'

# 4. Favicon (se existir)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/favicon.svg'

# 5. API Health
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health'
```

**Evidência Obrigatória:**
- Output de cada comando acima colado em `EVIDENCIAS/gate_z11_end_user_smoke_proof.md`
- Cada comando deve retornar resultado esperado (HTML válido, HTTP 200, healthy)
- Status final: `Status: PASS` ou `Status: FAIL`

### Artifacts Esperados

- `EVIDENCIAS/gate_z11_end_user_smoke_proof.md` (evidência canônica com outputs)
- Comandos executados via Docker (não local)
- Status final: PASS ou FAIL

### Comando de Prova

```bash
# Validação completa do Gate Z11
docker compose exec app bash -c '
  echo "=== Z11.0: HTML ===" && \
  curl -s http://localhost:8000/ | head -1 && \
  echo "=== Z11.1: CSS ===" && \
  curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/static/css/style.css && \
  echo "=== Z11.2: JS ===" && \
  curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/static/js/app.js && \
  echo "=== Z11.4: Health ===" && \
  curl -s http://localhost:8000/api/health
'
```

**Critério de PASS:** Todos os comandos retornam resultado esperado (HTML válido, HTTP 200, healthy).

### Critérios de FAIL

Gate Z11 FALHA se:

- HTML retorna 404 ou 500
- CSS retorna 404 ou 500
- JS retorna 404 ou 500
- Interface não renderiza visualmente (estilos não aplicados)
- Console do navegador mostra erros 404 para recursos estáticos
- API Health não responde
- Qualquer recurso referenciado no HTML retorna 404

**Regra Crítica:** Gate Z11 falhou = PR bloqueado, mesmo com todos os outros gates (Z0-Z10) PASS.

### Regra de Bloqueio Estrutural

**Gate Z11 é BLOQUEANTE:**

- Se Gate Z11 falhar, **TODOS os outros gates (Z0-Z10) são considerados INCOMPLETOS**
- Nenhum PR pode ser aprovado com Gate Z11 em FAIL
- Nenhuma correção de produto pode ser aplicada sem Gate Z11 PASS

**Ordem de Validação:**
1. Gates Z0-Z10 (validação técnica)
2. **Gate Z11 (validação de experiência do usuário final) — BLOQUEANTE**

Se Z11 falhar → sistema estruturalmente quebrado → PR bloqueado.

### Exceções e Casos Especiais

**Quando Gate Z11 não se aplica:**
- Sistema puramente CLI (sem interface web)
- Sistema em modo API-only (sem frontend)
- Desenvolvimento de backend isolado (sem frontend ativo)

**Regra:** Se o sistema expõe interface web (`http://localhost:8000/` ou equivalente), Gate Z11 é **OBRIGATÓRIO**.

---

## Notas Importantes

- Este checklist é CANÔNICO e IMUTÁVEL sem PR explícito
- Nada está "feito" se não passar pelo Gate correspondente
- Qualquer mudança neste checklist requer aprovação explícita
- O sistema deve sempre validar contra este checklist antes de declarar conclusão
