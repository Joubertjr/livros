---
document_id: CURSOR_INSTRUCTIONS
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-10
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.2
created_at: 2026-01-10
---

# CURSOR INSTRUCTIONS — Instruções Operacionais para Cursor

**Versão:** 1.2  
**Data:** 19 de Janeiro de 2026 (atualizado)  
**Tipo:** Operacional (Tipo B)  
**Owner:** CEO (Joubert Jr)

---

## 🎯 OBJETIVO

Este documento contém **instruções operacionais diretas** para o Cursor (executor técnico) seguir durante a execução de incrementos.

**Regra:**
> Cursor DEVE ler este documento antes de iniciar qualquer incremento.

---

## 🔒 BLOQUEIO DE TEMPLATE (END-FIRST v2)

### Regra absoluta

> **Demandas fora do template canônico são FAIL estrutural.**

### O que é o Template Canônico

**Template Canônico de Demanda** é a estrutura obrigatória de 11 seções que toda demanda deve seguir.

**Documento oficial:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`

### Estrutura Obrigatória (11 seções)

Toda demanda DEVE conter:

1. Cabeçalho canônico (YAML frontmatter)
2. 🔒 END (Resultado Observável)
3. 🚫 Regras Canônicas
4. ✅ Critérios de Aceitação (PASS / FAIL)
5. 🧠 Problemas Observados
6. 🚫 DO / DON'T
7. 🧱 Bloqueios Estruturais
8. 📋 TODO Canônico
9. ❌ Fora de Escopo
10. 📌 Status
11. 🧭 Regra Final

### Como verificar

**Antes de iniciar execução:**

1. **Ler a demanda completa**
2. **Verificar presença das 11 seções obrigatórias**
3. **Se alguma seção estiver faltando:** **BLOQUEAR execução**

### Frase de bloqueio

Se demanda não segue o template:

> "Esta demanda não segue o template canônico. Demandas fora do template são FAIL estrutural. Por favor, reescreva a demanda usando `/METODO/TEMPLATE_DEMANDA_CANONICA.md`."

### Regra de UX Canônica (GLOBAL)

> **Scroll interno é PROIBIDO.**

- Nenhum componente pode esconder conteúdo
- Todo bloco deve expandir verticalmente
- Conteúdo invisível ou cortado é BUG estrutural

**Esta regra se aplica a TODAS as demandas.**

---

## 🔒 BLOQUEIO F-1 (END-FIRST v2)

### Regra absoluta

> **Sem F-1 aprovada, não executar demandas complexas.**

### O que é F-1

**F-1 (Planejamento Canônico)** é o estágio obrigatório de planejamento que deve ser concluído e aprovado antes de qualquer execução.

**Documento canônico:** `/METODO/END_FIRST_V2.md`

### Quando F-1 é obrigatório

**F-1 é obrigatório para:**
- ✅ Projetos complexos (múltiplos arquivos, múltiplas etapas)
- ✅ Mudanças estruturais no método
- ✅ Implementação de novos produtos
- ✅ Demandas com dependências entre etapas

**F-1 é opcional para:**
- ❌ Demandas simples (1 arquivo, 1 etapa, escopo claro)
- ❌ Correções triviais (typo, formatação)

**Regra de decisão:**
> Se há dúvida se F-1 é necessário, F-1 é necessário.

### Como verificar F-1

**Antes de iniciar execução:**

1. **Ler a demanda completa**
2. **Avaliar complexidade:**
   - Múltiplos arquivos? → F-1 obrigatório
   - Múltiplas etapas? → F-1 obrigatório
   - Dependências entre etapas? → F-1 obrigatório
   - Mudança estrutural? → F-1 obrigatório
3. **Procurar documento de planejamento:**
   - Arquivo com nome `PLANEJAMENTO_*` ou `F1_*`
   - Seção "F-1" ou "Planejamento Canônico" na demanda
4. **Verificar aprovação:**
   - Procurar declaração explícita: **"F-1 aprovada"**
   - Se não houver: **BLOQUEAR execução**

### Frase de bloqueio

Se F-1 é necessário mas não existe ou não foi aprovado:

> "Esta demanda requer F-1 (Planejamento Canônico). Sem F-1 aprovada, não posso executar. Por favor, crie o documento de planejamento com END, TODO canônico, escopo DO/DON'T, ordem de execução e critérios de FAIL."

### O que F-1 deve conter

**Mínimo obrigatório:**
- ✅ END (resultado esperado da demanda)
- ✅ TODO canônico (lista de etapas)
- ✅ Escopo DO / DON'T explícito
- ✅ Ordem de execução explícita
- ✅ Critérios de FAIL explícitos
- ✅ Declaração: "F-1 aprovada"

### PROIBIÇÕES durante F-1

Se você está criando F-1 (planejamento), é **estritamente proibido:**

- ❌ Executar comandos
- ❌ Criar código
- ❌ Criar automações
- ❌ "Validar rapidamente"

**F-1 é planejamento, não execução.**

---

## 🔗 RASTREABILIDADE OBRIGATÓRIA (KANBAN)

### Regra absoluta

**Todo commit DEVE referenciar card do GitHub Projects.**

**Formato obrigatório:**
- `Refs #X` ou `[#X]` na mensagem de commit
- Onde `X` = número do card/issue

