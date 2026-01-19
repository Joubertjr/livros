---
name: Book Summarizer Robusto - Pipeline Verificável
overview: Evoluir o sistema atual para um pipeline robusto e verificável que garante cobertura completa através de Recall Sets, extração primária por chunks, auditoria cruzada automática e evidências estruturadas.
todos:
  - id: "0"
    content: "Definir contrato do Recall Set + Auditoria determinística: formato JSON com item_id (hash imutável), critical/supporting, enum CriticalityReason, regra de marcadores [[RS:cap(\d+):hash|chunks:...]] com evidência de ancoragem, auditoria determinística com validação anti-fraude, coverage_report.json (PRIORIDADE 1 - BLOQUEANTE)"
    status: pending
  - id: "0.1"
    content: "Atualizar .cursorrules com regras mínimas: TDD + estrutura de testes + regra de marcadores no resumo + regra de evidências"
    status: pending
  - id: "1"
    content: "Adicionar dependências de testes (pytest, pytest-cov, pytest-mock) ao requirements.txt e criar estrutura de diretórios de testes (src/tests/unit/, src/tests/integration/, src/tests/fixtures/)"
    status: pending
  - id: "2"
    content: "Criar módulo chunk_extractor.py com extração primária estruturada por chunk (TDD: testes antes do código, Clean Code, type hints, docstrings)"
    status: pending
  - id: "3"
    content: "Criar módulo recall_auditor.py com auditoria cruzada automática (TDD: testes antes do código, Clean Code, type hints, docstrings)"
    status: pending
  - id: "4"
    content: "Refatorar chapter_summarizer.py: adicionar divisão em chunks numerados, integrar extração primária, gerar Recall Set, usar Recall Set no prompt, integrar auditoria com loop de regeneração (com testes)"
    status: pending
  - id: "5"
    content: "Atualizar quality_gate.py: adicionar validação de cobertura (100% chunks processados, todos Recall Sets passaram na auditoria) (com testes TDD)"
    status: pending
  - id: "6"
    content: "Atualizar evidence_generator.py: adicionar relatório de cobertura estruturado (capítulos, chunks, %, Recall Sets, resultados de auditoria, logs de regeneração) (com testes)"
    status: pending
  - id: "7"
    content: "Atualizar summarizer.py: integrar novo pipeline robusto, validação final antes de retornar resultado, tratamento de falhas com erro claro (com testes de integração)"
    status: pending
  - id: "8"
    content: "Garantir cobertura de testes >= 80% e executar todos os testes (unitários e integração)"
    status: pending
  - id: "9"
    content: "Testar pipeline completo com livro real e validar todos os critérios binários (100% chunks, Recall Sets, auditoria, evidências)"
    status: pending
  - id: "10"
    content: "Code review e refatoração final (aplicar Clean Code, remover duplicação, melhorar legibilidade)"
    status: pending
---

# Plano: Book Summarizer Robusto - Pipeline Verificável

## Análise do Estado Atual vs. Demanda

### O que já existe:

- ✅ Detecção de capítulos (MarkdownParser)
- ✅ Resumos por capítulo (ChapterSummarizer)
- ✅ Resumo executivo/global
- ✅ Quality Gate básico (valida comprimento, conteúdo, estrutura)
- ✅ Chunking de texto (ChunkProcessor) - mas não usado para capítulos
- ✅ Geração de evidências básica (EvidenceGenerator)

### O que falta (GAPS críticos):

- ❌ **Etapa 1**: Capítulos não são divididos em chunks numerados com chunk_id
- ❌ **Etapa 2**: Não existe extração primária estruturada por chunk (ideias, conceitos, afirmações, exemplos)
- ❌ **Etapa 3**: Não existe Recall Set por capítulo (lista mínima obrigatória)
- ❌ **Etapa 4**: Resumo não usa Recall Set explicitamente
- ❌ **Etapa 5**: Não existe auditoria cruzada automática (verificar se Recall Set está no resumo)
- ❌ **Etapa 6**: Resumo global já existe, mas precisa manter rastreabilidade
- ❌ Quality Gate atual é subjetivo (palavras em comum) - não prova cobertura
- ❌ Evidências não incluem relatório de cobertura estruturado

---

## Arquitetura do Novo Pipeline

```
[PDF/MD] 
  ↓
[Etapa 1: Ingestão Estrutural]
  ├─ Detectar capítulos (já existe)
  └─ Dividir cada capítulo em chunks numerados (chunk_id)
  ↓
[Etapa 2: Extração Primária por Chunk]
  ├─ Para cada chunk: extrair ideias, conceitos, afirmações, exemplos
  └─ Salvar como estrutura intermediária (JSON)
  ↓
[Etapa 3: Recall Set por Capítulo]
  ├─ Agregar extrações de todos os chunks do capítulo
  └─ Gerar lista mínima obrigatória (conceitos, teses, definições, exemplos)
  ↓
[Etapa 4: Resumo do Capítulo]
  ├─ Gerar resumo usando Recall Set explicitamente
  └─ Garantir que todo item do Recall Set está representado
  ↓
[Etapa 5: Auditoria Cruzada Automática]
  ├─ Verificar: "O que está no Recall Set e NÃO está no resumo?"
  ├─ Se faltar item crítico → ❌ FALHA → 🔁 REGENERAR
  └─ Repetir até passar ou max tentativas
  ↓
[Etapa 6: Resumo Global]
  ├─ Gerar a partir dos resumos dos capítulos (já existe)
  └─ Manter rastreabilidade capítulo → global
  ↓
[Evidências Estruturadas]
  ├─ Relatório de cobertura (capítulos, chunks, % processado)
  ├─ Recall Set por capítulo
  ├─ Resultado da auditoria (pass/fail)
  └─ Logs de regeneração
```

---

## Contrato do Recall Set (DEFINIR PRIMEIRO - BLOQUEANTE)

