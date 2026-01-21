# DEFINIÇÃO: VALOR COGNITIVO PERSISTENTE

**Demanda:** DEMANDA-PROD-004 — Persistência Progressiva e Retomada Segura  
**Fase:** F1 — Definir "Valor Cognitivo Persistente"  
**Data:** 2026-01-21  
**Status:** ✅ DEFINIDO  
**Governado por:** END-FIRST v2

---

## 🔒 END (Resultado Observável)

**Definição clara e verificável do que constitui "valor cognitivo persistente"**

Esta definição permite ao sistema distinguir entre:
- **Valor cognitivo persistente** (não pode se perder)**
- **Processamento transitório** (pode ser descartado e recalculado)

---

## 📋 VALOR COGNITIVO PERSISTENTE

### Definição

**Valor cognitivo persistente** é qualquer artefato gerado pelo sistema que:
1. Representa conhecimento extraído do texto original
2. Não pode ser recalculado de forma idêntica sem reprocessar o texto
3. Tem valor independente do estado do processamento
4. Deve estar disponível para consulta mesmo após falha ou desconexão

### Lista Explícita de Artefatos

#### 1. Resumos de Capítulos Processados

**Estrutura:** `ChapterSummary`

**Campos que são valor cognitivo:**
- `numero` (str) - Número do capítulo
- `titulo` (str) - Título do capítulo
- `palavras` (int) - Contagem de palavras do texto original
- `palavras_resumo` (int) - Contagem de palavras do resumo gerado
- `paginas` (List[int]) - Páginas do capítulo (se detectadas)
- `resumo` (str) - Resumo completo do capítulo (300-500 palavras)
- `pontos_chave` (List[str]) - 5-8 pontos principais identificados
- `citacoes` (List[str]) - Citações marcantes extraídas
- `exemplos` (List[str]) - Exemplos concretos identificados

**Por que é valor cognitivo:**
- Representa conhecimento extraído do texto
- Não pode ser recalculado sem reprocessar o capítulo
- Tem valor independente (pode ser consultado isoladamente)

---

#### 2. Coverage Reports Parciais

**Estrutura:** `CoverageReport` (por capítulo ou parcial)

**Campos que são valor cognitivo:**
- `chapter_number` (str) - Número do capítulo
- `chapter_title` (str) - Título do capítulo
- `total_chunks` (int) - Total de chunks do capítulo
- `processed_chunks` (int) - Chunks já processados
- `chunk_coverage_percentage` (float) - Percentual de cobertura
- `recall_set` (RecallSetData) - Dados do recall set:
  - `critical_items_total` (int)
  - `critical_items_covered` (int)
  - `supporting_items_total` (int)
  - `missing_critical_item_ids` (List[str])
- `audit_result` (AuditResultData) - Resultado da auditoria:
  - `passed` (bool)
  - `regeneration_count` (int)
  - `addendum_count` (int)
  - `missing_markers` (List[str])
  - `invalid_chunks` (List[str])

**Por que é valor cognitivo:**
- Representa estado de processamento validado
- Não pode ser recalculado sem reprocessar
- Necessário para retomada segura (sabe o que já foi processado)

---

#### 3. Pontos-Chave Identificados

**Estrutura:** `List[str]` (5-8 pontos principais)

**Conteúdo:**
- Ideias principais do capítulo
- Conceitos-chave identificados
- Argumentos centrais extraídos

**Por que é valor cognitivo:**
- Representa síntese cognitiva do texto
- Não pode ser recalculado de forma idêntica
- Tem valor independente (pode ser consultado isoladamente)

---

#### 4. Citações Extraídas

**Estrutura:** `List[str]` (2-4 citações)

**Conteúdo:**
- Frases marcantes do autor
- Citações exatas do texto original
- Entre aspas, copiadas literalmente

**Por que é valor cognitivo:**
- Representa extração literal do texto
- Não pode ser recalculado (é citação exata)
- Tem valor independente (pode ser consultado isoladamente)

---

#### 5. Exemplos Encontrados

**Estrutura:** `List[str]` (2-5 exemplos)

**Conteúdo:**
- Casos concretos mencionados
- Nomes próprios identificados
- Estudos ou pesquisas citadas
- Experimentos mencionados

**Por que é valor cognitivo:**
- Representa extração de exemplos específicos
- Não pode ser recalculado de forma idêntica
- Tem valor independente (pode ser consultado isoladamente)

---

#### 6. Metadados de Processamento (Essenciais)

**Estrutura:** Metadados que permitem retomada segura

**Campos que são valor cognitivo:**
- `session_id` (str) - Identificador único da execução
- `timestamp_inicio` (datetime) - Quando processamento começou
- `timestamp_ultimo_checkpoint` (datetime) - Quando último checkpoint foi salvo
- `capitulos_processados` (List[str]) - Lista de números de capítulos já processados
- `chunks_processados_por_capitulo` (Dict[str, int]) - Quantos chunks foram processados por capítulo
- `total_chunks_por_capitulo` (Dict[str, int]) - Total de chunks por capítulo

**Por que é valor cognitivo:**
- Permite identificar onde parou
- Necessário para retomada segura
- Não pode ser recalculado (é histórico de execução)

---

## 🚫 PROCESSAMENTO TRANSITÓRIO (NÃO É VALOR COGNITIVO)

