---
demanda_id: DEMANDA-PROD-003
title: Persistência Confiável e Garantida de Dados
type: Produto
altera_funcionalidade: sim
exige_f1: sim
status: backlog
created_at: 2026-01-21
created_by: CEO (Joubert Jr)
executor: Cursor
---

# DEMANDA-PROD-003 — PERSISTÊNCIA CONFIÁVEL E GARANTIDA DE DADOS

**Tipo:** Produto / Plataforma  
**Método:** END-FIRST v2  
**Status:** BACKLOG (NÃO EXECUTAR)  
**Sistema:** CoverageSummarizer / livros  
**Projeto:** https://github.com/Joubertjr/livros

⸻

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

⸻

## 🚫 Regras Canônicas

**Persistência:**
> "Processo que não deixa rastro não é produto, é experimento descartável."

**Segurança:**
> "Dados não persistidos são dados perdidos. Perda de dados é FAIL estrutural."

**Atomicidade:**
> "Persistência é tudo ou nada. Não existe 'salvamento parcial'."

**Validação:**
> "Validação antes de salvar. Erro de validação = não tenta salvar."

**Rastreabilidade:**
> "Todo erro de persistência deve ser rastreável e reportável."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

⸻

## 📋 Problema Identificado

**Evidência:**
- Erro de validação de schema (`SummaryStorage.summaries`) impediu persistência silenciosamente
- Usuário processou resumo mas não apareceu no histórico (dados perdidos)
- Erro foi detectado apenas quando usuário tentou acessar histórico
- Não há validação pré-salvamento (validação acontece durante tentativa de salvar)
- Não há retry para falhas temporárias
- Não há validação pós-salvamento para garantir que dados foram escritos

**Causa Raiz:**
- Validação de schema acontece durante `save_summary()`, não antes
- Erros de validação são silenciosos (apenas log, não reportado ao usuário)
- Não há garantia de atomicidade (pode salvar parcialmente)
- Não há validação pós-salvamento
- Não há mecanismo de retry

⸻

## 🎯 Solução Esperada

1. **Validação Pré-Salvamento:**
   - Validar schema **antes** de tentar salvar
   - Se validação falhar, reportar erro ao usuário imediatamente
   - Não tentar salvar se validação falhar

2. **Persistência Transacional:**
   - Salvar tudo ou não salvar nada (atomicidade)
   - Validar dados após salvamento para garantir que foram escritos corretamente
   - Se validação pós-salvamento falhar, reverter (se possível) ou reportar erro

3. **Mecanismo de Retry:**
   - Retry automático para falhas temporárias (ex.: disco cheio temporário)
   - Limite de tentativas (ex.: 3 tentativas)
   - Backoff exponencial entre tentativas

4. **Rastreabilidade Completa:**
   - Logs detalhados de todas as tentativas de persistência
   - Logs incluem: dados que tentaram ser salvos, resultado (sucesso/falha), motivo da falha
   - Erros reportados ao usuário de forma clara

5. **Testes Abrangentes:**
   - Testes que garantem persistência em todos os cenários
   - Testes que garantem detecção de erros antes de tentar salvar
   - Testes que garantem recuperação de dados após salvamento
   - Testes que garantem atomicidade

⸻

## ✅ Critérios de Aceitação (Binários)

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

⸻

## 📊 Impacto Esperado

- ✅ **Zero perda de dados**: todos os resumos processados são garantidamente persistidos
- ✅ **Certeza absoluta**: usuário sabe que dados estão salvos
- ✅ **Rastreabilidade completa**: todos os erros são detectados e reportados
- ✅ **Confiabilidade**: sistema garante atomicidade e validação pós-salvamento
- ✅ **Resiliência**: retry automático para falhas temporárias