**⚠️ CRÍTICO**: Este contrato deve ser definido e documentado ANTES de qualquer implementação. Sem isso, o sistema é frágil.

### Estrutura de Dados

```python
from enum import Enum

class CriticalityReason(Enum):
    MULTI_CHUNK = "MULTI_CHUNK"                    # Aparece em ≥2 chunks
    STRUCTURAL_POSITION = "STRUCTURAL_POSITION"    # Heading/título/primeira/última seção
    DEFINITION_MARKER = "DEFINITION_MARKER"         # Contém marcador de definição
    LAW_MARKER = "LAW_MARKER"                       # É passo/heurística/lei

@dataclass
class RecallSetItem:
    item_id: str                      # "RS:cap1:9f3a1c" (hash do conteúdo normalizado, imutável)
    content: str                      # Texto do item
    content_normalized: str           # Conteúdo normalizado (lowercase, sem pontuação) para hash
    level: str                        # "critical" ou "supporting"
    source_chunks: List[int]          # Chunks onde aparece (para rastreabilidade)
    criticality_reason: CriticalityReason  # Enum: MULTI_CHUNK, STRUCTURAL_POSITION, etc.

@dataclass
class ChapterRecallSet:
    chapter_number: str
    chapter_title: str
    critical_items: List[RecallSetItem]    # Máximo 12 itens (HARD CAP)
    supporting_items: List[RecallSetItem]  # Sem limite, mas não auditado como bloqueio
    chunk_extractions: List[ChunkExtraction]  # Extrações originais
```

### Regras de Criticidade (MECÂNICAS - SÓ ENUM)

Um item é `critical` se atender a pelo menos 1 das regras abaixo (implementação determinística):

1. **MULTI_CHUNK**: Aparece em ≥2 chunks do capítulo (sinal de importância estrutural)
2. **STRUCTURAL_POSITION**: Está em heading/título/primeira ou última seção (posição estrutural)
3. **DEFINITION_MARKER**: Contém marcador de definição (regex para "is/means/define", "é/define", "significa")
4. **LAW_MARKER**: É um passo/heurística/lei (regex para "sempre", "nunca", "regra", "portanto", "conclusão")

**Hard Cap**: Máximo 12 itens `critical` por capítulo. Se mais de 12, priorizar por:
- Frequência (aparece em mais chunks)
- Posição estrutural (headings > início > meio > fim)
- Marcadores de definição/lei

**IMPORTANTE**: `criticality_reason` é SEMPRE um enum (`CriticalityReason`), nunca texto livre.

### Geração de item_id (DETERMINÍSTICO E IMUTÁVEL)

**Regra**: `item_id = f"RS:cap{chapter_number}:{hash_curto}"`

Onde:
- `hash_curto` = primeiros 6 caracteres do hash SHA256 do `content_normalized`
- `content_normalized` = conteúdo em lowercase, sem pontuação, espaços normalizados

**Exemplo**:
- Conteúdo: "A dopamina é um neurotransmissor..."
- Normalizado: "a dopamina é um neurotransmissor"
- Hash SHA256: `9f3a1c...` (primeiros 6 chars)
- `item_id`: `RS:cap1:9f3a1c`

**Vantagem**: Reprocessar não muda IDs (imutável).

### Formato de Marcadores no Resumo (COM EVIDÊNCIA DE ANCORAGEM)

Cada item `critical` do Recall Set DEVE aparecer no resumo com marcador e evidência de ancoragem:

**Formato obrigatório**:
```
[[RS:cap1:9f3a1c|chunks:2,4]]
```

ou

```
[[RS:cap1:9f3a1c|src:cap1_chunk_2,cap1_chunk_4]]
```

Onde:
- `RS` = Recall Set
- `cap1` = número do capítulo
- `9f3a1c` = hash curto do conteúdo (item_id)
- `chunks:2,4` = referência aos chunks de origem (índices numéricos)
- `src:cap1_chunk_2,cap1_chunk_4` = referência aos chunks de origem (chunk_ids)

**Regex para extração**: `\[\[RS:cap(\d+):([a-f0-9]{6})\|(chunks|src):([^\]]+)\]\]`

**Anti-fraude**: O marcador sem evidência de ancoragem é INVÁLIDO. O auditor verifica:
1. Marcador existe ✅
2. Referência de chunks existe ✅
3. **Mínimo 1 chunk**: `chunks:` ou `src:` deve ter pelo menos 1 inteiro válido ✅
4. Chunks referenciados são válidos ✅ (cada chunk deve estar em `source_chunks` do Recall Set)

### Regra de Auditoria Determinística (COM VALIDAÇÃO DE ANCORAGEM)

**Camada A (Determinística - OBRIGATÓRIA)**:
1. Extrair todos os marcadores `[[RS:cap(\d+):hash|chunks:...]]` do resumo via regex
2. Para cada marcador extraído:
   - Validar que `item_id` existe no `critical_items` do Recall Set ✅
   - Validar que referência de chunks existe (`chunks:` ou `src:`) ✅
   - **Validar mínimo 1 chunk**: `chunks:` ou `src:` deve ter pelo menos 1 inteiro válido ✅
   - Validar que chunks referenciados estão em `source_chunks` do item ✅ (cada chunk deve estar na lista)
3. Comparar com `critical_items` do Recall Set:
   - Se todos os `critical_items` têm marcador válido → PASSA
   - Se falta qualquer marcador → FALHA (regenerar)
   - Se marcador existe mas chunks inválidos (vazio, sem chunks, ou não estão em `source_chunks`) → FALHA (regenerar)
4. Não depende de LLM, é validação pura (regex + comparação)

**Camada B (LLM opcional - NÃO BLOQUEANTE)**:
- Valida qualidade textual (redundância, clareza, coesão)
- NUNCA valida cobertura (isso é Camada A)
- Pode retornar score 0-1, mas não bloqueia aprovação

