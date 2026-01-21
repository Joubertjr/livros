---
demanda_id: DEMANDA-METODO-005
title: TDD Rigoroso e Bloqueio Estrutural para Prevenir Erros
type: Método
altera_funcionalidade: sim
exige_f1: sim
status: backlog
created_at: 2026-01-21
created_by: CEO (Joubert Jr)
executor: Cursor
---

# DEMANDA-METODO-005 — TDD RIGOROSO E BLOQUEIO ESTRUTURAL PARA PREVENIR ERROS

**Tipo:** Método / Governança  
**Método:** END-FIRST v2  
**Status:** BACKLOG (NÃO EXECUTAR)  
**Sistema:** CoverageSummarizer / livros  
**Projeto:** https://github.com/Joubertjr/livros

⸻

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

⸻

## 🚫 Regras Canônicas

**TDD:**
> "Teste primeiro, código depois. Sem exceção."

**Bloqueio:**
> "Código sem teste é dívida técnica. Teste sem código é especificação executável."

**END-FIRST:**
> "Planejamento é artefato de primeira classe. Executor apenas executa."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

⸻

## 📋 Problema Identificado

**Evidência:**
- Erro de validação de schema (`SummaryStorage.summaries`) apareceu em produção
- Testes foram criados DEPOIS da correção (violação de TDD)
- Mudanças complexas foram feitas sem F-1 (violação de END-FIRST v2)
- Usuário teve que reportar erro manualmente

**Causa Raiz:**
- TDD não foi seguido rigorosamente (testes depois do código)
- Não há bloqueio estrutural que impeça commits sem testes
- F-1 não foi aplicada para mudanças complexas
- Validação de schema não tem testes que detectem mudanças incompatíveis

⸻

## 🎯 Solução Esperada

1. **Bloqueio Estrutural de TDD:**
   - Pre-commit hook ou CI que valida: teste existe antes do código?
   - Gate Z10 expandido para validar ordem de commits (teste antes de código)

2. **Testes de Validação de Schema:**
   - Testes que validam estrutura completa de `SummaryStorage` com `summaries` complexo
   - Testes que detectam mudanças incompatíveis no schema

3. **Processo END-FIRST v2 Rigoroso:**
   - F-1 obrigatória para qualquer mudança que altere schema, persistência, ou estrutura
   - Validação de F-1 antes de qualquer execução

4. **Evidência de TDD:**
   - Commits mostram ordem: teste primeiro (RED), código depois (GREEN)
   - Documentação de processo TDD atualizada com exemplos práticos

⸻

## ✅ Critérios de Aceitação (Binários)

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

⸻

## 📊 Impacto Esperado

- ✅ Zero erros de validação em produção (todos detectados por testes)
- ✅ TDD seguido rigorosamente (teste sempre antes de código)
- ✅ Processo END-FIRST v2 respeitado (F-1 para mudanças complexas)
- ✅ Bloqueio estrutural impede violações de TDD
- ✅ Validação binária: TDD foi seguido? SIM/NÃO
