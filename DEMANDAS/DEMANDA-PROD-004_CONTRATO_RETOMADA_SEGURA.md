# DEFINIÇÃO: CONTRATO DE RETOMADA SEGURA

**Demanda:** DEMANDA-PROD-004 — Persistência Progressiva e Retomada Segura  
**Fase:** F3 — Definir Contrato de Retomada Segura  
**Data:** 2026-01-21  
**Status:** ✅ DEFINIDO  
**Governado por:** END-FIRST v2  
**Base:** DEMANDA-PROD-004_PONTOS_MINIMOS_PERSISTENCIA_INCREMENTAL.md (F2)

---

## 🔒 END (Resultado Observável)

**Contrato explícito de como o sistema retoma execução a partir de um checkpoint**

Este contrato estabelece:
- **Formato** de checkpoint (estrutura de dados)
- **Identificação** de checkpoint válido (como detectar último checkpoint válido)
- **Lógica** de retomada (como continuar sem reprocessar)
- **Tratamento** de checkpoint inválido/corrompido

---

## 📋 BASE: PONTOS MÍNIMOS DE PERSISTÊNCIA (F2)

Esta definição é baseada **exclusivamente** na definição de F2, que estabelece:

**Ponto de Checkpoint:**
- **CHECKPOINT 1:** Após processamento completo de cada capítulo

**Critério de Checkpoint Válido (F2):**
```
SE checkpoint contém ChapterSummary completo
E checkpoint contém CoverageReport parcial
E checkpoint contém metadados atualizados
E checkpoint foi salvo atomicamente (ou tudo ou nada)
ENTÃO checkpoint é VÁLIDO e pode ser usado para retomada
```

**Checkpoint Inválido (F2):**
- `ChapterSummary` incompleto
- `CoverageReport` ausente ou incompleto
- Metadados não atualizados
- Persistência interrompida (arquivo corrompido ou parcial)
- Validação de schema falhou

---

## 📦 FORMATO DE CHECKPOINT (ESTRUTURA DE DADOS)

### Estrutura Baseada em F2

**Um checkpoint é uma estrutura de dados que contém:**