---

## Implementação Detalhada

**⚠️ IMPORTANTE**: Antes de implementar qualquer módulo, o **Contrato do Recall Set** (seção anterior) deve estar completamente definido e documentado.

### 1. Novo Módulo: `chunk_extractor.py`

**Responsabilidade**: Extração primária estruturada por chunk

**Estruturas de dados**:

```python
@dataclass
class ChunkExtraction:
    chunk_id: str                    # "cap_1_chunk_3"
    chapter_number: str
    chunk_number: int
    text: str
    ideias_centrais: List[str]       # Ideias principais do chunk
    conceitos_termos: List[str]       # Conceitos/termos importantes
    afirmacoes_autor: List[str]      # Afirmações do autor
    exemplos_relevantes: List[str]   # Exemplos mencionados

@dataclass
class ChapterRecallSet:
    chapter_number: str
    chapter_title: str
    critical_items: List[RecallSetItem]    # Máximo 12 (HARD CAP)
    supporting_items: List[RecallSetItem]  # Sem limite
    chunk_extractions: List[ChunkExtraction]  # Extrações originais
```

**Métodos principais**:

- `extract_from_chunk(chunk_text, chunk_id) -> ChunkExtraction`: Extrai estrutura do chunk usando LLM
- `aggregate_to_recall_set(chunk_extractions) -> ChapterRecallSet`: Agrega chunks em Recall Set

**Arquivo**: `src/chunk_extractor.py`

---

### 2. Novo Módulo: `recall_auditor.py`

**Responsabilidade**: Auditoria cruzada automática (DETERMINÍSTICA)

**Estrutura**:

```python
@dataclass
class AuditResult:
    chapter_number: str
    passed: bool                      # True se todos critical_items têm marcador
    missing_markers: List[str]        # item_ids sem marcador [[RS:...]]
    coverage_percentage: float         # % de marcadores encontrados (critical_items)
    critical_missing: List[str]        # item_ids críticos faltantes (mesmo que missing_markers)
    llm_quality_score: Optional[float]  # Opcional: qualidade textual (não bloqueia)
```

**Métodos principais**:

- `audit_chapter_summary_deterministic(recall_set, summary) -> AuditResult`: 
  - **Camada A (Determinística)**: Valida marcadores `[[RS:cap(\d+):hash|chunks:...]]` no resumo
  - Extrai todos os marcadores com regex: `\[\[RS:cap(\d+):([a-f0-9]{6})\|(chunks|src):([^\]]+)\]\]`
  - Para cada marcador:
    - Valida que `item_id` existe no `critical_items` ✅
    - Valida que referência de chunks existe ✅
    - **Valida mínimo 1 chunk**: `chunks:` ou `src:` deve ter pelo menos 1 inteiro válido ✅
    - Valida que chunks referenciados estão em `source_chunks` do item ✅ (cada chunk deve estar na lista)
  - Compara com `critical_items` do Recall Set
  - Retorna `passed=False` se:
    - Qualquer `critical_item` não tem marcador, OU
    - Marcador existe mas chunks inválidos (anti-fraude: vazio, sem chunks, ou chunks não estão em `source_chunks`)
  
- `audit_chapter_summary_llm_quality(recall_set, summary) -> Optional[float]`:
  - **Camada B (Opcional)**: Valida qualidade textual, redundância, clareza
  - NUNCA valida cobertura (isso é Camada A)
  - Retorna score 0-1 ou None se não executado

- `should_regenerate(audit_result) -> bool`: 
  - Retorna `True` se `audit_result.passed == False`
  - Não depende de LLM

**Arquivo**: `src/recall_auditor.py`

**IMPORTANTE**: A auditoria determinística (Camada A) é OBRIGATÓRIA e BLOQUEANTE. A Camada B (LLM) é opcional e não bloqueia.

---

### 3. Refatorar: `chapter_summarizer.py`

**Mudanças necessárias**:

1. **Adicionar divisão em chunks**:
   - Método `_chunk_chapter(chapter_text) -> List[Chunk]`: Divide capítulo em chunks numerados
   - Cada chunk recebe `chunk_id` único: `f"cap_{chapter.number}_chunk_{i}"`

2. **Integrar extração primária**:
   - Chamar `ChunkExtractor.extract_from_chunk()` para cada chunk
   - Salvar extrações como estrutura intermediária

3. **Gerar Recall Set**:
   - Chamar `ChunkExtractor.aggregate_to_recall_set()` após processar todos os chunks

4. **Usar Recall Set no prompt**:
   - Modificar prompt de resumo para incluir explicitamente o Recall Set
   - **OBRIGATÓRIO**: Exigir que cada `critical_item` apareça no resumo com marcador e evidência de ancoragem
   - Formato: `[[RS:cap(\d+):hash|chunks:N,M]]` onde `hash` é o `item_id` e `N,M` são os `source_chunks`
   - Exemplo no prompt: "Cada item crítico do Recall Set DEVE aparecer com seu marcador e chunks de origem: [[RS:cap1:9f3a1c|chunks:2,4]], [[RS:cap1:a2b3c4|chunks:1,3,5]], etc."

5. **Integrar auditoria**:
   - Após gerar resumo, chamar `RecallAuditor.audit_chapter_summary()`
   - Se falhar, regenerar com prompt reforçado
   - Loop até passar ou max tentativas (3)

**Mudanças no `ChapterSummary`**:

```python
@dataclass
class ChapterSummary:
    # ... campos existentes ...
    recall_set: ChapterRecallSet      # NOVO
    audit_result: AuditResult        # NOVO
    chunk_extractions: List[ChunkExtraction]  # NOVO
    regeneration_count: int = 0       # NOVO
```

---

### 4. Refatorar: `quality_gate.py`

**Mudanças necessárias**:

