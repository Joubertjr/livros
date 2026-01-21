# Evidência F3 — DEMANDA-PROD-004: PERSISTÊNCIA PROGRESSIVA E RETOMADA SEGURA

**Data:** 2026-01-21  
**Demanda:** DEMANDA-PROD-004_PERSISTENCIA_PROGRESSIVA_RETOMADA_SEGURA.md  
**Planejamento:** planejamento/DEMANDA-PROD-004_PLAN.md  
**Fase:** F3 — Definir Contrato de Retomada Segura  
**Status:** ✅ COMPLETA

---

## ✅ PROVA DE VALIDAÇÃO

### Comando Executado

```bash
test -f DEMANDAS/DEMANDA-PROD-004_CONTRATO_RETOMADA_SEGURA.md && grep -q "retomada" DEMANDAS/DEMANDA-PROD-004_CONTRATO_RETOMADA_SEGURA.md && echo "OK: contrato definido" || echo "FAIL: contrato não encontrado"
```

### Resultado

**String Esperada:** `OK: contrato definido`  
**Status:** ✅ PASS

---

## 📋 CHECKLIST F3

### DONE WHEN

- [x] Formato de checkpoint definido (estrutura de dados) ✅
  - [x] Estrutura baseada em F2 (ChapterSummary + CoverageReport + Metadados) ✅
  - [x] Formato de persistência definido (JSON, localização, nomenclatura) ✅
- [x] Identificação de checkpoint válido definida ✅
  - [x] Algoritmo de detecção do último checkpoint válido ✅
  - [x] Critério binário de validade ✅
  - [x] Invalidações explícitas listadas ✅
- [x] Lógica de retomada definida ✅
  - [x] Como identificar onde parou ✅
  - [x] Como validar que checkpoint é válido ✅
  - [x] Como continuar a partir do checkpoint ✅
  - [x] Como evitar reprocessamento ✅
- [x] Tratamento de checkpoint inválido/corrompido definido ✅
  - [x] Detecção de checkpoint inválido ✅
  - [x] Ação ao detectar checkpoint inválido ✅
  - [x] Invalidações explícitas documentadas ✅
- [x] Baseada exclusivamente em F2 ✅
- [x] Documentação do contrato criada ✅

---

## 📄 ARQUIVOS CRIADOS

1. **`DEMANDAS/DEMANDA-PROD-004_CONTRATO_RETOMADA_SEGURA.md`**
   - Contrato completo e verificável
   - Formato de checkpoint baseado em F2
   - Algoritmo de identificação de checkpoint válido
   - Lógica completa de retomada
   - Tratamento de checkpoint inválido
   - Garantias explícitas de não reprocessamento
   - Invalidações explícitas documentadas

2. **`EVIDENCIAS/produto/persistencia_progressiva_retomada_segura_F3_proof.md`** (este arquivo)
   - Evidência consolidada de F3
   - Prova de validação
   - Relatório de execução
   - Status da fase

---

## 📊 RESUMO DO CONTRATO

### Formato de Checkpoint

**Estrutura baseada em F2:**
- `chapter_summary` completo (ChapterSummary)
- `coverage_report` parcial (CoverageReport)
- `metadata` atualizado (Metadados de processamento)

**Formato de persistência:**
- Arquivo: `{session_id}_checkpoint_{chapter_number}.json`
- Localização: `/app/volumes/summaries/checkpoints/`

### Identificação de Checkpoint Válido

**Algoritmo:**
1. Listar checkpoints da sessão
2. Validar cada checkpoint (do mais recente para o mais antigo)
3. Selecionar primeiro checkpoint válido encontrado

**Critério binário:**
```
SE arquivo existe E é JSON válido
E chapter_summary está completo
E coverage_report está completo
E metadata está atualizado
E validação de schema passa
ENTÃO checkpoint é VÁLIDO
```

### Lógica de Retomada

**Como identificar onde parou:**
- Extrair `capitulos_processados` do último checkpoint válido
- Próximo capítulo = próximo após último em `capitulos_processados`

**Como evitar reprocessamento:**
- Verificar se capítulo está em `capitulos_processados`
- Se está → **PULAR** (restaurar do checkpoint)
- Se não está → processar normalmente

**Garantia explícita:**
- ✅ Capítulos já processados **NUNCA** são reprocessados
- ✅ Valor cognitivo já persistido é **SEMPRE** reutilizado

### Tratamento de Checkpoint Inválido

**Checkpoint inválido se:**
- Arquivo corrompido (JSON inválido, parcialmente escrito)
- Estrutura incompleta (faltam componentes obrigatórios)
- Dados inconsistentes (valores não correspondem)
- Validação de schema falha

**Ação:**
- Descartar checkpoint inválido
- Buscar próximo checkpoint válido
- Se nenhum válido → retomar do início

---

## 🧭 REGRAS CANÔNICAS APLICADAS

**"Retomar não é recomeçar."**

O contrato garante que:
- ✅ Retomada **reutiliza** valor cognitivo já persistido
- ✅ Retomada **não reprocessa** capítulos já processados
- ✅ Retomada **continua** a partir do último ponto válido

**"Falha não pode apagar história."**

O contrato garante que:
- ✅ Checkpoints válidos são **preservados** mesmo após falhas
- ✅ Checkpoints inválidos são **descartados**, mas não apagam checkpoints válidos anteriores
- ✅ Histórico de processamento é **mantido** através de checkpoints

---

## ✅ F3: COMPLETA

**Status:** ✅ F3 COMPLETA  
**Próxima Fase:** F4 — Ajustar Pipeline para Respeitar Contrato de Persistência

---

**Evidência gerada:** 2026-01-21  
**Governado por:** END-FIRST v2