1. **ChapterSummary completo:**
   - `numero` (str - Número do capítulo
   - `titulo` (str) - Título do capítulo
   - `palavras` (int) - Contagem de palavras do texto original
   - `palavras_resumo` (int) - Contagem de palavras do resumo gerado
   - `paginas` (List[int]) - Páginas do capítulo
   - `resumo` (str) - Resumo completo (300-500 palavras)
   - `pontos_chave` (List[str]) - 5-8 pontos principais
   - `citacoes` (List[str]) - 2-4 citações marcantes
   - `exemplos` (List[str]) - 2-5 exemplos concretos

2. **CoverageReport parcial do capítulo:**
   - `chapter_number` (str) - Número do capítulo
   - `chapter_title` (str) - Título do capítulo
   - `total_chunks` (int) - Total de chunks do capítulo
   - `processed_chunks` (int) - Chunks já processados
   - `chunk_coverage_percentage` (float) - Percentual de cobertura
   - `recall_set` (RecallSetData) - Dados do recall set completo
   - `audit_result` (AuditResultData) - Resultado da auditoria completo

3. **Metadados de processamento atualizados:**
   - `session_id` (str) - Identificador único da execução
   - `timestamp_inicio` (datetime) - Quando processamento começou
   - `timestamp_ultimo_checkpoint` (datetime) - Quando checkpoint foi salvo
   - `capitulos_processados` (List[str]) - Lista de números de capítulos já processados
   - `chunks_processados_por_capitulo` (Dict[str, int]) - Quantos chunks foram processados por capítulo
   - `total_chunks_por_capitulo` (Dict[str, int]) - Total de chunks por capítulo

### Representação de Checkpoint

**Formato de persistência:**
- **Arquivo:** `{session_id}_checkpoint_{chapter_number}.json`
- **Localização:** `/app/volumes/summaries/checkpoints/`
- **Estrutura:** JSON válido contendo os 3 componentes acima

**Exemplo de estrutura:**
```json
{
  "session_id": "uuid-da-execucao",
  "chapter_number": "1",
  "timestamp_checkpoint": "2026-01-21T10:30:00",
  "chapter_summary": {
    "numero": "1",
    "titulo": "Título do Capítulo",
    "palavras": 5000,
    "palavras_resumo": 400,
    "paginas": [1, 2, 3],
    "resumo": "Resumo completo...",
    "pontos_chave": ["Ponto 1", "Ponto 2"],
    "citacoes": ["Citação 1"],
    "exemplos": ["Exemplo 1"]
  },
  "coverage_report": {
    "chapter_number": "1",
    "chapter_title": "Título do Capítulo",
    "total_chunks": 10,
    "processed_chunks": 10,
    "chunk_coverage_percentage": 100.0,
    "recall_set": {...},
    "audit_result": {...}
  },
  "metadata": {
    "session_id": "uuid-da-execucao",
    "timestamp_inicio": "2026-01-21T10:00:00",
    "timestamp_ultimo_checkpoint": "2026-01-21T10:30:00",
    "capitulos_processados": ["1"],
    "chunks_processados_por_capitulo": {"1": 10},
    "total_chunks_por_capitulo": {"1": 10}
  }
}
```

---

## 🔍 IDENTIFICAÇÃO DE CHECKPOINT VÁLIDO

### Como Detectar Último Checkpoint Válido

**Algoritmo de identificação:**

1. **Listar todos os checkpoints da sessão:**
   - Buscar arquivos `{session_id}_checkpoint_*.json` em `/app/volumes/summaries/checkpoints/`
   - Ordenar por `timestamp_checkpoint` (mais recente primeiro)

2. **Validar cada checkpoint (do mais recente para o mais antigo):**
   - Verificar se arquivo existe e é JSON válido
   - ❌ Se não existe ou não é JSON válido → **INVÁLIDO**
   - Verificar se contém `chapter_summary` completo (todos os campos obrigatórios)
     - ❌ Se faltam campos obrigatórios → **INVÁLIDO**
   - Verificar se contém `coverage_report` completo (todos os campos obrigatórios)
     - ❌ Se faltam campos obrigatórios → **INVÁLIDO**
   - Verificar se contém `metadata` atualizado (session_id, timestamps, capítulos processados)
     - ❌ Se faltam campos obrigatórios → **INVÁLIDO**
   - Validar schema (usar Pydantic para validar estrutura)
     - ❌ Se validação de schema falha → **INVÁLIDO**

3. **Selecionar primeiro checkpoint válido encontrado:**
   - Este é o **último checkpoint válido**
   - Se nenhum checkpoint válido for encontrado → **NENHUM CHECKPOINT VÁLIDO**

**Critério binário:**
```
SE arquivo existe E é JSON válido
E chapter_summary está completo (todos os campos obrigatórios)
E coverage_report está completo (todos os campos obrigatórios)
E metadata está atualizado (todos os campos obrigatórios)
E validação de schema passa
ENTÃO checkpoint é VÁLIDO
```

### Invalidações Explícitas

**Um checkpoint é explicitamente inválido se:**

1. **Arquivo não existe ou não é acessível:**
   - Arquivo não encontrado
   - Permissões insuficientes
   - Arquivo corrompido (não é JSON válido)

2. **ChapterSummary incompleto:**
   - Faltam campos obrigatórios: `numero`, `titulo`, `resumo`, `pontos_chave`, `citacoes`, `exemplos`
   - Campos obrigatórios são `None` ou vazios (exceto `paginas` que pode ser lista vazia)

3. **CoverageReport incompleto:**
   - Faltam campos obrigatórios: `chapter_number`, `total_chunks`, `processed_chunks`, `chunk_coverage_percentage`
   - `recall_set` ausente ou incompleto
   - `audit_result` ausente ou incompleto

4. **Metadados não atualizados:**
   - `session_id` ausente ou não corresponde à sessão atual
   - `capitulos_processados` ausente ou não inclui o capítulo do checkpoint
   - `timestamp_ultimo_checkpoint` ausente ou inválido

5. **Validação de schema falha:**
   - Estrutura não corresponde ao schema esperado
   - Tipos de dados incorretos
   - Valores fora dos limites esperados

**Ação ao detectar checkpoint inválido:**
- Checkpoint inválido é **descartado** (não usado para retomada)
- Sistema busca o próximo checkpoint mais antigo
- Se nenhum checkpoint válido for encontrado, retomada começa do início

---

## 🔄 LÓGICA DE RETOMADA

### Como Identificar Onde Parou

**Algoritmo de identificação do ponto de retomada:**

1. **Identificar último checkpoint válido:**
   - Usar algoritmo de identificação de checkpoint válido (seção anterior)
   - Se nenhum checkpoint válido → retomar do início (capítulo 1)

2. **Extrair informações do checkpoint válido:**
   - `capitulos_processados`: Lista de capítulos já processados
   - `chapter_number`: Número do último capítulo processado
   - `metadata.capitulos_processados`: Lista completa de capítulos processados

3. **Determinar próximo capítulo a processar:**
   - Se `capitulos_processados = ["1", "2", "3"]` → próximo capítulo é "4"
   - Se `capitulos_processados = []` → próximo capítulo é "1" (nenhum processado)

**Critério binário:**
```
SE último checkpoint válido existe
ENTÃO próximo capítulo = próximo após último em capitulos_processados
SENÃO próximo capítulo = 1 (início)
```

### Como Validar que Checkpoint é Válido

**Validação antes de usar checkpoint para retomada:**

1. **Validação estrutural:**
   - Arquivo existe e é JSON válido
   - Estrutura contém os 3 componentes (chapter_summary, coverage_report, metadata)

2. **Validação de conteúdo:**
   - `chapter_summary` completo (todos os campos obrigatórios presentes e não vazios)
   - `coverage_report` completo (todos os campos obrigatórios presentes)
   - `metadata` atualizado (session_id corresponde, capítulos processados coerentes)

3. **Validação de schema:**
   - Usar Pydantic para validar estrutura completa
   - Todos os tipos de dados corretos
   - Valores dentro dos limites esperados

4. **Validação de consistência:**
   - `chapter_number` em `chapter_summary` corresponde a `chapter_number` em `coverage_report`
   - `chapter_number` está em `metadata.capitulos_processados`
   - `timestamp_ultimo_checkpoint` é posterior a `timestamp_inicio`

**Critério binário:**
```
SE todas as validações passam
ENTÃO checkpoint é VÁLIDO e pode ser usado
SENÃO checkpoint é INVÁLIDO e deve ser descartado
```

### Como Continuar a Partir do Checkpoint

**Algoritmo de continuação:**

1. **Carregar último checkpoint válido:**
   - Ler arquivo do checkpoint
   - Validar checkpoint (usar validação acima)
   - Se inválido → descartar e buscar próximo

2. **Restaurar estado do processamento:**
   - Carregar `capitulos_processados` dos metadados
   - Carregar `chunks_processados_por_capitulo` dos metadados
   - Carregar `total_chunks_por_capitulo` dos metadados
   - Restaurar `session_id` (usar mesmo session_id da execução original)

3. **Identificar próximo capítulo:**
   - Determinar próximo capítulo a processar (algoritmo acima)
   - Se não há próximo capítulo → processamento já está completo

4. **Continuar processamento:**
   - Processar apenas capítulos **não processados**
   - Usar metadados restaurados para manter consistência
   - Criar novos checkpoints após cada capítulo processado

**Critério binário:**
```
SE checkpoint válido existe
ENTÃO restaurar estado E processar apenas capítulos não processados
SENÃO processar todos os capítulos do início
```

### Como Evitar Reprocessamento

**Garantias de não reprocessamento:**

1. **Verificação antes de processar capítulo:**
   - Verificar se capítulo está em `capitulos_processados`
   - Se está → **PULAR** capítulo (já foi processado)
   - Se não está → processar capítulo

2. **Uso de checkpoints para restaurar valor cognitivo:**
   - Capítulos já processados são **restaurados** dos checkpoints
   - Não são **reprocessados**
   - Valor cognitivo já persistido é **reutilizado**

3. **Atualização de metadados:**
   - Metadados são atualizados apenas com novos capítulos processados
   - Capítulos já processados não alteram metadados

**Critério binário:**
```
SE capítulo está em capitulos_processados
ENTÃO restaurar do checkpoint (NÃO reprocessar)
SENÃO processar capítulo normalmente
```

**Garantia explícita:**
- ✅ Capítulos já processados **NUNCA** são reprocessados
- ✅ Valor cognitivo já persistido é **SEMPRE** reutilizado
- ✅ Apenas capítulos não processados são processados

---

## 🚨 TRATAMENTO DE CHECKPOINT INVÁLIDO/CORROMPIDO

### Detecção de Checkpoint Inválido

**Checkpoint inválido é detectado quando:**
- Validação estrutural falha (arquivo não existe, JSON inválido)
- Validação de conteúdo falha (campos obrigatórios ausentes ou vazios)
- Validação de schema falha (tipos incorretos, valores fora dos limites)
- Validação de consistência falha (dados inconsistentes entre componentes)

### Ação ao Detectar Checkpoint Inválido

**Algoritmo de tratamento:**

1. **Descartar checkpoint inválido:**
   - Checkpoint inválido é **marcado como inválido** (não usado)
   - Arquivo pode ser mantido para análise, mas não é usado para retomada

2. **Buscar próximo checkpoint válido:**
   - Buscar checkpoints mais antigos (ordem reversa de timestamp)
   - Validar cada checkpoint encontrado
   - Se válido → usar para retomada
   - Se inválido → continuar buscando

3. **Se nenhum checkpoint válido for encontrado:**
   - Retomada começa do **início** (capítulo 1)
   - Todos os capítulos são processados do zero
   - Novos checkpoints são criados normalmente

**Critério binário:**
```
SE checkpoint inválido detectado
ENTÃO descartar E buscar próximo checkpoint válido
SE nenhum checkpoint válido encontrado
ENTÃO retomar do início (capítulo 1)
```

### Invalidações Explícitas

**Checkpoint é explicitamente inválido se:**

1. **Arquivo corrompido:**
   - JSON inválido (sintaxe incorreta)
   - Arquivo parcialmente escrito (interrompido durante escrita)
   - Arquivo vazio

2. **Estrutura incompleta:**
   - Faltam componentes obrigatórios (chapter_summary, coverage_report, metadata)
   - Componentes presentes mas incompletos (campos obrigatórios ausentes)

3. **Dados inconsistentes:**
   - `chapter_number` diferente entre `chapter_summary` e `coverage_report`
   - `session_id` diferente entre checkpoint e execução atual
   - `capitulos_processados` não inclui o capítulo do checkpoint

4. **Validação de schema falha:**
   - Tipos de dados incorretos
   - Valores fora dos limites esperados
   - Campos obrigatórios ausentes

**Ação para cada tipo de invalidação:**
- Checkpoint inválido é **descartado**
- Sistema busca próximo checkpoint válido
- Se nenhum válido → retoma do início

---

## 🧭 REGRAS CANÔNICAS APLICADAS

**"Retomar não é recomeçar."**

Este contrato garante que:
- ✅ Retomada **reutiliza** valor cognitivo já persistido
- ✅ Retomada **não reprocessa** capítulos já processados
- ✅ Retomada **continua** a partir do último ponto válido

**"Falha não pode apagar história."**

Este contrato garante que:
- ✅ Checkpoints válidos são **preservados** mesmo após falhas
- ✅ Checkpoints inválidos são **descartados**, mas não apagam checkpoints válidos anteriores
- ✅ Histórico de processamento é **mantido** através de checkpoints

---

## 📌 PROVA DE VALIDAÇÃO

**Comando de Prova (F3):**

```bash
# Verificar que contrato está documentado
docker compose exec app bash -c 'grep -E "retomada|checkpoint|resume" /app/planejamento/DEMANDA-PROD-004_PLAN.md | head -5'
```

**String Esperada:** Deve encontrar referências a "retomada", "checkpoint" ou "resume"

**Prova adicional:**
```bash
# Verificar que definição de contrato existe
test -f DEMANDAS/DEMANDA-PROD-004_CONTRATO_RETOMADA_SEGURA.md && grep -q "retomada" DEMANDAS/DEMANDA-PROD-004_CONTRATO_RETOMADA_SEGURA.md && echo "OK: contrato definido" || echo "FAIL: contrato não encontrado"
```

**String Esperada:** `OK: contrato definido`

---

## 📚 REFERÊNCIAS

- **F1 - Valor Cognitivo Persistente:** `DEMANDAS/DEMANDA-PROD-004_DEFINICAO_VALOR_COGNITIVO_PERSISTENTE.md`
- **F2 - Pontos Mínimos:** `DEMANDAS/DEMANDA-PROD-004_PONTOS_MINIMOS_PERSISTENCIA_INCREMENTAL.md`
- **SummaryStorage:** `src/schemas/summary_storage.py`
- **ChapterSummary:** `src/chapter_summarizer.py` (linha 18-29)
- **CoverageReport:** `src/schemas/coverage_report.py`

---

**Documento criado:** 2026-01-21  
**Última atualização:** 2026-01-21  
**Fase:** F3 — Definir Contrato de Retomada Segura  
**Status:** ✅ COMPLETA  
**Governado por:** END-FIRST v2