1. **Usar `coverage_report.json` como fonte única de verdade**:
   - Quality Gate **NÃO recalcula** no ar
   - Método `validate_from_coverage_report(coverage_report_path) -> bool`: Lê `EVIDENCIAS/coverage_report.json`
   - Critério binário: 
     - ✅ `overall_coverage_percentage == 100.0`
     - ✅ `missing_critical_item_ids` vazio em TODOS os capítulos
     - ✅ `total_chapters == chapters_processed`
     - ✅ `total_critical_items == total_covered`

2. **Validação determinística**:
   - Se arquivo não existe → FALHA
   - Se estrutura JSON inválida → FALHA
   - Se qualquer critério acima falhar → FALHA
   - Não depende de recálculo, apenas leitura do arquivo gerado

3. **Integrar com pipeline**:
   - Quality Gate só aprova se `coverage_report.json` mostrar 100% de cobertura
   - Fonte única de verdade: o arquivo gerado, não recálculo em memória

---

### 5. Refatorar: `evidence_generator.py`

**Mudanças necessárias**:

1. **Adicionar relatório de cobertura**:
   - Seção "Cobertura de Capítulos e Chunks"
   - Lista: capítulos processados, chunks por capítulo, % processado

2. **Adicionar Recall Sets**:
   - Seção "Recall Sets por Capítulo"
   - Mostrar conceitos, teses, definições, exemplos de cada capítulo

3. **Adicionar resultados de auditoria**:
   - Seção "Auditoria Cruzada"
   - Mostrar pass/fail por capítulo, itens faltantes, % de cobertura

4. **Adicionar logs de regeneração**:
   - Seção "Regenerações"
   - Mostrar quantas vezes cada capítulo foi regenerado

5. **Gerar Matriz de Cobertura (BINÁRIA)**:
   - Arquivo obrigatório: `EVIDENCIAS/coverage_report.json`
   - Estrutura binária e fácil de auditar (1 linha por item crítico)

**Formato de saída**: JSON estruturado + Markdown legível + `coverage_report.json`

### Estrutura do coverage_report.json

**Arquivo obrigatório**: `EVIDENCIAS/coverage_report.json`

**Estrutura mínima**:
```json
{
  "chapters": [
    {
      "chapter_number": "1",
      "chapter_title": "The Problem",
      "total_chunks": 5,
      "processed_chunks": 5,
      "critical_items_total": 8,
      "critical_items_covered": 8,
      "missing_critical_item_ids": [],
      "regeneration_count": 0,
      "coverage_percentage": 100.0,
      "items": [
        {
          "item_id": "RS:cap1:9f3a1c",
          "content_preview": "A dopamina é...",
          "criticality_reason": "MULTI_CHUNK",
          "source_chunks": [2, 4],
          "covered": true,
          "marker_found": true,
          "chunks_validated": true
        }
      ]
    }
  ],
  "summary": {
    "total_chapters": 11,
    "chapters_processed": 11,
    "total_critical_items": 95,
    "total_covered": 95,
    "overall_coverage_percentage": 100.0
  }
}
```

**Propósito**: Painel binário do sistema. Fácil de auditar, sem ambiguidade.

---

### 6. Atualizar: `summarizer.py`

**Mudanças necessárias**:

1. **Integrar novo pipeline**:
   - Quando capítulos detectados, usar novo pipeline robusto
   - Garantir que todas as etapas sejam executadas em ordem

2. **Validação final**:
   - Antes de retornar resultado, verificar:
     - ✅ 100% chunks processados
     - ✅ Todo capítulo tem Recall Set
     - ✅ Todo Recall Set passou na auditoria
     - ✅ Evidências geradas

3. **Tratamento de falhas**:
   - Se qualquer critério falhar → resultado inválido
   - Retornar erro claro indicando qual critério falhou

---

### 7. Estrutura de Dados Intermediária

**Salvar extrações primárias**:

- Formato: JSON
- Localização: `EVIDENCIAS/extractions_{timestamp}.json`
- Estrutura:
```json
{
  "chapters": [
    {
      "chapter_number": "1",
      "chapter_title": "The Problem",
      "chunks": [
        {
          "chunk_id": "cap_1_chunk_1",
          "chunk_number": 1,
          "text": "...",
          "extraction": {
            "ideias_centrais": [...],
            "conceitos_termos": [...],
            "afirmacoes_autor": [...],
            "exemplos_relevantes": [...]
          }
        }
      ],
      "recall_set": {
        "conceitos": [...],
        "teses": [...],
        "definicoes": [...],
        "exemplos": [...]
      }
    }
  ]
}
```

---

## Critérios de Qualidade Binários

O sistema SÓ retorna resultado válido se:

1. ✅ **100% dos chunks processados**: `total_chunks == processed_chunks`
2. ✅ **Todo capítulo tem Recall Set**: `len(recall_sets) == len(chapters)`
3. ✅ **Todo Recall Set tem ≤12 itens críticos**: `all(len(rs.critical_items) <= 12 for rs in recall_sets)`
4. ✅ **Todo Recall Set passou na auditoria determinística**: `all(audit.passed for audit in audit_results)`
   - Auditoria determinística: todos `critical_items` têm marcador válido `[[RS:cap(\d+):hash|chunks:...]]` no resumo
   - Validação anti-fraude: marcador existe, mínimo 1 chunk válido, chunks referenciados estão em `source_chunks`
   - Não depende de LLM, é validação pura (regex + comparação)
5. ✅ **Nenhuma omissão crítica**: `all(len(audit.critical_missing) == 0 for audit in audit_results)`
6. ✅ **Evidências geradas**: Arquivo de evidência existe e é válido

Se qualquer um falhar → **resultado inválido** → erro claro

**IMPORTANTE**: A auditoria determinística (contagem de marcadores) é OBRIGATÓRIA e BLOQUEANTE. LLM pode validar qualidade textual, mas NUNCA valida cobertura.

---

## Fluxo de Execução

