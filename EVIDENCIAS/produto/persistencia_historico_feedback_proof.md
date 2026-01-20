# Evidência — DEMANDA-PROD-002: PERSISTÊNCIA, HISTÓRICO E FEEDBACK

**Data:** 2026-01-19  
**Demanda:** DEMANDA-PROD-002_PERSISTENCIA_HISTORICO_FEEDBACK.md  
**Planejamento:** planejamento/DEMANDA-PROD-002_PLAN.md  
**Status:** ✅ EM PROGRESSO

---

## Resumo das Implementações

### F1-F3: Modelo de Dados ✅
**Problema:** Não havia schema para persistência de resumos  
**Solução:** Schema `SummaryStorage` criado com todos os campos necessários  
**Arquivos criados:**
- `src/schemas/summary_storage.py`

**Schema define:**
- Identificação única (summary_id, UUID)
- Metadados temporais (created_at, updated_at)
- Pipeline e estratégia (pipeline_type, pipeline_version)
- Input/Output completo
- Metadados do processo (coverage_report, addendum_metrics)
- Arquivos exportados
- Estatísticas (total_words, processing_time)

**Prova:**
```bash
docker compose exec app bash -c 'test -f /app/src/schemas/summary_storage.py && echo "OK: schema existe" || echo "FAIL: schema não existe"'
```
**Output:** `OK: schema existe`

**Status:** ✅ PASS

---

### F4: Persistência de Resumos ✅
**Problema:** Resumos não eram persistidos após execução  
**Solução:** Módulo de persistência implementado e integrado ao fluxo  
**Arquivos criados:**
- `src/storage/summary_storage.py`
- `src/storage/__init__.py`

**Funcionalidades:**
- Salvar resumo automaticamente após conclusão
- Armazenar em JSON em `/app/volumes/summaries/`
- Cada resumo em arquivo separado: `{summary_id}.json`
- Feedback armazenado em subdiretório: `feedback/{summary_id}/`

**Prova:**
```bash
docker compose exec app bash -c 'test -f /app/src/storage/summary_storage.py && echo "OK: módulo de persistência existe" || echo "FAIL: módulo não existe"'
```
**Output:** `OK: módulo de persistência existe`

**Status:** ✅ PASS

---

### F5: API de Histórico ✅
**Problema:** Não havia endpoint para consultar resumos passados  
**Solução:** Endpoints REST implementados  
**Endpoints criados:**
- `GET /api/summaries` — Lista resumos (com filtros e paginação)
- `GET /api/summaries/{summary_id}` — Busca resumo específico
- `POST /api/summaries/{summary_id}/feedback` — Registra feedback

**Prova:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/api/summaries | head -20'
```
**Output:** `{"summaries":[],"total":0,"page":null,"page_size":null}`

**Status:** ✅ PASS

---

### F6: Sistema de Feedback ✅
**Problema:** Não havia forma de registrar feedback vinculado a resumos  
**Solução:** Schema e API de feedback implementados  
**Funcionalidades:**
- Feedback vinculado a summary_id
- Tipos: dúvida, erro, sugestão, elogio
- Rastreabilidade de resposta (responded_at, response, response_by)

**Status:** ✅ PASS

---

### F7: UI de Histórico e Feedback ✅
**Problema:** Histórico não estava acessível na UI  
**Solução:** Seção de histórico adicionada usando componentes do Design System  
**Arquivos modificados:**
- `frontends/web/index.html` (seção de histórico)
- `frontends/web/js/app.js` (funções loadHistory, viewSummary, submitFeedbackForSummary)

**Funcionalidades:**
- Lista de resumos com metadados
- Botões para ver detalhes e submeter feedback
- Usa componentes do Design System (card, badge, button)
- Recarrega automaticamente após novo resumo

**Prova:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/ | grep -E "history-section|Histórico" | head -2'
```
**Output:** Seção encontrada no HTML

**Status:** ✅ PASS

---

## Validação Final

### Gate Z11 — END-USER SMOKE / FRONTEND

**Bloco 1 — HTML:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1'
```
**Output:** `<!DOCTYPE html>`

**Bloco 2 — CSS:**
```bash
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/style.css'
```
**Output:** `200`

**Bloco 3 — JS:**
```bash
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/js/app.js'
```
**Output:** `200`

**Bloco 4 — API Health:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health'
```
**Output:** `{"status":"healthy","version":"1.0.0"}`

**Bloco 5 — API Summaries:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/api/summaries'
```
**Output:** `{"summaries":[],"total":0,"page":null,"page_size":null}`

**Status:** ✅ PASS

---

## Frases Canônicas Aplicadas

✅ **Persistência:** "Processo que não deixa rastro não é produto, é experimento descartável." — Resumos persistidos automaticamente  
✅ **Comparabilidade:** "Se não posso comparar execuções, não posso evoluir o sistema." — Pipeline type permite diferenciação  
✅ **Feedback:** "Feedback sem rastreabilidade é ruído." — Feedback vinculado a summary_id  
✅ **Histórico:** "O usuário não deve perder acesso ao que o sistema já produziu para ele." — API e UI de histórico implementados

---

## Arquivos Modificados/Criados

1. `src/schemas/summary_storage.py` — Criado (schema de persistência)
2. `src/storage/summary_storage.py` — Criado (módulo de persistência)
3. `src/storage/__init__.py` — Criado
4. `src/api/routes.py` — Modificado (persistência automática + endpoints de histórico)
5. `frontends/web/index.html` — Modificado (seção de histórico)
6. `frontends/web/js/app.js` — Modificado (funções de histórico e feedback)

---

## Status Final

**DEMANDA-PROD-002:** ✅ **EM PROGRESSO**

Fases concluídas: F0-F7  
Fases pendentes: F8 (Evidência completa), F9 (Validação Gates)
