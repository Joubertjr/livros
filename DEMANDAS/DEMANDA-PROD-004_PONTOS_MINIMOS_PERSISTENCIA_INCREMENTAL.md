# DEFINIÇÃO: PONTOS MÍNIMOS DE PERSISTÊNCIA INCREMENTAL

**Demanda:** DEMANDA-PROD-004 — Persistência Progressiva e Retomada Segura  
**Fase:** F2 — Definir Pontos Mínimos de Persistência Incremental  
**Data:** 2026-01-21  
**Status:** ✅ DEFINIDO  
**Governado por:** END-FIRST v2  
**Base:** DEMANDA-PROD-004_DEFINICAO_VALOR_COGNITIVO_PERSISTENTE.md (F1)

---

## 🔒 END (Resultado Observável)

**Pontos de checkpoint definidos onde valor cognitivo deve ser persistido**

Esta definição estabelece:
- **Onde** persistir (pontos de checkpoint)
- **Quando** persistir (frequência mínima)
- **O que** pode ser retomado (critério de ponto válido)

---

## 📋 BASE: VALOR COGNITIVO PERSISTENTE (F1)

Esta definição é baseada **exclusivamente** na definição de F1, que identifica 6 categorias de valor cognitivo persistente:

1. **Resumos de Capítulos Processados** (`ChapterSummary`)
2. **Coverage Reports Parciais** (`CoverageReport`)
3. **Pontos-Chave Identificados** (`List[str]`) — parte de `ChapterSummary`
4. **Citações Extraídas** (`List[str]`) — parte de `ChapterSummary`
5. **Exemplos Encontrados** (`List[str]`) — parte de `ChapterSummary`
6. **Metadados de Processamento Essenciais** (session_id, timestamps, capítulos processados)

---

## 🎯 PONTOS DE CHECKPOINT (ONDE PERSISTIR)

### Análise do Pipeline Atual

**Fluxo de processamento identificado:**
1. Detecção de capítulos
2. Para cada capítulo:
   - Extração de Recall Set
   - Geração de resumo com auditoria e regeneração
   - Parse do resumo estruturado
   - Criação de `ChapterSummary` (contém: resumo, pontos_chave, citacoes, exemplos)
   - Geração de `CoverageReport` parcial
   - Coleta de metadados de processamento

**Observação crítica:**
- `pontos_chave`, `citacoes` e `exemplos` são **gerados junto** com o `ChapterSummary`
- Não há pontos intermediários onde esses valores são gerados separadamente
- O `CoverageReport` parcial é gerado **após** o `ChapterSummary` ser criado

### Ponto Mínimo de Checkpoint

**CHECKPOINT 1: Após Processamento Completo de Cada Capítulo**

**Justificativa (baseada em F1):**
- ✅ **Resumo do Capítulo** (`ChapterSummary`) está completo
- ✅ **Pontos-Chave** estão disponíveis (dentro de `ChapterSummary`)
- ✅ **Citações** estão disponíveis (dentro de `ChapterSummary`)
- ✅ **Exemplos** estão disponíveis (dentro de `ChapterSummary`)
- ✅ **Coverage Report Parcial** está disponível
- ✅ **Metadados de Processamento** podem ser atualizados (capítulo processado)

**Localização no código:**
- Após `_summarize_chapter_with_data()` retornar `summary` e `pipeline_data`
- Após `coverage_report` ser gerado para o capítulo
- Antes de processar o próximo capítulo

**Critério binário:**
```
SE ChapterSummary está completo
E CoverageReport parcial está disponível
E Metadados de processamento podem ser atualizados
ENTÃO checkpoint é válido e deve ser persistido
```

---

## ⏱️ FREQUÊNCIA MÍNIMA DE PERSISTÊNCIA

### Frequência Definida

**Frequência:** **Após cada capítulo processado**

**Justificativa (baseada em F1):**
- Cada capítulo gera **todos os 6 tipos** de valor cognitivo persistente
- Não há valor cognitivo gerado **entre** capítulos (apenas processamento transitório)
- Persistir após cada capítulo garante que **nenhum valor cognitivo se perde**
- É o **mínimo necessário** (não há necessidade de persistir mais frequentemente)

**Exceções:**
- ❌ **Não** persistir durante processamento de um capítulo (valor ainda não está completo)
- ❌ **Não** persistir a cada chunk (chunks são processamento transitório, não valor cognitivo)
- ❌ **Não** persistir a cada tentativa de regeneração (tentativas são transitórias)

**Critério de frequência mínima:**
```
Frequência mínima = Após cada capítulo processado
Razão: É o menor intervalo onde todos os 6 tipos de valor cognitivo estão completos
```

---

## ✅ CRITÉRIO DE "PONTO VÁLIDO" (O QUE PODE SER RETOMADO)

### Definição de Checkpoint Válido

**Um checkpoint é válido se contém:**

1. **ChapterSummary completo** do capítulo:
   - `numero`, `titulo`, `palavras`, `palavras_resumo`, `paginas`
   - `resumo` (300-500 palavras)
   - `pontos_chave` (5-8 pontos)
   - `citacoes` (2-4 citações)
   - `exemplos` (2-5 exemplos)

