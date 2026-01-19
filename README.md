# CoverageSummarizer

**Summaries with guaranteed coverage and auditability.**

CoverageSummarizer is a deterministic, evidence-first system that guarantees
100% coverage of critical knowledge or fails explicitly with audit proof.

## Pré-requisitos

- Docker
- Docker Compose

## Instalação e Execução

1. Copie o arquivo `.env.example` para `.env` e configure suas variáveis:
   ```bash
   cp .env.example .env
   # Edite .env e adicione sua OPENAI_API_KEY
   ```

2. Execute o sistema:
   ```bash
   docker compose up --build
   ```

3. O sistema estará disponível via CLI dentro do container.

## Estrutura do Projeto

- `DEMANDAS/` - Documentação de demandas e critérios de aceitação
- `EVIDENCIAS/` - Evidências geradas automaticamente
- `src/` - Código fonte
- `volumes/` - Exportações (MD/PDF)
- `planejamento/` - Planos de execução

## Engineering Principles

CoverageSummarizer é um projeto **TDD-first** e **Clean-Code enforced**.

Regras obrigatórias:

- Nenhuma implementação sem testes
- Teste falha antes da implementação (ou RED/xfail por design)
- Funções pequenas (≤50 linhas)
- Nomes explicam intenção
- Nenhuma lógica implícita
- Nenhuma duplicação
- Nenhum TODO, HACK ou FIXME
- Refatoração faz parte da tarefa
- Critério de feito: Funciona + Passa testes + É legível

## Regras de Manutenção de Arquivos de Configuração

### Atualização do `.cursorrules`

**⚠️ REGRA CANÔNICA:** O arquivo `.cursorrules` DEVE ser atualizado APENAS via terminal.

**Método obrigatório:**
```bash
cd /Users/joubertsouza/Documents/livros && cat > .cursorrules << 'CURSORRULES_EOF'
[conteúdo completo do arquivo]
CURSORRULES_EOF
```

**Alternativa (se cat falhar):**
```bash
python3 << 'PYEOF'
content = """[conteúdo completo do arquivo]"""
with open('.cursorrules', 'w', encoding='utf-8') as f:
    f.write(content)
PYEOF
```

**PROIBIDO:**
- ❌ Usar `search_replace` tool (causa travamento)
- ❌ Usar `write` tool (pode travar)
- ❌ Editar parcialmente (sempre reescrever completamente)

**Motivo:** Arquivos ocultos (`.cursorrules`) podem travar o Cursor quando editados com ferramentas de edição parcial. A reescrita completa via terminal é o método garantido.

## Comandos Úteis

- `docker compose exec app make evidence` - Gera evidências de execução

## Execução de Testes

Todos os testes devem ser executados dentro do container Docker:

```bash
# Executar todos os testes
docker compose exec app pytest -q

# Executar testes específicos do Gate Z9
docker compose exec app pytest -q \
  src/tests/unit/test_api_schema_gate_z9.py \
  src/tests/integration/test_api_gate_z9.py
```

**Importante:** Testes não funcionam no ambiente local (dependências como `pydantic` e `fastapi` estão apenas no container).

## Demanda

Ver `DEMANDAS/DEMANDA-000_BOOK_SUMMARIZER.md` para especificação completa (documentação histórica).

## Verificação de Integridade do Contrato

O sistema usa artefatos canônicos para garantir integridade:

- `CHECKLIST_Z_GATES.md` - Constituição do sistema (checklist imutável)
- `gates_manifest.json` - Contrato executável (manifest)

### Gerar Hash dos Artefatos

```bash
# Dentro do Docker (recomendado)
docker compose exec app python3 scripts/generate_contract_hash.py

# Ou localmente (se dependências estiverem instaladas)
python3 scripts/generate_contract_hash.py
```

Isso gera `CONTRACT_HASH.txt` com hash SHA256 de ambos os artefatos.

### Verificar Integridade

Para verificar que os artefatos não foram alterados:

```bash
# Gerar hash atual (dentro do Docker)
docker compose exec app python3 scripts/generate_contract_hash.py

# Comparar com CONTRACT_HASH.txt
cat CONTRACT_HASH.txt

# Verificar manualmente (se disponível)
sha256sum CHECKLIST_Z_GATES.md gates_manifest.json
```

Os hashes devem corresponder aos valores em `CONTRACT_HASH.txt`.

### Política de Breaking Changes

Breaking changes só são permitidos via criação de novo Gate (Gate Z-1, Z-2, etc.).

Para criar novo gate:
1. Adicionar entrada em `CHECKLIST_Z_GATES.md`
2. Adicionar entrada em `gates_manifest.json`
3. Implementar seguindo metodologia ENDFIRST
4. Validar com `docker compose exec app pytest -q`
5. Gerar novo hash: `docker compose exec app python3 scripts/generate_contract_hash.py`

## Release v1.0

Ver `RELEASE_v1.0.md` para detalhes da primeira release verificável.

**Status:** Todos os Gates (Z0-Z9) PASS, 100% coverage validado com livro real.

## Estado Atual do Repositório

**Status:** ✅ **UNBLOCKED** (2026-01-18)

**Validação:**
```bash
$ docker compose exec app pytest -q
64 passed, 4 xfailed, 0 failed, 11 warnings in 0.56s
```

**Critério:** `0 failed` = suite 100% verde = repositório desbloqueado

**Nota sobre Gate Z0:** Os 4 testes xfailed são testes RED (falham por design) do Gate Z0. Isso é comportamento esperado e documentado em `CHECKLIST_Z_GATES.md` e `gates_manifest.json` (`z0_mode: "XFAIL_BY_DESIGN"`). Não é workaround - é decisão arquitetural formalizada.

**Artefatos de Validação:**
- `gates_manifest.json`: `suite_status: "GREEN"`
- `CONTRACT_HASH.txt`: Hash regenerado e validado
- `EVIDENCIAS/gates_status.md`: Prova canônica registrada