### Definição

**Processamento transitório** é qualquer artefato que:
1. É temporário e pode ser descartado
2. Pode ser recalculado sem perda de valor
3. Depende do estado atual do processamento
4. Não tem valor independente

### Lista Explícita de Artefatos Transitórios

#### 1. Logs de Processamento

**Exemplos:**
- Logs de debug (`logger.debug()`)
- Mensagens de progresso temporárias
- Logs de tentativas de regeneração

**Por que é transitório:**
- Pode ser recalculado
- Não tem valor independente
- É apenas rastreabilidade técnica

---

#### 2. Estados Temporários em Memória

**Exemplos:**
- Variáveis de controle de loop
- Flags de estado interno
- Contadores temporários
- Cache de chunks em memória

**Por que é transitório:**
- Depende do estado atual
- Pode ser recalculado
- Não tem valor independente

---

#### 3. Tentativas de Regeneração (Histórico)

**Exemplos:**
- Histórico de tentativas de regeneração (exceto contagem final)
- Versões intermediárias de resumos rejeitados
- Logs de validação intermediários

**Por que é transitório:**
- Representa processo, não resultado
- Pode ser descartado após validação final
- Não tem valor independente

**Exceção:** A contagem final de regenerações (`regeneration_count`) é valor cognitivo (está em `audit_result`).

---

#### 4. Chunks em Processamento

**Exemplos:**
- Chunks que ainda não foram processados
- Chunks em fila de processamento
- Estados intermediários de chunks

**Por que é transitório:**
- Ainda não foi extraído valor cognitivo
- Pode ser recalculado
- Não tem valor independente

**Exceção:** Chunks já processados e validados são parte do valor cognitivo (via `coverage_report`).

---

## 📊 DISTINÇÃO CLARA

### Critério Binário

**Um artefato é "valor cognitivo persistente" se:**

```
SE artefato representa conhecimento extraído do texto
E artefato não pode ser recalculado de forma idêntica sem reprocessar
E artefato tem valor independente do estado do processamento
ENTÃO artefato é VALOR COGNITIVO PERSISTENTE
```

**Um artefato é "processamento transitório" se:**

```
SE artefato pode ser recalculado sem perda de valor
OU artefato depende do estado atual do processamento
OU artefato não tem valor independente
ENTÃO artefato é PROCESSAMENTO TRANSITÓRIO
```

---

## ✅ EXEMPLOS PRÁTICOS

### ✅ Valor Cognitivo Persistente

1. **Resumo do Capítulo 1 processado:**
   - `resumo`: "O capítulo discute..."
   - `pontos_chave`: ["Ponto 1", "Ponto 2"]
   - `citacoes`: ["Citação exata"]
   - `exemplos`: ["Exemplo específico"]
   - **Por quê:** Conhecimento extraído, não pode ser recalculado idêntico

2. **Coverage Report do Capítulo 1:**
   - `processed_chunks: 10`
   - `chunk_coverage_percentage: 100.0`
   - `recall_set.critical_items_covered: 12`
   - **Por quê:** Estado validado, necessário para retomada

3. **Metadados de Processamento:**
   - `capitulos_processados: ["1", "2"]`
   - `timestamp_ultimo_checkpoint: "2026-01-21T10:30:00"`
   - **Por quê:** Permite identificar onde parou

### ❌ Processamento Transitório

1. **Log de debug:**
   - `"Processando chunk 5 de 10..."`
   - **Por quê:** Pode ser recalculado, não tem valor independente

2. **Cache de chunks em memória:**
   - Chunks não processados ainda
   - **Por quê:** Pode ser recalculado, depende do estado atual

3. **Tentativas intermediárias de regeneração:**
   - Versões de resumo rejeitadas pelo Quality Gate
   - **Por quê:** Processo, não resultado final

---

## 🧭 REGRAS CANÔNICAS APLICADAS

**"Valor cognitivo produzido não é descartável."**

Esta definição garante que:
- Todo conhecimento extraído é identificado
- Distinção clara entre valor e processo
- Critério binário e verificável

---

## 📌 PROVA DE VALIDAÇÃO

**Comando de Prova (F1):**

```bash
# Verificar que definição existe e está documentada
docker compose exec app bash -c 'test -f /app/DEMANDAS/DEMANDA-PROD-004_DEFINICAO_VALOR_COGNITIVO_PERSISTENTE.md && grep -q "valor cognitivo" /app/DEMANDAS/DEMANDA-PROD-004_DEFINICAO_VALOR_COGNITIVO_PERSISTENTE.md && echo "OK: definição existe" || echo "FAIL: definição não encontrada"'
```

**String Esperada:** `OK: definição existe`

---

## 📚 REFERÊNCIAS

- **ChapterSummary:** `src/chapter_summarizer.py` (linha 18-29)
- **CoverageReport:** `src/schemas/coverage_report.py`
- **SummaryStorage:** `src/schemas/summary_storage.py`
- **ProcessMetadataCollector:** `src/process_metadata_collector.py`

---

**Documento criado:** 2026-01-21  
**Última atualização:** 2026-01-21  
**Fase:** F1 — Definir "Valor Cognitivo Persistente"  
**Status:** ✅ COMPLETA  
**Governado por:** END-FIRST v2
