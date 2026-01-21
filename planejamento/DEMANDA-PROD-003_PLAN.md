# PLANEJAMENTO CANÔNICO — DEMANDA-PROD-003: PERSISTÊNCIA CONFIÁVEL E GARANTIDA

**Demanda:** DEMANDA-PROD-003_PERSISTENCIA_CONFIAVEL_GARANTIDA.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-21  
**Status:** ⏸️ F-1 PENDENTE APROVAÇÃO  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para o Usuário Final:**
- Todo resumo processado é **garantidamente persistido** (zero perda de dados)
- Usuário tem **certeza absoluta** de que seus dados estão salvos
- Histórico sempre mostra todos os resumos processados (sem gaps)
- Nenhum erro silencioso de persistência (todos os erros são detectados e reportados)
- Sistema garante **atomicidade**: ou salva completamente ou falha explicitamente

**Para o Sistema:**
- Persistência é **transacional**: ou salva tudo ou não salva nada
- Validação de schema acontece **antes** de tentar salvar (não durante)
- Erros de persistência são **detectados imediatamente** e reportados ao usuário
- Sistema tem **mecanismo de retry** para falhas temporárias
- Sistema tem **validação pós-salvamento** para garantir que dados foram escritos corretamente
- Logs detalhados de todas as tentativas de persistência (sucesso ou falha)

**Para o Desenvolvedor:**
- Testes garantem que persistência funciona em todos os cenários (happy path + erros)
- Testes garantem que erros de validação são detectados antes de tentar salvar
- Testes garantem que dados são recuperáveis após salvamento
- Evidência clara: todos os resumos processados estão no histórico

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS)

- **Persistência:** "Processo que não deixa rastro não é produto, é experimento descartável."
- **Segurança:** "Dados não persistidos são dados perdidos. Perda de dados é FAIL estrutural."
- **Atomicidade:** "Persistência é tudo ou nada. Não existe 'salvamento parcial'."
- **Validação:** "Validação antes de salvar. Erro de validação = não tenta salvar."
- **Rastreabilidade:** "Todo erro de persistência deve ser rastreável e reportável."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## ✅ CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)

### PASS

- ✅ Validação de schema acontece **antes** de tentar salvar
- ✅ Erros de validação são **reportados ao usuário** imediatamente
- ✅ Persistência é **transacional** (tudo ou nada)
- ✅ Validação pós-salvamento garante que dados foram escritos corretamente
- ✅ Mecanismo de retry para falhas temporárias (3 tentativas, backoff exponencial)
- ✅ Logs detalhados de todas as tentativas de persistência
- ✅ Testes garantem persistência em todos os cenários (happy path + erros)
- ✅ Zero perda de dados (todos os resumos processados aparecem no histórico)
- ✅ Usuário tem certeza absoluta de que dados estão salvos

### FAIL

- ❌ Erro de validação impede persistência silenciosamente
- ❌ Dados são perdidos sem aviso ao usuário
- ❌ Validação acontece durante tentativa de salvar (não antes)
- ❌ Não há atomicidade (salvamento parcial possível)
- ❌ Não há validação pós-salvamento
- ❌ Não há retry para falhas temporárias
- ❌ Erros não são reportados ao usuário
- ❌ Resumo processado não aparece no histórico

---

## 🚫 DO / DON'T

### DO (Fazer)

**Durante Planejamento (F-1):**
- ✅ Criar este documento de planejamento
- ✅ Definir TODO canônico
- ✅ Definir escopo DO/DON'T
- ✅ Definir ordem de execução
- ✅ Definir critérios de FAIL
- ✅ Aguardar aprovação explícita ("F-1 aprovada")

**Durante Execução (após F-1 aprovada):**
- ✅ Implementar validação pré-salvamento (antes de tentar salvar)
- ✅ Implementar persistência transacional (atomicidade)
- ✅ Implementar validação pós-salvamento
- ✅ Implementar mecanismo de retry (3 tentativas, backoff exponencial)
- ✅ Implementar logs detalhados de todas as tentativas
- ✅ Reportar erros ao usuário de forma clara
- ✅ Criar testes que garantem persistência em todos os cenários
- ✅ Seguir TDD rigorosamente (teste antes de código)

### DON'T (Não Fazer)

**Durante Planejamento (F-1):**
- ❌ Executar comandos
- ❌ Criar código
- ❌ Criar testes
- ❌ "Validar rapidamente"
- ❌ Interpretar regras durante execução

**Durante Execução:**
- ❌ Permitir persistência silenciosa (sem validação prévia)
- ❌ Permitir salvamento parcial (sem atomicidade)
- ❌ Ignorar erros de validação
- ❌ Não reportar erros ao usuário
- ❌ Criar código sem teste correspondente (viola TDD)

---

## 📋 TODO CANÔNICO

**Sequência derivada do END (sem interpretação):**

1. **F-1: Planejamento Canônico**
   - Criar este documento
   - Definir END, critérios, DO/DON'T, bloqueios, TODO
   - Aguardar aprovação explícita ("F-1 aprovada")

2. **Testes de Validação Pré-Salvamento (TDD - RED)**
   - Escrever teste que valida schema **antes** de tentar salvar
   - Teste deve falhar se validação não acontece antes
   - Teste deve validar que erro é reportado ao usuário
   - Validar que teste falha primeiro (RED)

3. **Implementar Validação Pré-Salvamento (TDD - GREEN)**
   - Implementar validação de schema antes de `save_summary()`
   - Se validação falhar, reportar erro ao usuário imediatamente
   - Não tentar salvar se validação falhar
   - Validar que teste passa (GREEN)

