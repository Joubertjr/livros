# Release v1.0-verifiable

**Data de Release:** 2026-01-18  
**Versão:** v1.0-verifiable  
**Status:** ✅ Todos os Gates (Z0-Z8) PASS

## Resumo

Esta é a primeira release verificável do sistema Book Summarizer, implementando pipeline robusto de sumarização com garantias determinísticas de cobertura.

## Gates Completos

- ✅ **Gate Z0:** Testes RED (falhas esperadas)
- ✅ **Gate Z1:** Quality Gate lendo coverage_report.json
- ✅ **Gate Z2:** Auditoria determinística + anti-fraude
- ✅ **Gate Z3:** IDs imutáveis (hash + normalização)
- ✅ **Gate Z4:** Recall Set com hard cap 12
- ✅ **Gate Z5:** Pipeline robusto com regeneração
- ✅ **Gate Z5.2:** Schema coverage_report (travado)
- ✅ **Gate Z6:** Evidence Generator
- ✅ **Gate Z7:** Summarizer integração final
- ✅ **Gate Z8:** Prova real (fim-a-fim) - **100% coverage validado**

## Prova Real

- **Livro processado:** Dopamine Nation - Anna Lembke
- **Tamanho:** 67,173 palavras, 11 capítulos
- **Resultado:** 100.0% coverage, todos os capítulos passaram
- **Estratégia A:** Addendum incremental implementado e validado

## Hash dos Artefatos Canônicos

Os artefatos canônicos que definem o contrato do sistema são:

1. `CHECKLIST_Z_GATES.md` - Constituição do sistema (checklist imutável)
2. `gates_manifest.json` - Contrato executável (manifest)

### Verificação de Integridade

Para verificar a integridade dos artefatos canônicos:

```bash
# Gerar hash atual
python3 scripts/generate_contract_hash.py

# Verificar manualmente
sha256sum CHECKLIST_Z_GATES.md gates_manifest.json
```

Os hashes devem corresponder aos valores em `CONTRACT_HASH.txt`.

### Hash Combinado

O hash combinado garante que ambos os artefatos não foram alterados.

**Ver arquivo:** `CONTRACT_HASH.txt` para hashes completos.

## Breaking Changes

**Política:** Breaking changes só são permitidos via Gate Z-1 (novo gate).

Para criar um novo gate:
1. Adicionar entrada em `CHECKLIST_Z_GATES.md`
2. Adicionar entrada em `gates_manifest.json`
3. Implementar gate seguindo metodologia ENDFIRST
4. Validar com `pytest -q`
5. Atualizar `EVIDENCIAS/gates_status.md`
6. Gerar novo hash: `python3 scripts/generate_contract_hash.py`

## Observabilidade

O sistema agora inclui métricas de addendum no `coverage_report.json`:

- `chapters_using_addendum`: Quantos capítulos precisaram de addendum
- `total_addendums_used`: Total de addendums usados
- `avg_addendums_per_chapter`: Média de addendums por capítulo
- Por capítulo: `audit_result.addendum_count`

Essas métricas permitem monitorar:
- Taxa de sucesso do resumo completo (sem addendum)
- Eficácia da Estratégia A (addendum incremental)
- Limites reais do LLM para gerar marcadores

## Artefatos de Release

- `CHECKLIST_Z_GATES.md` - Checklist canônico
- `gates_manifest.json` - Manifest executável
- `CONTRACT_HASH.txt` - Hash dos artefatos canônicos
- `EVIDENCIAS/coverage_report.json` - Evidência de execução (100% coverage)
- `EVIDENCIAS/report.md` - Relatório humano-legível
- `EVIDENCIAS/extractions_*.json` - Lastro bruto das extrações

## Comandos de Validação

```bash
# Validar todos os gates
pytest src/tests/ -q

# Executar Gate Z8 (prova real)
docker compose exec app python3 src/cli_z8.py --file /app/volumes/Dopamine_Nation_-_Anna_Lembke.pdf

# Verificar hash do contrato
python3 scripts/generate_contract_hash.py
cat CONTRACT_HASH.txt

# Verificar manualmente (se tiver sha256sum)
sha256sum CHECKLIST_Z_GATES.md gates_manifest.json
```

## Notas Técnicas

- **Estratégia A (Addendum Incremental):** Implementada para garantir 100% de cobertura sem depender de perfeição do LLM
- **Docker-first:** Todo código funciona dentro do container Docker
- **ENDFIRST:** Desenvolvimento guiado por provas (RED → GREEN)
- **Governança por Gates:** Cada gate é bloqueante e verificável

## Próximas Versões

Para v1.1+ (opcional):
- Observabilidade avançada (métricas de tempo, custo)
- Suporte multi-livro
- Cross-recall (referências entre livros)
- Knowledge graph

---

**Release criado em:** 2026-01-18  
**Hash gerado em:** [ver CONTRACT_HASH.txt]