```
1. Detectar capítulos (MarkdownParser) ✅
2. Para cada capítulo:
   a. Dividir em chunks numerados
   b. Para cada chunk:
      - Extrair estrutura (ideias, conceitos, afirmações, exemplos)
      - Salvar extração
   c. Agregar extrações → Recall Set
   d. Gerar resumo usando Recall Set
   e. Auditar resumo vs Recall Set
   f. Se falhar → regenerar (max 3x)
3. Gerar resumo global dos resumos dos capítulos
4. Gerar evidências estruturadas (incluindo `coverage_report.json`)
5. Validar cobertura completa (Quality Gate lê `coverage_report.json` como fonte única)
6. Retornar resultado (ou erro se inválido)
```

---

## Arquivos a Criar/Modificar

### Novos arquivos:

- `src/chunk_extractor.py` - Extração primária por chunk
- `src/recall_auditor.py` - Auditoria cruzada automática

### Arquivos a modificar:

- `.cursorrules` - Adicionar regras de Clean Code/TDD, estrutura de testes, regras operacionais e checklist
- `requirements.txt` ou `pyproject.toml` - Adicionar pytest, pytest-cov, pytest-mock
- `src/chapter_summarizer.py` - Integrar chunks, Recall Set, auditoria
- `src/quality_gate.py` - Adicionar validação de cobertura usando `coverage_report.json` como fonte única
- `src/evidence_generator.py` - Adicionar relatório de cobertura estruturado
- `src/summarizer.py` - Integrar novo pipeline e validação final

### Estrutura de testes a criar:

- `src/tests/unit/test_chunk_extractor.py`
- `src/tests/unit/test_recall_auditor.py`
- `src/tests/integration/test_pipeline_complete.py`
- `src/tests/fixtures/sample_chapters.json`

---

## Considerações Técnicas

1. **Chunking de capítulos**:
   - Usar `ChunkProcessor` existente, mas adaptado para capítulos
   - Tamanho: 800-1200 palavras por chunk (menor que texto completo)
   - Overlap: 100 palavras

2. **Extração primária**:
   - Usar LLM (gpt-4o-mini) com prompt estruturado
   - Formato de resposta: JSON ou texto estruturado parseável
   - Retry com backoff exponencial

3. **Recall Set**:
   - Agregar extrações removendo duplicatas
   - Aplicar regras mecânicas de criticidade (≥2 chunks, heading, definição, lei)
   - **HARD CAP**: Máximo 12 itens `critical` por capítulo
   - Se mais de 12, priorizar por frequência e posição estrutural
   - `supporting_items` sem limite, mas não auditado como bloqueio

4. **Auditoria**:
   - **Camada A (Determinística)**: Validar marcadores `[[RS:cap(\d+):hash|chunks:...]]` no resumo via regex
   - Validação anti-fraude: marcador existe, mínimo 1 chunk válido, chunks referenciados estão em `source_chunks`
   - Se todos `critical_items` têm marcador válido → PASSA
   - Se falta qualquer marcador ou chunks inválidos (vazio, sem chunks, ou não estão em `source_chunks`) → FALHA (regenerar)
   - **Camada B (Opcional)**: LLM valida qualidade textual (redundância, clareza)
   - LLM NUNCA valida cobertura (isso é Camada A)

5. **Performance**:
   - Processar chunks em paralelo (dentro de cada capítulo)
   - Processar capítulos em paralelo
   - Cache de extrações para evitar reprocessamento

---

## Testes e Validação

1. **Teste unitário**: Extração primária de um chunk
2. **Teste unitário**: Agregação de chunks em Recall Set
3. **Teste unitário**: Auditoria de resumo vs Recall Set
4. **Teste de integração**: Pipeline completo com livro pequeno (3-5 capítulos)
5. **Teste de regressão**: Verificar que resumos ainda são gerados corretamente

---

## Clean Code / TDD: Regras Operacionais para Desenvolvimento

### Princípios de Clean Code

1. **Nomes Significativos**:
   - Variáveis, funções e classes devem ter nomes que expressam claramente sua intenção
   - Evitar abreviações desnecessárias
   - Exemplo: `extract_chunk_ideas()` ao invés de `ext()`

2. **Funções Pequenas e com Responsabilidade Única**:
   - Uma função deve fazer uma coisa e fazer bem
   - Máximo 20-30 linhas por função
   - Se uma função faz mais de uma coisa, dividir em funções menores

3. **Comentários Explicativos, não Óbvios**:
   - Comentários devem explicar "por quê", não "o quê"
   - Código autoexplicativo é preferível a comentários
   - Documentar decisões de design e trade-offs

4. **Estruturas de Dados Simples**:
   - Preferir dataclasses para estruturas de dados
   - Evitar dicionários aninhados complexos
   - Type hints obrigatórios em todas as funções

5. **Tratamento de Erros Explícito**:
   - Nunca usar `except: pass` silencioso
   - Erros devem ser específicos e informativos
   - Usar exceções customizadas quando apropriado

6. **Sem Duplicação (DRY)**:
   - Extrair código duplicado em funções reutilizáveis
   - Usar composição ao invés de repetição

7. **Separação de Responsabilidades**:
   - Cada módulo/classe tem uma responsabilidade clara
   - Alta coesão, baixo acoplamento

### Test-Driven Development (TDD)

**Ciclo Red-Green-Refactor obrigatório**:

1. **RED**: Escrever teste que falha (define comportamento esperado)
2. **GREEN**: Escrever código mínimo para passar no teste
3. **REFACTOR**: Melhorar código mantendo testes passando

**Regras de TDD**:

1. **Teste antes do código**:
   - Nunca escrever código de produção sem teste correspondente
   - Teste define a interface e comportamento esperado

2. **Testes unitários obrigatórios**:
   - Cada função pública deve ter pelo menos um teste
   - Cobertura mínima: 80% (objetivo: 90%+)

