# Gate Z0 - Testes de Integração: "Resumo Impossível"

## Objetivo ENDFIRST

Estes testes provam que o sistema **NÃO pode retornar resumo** se não cumprir o contrato.

## Testes Criados

Arquivo: `src/tests/integration/test_gate_z0_impossible_summary.py`

### Testes que devem FALHAR (RED) antes da implementação:

1. **test_should_fail_when_no_recall_set**
   - Sistema deve falhar quando não existe Recall Set

2. **test_should_fail_when_no_marker_in_summary**
   - Sistema deve falhar quando não existe marcador no resumo

3. **test_should_fail_when_marker_has_invalid_chunks**
   - Sistema deve falhar quando marcador aponta para chunks inválidos

4. **test_should_fail_when_marker_has_empty_chunks**
   - Sistema deve falhar quando marcador tem chunks vazios (anti-fraude)

5. **test_should_fail_when_marker_invented_item_id**
   - Sistema deve falhar quando marcador aponta para item_id que não existe

6. **test_should_pass_when_all_markers_valid**
   - Sistema deve passar quando todos os marcadores são válidos (GREEN)

## Como Executar

```bash
# Dentro do container Docker
docker compose exec app pytest src/tests/integration/test_gate_z0_impossible_summary.py -v

# Ou com saída quieta
docker compose exec app pytest src/tests/integration/test_gate_z0_impossible_summary.py -q
```

## Status Esperado

- **Antes da implementação**: Testes devem FALHAR (RED) ✅
- **Após implementação**: Testes devem PASSAR (GREEN) ✅

## Estrutura de Dados Mínima

Os testes usam estruturas mínimas (`RecallSetItem`, `ChapterRecallSet`, `ChapterSummary`) que serão expandidas na implementação real.
