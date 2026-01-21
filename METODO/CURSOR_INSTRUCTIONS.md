---
document_id: CURSOR_INSTRUCTIONS
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-10
governed_by: /METODO/PILAR_ENDFIRST.md
version: 1.5
created_at: 2026-01-10
---

# CURSOR INSTRUCTIONS — Instruções Operacionais para Cursor

**Versão:** 1.5  
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
| 1.3 | 2026-01-19 | Adicionado Gate Z12 — Checklist de Auditoria Canônica |
| 1.4 | 2026-01-19 | Adicionada automação de Z12-A e Z12-B (make z12) |
| 1.5 | 2026-01-19 | Adicionado Gate Z13 — UI/UX Sistêmica (elimina subjetividade de UI) |

---

**Governado por:** `/METODO/PILAR_ENDFIRST.md`  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)


---

## ✅ Gate Z12 — Checklist de Auditoria Canônica (Obrigatório)

**Ordem Canônica:** Z0 (Estrutura) → Z11 (END-USER SMOKE) PASS → **Z12 (Auditoria Canônica)** → **Z13 (UI/UX Sistêmica)** → DONE

O Gate Z12 valida coerência entre planejamento, execução e evidências (incluindo Z11). O Gate Z13 valida conformidade de UI/UX (quando aplicável).

### Automação Disponível

Para executar as validações automatizadas de Z12-A e Z12-B, use:

```bash
make z12
```

Este comando executa:
- `tools/z12_audit.sh` (Z12-A: Auditoria de Método)
- `tools/z12_docs_check.sh` (Z12-B: Auditoria de Documentação)

Se `make z12` retornar **PASS**, as validações automáticas estão OK. Z12-C (Coerência) ainda requer validação manual.

### Checklist Manual (Z12-C e revisão final)

Antes de declarar qualquer demanda como **DONE**, você **DEVE** executar este checklist de auditoria. Uma falha em qualquer um dos itens abaixo significa que o **Gate Z12 falhou (FAIL)**, e a declaração de DONE está **proibida**. A demanda deve ser corrigida e este checklist deve ser re-executado até que todos os itens passem (PASS).

### Z12-A — Auditoria de Método (Estrutural)

- [ ] **Template Canônico:** A demanda segue rigorosamente a estrutura de 11 seções do Template Canônico?
- [ ] **Aprovação F-1:** Existe um artefato de aprovação F-1 claro e datado que precede o início da execução?
- [ ] **Respeito ao Escopo:** Nenhum arquivo foi criado, modificado ou excluído fora das diretrizes explícitas de `DO` e `DON'T` da demanda?
- [ ] **Violação de Frases Canônicas:** Nenhuma das frases canônicas do método foi violada durante a execução ou na documentação gerada?

### Z12-B — Auditoria de Documentação (Qualidade)

- [ ] **Markdown Válido:** Todos os arquivos `.md` gerados ou modificados são sintaticamente válidos e renderizam corretamente, sem artefatos de lixo técnico (ex: números de linha, marcadores de conflito)?
- [ ] **Checklists Renderizáveis:** Todos os checklists usam a sintaxe correta (`- [ ]` ou `- [x]`) e são funcionais?
- [ ] **Existência de Evidências:** Todas as declarações de conclusão ou resultado são suportadas por evidências (arquivos, logs, screenshots) que estão devidamente referenciadas no corpo do texto?
- [ ] **Sem Vazamento de Artefatos:** Nenhum artefato técnico (ex: snippets de código de depuração, logs internos) vazou para documentos destinados ao usuário final ou à gestão?

### Z12-C — Auditoria de Coerência (Lógica)

- [ ] **Execução vs. Planejamento:** Todas as ações executadas (commits, criação de arquivos, etc.) correspondem diretamente a um item que foi definido no planejamento (F-1)?
- [ ] **Planejamento vs. Execução:** Todos os itens definidos no planejamento foram de fato executados e concluídos?
- [ ] **DONE vs. PROOF:** Cada item declarado como "concluído" ou "entregue" possui uma prova (PROOF) clara e irrefutável de sua conclusão?

---

**Regra Final:** Somente após a verificação positiva de **TODOS** os itens acima (incluindo Z11 PASS e Z13 PASS se aplicável), você pode declarar a demanda como **DONE**.

---

## 🎨 Gate Z13 — Checklist de UI/UX Sistêmica (Obrigatório para demandas com UI)