3. **Testes de integração**:
   - Testar fluxo completo do pipeline
   - Testar integração entre módulos

4. **Testes determinísticos**:
   - Sempre usar dados fixos/mocks para testes
   - Não depender de ordem de execução
   - Não depender de estado externo (API, arquivos)

5. **Estrutura AAA (Arrange-Act-Assert)**:
   ```python
   def test_extract_chunk_ideas():
       # Arrange
       chunk_text = "Texto de exemplo..."
       chunk_id = "cap_1_chunk_1"
       
       # Act
       result = extractor.extract_from_chunk(chunk_text, chunk_id)
       
       # Assert
       assert len(result.ideias_centrais) > 0
       assert result.chunk_id == chunk_id
   ```

6. **Testes isolados**:
   - Cada teste deve ser independente
   - Não compartilhar estado entre testes
   - Usar fixtures/pytest quando necessário

### Estrutura de Testes

**Organização**:

```
src/
  tests/
    unit/
      test_chunk_extractor.py
      test_recall_auditor.py
      test_quality_gate.py
    integration/
      test_pipeline_complete.py
      test_chapter_summarization.py
    fixtures/
      sample_chapters.json
      sample_chunks.txt
```

**Convenções de nomenclatura**:

- Arquivos de teste: `test_*.py`
- Funções de teste: `test_*`
- Classes de teste: `Test*`

**Ferramentas**:

- Framework: `pytest`
- Mocks: `unittest.mock` ou `pytest-mock`
- Cobertura: `pytest-cov`
- Fixtures: `pytest.fixture`

### Regras Operacionais de Desenvolvimento

1. **Commits Atômicos**:
   - Um commit = uma funcionalidade/teste completo
   - Mensagens claras: "feat: adiciona extração primária por chunk"
   - Nunca commitar código que quebra testes

2. **Code Review Obrigatório** (se aplicável):
   - Verificar: testes passando, cobertura adequada, Clean Code
   - Revisar lógica, não apenas sintaxe

3. **Refatoração Contínua**:
   - Refatorar após adicionar funcionalidade
   - Manter código limpo a cada iteração
   - Não acumular "dívida técnica"

4. **Documentação de Código**:
   - Docstrings obrigatórias em todas as funções públicas
   - Formato: Google style ou NumPy style
   - Explicar parâmetros, retorno e exceções

5. **Type Hints Obrigatórios**:
   ```python
   def extract_from_chunk(
       self, 
       chunk_text: str, 
       chunk_id: str
   ) -> ChunkExtraction:
       """Extrai estrutura do chunk."""
   ```

6. **Logging Estruturado**:
   - Usar `logging` module, não `print()`
   - Níveis apropriados: DEBUG, INFO, WARNING, ERROR
   - Logs devem ser úteis para debugging

7. **Validação de Entrada**:
   - Validar todos os inputs de funções públicas
   - Usar `assert` para invariantes internas
   - Levantar exceções específicas para erros de validação

8. **Performance e Otimização**:
   - Otimizar apenas após medir (profiling)
   - Preferir código legível a micro-otimizações
   - Documentar trade-offs de performance

### Checklist de Desenvolvimento

Antes de considerar uma funcionalidade completa:

- [ ] Código segue princípios de Clean Code
- [ ] Testes unitários escritos (TDD)
- [ ] Testes passando (100%)
- [ ] Cobertura de código >= 80%
- [ ] Type hints em todas as funções
- [ ] Docstrings em funções públicas
- [ ] Sem código duplicado
- [ ] Tratamento de erros adequado
- [ ] Logging estruturado implementado
- [ ] Validação de inputs
- [ ] Testes de integração (se aplicável)
- [ ] Refatoração aplicada (se necessário)
- [ ] Código revisado (se aplicável)

### Exemplo de Código Limpo

**❌ Ruim**:

```python
def proc(txt, id):
    # processa texto
    r = {}
    for w in txt.split():
        if len(w) > 4:
            r[w] = r.get(w, 0) + 1
    return r
```

**✅ Bom**:

```python
def extract_key_concepts(
    chunk_text: str, 
    chunk_id: str
) -> Dict[str, int]:
    """
    Extrai conceitos-chave do chunk contando palavras significativas.
    
    Args:
        chunk_text: Texto do chunk a processar
        chunk_id: Identificador único do chunk
        
    Returns:
        Dicionário com conceitos e suas frequências
        
    Raises:
        ValueError: Se chunk_text estiver vazio
    """
    if not chunk_text or not chunk_text.strip():
        raise ValueError(f"chunk_text não pode estar vazio (chunk_id: {chunk_id})")
    
    MIN_WORD_LENGTH = 4
    concept_frequencies: Dict[str, int] = {}
    
    words = chunk_text.split()
    for word in words:
        if len(word) > MIN_WORD_LENGTH:
            concept_frequencies[word] = concept_frequencies.get(word, 0) + 1
    
    return concept_frequencies
```

### Integração com Pipeline

**Ordem de desenvolvimento seguindo TDD**:

1. **Escrever teste para `ChunkExtractor.extract_from_chunk()`**
2. **Implementar `ChunkExtractor.extract_from_chunk()` (mínimo para passar)**
3. **Refatorar código**
4. **Escrever teste para `ChunkExtractor.aggregate_to_recall_set()`**
5. **Implementar agregação**
6. **Repetir para cada módulo**

**Testes de integração do pipeline**:

- Teste completo: PDF → Capítulos → Chunks → Extrações → Recall Set → Resumo → Auditoria
- Validar que todos os critérios binários são verificados
- Validar que evidências são geradas corretamente

---

## Atualização do .cursorrules (MÍNIMA)

**Arquivo**: `.cursorrules`

**Conteúdo MÍNIMO a adicionar** (sem luxo):

