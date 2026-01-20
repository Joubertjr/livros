---
demanda_id: DEMANDA-METODO-003
title: Governança do Ciclo de Vida de Demandas, Planejamento, Evidências e Histórico
type: Metodo
altera_funcionalidade: nao
exige_f1: sim
status: backlog
created_at: 2026-01-19
created_by: CEO (Joubert Jr)
executor: Cursor
---

# DEMANDA-METODO-003 — GOVERNANÇA DO CICLO DE VIDA DE ARTEFATOS

**Tipo:** Método / Governança  
**Método:** END-FIRST v2  
**Status:** BACKLOG (NÃO EXECUTAR)  
**Repositório alvo:** livros (e futuros projetos que usem END-FIRST)

⸻

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para qualquer projeto que use END-FIRST:**

- O ciclo completo **DEMANDA → F-1 → Execução → Evidências → Histórico** é:
  - conceitualmente explícito
  - semanticamente inequívoco
  - fácil de entender sem explicação verbal
- Cada artefato gerado durante o ciclo:
  - tem papel claro
  - tem tempo de vida compreensível
  - não gera confusão sobre "ativo vs histórico"
- Um observador externo consegue:
  - entender o estado do projeto apenas olhando os artefatos
  - diferenciar intenção, planejamento, execução, prova e memória
- A organização dos artefatos:
  - reduz fricção cognitiva
  - evita sensação de "zona"
  - elimina necessidade de auditoria humana para entender contexto

**⚠️ Importante:**  
Este END **não define estrutura de pastas específica**, nem impõe layout de filesystem.  
Ele define **governança conceitual do ciclo de vida**, não implementação.

⸻

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS)

**Ciclo de Vida:**
> "Artefatos com naturezas diferentes não podem ocupar o mesmo plano semântico."

**Intenção vs Memória:**
> "Demanda não é histórico. Histórico não governa execução."

**Planejamento:**
> "F-1 existe para governar execução, não para se perpetuar."

**Evidência:**
> "Evidência prova o END; não substitui o END."

**Clareza Cognitiva:**
> "Se é preciso explicar onde algo se encaixa, o método falhou."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

⸻

## ✅ CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)

### PASS

- ✅ O ciclo DEMANDA → F-1 → Execução → Evidências → Histórico está explicitamente descrito
- ✅ Cada tipo de artefato tem:
  - propósito claro
  - momento de criação definido
  - papel no método explícito
- ✅ Fica claro quando um artefato deixa de ser "ativo"
- ✅ Evidências são distinguíveis de planejamento e de histórico
- ✅ Histórico é tratado como memória sistêmica, não como artefato operacional
- ✅ O método reduz necessidade de explicação humana para entender organização
- ✅ Nenhuma mudança quebra END-FIRST v2
- ✅ Nenhum gate existente é enfraquecido
- ✅ Evidência conceitual gerada (documentação)

### FAIL (AUTOMÁTICO)

- ❌ Continuidade de ambiguidade entre planejamento, evidência e histórico
- ❌ Mistura conceitual entre artefatos ativos e memória
- ❌ Dependência de convenção tácita para entender organização
- ❌ Solução focada apenas em filesystem, sem governança conceitual
- ❌ Introdução de complexidade estrutural sem ganho cognitivo
- ❌ Alteração de comportamento operacional sem END claro
- ❌ Execução sem F-1 aprovada
- ❌ Violação de qualquer frase canônica

⸻

## 🧠 PROBLEMA OBSERVADO (CONTEXTO)

**Contexto real:**

- Demandas, planejamentos e evidências coexistem sem fronteira conceitual explícita
- A compreensão do "estado do sistema" exige leitura extensa
- Histórico emerge de forma orgânica, não governada
- A organização atual gera sensação de desordem, apesar de execução correta

**Causa raiz identificada:**

> O método governa muito bem intenção e execução, mas não governa explicitamente a transição para memória e histórico.

⸻

## 🚫 DO / DON'T

### DO

- ✅ Tratar ciclo de vida como conceito de método
- ✅ Diferenciar intenção, execução, prova e memória
- ✅ Reduzir fricção cognitiva
- ✅ Manter independência de ferramenta e filesystem
- ✅ Usar Pilar END-FIRST como base
- ✅ Documentar governança conceitual

### DON'T

- ❌ Resolver apenas reorganizando pastas
- ❌ Criar convenções implícitas
- ❌ Misturar artefatos ativos com históricos
- ❌ Criar regras dependentes de um projeto específico
- ❌ Aumentar burocracia sem ganho cognitivo
- ❌ Alterar produto ou UX
- ❌ Criar novos gates automaticamente
- ❌ Alterar regras existentes sem evidência clara

⸻

## 🧱 BLOQUEIOS ESTRUTURAIS

- 🔒 F-1 obrigatório (demanda de método)
- 🔒 Nenhuma execução sem aprovação explícita
- 🔒 Não criar novos gates automaticamente
- 🔒 Não alterar regras existentes sem evidência clara
- 🔒 Governança conceitual precede implementação
- 🔒 END-FIRST v2 continua bloqueante

⸻

## 📋 TODO CANÔNICO (SOMENTE APÓS F-1 APROVADA)

1. F-1: Planejamento Canônico (Ciclo de Vida de Artefatos)
2. Mapear conceitualmente cada etapa do ciclo
3. Definir fronteiras semânticas entre artefatos
4. Identificar pontos de fricção cognitiva atuais
5. Validar alinhamento com END-FIRST v2
6. Gerar evidência conceitual (documentação)
7. Declarar PASS

⸻

## ❌ FORA DE ESCOPO

- ❌ Mudanças em produto
- ❌ Refatoração de código
- ❌ Reorganização concreta de pastas
- ❌ Automação
- ❌ Criação de novos gates
- ❌ Ajustes em Cursor ou Manus
- ❌ Implementação de ferramentas

⸻

## 📌 STATUS

**BACKLOG (NÃO EXECUTAR)**

Este arquivo não autoriza execução.  
Só pode ser executado após:
- Priorização explícita
- F-1 aprovada
- Ordem clara do CEO

⸻

## 🧭 REGRA FINAL (CANÔNICA)

> "Quando o ciclo de vida é claro, a organização deixa de ser um problema."

⸻

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Template:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`
