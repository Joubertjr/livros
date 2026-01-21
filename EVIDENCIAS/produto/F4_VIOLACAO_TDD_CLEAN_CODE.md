# EVIDÊNCIA: VIOLAÇÃO DE TDD E CLEAN CODE EM F4

**Data:** 2026-01-21  
**Fase:** F4 — Ajustar Pipeline para Respeitar Contrato de Persistência  
**Status:** ❌ VIOLAÇÃO IDENTIFICADA

---

## ❌ VIOLAÇÕES IDENTIFICADAS

### 1. TDD Violado

**Problema:**
- Código foi criado ANTES dos testes
- `CheckpointManager` implementado sem testes unitários
- Violação da regra canônica: "Teste primeiro, código depois. Sem exceção."

**Evidência:**
- `src/storage/checkpoint_manager.py` criado sem `test_checkpoint_manager.py`
- Commits mostram código antes de testes

**Correção necessária:**
- Criar testes unitários completos (RED primeiro)
- Refatorar código se necessário para passar testes (GREEN)
- Melhorar código mantendo testes passando (REFACTOR)

---

### 2. Clean Code Violado

**Problema 1: Função muito longa**
- `_validate_checkpoint()` tem 66 linhas
- Violação: "Funções devem ser pequenas"

**Código problemático:**
```python
def _validate_checkpoint(self, data: Dict) -> bool:
    # 1. Validar estrutura básica
    if not self._validate_checkpoint_structure(data):
        return False
    
    # 2. Validar chapter_summary completo
    chapter_summary = data.get('chapter_summary', {})
    required_summary_fields = ['numero', 'titulo', 'resumo', 'pontos_chave', 'citacoes', 'exemplos']
    for field in required_summary_fields:
        if field not in chapter_summary or not chapter_summary[field]:
            logger.debug(f"❌ chapter_summary incompleto: falta {field}")
            return False
    
    # 3. Validar coverage_report completo
    coverage_report = data.get('coverage_report', {})
    required_coverage_fields = ['chapter_number', 'total_chunks', 'processed_chunks', 'chunk_coverage_percentage']
    for field in required_coverage_fields:
        if field not in coverage_report:
            logger.debug(f"❌ coverage_report incompleto: falta {field}")
            return False
    
    # Validar recall_set e audit_result (devem existir)
    if 'recall_set' not in coverage_report:
        logger.debug(f"❌ coverage_report incompleto: falta recall_set")
        return False
    if 'audit_result' not in coverage_report:
        logger.debug(f"❌ coverage_report incompleto: falta audit_result")
        return False
    
    # 4. Validar metadata atualizado
    metadata = data.get('metadata', {})
    required_metadata_fields = ['session_id', 'capitulos_processados']
    for field in required_metadata_fields:
        if field not in metadata:
            logger.debug(f"❌ metadata incompleto: falta {field}")
            return False
    
    # Validar consistência: chapter_number deve estar em capitulos_processados
    chapter_number = data.get('chapter_number')
    capitulos_processados = metadata.get('capitulos_processados', [])
    if chapter_number not in capitulos_processados:
        logger.debug(f"❌ Inconsistência: chapter_number {chapter_number} não está em capitulos_processados")
        return False
    
    # Validar consistência: session_id deve corresponder
    if metadata.get('session_id') != data.get('session_id'):
        logger.debug(f"❌ Inconsistência: session_id não corresponde")
        return False
    
    return True
```

**Problema 2: Responsabilidade múltipla**
- `_validate_checkpoint()` valida estrutura, conteúdo E consistência
- Violação: "Uma função deve fazer uma coisa só"

**Problema 3: Lógica complexa em `find_last_valid_checkpoint()`**
- Método faz: listar, ordenar, validar, selecionar
- Violação: "Funções devem ser pequenas e focadas"

---

## ✅ CORREÇÕES NECESSÁRIAS

### 1. Criar Testes Primeiro (TDD)

**Ação:**
- Criar `test_checkpoint_manager.py` com testes completos
- Testes devem falhar primeiro (RED)
- Implementar código mínimo para passar (GREEN)
- Refatorar mantendo testes passando (REFACTOR)

### 2. Refatorar para Clean Code

**Ações:**
- Extrair validações em funções menores:
  - `_validate_chapter_summary()`
  - `_validate_coverage_report()`
  - `_validate_metadata()`
  - `_validate_consistency()`
- Extrair lógica de `find_last_valid_checkpoint()`:
  - `_list_checkpoint_files()`
  - `_load_and_sort_checkpoints()`
  - `_find_first_valid()`

**Princípios Clean Code aplicados:**
- Funções pequenas (< 20 linhas)
- Responsabilidade única
- Nomes descritivos
- Sem duplicação

---

## 📋 CHECKLIST DE CORREÇÃO

- [ ] Criar testes unitários completos (TDD RED)
- [ ] Refatorar `_validate_checkpoint()` em funções menores
- [ ] Refatorar `find_last_valid_checkpoint()` em funções menores
- [ ] Validar que todos os testes passam
- [ ] Validar que código segue Clean Code
- [ ] Atualizar evidência F4 com correções

---

**Violação identificada:** 2026-01-21  
**Correção em andamento:** TDD e Clean Code