1. **TDD (Test-Driven Development)**:
   - Ciclo Red-Green-Refactor obrigatório
   - Teste antes do código
   - Cobertura mínima: 80%
   - Estrutura AAA (Arrange-Act-Assert)

2. **Estrutura de Testes**:
   - Organização: `src/tests/unit/`, `src/tests/integration/`, `src/tests/fixtures/`
   - Framework: pytest
   - Convenções: `test_*.py`, `test_*`, `Test*`

3. **Regra de Marcadores no Resumo**:
   - Cada item crítico do Recall Set DEVE aparecer no resumo com marcador e evidência de ancoragem: `[[RS:cap(\d+):hash|chunks:N,M]]`
   - Auditoria determinística valida marcadores + chunks referenciados (anti-fraude, não depende de LLM)

4. **Regra de Evidências**:
   - Evidências são artefato canônico (sistema fala por evidência, não por conversa)
   - Formato: JSON estruturado + Markdown legível

**Ordem de atualização**: Atualizar `.cursorrules` após definir contrato do Recall Set (TODO 0)

---

## GO / NO-GO (Pré-Desenvolvimento)

**⚠️ BLOQUEANTE**: O desenvolvimento SÓ pode começar se estes 3 itens estiverem 100% claros para o Cursor. Se qualquer um estiver "meio aberto", é **NO-GO** (o Cursor vai implementar "do jeito dele" e você perde a verificabilidade).

### ✅ GO se estes 3 itens estão claros:

1. **Contrato fechado (TODO 0)**
   - ✅ Existe definição final do Recall Set JSON
   - ✅ `CriticalityReason` enum definido
   - ✅ `item_id` com hash imutável definido
   - ✅ Marcador com ancoragem definido: `[[RS:cap(\d+):hash|chunks:...]]`
   - ✅ Auditoria determinística anti-fraude definida

2. **Evidência canônica definida**
   - ✅ `EVIDENCIAS/coverage_report.json` é fonte única de verdade do Quality Gate
   - ✅ Quality Gate **NÃO recalcula**, apenas lê o arquivo

3. **Regeneração com limite**
   - ✅ Loop de regeneração: max 3 tentativas por capítulo
   - ✅ Falha explícita após 3 tentativas

**Se qualquer um desses 3 estiver "meio aberto" → NO-GO**

---

## 🔥 Gates ENDFIRST (Z0 → Z5)

**⚠️ ORDEM OBRIGATÓRIA (ENDFIRST)**: Você NÃO pode começar pelos módulos "legais". Comece provando que o sistema não consegue dar resultado sem cumprir o contrato.

**⚠️ CRÍTICO**: Cada gate é **BLOQUEANTE**. Não avance sem: `pytest -q` passando + artefatos do gate.

### ✅ Gate Z0 — "Resumo Impossível" (Falhas Esperadas)

**Objetivo ENDFIRST**: Criar testes de integração que provem que o sistema falha quando não cumpre o contrato.

**Testes que devem provar falhas esperadas**:
1. Não existe Recall Set → FAIL
2. Não existe marcador → FAIL
3. Marcador existe mas chunks inválidos → FAIL
4. Marcador inventado (item_id não existe) → FAIL

**Entrega obrigatória**:
- ✅ `src/tests/integration/test_gate_z0_impossible_summary.py`
- ✅ Testes devem falhar antes da implementação completa (RED)
- ✅ Testes devem passar após implementação (GREEN)
- ✅ `pytest -q` passando

**Sem isso → NÃO avança**

---

### ✅ Gate Z1 — coverage_report.json como "Fonte Única"

**Objetivo ENDFIRST**: Implementar primeiro a estrutura de cobertura e o Quality Gate que apenas lê (não recalcula).

**Implementação**:
- ✅ Estrutura de `coverage_report.json` definida
- ✅ `quality_gate.py` que apenas lê o report (não recalcula nada)

**Testes obrigatórios**:
- ✅ Sem arquivo → FAIL
- ✅ JSON inválido → FAIL
- ✅ 99% coverage → FAIL
- ✅ 100% coverage → PASS

**Entrega obrigatória**:
- ✅ `EVIDENCIAS/coverage_report.json` de exemplo (fixture)
- ✅ `src/tests/unit/test_quality_gate_from_coverage_report.py`
- ✅ `pytest -q` passando

**Sem isso → NÃO avança**

---

### ✅ Gate Z2 — Auditoria Determinística Anti-Fraude (Sem LLM)

**Objetivo ENDFIRST**: Implementar auditoria que funciona sem IA, apenas com regex e validações determinísticas.

**Implementação**:
- ✅ `recall_auditor.py` com regex e validações
- ✅ Marcador obrigatório: `[[RS:cap(\d+):([a-f0-9]{6})|(chunks|src):...]]`

**Validações determinísticas**:
- ✅ Marker encontrado
- ✅ `item_id` existe no `recall_set.critical_items`
- ✅ Possui mínimo 1 chunk
- ✅ Chunks no marker pertencem a `source_chunks` do item

**Testes obrigatórios**:
- ✅ Missing marker → FAIL
- ✅ Marker com chunks vazios → FAIL
- ✅ Marker com chunk inexistente → FAIL
- ✅ Marker ok → PASS
- ✅ Marker inventado → FAIL

**Entrega obrigatória**:
- ✅ `src/recall_auditor.py` implementado
- ✅ `src/tests/unit/test_recall_auditor.py`
- ✅ `pytest -q` passando

**Sem isso → NÃO avança**

---

### ✅ Gate Z3 — IDs Imutáveis (Determinismo)

**Objetivo ENDFIRST**: Garantir que IDs são determinísticos e imutáveis.

**Implementação**:
- ✅ Função de normalização + hash curto SHA256
- ✅ `item_id = f"RS:cap{chapter_number}:{hash_curto}"`

**Testes obrigatórios**:
- ✅ Mesmo texto normalizado → mesmo `item_id`
- ✅ Mudança mínima → `item_id` muda
- ✅ Normalização remove pontuação e espaços redundantes