2. **CoverageReport parcial** do capítulo:
   - `chapter_number`, `chapter_title`
   - `total_chunks`, `processed_chunks`
   - `chunk_coverage_percentage`
   - `recall_set` completo
   - `audit_result` completo

3. **Metadados de processamento atualizados:**
   - `session_id` (identificador único da execução)
   - `timestamp_ultimo_checkpoint` (quando checkpoint foi salvo)
   - `capitulos_processados` (lista incluindo o capítulo atual)
   - `chunks_processados_por_capitulo` (atualizado com o capítulo atual)

**Critério binário de validade:**
```
SE checkpoint contém ChapterSummary completo
E checkpoint contém CoverageReport parcial
E checkpoint contém metadados atualizados
E checkpoint foi salvo atomicamente (ou tudo ou nada)
ENTÃO checkpoint é VÁLIDO e pode ser usado para retomada
```

### Checkpoint Inválido

**Um checkpoint é inválido se:**
- ❌ `ChapterSummary` está incompleto (faltam campos obrigatórios)
- ❌ `CoverageReport` está ausente ou incompleto
- ❌ Metadados não foram atualizados
- ❌ Persistência foi interrompida (arquivo corrompido ou parcial)
- ❌ Validação de schema falhou

**Tratamento de checkpoint inválido:**
- Sistema deve identificar o último checkpoint válido anterior
- Retomada deve ocorrer a partir do último checkpoint válido
- Checkpoint inválido deve ser descartado (não usado para retomada)

---

## 📊 RESUMO DOS PONTOS DE CHECKPOINT

### Lista Explícita

1. **Após processamento de cada capítulo**
   - **Valor cognitivo persistido:**
     - `ChapterSummary` completo (inclui resumo, pontos_chave, citacoes, exemplos)
     - `CoverageReport` parcial do capítulo
     - Metadados de processamento atualizados
   - **Frequência:** Após cada capítulo
   - **Critério de validade:** Todos os campos obrigatórios presentes e validados

### Pontos NÃO Incluídos (Justificativa)

**❌ Após geração de pontos-chave isoladamente:**
- **Razão:** Pontos-chave são gerados **junto** com `ChapterSummary`, não isoladamente
- **Base F1:** Pontos-chave são parte de `ChapterSummary`, não valor cognitivo independente

**❌ Após extração de citações isoladamente:**
- **Razão:** Citações são geradas **junto** com `ChapterSummary`, não isoladamente
- **Base F1:** Citações são parte de `ChapterSummary`, não valor cognitivo independente

**❌ Após identificação de exemplos isoladamente:**
- **Razão:** Exemplos são gerados **junto** com `ChapterSummary`, não isoladamente
- **Base F1:** Exemplos são parte de `ChapterSummary`, não valor cognitivo independente

**❌ Após processamento de cada chunk:**
- **Razão:** Chunks são **processamento transitório**, não valor cognitivo persistente
- **Base F1:** "Chunks em processamento" são explicitamente listados como transitórios

**❌ Após cada tentativa de regeneração:**
- **Razão:** Tentativas são **processamento transitório**, não valor cognitivo persistente
- **Base F1:** "Tentativas de regeneração (histórico)" são explicitamente listadas como transitórias

---

## 🧭 REGRAS CANÔNICAS APLICADAS

**"Execução longa sem persistência progressiva é desperdício estrutural."**

Esta definição garante que:
- ✅ Persistência ocorre no **mínimo necessário** (após cada capítulo)
- ✅ **Nenhum valor cognitivo se perde** (todos os 6 tipos são persistidos)
- ✅ **Não há persistência desnecessária** (não persiste processamento transitório)
- ✅ Critério binário e verificável

---

## 📌 PROVA DE VALIDAÇÃO

**Comando de Prova (F2):**

```bash
# Verificar que pontos de checkpoint estão documentados
docker compose exec app bash -c 'grep -E "checkpoint|persistência incremental" /app/planejamento/DEMANDA-PROD-004_PLAN.md | head -5'
```

**String Esperada:** Deve encontrar referências a "checkpoint" e "persistência incremental"

**Prova adicional:**
```bash
# Verificar que definição de pontos mínimos existe
test -f DEMANDAS/DEMANDA-PROD-004_PONTOS_MINIMOS_PERSISTENCIA_INCREMENTAL.md && grep -q "checkpoint" DEMANDAS/DEMANDA-PROD-004_PONTOS_MINIMOS_PERSISTENCIA_INCREMENTAL.md && echo "OK: pontos definidos" || echo "FAIL: pontos não encontrados"
```

**String Esperada:** `OK: pontos definidos`

---

## 📚 REFERÊNCIAS

- **F1 - Valor Cognitivo Persistente:** `DEMANDAS/DEMANDA-PROD-004_DEFINICAO_VALOR_COGNITIVO_PERSISTENTE.md`
- **Pipeline:** `src/summarizer_robust.py` (método `_summarize_chapter_with_data`)
- **ChapterSummary:** `src/chapter_summarizer.py` (linha 18-29)
- **CoverageReport:** `src/schemas/coverage_report.py`

---

**Documento criado:** 2026-01-21  
**Última atualização:** 2026-01-21  
**Fase:** F2 — Definir Pontos Mínimos de Persistência Incremental  
**Status:** ✅ COMPLETA  
**Governado por:** END-FIRST v2
