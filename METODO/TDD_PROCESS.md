# Processo TDD Obrigatório — Gate Z10

**Data:** 2026-01-19  
**Status:** ✅ CANÔNICO  
**Gate:** Z10 (TDD + Clean Code)

---

## 🔒 REGRA FUNDAMENTAL

> **"Teste primeiro, código depois. Sem exceção."**

**Violação = FAIL do Gate Z10 = Bloqueio de commit/merge**

---

## 📋 PROCESSO TDD OBRIGATÓRIO

### Fase 1: RED (Teste Falha)

**Antes de escrever QUALQUER código:**

1. **Escrever teste que falha**
   - Teste deve descrever comportamento esperado
   - Teste deve falhar por falta de implementação
   - Teste deve ser executável (`pytest` roda, mas falha)

2. **Validar que teste falha**
   ```bash
   pytest src/tests/.../test_nova_feature.py -v
   # Deve mostrar: FAILED (teste não encontra código)
   ```

3. **Documentar comportamento esperado**
   - O que o teste valida?
   - Por que esse comportamento é necessário?
   - Qual é o critério de sucesso?

### Fase 2: GREEN (Implementação Mínima)

**Apenas após teste escrito e falhando:**

1. **Implementar código mínimo para teste passar**
   - Apenas o necessário para teste passar
   - Não adicionar funcionalidades extras
   - Não otimizar prematuramente

2. **Validar que teste passa**
   ```bash
   pytest src/tests/.../test_nova_feature.py -v
   # Deve mostrar: PASSED
   ```

3. **Validar que não quebrou outros testes**
   ```bash
   pytest -q
   # Deve mostrar: 0 failed (ou xfailed documentado)
   ```

### Fase 3: REFACTOR (Clean Code)

**Apenas após teste passar:**

1. **Refatorar código**
   - Funções pequenas (< 50 linhas)
   - Nomes claros
   - Sem duplicação
   - Sem lógica implícita
   - Sem TODOs/HACKs/FIXMEs

2. **Validar que testes ainda passam**
   ```bash
   pytest -q
   # Deve mostrar: 0 failed
   ```

3. **Validar Clean Code**
   - Funções < 50 linhas (ou justificada)
   - Sem duplicação óbvia
   - Sem lógica implícita
   - Sem TODOs/HACKs/FIXMEs

---

## 🚨 REGRAS CRÍTICAS

### Regra 1: Teste Antes de Código
- ❌ **PROIBIDO:** Escrever código sem teste correspondente
- ✅ **OBRIGATÓRIO:** Teste escrito antes de qualquer implementação
- ✅ **VALIDAÇÃO:** Teste deve falhar antes da implementação

### Regra 2: Teste Deve Falhar Primeiro
- ❌ **PROIBIDO:** Teste que passa sem implementação (teste inválido)
- ✅ **OBRIGATÓRIO:** Teste deve falhar antes da implementação
- ✅ **VALIDAÇÃO:** `pytest` mostra FAILED antes de implementar

### Regra 3: Cobertura de Erro Obrigatória
- ❌ **PROIBIDO:** Apenas happy path testado
- ✅ **OBRIGATÓRIO:** Cenários de erro testados
- ✅ **VALIDAÇÃO:** Testes de erro existem e passam

### Regra 4: Testes de Integração para Fluxos Críticos
- ❌ **PROIBIDO:** Apenas testes unitários isolados
- ✅ **OBRIGATÓRIO:** Testes end-to-end para fluxos críticos
- ✅ **VALIDAÇÃO:** Testes de integração cobrem fluxos críticos

---

## 📊 CHECKLIST TDD OBRIGATÓRIO

### Antes de Escrever Código:
- [ ] Teste escrito descrevendo comportamento esperado
- [ ] Teste falha (RED) - validação executada
- [ ] Comportamento esperado documentado
- [ ] Cenários de erro identificados

### Durante Implementação:
- [ ] Código mínimo implementado (apenas para teste passar)
- [ ] Teste passa (GREEN) - validação executada
- [ ] Outros testes não quebraram - validação executada
- [ ] Testes de erro implementados e passando

### Após Implementação:
- [ ] Código refatorado (Clean Code)
- [ ] Testes ainda passam após refatoração
- [ ] Funções < 50 linhas (ou justificada)
- [ ] Sem duplicação, lógica implícita, TODOs

### Validação Final:
- [ ] `pytest -q` = 0 failed
- [ ] Testes de integração cobrem fluxos críticos
- [ ] Testes de erro cobrem cenários de falha
- [ ] Clean Code validado