**Entrega obrigatória**:
- ✅ Função de normalização implementada
- ✅ `src/tests/unit/test_item_id_immutability.py`
- ✅ `pytest -q` passando

**Sem isso → NÃO avança**

---

### ✅ Gate Z4 — Recall Set com Hard Cap (12 Críticos)

**Objetivo ENDFIRST**: Implementar geração de Recall Set com limites determinísticos.

**Implementação**:
- ✅ Criticidade por enum (`CriticalityReason`)
- ✅ Hard cap 12 em `critical_items`
- ✅ Desempate determinístico (freq > posição > marcador)

**Teste obrigatório**:
- ✅ Gerar 20 críticos → retorna 12 sempre iguais na mesma ordem

**Entrega obrigatória**:
- ✅ `src/chunk_extractor.py` com agregação e hard cap
- ✅ `src/tests/unit/test_recall_set_hard_cap.py`
- ✅ `pytest -q` passando

**Sem isso → NÃO avança**

---

### ✅ Gate Z5 — Pipeline Completo com Loop de Regeneração

**Objetivo ENDFIRST**: Integrar tudo com loop de regeneração e validação final.

**Refatoração de `chapter_summarizer.py`**:
- ✅ Chunking por capítulo
- ✅ Extração por chunk (pode mockar LLM nos testes)
- ✅ Gerar recall set
- ✅ Gerar resumo COM marcadores e ancoragem
- ✅ Auditoria determinística
- ✅ Se falhar → regenerar até 3x
- ✅ Se falhar após 3x → erro explícito, sem output parcial

**Teste de integração obrigatório**:
- ✅ Mock LLM gera resumo falho 2x e correto na 3ª
- ✅ Valida `regeneration_count` e coverage 100%

**Entrega obrigatória**:
- ✅ `src/chapter_summarizer.py` refatorado
- ✅ `src/tests/integration/test_pipeline_regeneration.py`
- ✅ `pytest -q` passando

**Sem isso → NÃO avança**

---

## Regras de Desenvolvimento (Obrigatórias)

- ✅ **TDD obrigatório**: RED → GREEN → REFACTOR
- ✅ **Cobertura mínima**: 80% (`pytest-cov`)
- ✅ **Type hints + docstrings**: Todas as funções públicas
- ✅ **Logging**: Usar `logging`, nada de `print()`
- ✅ **Commits atômicos**: Um commit = uma funcionalidade/teste completo

---

## Entrega Final

**Rodar com um livro real e gerar**:
- ✅ `EVIDENCIAS/coverage_report.json` (100%)
- ✅ Extrações por chunk em JSON
- ✅ Relatório MD final

---

## Como Acompanhar (Sem Ler Código)

**A cada Gate você deve entregar**:
1. ✅ Saída do `pytest -q`
2. ✅ Arquivos criados/modificados (lista)
3. ✅ Se houver, `EVIDENCIAS/coverage_report.json` ou fixtures

**Se um gate falhar, você para e corrige antes de seguir.**

---

## Instruções para o Cursor (Curto e Direto)

**Mensagem obrigatória ao iniciar desenvolvimento**:

1. **"Siga o plano exatamente na ordem ENDFIRST. Gates Z0 → Z5 são bloqueantes."**
2. **"Não avance para a próxima etapa sem me entregar o gate atual com evidências."**
3. **"Cada gate precisa terminar com `pytest -q` passando e com os artefatos em `/EVIDENCIAS` quando aplicável."**
4. **"Se o contrato mudar no meio, pare e proponha diff do contrato antes de codar."**
5. **"Comece provando que o sistema falha sem cumprir o contrato (Gate Z0)."**

**Recomendação**: Cobrar **Gate Z0 → Gate Z1** primeiro. Se passar nesses dois, o resto tende a ficar sob controle.

---

## Próximos Passos (ORDEM CORRETA)

1. **Definir contrato do Recall Set + Auditoria determinística** (TODO 0 - BLOQUEANTE)
   - Formato JSON do recall set com `item_id` (hash imutável), `critical`/`supporting`
   - Enum `CriticalityReason` (MULTI_CHUNK, STRUCTURAL_POSITION, DEFINITION_MARKER, LAW_MARKER)
   - Regra de marcadores `[[RS:cap(\d+):hash|chunks:N,M]]` com evidência de ancoragem (anti-fraude)
   - Regra da auditoria: validar marcadores + chunks referenciados → passa/falha (determinístico)
   - Regras mecânicas de criticidade (≥2 chunks, heading, definição, lei)
   - Hard cap: máximo 12 itens `critical` por capítulo
   - Estrutura do `coverage_report.json` (matriz binária de cobertura)

2. **Atualizar `.cursorrules`** com regras mínimas (TODO 0.1)
   - TDD + estrutura de testes
   - Regra de marcadores no resumo
   - Regra de evidências

3. Adicionar dependências de testes (`pytest`, `pytest-cov`, `pytest-mock`) ao `requirements.txt`
4. Criar estrutura de diretórios de testes (`src/tests/unit/`, `src/tests/integration/`, `src/tests/fixtures/`)
5. Implementar `chunk_extractor.py` (com testes TDD, seguindo contrato do Recall Set)
6. Implementar `recall_auditor.py` (com testes TDD, auditoria determinística primeiro)
7. Refatorar `chapter_summarizer.py` para usar novo pipeline (com testes)
8. Atualizar `quality_gate.py` com validação de cobertura (com testes)
9. Atualizar `evidence_generator.py` com relatório estruturado (com testes)
10. Integrar tudo em `summarizer.py` (com testes de integração)
11. Garantir cobertura de testes >= 80% e executar todos os testes
12. Testar pipeline completo com livro real
13. Gerar evidências e validar todos os critérios binários
14. Code review e refatoração final
