---
demanda_id: DEMANDA-PROD-004
title: Persistência Progressiva de Resumo e Retomada Segura
type: Produto
altera_funcionalidade: sim
exige_f1: sim
status: backlog
created_at: 2026-01-21
created_by: CEO (Joubert Jr)
executor: Cursor
---

# DEMANDA-PROD-004 — PERSISTÊNCIA PROGRESSIVA DE RESUMO E RETOMADA SEGURA

**Tipo:** Produto / Execução Longa  
**Método:** END-FIRST v2  
**Sistema:** Projeto Livro (Book Summarizer)  
**Status:** BACKLOG (NÃO EXECUTAR)  
**Exige F-1:** ✅ Sim  
**Impacto:** Alto (valor cognitivo, custo computacional, confiabilidade)

⸻

## 🔒 END (Resultado Observável)

### Estado Final Esperado

Para qualquer execução de resumo (PDF, livro ou texto longo):

- Todo valor cognitivo gerado pelo sistema é persistido progressivamente
- Nenhuma falha técnica, desconexão ou erro parcial faz o sistema:
  - perder trabalho já executado
  - exigir reprocessamento de etapas concluídas
- O usuário (ou sistema) consegue:
  - inspecionar o progresso já realizado
  - retomar a execução a partir do último ponto válido
  - validar partes do resumo sem esperar o fim do processamento
- O sistema consegue responder objetivamente, a qualquer momento:
  **"O que já foi feito, está salvo e é reaproveitável?"**

### 📌 Resumo do END:

**"Se o sistema produziu valor cognitivo, esse valor não se perde."**

⸻

## 🧭 FRASES CANÔNICAS (BLOQUEANTES)

- **Valor:**
  > "Valor cognitivo produzido não é descartável."

- **Execução longa:**
  > "Execução longa sem persistência progressiva é desperdício estrutural."

- **Falha:**
  > "Falha não pode apagar história."

- **Retomada:**
  > "Retomar não é recomeçar."

- **END-FIRST:**
  > "END não é só o final; END é o que permanece."

**Violação de qualquer frase canônica = FAIL automático.**

⸻

## 🧠 PROBLEMA OBSERVADO (EVIDÊNCIA, NÃO TAREFA)

### Sintomas reais

- Processamento avança e falha → progresso perdido
- Validação exige reprocessar etapas já concluídas
- Não existe inspeção confiável de resultados parciais
- Execuções longas geram retrabalho técnico e humano
- Histórico de resumos é frágil ou inexistente

### Causa raiz identificada

O sistema trata execução como pipeline descartável, não como geração incremental de valor persistente.

⸻

## 🚫 O QUE ESTA DEMANDA NÃO É

- ❌ Não é apenas "adicionar banco"
- ❌ Não é apenas "bug de SSE"
- ❌ Não é refatoração técnica isolada
- ❌ Não é melhoria cosmética de UX

### 📌 É uma demanda estrutural de produto, governando como valor é produzido, preservado e validado.

⸻

## ✅ CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)

### PASS

- ✅ O sistema persiste resultados intermediários relevantes do resumo
- ✅ Progresso já executado não se perde em caso de falha
- ✅ Existe distinção clara entre:
  - processamento transitório
  - valor cognitivo persistente
- ✅ O sistema permite inspeção de resultados parciais
- ✅ Retomada não exige reprocessamento do que já foi concluído
- ✅ Execuções anteriores ficam disponíveis para consulta
- ✅ END é verificável antes do término total do processo
- ✅ Gate Z10 aplicado (execução longa + persistência)
- ✅ Gate Z11 continua PASS
- ✅ Evidência gerada em `/EVIDENCIAS/produto/`

### FAIL (AUTOMÁTICO)

- ❌ Falha apaga progresso já produzido
- ❌ Persistência só ocorre no final
- ❌ Retomar execução implica reprocessar etapas concluídas
- ❌ "Salvar tudo no final" tratado como suficiente
- ❌ Persistência validada apenas no caminho feliz
- ❌ Histórico inexistente ou inconsistente
- ❌ END só é observável no final da execução
- ❌ Qualidade tratada como opcional

⸻

## 🧱 BLOQUEIOS ESTRUTURAIS

- 🔒 F-1 obrigatório (demanda de execução longa)
- 🔒 Gate Z10 obrigatório (robustez + persistência)
- 🔒 Nenhuma perda de valor cognitivo é aceitável
- 🔒 END-FIRST v2 continua governando
- 🔒 Evidência obrigatória antes de declarar PASS

⸻

## 📋 TODO CANÔNICO (APÓS F-1 APROVADA)

1. F-1: Planejamento Canônico
2. Definir o que é "valor cognitivo persistente"
3. Definir pontos mínimos de persistência incremental
4. Definir contrato de retomada segura
5. Ajustar pipeline para respeitar o contrato
6. Expor inspeção de progresso/resultados parciais
7. Garantir histórico de execuções
8. Gerar evidência de falha sem perda de progresso
9. Validar Gates (Z10, Z11)
10. Declarar PASS

⸻

## 🚫 FORA DE ESCOPO

- ❌ Otimização de performance
- ❌ Mudança de modelo de IA
- ❌ Redesign completo de UI
- ❌ Automação fora do método
- ❌ "Resolver rápido sem método"

⸻

## 🧭 REGRA FINAL (CANÔNICA)

**"Se o sistema gerou valor e o perdeu, o END não foi alcançado."**

⸻

## 📌 STATUS

**BACKLOG (NÃO EXECUTAR)**

Aguardando:
- Priorização explícita
- Aprovação do CEO
- Criação de F-1

⸻

## 📚 RELAÇÃO COM OUTRAS DEMANDAS

- **DEMANDA-PROD-003** (Persistência Confiável e Garantida): Foca em garantir que quando salvar, salve corretamente (atomicidade, validação, retry). Esta demanda (PROD-004) complementa ao focar em **quando** salvar (progressivamente) e **como** retomar (sem reprocessar).
- **DEMANDA-PROD-002** (Persistência Histórico Feedback): Foca em histórico e feedback. Esta demanda (PROD-004) garante que o histórico seja construído progressivamente, não apenas no final.

⸻

**Documento criado:** 2026-01-21  
**Última atualização:** 2026-01-21  
**Governado por:** END-FIRST v2
