# PLANEJAMENTO CANÔNICO — DEMANDA-METODO-005: TDD RIGOROSO E BLOQUEIO ESTRUTURAL

**Demanda:** DEMANDA-METODO-005_TDD_RIGOROSO_BLOQUEIO_ESTRUTURAL.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-21  
**Status:** ⏸️ F-1 PENDENTE APROVAÇÃO  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para o Desenvolvedor/Executor:**
- Nenhum código é escrito sem teste correspondente escrito ANTES
- Teste sempre falha primeiro (RED) antes da implementação
- Bloqueio estrutural impede commit/merge se TDD não foi seguido
- Erros de validação (schema, persistência, etc.) são detectados por testes ANTES de aparecerem em produção
- Processo END-FIRST v2 é seguido rigorosamente (F-1 obrigatória para mudanças complexas)

**Para o Sistema:**
- Gate Z10 (TDD + Clean Code) tem validação automática que bloqueia commits
- Testes cobrem todos os cenários críticos (happy path + erros)
- Schema changes têm testes que validam antes e depois
- Persistência tem testes que validam estrutura completa

**Para o CEO/Revisor:**
- Validação binária: TDD foi seguido? SIM/NÃO (sem interpretação)
- Evidência clara: testes escritos antes do código (commits mostram ordem)
- Zero erros de validação em produção (todos detectados por testes)

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS)

- **TDD:** "Teste primeiro, código depois. Sem exceção."
- **Bloqueio:** "Código sem teste é dívida técnica. Teste sem código é especificação executável."
- **END-FIRST:** "Planejamento é artefato de primeira classe. Executor apenas executa."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## ✅ CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)

### PASS

- ✅ Pre-commit hook ou CI valida ordem de commits (teste antes de código)
- ✅ Testes de schema cobrem estrutura completa (`summaries` com `capitulos`)
- ✅ Gate Z10 bloqueia commits se TDD não foi seguido
- ✅ F-1 obrigatória para mudanças de schema/persistência
- ✅ Zero erros de validação em produção (todos detectados por testes)
- ✅ Evidência clara: commits mostram teste antes de código

### FAIL

- ❌ Código commitado sem teste correspondente
- ❌ Teste criado depois do código (ordem incorreta)
- ❌ Erro de validação aparece em produção sem teste que detecte
- ❌ Mudança de schema sem F-1 aprovada
- ❌ Gate Z10 não bloqueia commits sem TDD

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
- ✅ Criar testes ANTES de qualquer código
- ✅ Validar que teste falha primeiro (RED)
- ✅ Implementar código mínimo para teste passar (GREEN)
- ✅ Refatorar seguindo Clean Code (REFACTOR)
- ✅ Validar que Gate Z10 bloqueia commits sem TDD
- ✅ Documentar processo TDD com exemplos práticos

### DON'T (Não Fazer)

**Durante Planejamento (F-1):**
- ❌ Executar comandos
- ❌ Criar código
- ❌ Criar testes
- ❌ "Validar rapidamente"
- ❌ Interpretar regras durante execução

**Durante Execução:**
- ❌ Criar código sem teste correspondente
- ❌ Criar teste depois do código
- ❌ Ignorar ordem RED → GREEN → REFACTOR
- ❌ Commit sem validação de TDD
- ❌ Alterar schema sem F-1 aprovada

---

## 📋 TODO CANÔNICO

**Sequência derivada do END (sem interpretação):**

1. **F-1: Planejamento Canônico**
   - Criar este documento
   - Definir END, critérios, DO/DON'T, bloqueios, TODO
   - Aguardar aprovação explícita ("F-1 aprovada")

2. **Expandir Testes de Schema (TDD)**
   - Escrever teste que valida `SummaryStorage` com `summaries` complexo (estrutura `capitulos`)
   - Teste deve falhar se schema não aceita estrutura completa
   - Validar que teste falha primeiro (RED)

3. **Implementar Validação de TDD no Gate Z10**
   - Adicionar validação que verifica ordem de commits (teste antes de código)
   - Pre-commit hook ou CI que bloqueia commits sem TDD
   - Documentar processo de validação

4. **Criar Testes de Regressão**
   - Testes que detectam mudanças incompatíveis no schema
   - Testes que validam persistência com estrutura completa
   - Testes que validam carregamento de resumos persistidos

5. **Documentar Processo TDD Rigoroso**
   - Atualizar `METODO/TDD_PROCESS.md` com exemplos práticos
   - Documentar ordem RED → GREEN → REFACTOR
   - Documentar bloqueio estrutural de TDD

6. **Validar Sistema Completo**
   - Validar que Gate Z10 bloqueia commits sem TDD
   - Validar que testes detectam erros antes de produção
   - Validar que processo END-FIRST v2 é seguido

**Ordem de Execução:**
1. F-1 (este documento) → APROVAÇÃO
2. Expandir Testes de Schema (TDD)
3. Implementar Validação de TDD no Gate Z10
4. Criar Testes de Regressão
5. Documentar Processo TDD Rigoroso
6. Validar Sistema Completo

---

## 🚨 CRITÉRIOS DE FAIL

**FAIL Automático se:**
- ❌ Código commitado sem teste correspondente
- ❌ Teste criado depois do código (ordem incorreta)
- ❌ Erro de validação aparece em produção sem teste que detecte
- ❌ Mudança de schema sem F-1 aprovada
- ❌ Gate Z10 não bloqueia commits sem TDD
- ❌ Execução iniciada sem F-1 aprovada

---

## 📝 STRINGS DE PROVA

**Comandos de Validação:**

```bash
# Validar que testes de schema existem e passam
docker compose exec app bash -c 'pytest src/tests/unit/test_summary_storage_capitulos.py -v'

# Validar que Gate Z10 bloqueia commits sem TDD
# (pre-commit hook ou CI deve retornar erro se teste não existe)

# Validar que processo TDD foi seguido (commits mostram ordem)
git log --oneline --all | grep -E "test|fix|feat" | head -10

# Validar que não há erros de validação em produção
docker compose logs app | grep -i "validation.*error" | tail -5
```

**Strings Esperadas:**
- Testes: `PASSED` (todos os testes de schema)
- Gate Z10: Bloqueia commits sem TDD
- Commits: Teste antes de código (ordem correta)
- Logs: Zero erros de validação

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