**Ordem Canônica:** Z0 (Estrutura) → Z11 (END-USER SMOKE) PASS → Z12 (Auditoria Canônica) PASS → **Z13 (UI/UX Sistêmica)** → DONE

O Gate Z13 é um gate de validação binário que garante que a interface do usuário final (UI) adere a um padrão mínimo de consistência, legibilidade e previsibilidade. Sua função é eliminar a subjetividade da avaliação de UI e transformá-la em um checklist de conformidade técnica.

> **Frase Canônica:** "Z13 não decide se a UI é boa. Decide se ela é aceitável como produto de engenharia."

### Aplicabilidade

O Gate Z13 é **obrigatório** para toda demanda que envolva **UI/UX** (interface do usuário final). Se a demanda não envolve UI/UX, este gate pode ser pulado.

### 4 Regras Canônicas (Não Negociáveis)

- **R1:** Se tudo tem o mesmo peso visual, a UI falhou.
- **R2:** Conteúdo do usuário e metadados de auditoria não podem ocupar o mesmo plano visual.
- **R3:** Uma UI que exige explicação externa para ser usada é FAIL.
- **R4:** Inconsistência entre componentes idênticos é FAIL.

### Checklist de Conformidade (PASS/FAIL)

Antes de declarar qualquer demanda com UI como **DONE**, você **DEVE** executar este checklist. Uma falha em qualquer um dos itens abaixo significa que o **Gate Z13 falhou (FAIL)**, e a declaração de DONE está **proibida**.

#### Eixo 1: Hierarquia e Layout

- [ ] **H1: Hierarquia Tipográfica** — Existe uma distinção clara e consistente entre títulos (H1, H2, H3), parágrafos e legendas? (FAIL se fontes de níveis diferentes são indistinguíveis).
- [ ] **H2: Escala de Espaçamento** — Todos os espaçamentos (margens, paddings) entre elementos seguem uma escala de tokens predefinida (ex: 4, 8, 12, 16, 24, 32px)? (FAIL se espaçamentos são aleatórios ou "mágicos").
- [ ] **H3: Alinhamento** — Todos os elementos estão visivelmente alinhados em um grid? (FAIL se elementos parecem "flutuar" ou estão desalinhados sem propósito claro).

#### Eixo 2: Consistência de Componentes

- [ ] **C1: Consistência de Cor** — Todas as cores usadas (primária, secundária, erro, sucesso) vêm de uma paleta de tokens definida? (FAIL se cores são hard-coded e fora da paleta).
- [ ] **C2: Consistência de Borda** — Todos os elementos interativos (botões, cards, inputs) usam o mesmo valor de border-radius definido nos tokens? (FAIL se há múltiplos estilos de arredondamento).
- [ ] **C3: Consistência de Sombra** — Todas as sombras aplicadas (em cards, modais) seguem os tokens de sombra predefinidos? (FAIL se há sombras customizadas).

#### Eixo 3: Interação e Feedback

- [ ] **I1: Feedback de Hover** — Todos os elementos clicáveis (botões, links, cards interativos) possuem um estado de hover visualmente distinto? (FAIL se um elemento clicável não reage ao passar do mouse).
- [ ] **I2: Estado de Foco Visível** — É possível navegar pela interface usando o teclado (Tab) e ver claramente qual elemento está em foco? (FAIL se o foco do teclado é invisível).
- [ ] **I3: Sem Conteúdo de Debug** — A interface final visível para o usuário não contém nenhum texto, borda ou cor que foi usado apenas para fins de debug? (FAIL se console.log visual, `border: 1px solid red` etc. estão visíveis).

### PROOF (Prova Objetiva de Conformidade)

A prova de que o Gate Z13 foi executado e obteve PASS é composta por:

1. **Checklist Preenchido:** Uma cópia deste checklist com cada item marcado como PASS.
2. **Evidência Visual (Screenshot):** Um screenshot da tela ou componente final, como prova visual da conformidade.

**Exemplo de PROOF:**

```markdown
## ✅ Gate Z13: PASS

**Evidência:**
- Checklist de Conformidade Z13: [link para o checklist preenchido]
- Screenshot da UI Final: ![UI Final](link_para_screenshot.png)
```

**Documentação completa:** `/METODO/GATE_Z13_UI_UX_SISTEMICA.md`

---

**Regra Final:** Somente após a verificação positiva de **TODOS** os itens acima (Z11 PASS, Z12 PASS, Z13 PASS se aplicável), você pode declarar a demanda como **DONE**.

---