4. **Testes de Persistência Transacional (TDD - RED)**
   - Escrever teste que valida atomicidade (tudo ou nada)
   - Teste deve falhar se salvamento parcial é possível
   - Teste deve validar validação pós-salvamento
   - Validar que teste falha primeiro (RED)

5. **Implementar Persistência Transacional (TDD - GREEN)**
   - Implementar atomicidade (salvar tudo ou não salvar nada)
   - Implementar validação pós-salvamento
   - Se validação pós-salvamento falhar, reportar erro
   - Validar que teste passa (GREEN)

6. **Testes de Retry (TDD - RED)**
   - Escrever teste que valida retry para falhas temporárias
   - Teste deve validar 3 tentativas com backoff exponencial
   - Validar que teste falha primeiro (RED)

7. **Implementar Mecanismo de Retry (TDD - GREEN)**
   - Implementar retry automático (3 tentativas)
   - Implementar backoff exponencial entre tentativas
   - Validar que teste passa (GREEN)

8. **Implementar Logs Detalhados**
   - Logs de todas as tentativas de persistência
   - Logs incluem: dados, resultado, motivo da falha
   - Logs são rastreáveis e reportáveis

9. **Testes de Regressão**
   - Testes que garantem zero perda de dados
   - Testes que garantem que todos os resumos aparecem no histórico
   - Testes que garantem recuperação de dados após salvamento

10. **Refatoração (Clean Code)**
    - Refatorar código seguindo Clean Code
    - Funções pequenas, responsabilidade única
    - Sem duplicação, sem lógica implícita

11. **Validar Sistema Completo**
    - Validar que validação pré-salvamento funciona
    - Validar que persistência transacional funciona
    - Validar que retry funciona
    - Validar que logs são detalhados
    - Validar que zero perda de dados

**Ordem de Execução:**
1. F-1 (este documento) → APROVAÇÃO
2. Testes de Validação Pré-Salvamento (TDD - RED)
3. Implementar Validação Pré-Salvamento (TDD - GREEN)
4. Testes de Persistência Transacional (TDD - RED)
5. Implementar Persistência Transacional (TDD - GREEN)
6. Testes de Retry (TDD - RED)
7. Implementar Mecanismo de Retry (TDD - GREEN)
8. Implementar Logs Detalhados
9. Testes de Regressão
10. Refatoração (Clean Code)
11. Validar Sistema Completo

---

## 🚨 CRITÉRIOS DE FAIL

**FAIL Automático se:**
- ❌ Erro de validação impede persistência silenciosamente
- ❌ Dados são perdidos sem aviso ao usuário
- ❌ Validação acontece durante tentativa de salvar (não antes)
- ❌ Não há atomicidade (salvamento parcial possível)
- ❌ Não há validação pós-salvamento
- ❌ Não há retry para falhas temporárias
- ❌ Erros não são reportados ao usuário
- ❌ Resumo processado não aparece no histórico
- ❌ Execução iniciada sem F-1 aprovada
- ❌ Código criado sem teste correspondente (viola TDD)

---

## 📝 STRINGS DE PROVA

**Comandos de Validação:**

```bash
# Validar que validação pré-salvamento funciona
docker compose exec app bash -c 'pytest src/tests/unit/test_summary_storage_validation.py -v'

# Validar que persistência transacional funciona
docker compose exec app bash -c 'pytest src/tests/integration/test_persistence_atomicity.py -v'

# Validar que retry funciona
docker compose exec app bash -c 'pytest src/tests/integration/test_persistence_retry.py -v'

# Validar que zero perda de dados
docker compose exec app bash -c 'python3 -c "
import sys
sys.path.insert(0, \"/app/src\")
from storage import get_storage_manager
storage = get_storage_manager()
summaries = storage.list_summaries()
print(f\"Total de resumos persistidos: {len(summaries)}\")
"'

# Validar que logs são detalhados
docker compose logs app | grep -i "persist.*summary" | tail -10
```

**Strings Esperadas:**
- Testes: `PASSED` (todos os testes de persistência)
- Validação: Erro reportado antes de tentar salvar
- Atomicidade: Tudo ou nada (sem salvamento parcial)
- Retry: 3 tentativas com backoff exponencial
- Logs: Detalhados e rastreáveis
- Dados: Zero perda (todos os resumos no histórico)

---

## 🎯 APROVAÇÃO

**Status:** PENDENTE DE APROVAÇÃO

**Checklist de Aprovação:**
- [x] TODO canônico existe
- [x] Escopo DO/DON'T explícito
- [x] Ordem de execução definida
- [x] Critérios de FAIL listados
- [x] Strings de prova definidas
- [x] Nenhum comando foi executado durante F-1
- [x] Nenhum código foi criado durante F-1

**Aguardando:**
- [ ] Declaração explícita: **"F-1 aprovada"**
- [ ] Aprovação do CEO ou arquiteto responsável

---

## 📌 NOTAS

**Regra Crítica:**
> "F-1 é planejamento, não execução. Executar durante F-1 é FAIL automático."

**Bloqueio Estrutural:**
> "Esta demanda requer F-1 (Planejamento Canônico). Sem F-1 aprovada, não posso executar."

**TDD Rigoroso:**
> "Teste primeiro, código depois. Sem exceção."

**Persistência:**
> "Dados não persistidos são dados perdidos. Perda de dados é FAIL estrutural."