### Fluxo obrigatório

**1. Ao iniciar incremento:**
- Mover card de **TODO → DOING** no GitHub Projects
- Criar primeiro commit com `Refs #X`

**2. Durante execução:**
- Todo commit DEVE incluir `Refs #X`
- Manter card em **DOING**

**3. Ao concluir incremento:**
- Último commit DEVE incluir `Refs #X`
- Mover card de **DOING → DONE** no GitHub Projects

### Exemplo de commit correto

```
feat(ui): implementa seleção de resposta [#5]

- Adiciona estado de seleção (useState)
- Implementa feedback visual inequívoco
- Cria evidência em EVIDENCIAS/CRITERIO_03.md

Prova Critério 3:
- ✅ Seleção funcional
- ✅ Feedback visual claro
- ✅ Deseleção automática

Refs #5
```

### Exemplo de commit INCORRETO (proibido)

```
feat(ui): implementa seleção de resposta

- Adiciona estado de seleção
- Implementa feedback visual

❌ FALTA: Refs #X
❌ FALTA: Mover card no Kanban
```

---

## 📋 CHECKLIST PRÉ-COMMIT

Antes de fazer commit, verificar:

- [ ] Mensagem de commit inclui `Refs #X` ou `[#X]`
- [ ] Card está em **DOING** (se primeiro commit, mover de TODO → DOING)
- [ ] Commit referencia o card correto (número bate com incremento)
- [ ] Se último commit do incremento, mover card para **DONE**

---

## 🚨 PROIBIÇÕES ABSOLUTAS

**❌ Commit sem referência ao card**
- Todo commit sem `Refs #X` viola rastreabilidade 100%

**❌ Card em TODO com commits já feitos**
- Se commit existe, card DEVE estar em DOING ou DONE

**❌ Card em DOING após incremento concluído**
- Se incremento terminou, card DEVE estar em DONE

**❌ Múltiplos cards em DOING simultaneamente**
- Apenas 1 incremento por vez (WIP = 1)

---

## 📜 FONTE DAS REGRAS

**Documentos canônicos:**
- `/METODO/KANBAN_CANONICO.md` — Definição de colunas, regras, automações
- `/METODO/CONTRATO_ESTADOS.md` — Quem move o quê, transições de estado
- `/METODO/INSTRUMENTACAO_VISIBILIDADE.md` — Como CEO vê estado sem conversa

**Princípio:**
> "Quem não está no Kanban não existe. E quem inventa status está estruturalmente errado." (CEO, 2026-01-10)

---

## 🎯 MUDANÇA COMPORTAMENTAL IMEDIATA

**A partir de agora:**
- Cursor não faz commit sem `Refs #X`
- Cursor não deixa card em TODO com commits feitos
- Cursor não deixa card em DOING após concluir incremento
- Sistema impede status inventado (não depende de disciplina)

**Lei ativa:**
- OD-009: Processo > Disciplina (não depende de "lembrar")
- OD-011: Entendimento sem mudança é fuga (muda comportamento agora)
- Kanban Canônico: Status é consequência, não narrativa

---

## 🔄 FLUXO VISUAL

```
TODO → DOING → DONE
  ↓       ↓       ↓
Início  Commits  Fim
        (Refs #X)
```

**Regra:**
- TODO = Nada iniciado (sem commits)
- DOING = Execução ativa (commits com Refs #X)
- DONE = Concluído (último commit + card movido)

---

## 📞 DÚVIDAS?

**Se algo não está claro:**
- Execução PARA (não tenta adivinhar)
- Lê documentos canônicos (KANBAN_CANONICO.md, CONTRATO_ESTADOS.md)
- Pergunta ao CEO (não ao Manus)

**Princípio:**
> "Executor não avalia se 'está certo'. Executor segue estados, critérios e evidências. Se algo não está claro, execução PARA." (OD-011 estendida)

---

## 📊 HISTÓRICO DE VERSÕES

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.0 | 2026-01-10 | Versão inicial: regras de rastreabilidade Kanban |

---

**Governado por:** `/METODO/PILAR_ENDFIRST.md`  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)
