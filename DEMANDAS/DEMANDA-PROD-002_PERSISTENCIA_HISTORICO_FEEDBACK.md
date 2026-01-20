---
demanda_id: DEMANDA-PROD-002
title: Persistência, Histórico e Feedback de Processos de Resumo
type: Produto
altera_funcionalidade: sim
exige_f1: sim
status: backlog
created_at: 2026-01-19
created_by: CEO (Joubert Jr)
executor: Cursor
---

# DEMANDA-PROD-002 — PERSISTÊNCIA, HISTÓRICO E FEEDBACK DE PROCESSOS DE RESUMO

**Tipo:** Produto / Plataforma  
**Método:** END-FIRST v2  
**Status:** BACKLOG (NÃO EXECUTAR)  
**Sistema:** CoverageSummarizer / livros  
**Projeto:** https://github.com/Joubertjr/livros

⸻

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para um usuário final:**
- Todo processo de resumo executado é persistido
- O usuário pode consultar resumos passados
- Cada resumo possui:
  - Identificador único
  - Nome/título definido
  - Data/hora de execução
  - Tipo de processo usado (ex.: estratégia A, B, experimental)
- É possível comparar diferentes execuções de resumo
- O usuário pode:
  - Registrar feedback, dúvida, erro ou sugestão
  - Ver claramente que sua solicitação foi recebida
  - Ver quando e como houve resposta

**Para o sistema:**
- Todos os dados do processo (input, estratégia, eventos, outputs) ficam armazenados
- Diferentes tipos de pipeline de resumo podem coexistir
- Feedback do usuário fica vinculado ao resumo específico
- Respostas posteriores (IA ou humano) ficam rastreadas
- Nenhuma informação gerada durante o processo se perde

**⚠️ Importante:**
Este END não define UI específica nem implementação técnica, apenas comportamento observável.

⸻

## 🚫 Regras Canônicas

**Persistência:**
> "Processo que não deixa rastro não é produto, é experimento descartável."

**Comparabilidade:**
> "Se não posso comparar execuções, não posso evoluir o sistema."

**Feedback:**
> "Feedback sem rastreabilidade é ruído."

**Histórico:**
> "O usuário não deve perder acesso ao que o sistema já produziu para ele."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

### Regras Estruturais

- Nenhum resumo pode existir apenas em memória
- Nenhuma execução pode ser sobrescrita silenciosamente
- Feedback do usuário deve estar ligado a um artefato concreto
- Histórico não pode depender de logs técnicos

⸻

## ✅ Critérios de Aceitação (Binários)

### PASS

- ✅ Resumos permanecem acessíveis após execução
- ✅ Cada execução é identificável e consultável
- ✅ Diferentes pipelines de resumo são distinguíveis
- ✅ Usuário consegue revisar resumos antigos
- ✅ Usuário consegue registrar feedback facilmente
- ✅ Sistema consegue responder ou registrar resposta ao feedback
- ✅ Feedback e resposta ficam associados ao resumo correto
- ✅ Nada depende de memória temporária ou sessão ativa
- ✅ Interface continua funcional (Gate Z11 permanece PASS)
- ✅ Nenhuma regressão funcional (Z0–Z11 continuam PASS)
- ✅ Evidência gerada (documentação e provas em `/EVIDENCIAS/`)

### FAIL (AUTOMÁTICO)

- ❌ Resumo se perde ao recarregar a página
- ❌ Não há como distinguir dois resumos diferentes
- ❌ Usuário não sabe se seu feedback foi visto
- ❌ Processos diferentes se misturam sem rastreabilidade
- ❌ Histórico depende de logs internos ou console
- ❌ Feedback não é associado a nada concreto
- ❌ UX alterada sem F-1 aprovada
- ❌ Qualquer regressão funcional
- ❌ Gate Z11 quebrado
- ❌ Correção aplicada direto no código sem planejamento

⸻

## 🧠 Problemas Observados (Evidência — Não São Tarefas)

**Contexto (não tarefas):**

Hoje o resumo:
- some após execução
- não pode ser revisitado
- não permite comparação

Não existe:
- histórico
- identidade do processo
- vínculo entre feedback e execução

Isso impede:
- evolução do produto
- aprendizado do sistema
- uso sério em cenários reais

**Causa raiz identificada:**

> Sistema trata resumo como resultado temporário, não como artefato de produto persistente.

⸻

## 🚫 DO / DON'T

### DO (fazer)

- ✅ Persistir dados do processo
- ✅ Tratar resumo como artefato de produto
- ✅ Separar processos de resumo por tipo
- ✅ Facilitar feedback do usuário
- ✅ Manter rastreabilidade completa
- ✅ Manter todos os gates PASS

### DON'T (não fazer)

- ❌ Resolver só com UI temporária
- ❌ Depender de sessão ativa
- ❌ Misturar execuções diferentes
- ❌ Ignorar feedback do usuário
- ❌ Tratar isso como "log técnico"
- ❌ Alterar pipeline de sumarização
- ❌ "Simplificar" removendo garantias
- ❌ Refatorar backend sem necessidade
- ❌ Quebrar Gate Z11

⸻

## 🧱 Bloqueios Estruturais

- 🔒 F-1 obrigatório (demanda de produto complexa)
- 🔒 Não executar sem definição clara de modelo de dados
- 🔒 Não executar sem decisão explícita de escopo
- 🔒 Gate Z11 continua bloqueante
- 🔒 Nenhuma alteração sem evidência visual
- 🔒 Persistência = produto, não experimento

⸻

## 📋 TODO Canônico (Somente Após F-1 Aprovada)

1. F-1: Planejamento Canônico (Persistência, Histórico, Feedback)
2. Definir quais dados de cada execução são persistidos
3. Definir modelo de identificação de resumo
4. Definir como diferenciar pipelines de resumo
5. Definir fluxo de feedback do usuário
6. Definir como respostas são registradas
7. Implementar persistência
8. Expor histórico ao usuário
9. Implementar sistema de feedback
10. Gerar evidências
11. Validar Gate Z11 e suite verde
12. Declarar PASS

⸻

## ❌ Fora de Escopo

**Esta demanda NÃO inclui:**

- ❌ Otimização de performance
- ❌ Treinamento de modelo
- ❌ Novas estratégias de resumo
- ❌ Automação de respostas
- ❌ Analytics avançado
- ❌ Mudanças no pipeline de sumarização
- ❌ Refatorações estruturais do backend

⸻

## 📌 Status

**BACKLOG (NÃO EXECUTAR)**

Este arquivo não autoriza execução. Só pode ser executado após:
- Priorização explícita
- F-1 aprovada
- Ordem clara do CEO

⸻

## 🧭 Regra Final (Canônica)

> "Resumo sem histórico não é produto. É só uma demonstração."

⸻

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Path Canônico:** `/DEMANDAS/DEMANDA-PROD-002_PERSISTENCIA_HISTORICO_FEEDBACK.md`  
**Template:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`