---

## 🎯 EXEMPLOS DE VIOLAÇÕES

### Violação 1: Código Sem Teste
```python
# ❌ ERRADO: Código escrito sem teste
def nova_funcao():
    return "resultado"

# ✅ CORRETO: Teste escrito primeiro
def test_nova_funcao():
    assert nova_funcao() == "resultado"  # Falha primeiro
```

### Violação 2: Teste Que Passa Sem Implementação
```python
# ❌ ERRADO: Teste passa sem código (teste inválido)
def test_funcao_inexistente():
    assert funcao_inexistente() == "resultado"  # Não existe, mas passa?

# ✅ CORRETO: Teste falha primeiro
def test_funcao_inexistente():
    assert funcao_inexistente() == "resultado"  # FAILED (função não existe)
```

### Violação 3: Apenas Happy Path
```python
# ❌ ERRADO: Apenas happy path
def test_processa_arquivo():
    resultado = processa_arquivo("arquivo_valido.pdf")
    assert resultado is not None

# ✅ CORRETO: Happy path + erros
def test_processa_arquivo_valido():
    resultado = processa_arquivo("arquivo_valido.pdf")
    assert resultado is not None

def test_processa_arquivo_inexistente():
    with pytest.raises(FileNotFoundError):
        processa_arquivo("arquivo_inexistente.pdf")
```

### Violação 4: Apenas Testes Unitários
```python
# ❌ ERRADO: Apenas teste unitário isolado
def test_progress_tracker_update():
    tracker = ProgressTracker()
    tracker.update_progress("id", "stage", 50, "message")
    assert tracker.get_state("id").percentage == 50

# ✅ CORRETO: Teste unitário + teste de integração
def test_progress_tracker_update():  # Unitário
    # ... teste isolado

def test_api_process_e2e():  # Integração E2E
    # Testa fluxo completo: upload → SSE → result
```

---

## 🔧 FERRAMENTAS E VALIDAÇÃO

### Comandos Obrigatórios:

```bash
# 1. Validar que teste falha antes da implementação
pytest src/tests/.../test_nova_feature.py -v
# Esperado: FAILED (antes de implementar)

# 2. Validar que teste passa após implementação
pytest src/tests/.../test_nova_feature.py -v
# Esperado: PASSED (após implementar)

# 3. Validar que não quebrou outros testes
pytest -q
# Esperado: 0 failed

# 4. Validar testes de integração
pytest src/tests/integration/ -v
# Esperado: Todos passam

# 5. Validar Clean Code
# (ferramentas de análise estática - ver seção específica)
```

---

## 📌 CRITÉRIOS DE FAIL

**Gate Z10 FALHA se:**
- ❌ Código escrito sem teste correspondente
- ❌ Teste não falha antes da implementação
- ❌ Apenas happy path testado (sem erros)
- ❌ Fluxo crítico sem teste de integração end-to-end
- ❌ Teste passa sem implementação (teste inválido)
- ❌ `pytest -q` != 0 failed

---

## 🎯 CONCLUSÃO

**TDD não é opcional. É obrigatório.**

**Processo:**
1. RED: Teste falha
2. GREEN: Implementação mínima
3. REFACTOR: Clean Code

**Validação:**
- Teste escrito antes de código
- Teste falha antes da implementação
- Teste passa após implementação
- Testes de erro existem
- Testes de integração para fluxos críticos

**Regra canônica:**
> "Código sem teste é dívida técnica. Teste sem código é especificação executável."

---

## 📚 DEMANDAS RELACIONADAS

**DEMANDA-METODO-005:** TDD Rigoroso e Bloqueio Estrutural para Prevenir Erros
- Status: F-1 pendente aprovação
- Path: `DEMANDAS/DEMANDA-METODO-005_TDD_RIGOROSO_BLOQUEIO_ESTRUTURAL.md`
- Planejamento: `planejamento/DEMANDA-METODO-005_PLAN.md`

**DEMANDA-PROD-003:** Persistência Confiável e Garantida de Dados
- Status: F-1 pendente aprovação
- Path: `DEMANDAS/DEMANDA-PROD-003_PERSISTENCIA_CONFIAVEL_GARANTIDA.md`
- Planejamento: `planejamento/DEMANDA-PROD-003_PLAN.md`

**Nota:** Ambas demandas seguem TDD rigoroso e END-FIRST v2. Aguardam aprovação de F-1 antes de execução.
