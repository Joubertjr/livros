---
document_id: TEMPLATE_DEMANDA_CANONICA
type: canonical
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-19
governed_by: /METODO/END_FIRST_V2.md
version: 1.0
created_at: 2026-01-19
---

# TEMPLATE CANÔNICO DE DEMANDA — END-FIRST v2

**Versão:** 1.0  
**Data:** 19 de Janeiro de 2026  
**Status:** Canônico (Obrigatório)  
**Autoria:** CEO (Joubert Jr) + Manus AI  
**Path Canônico:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`

---

## 🎯 O QUE É O TEMPLATE CANÔNICO

O **Template Canônico de Demanda** é a estrutura obrigatória que toda demanda deve seguir no método END-FIRST v2.

**Princípio fundamental:**
> "Se uma demanda precisa ser explicada, ela está errada. Se precisa ser revisada várias vezes, o método falhou."

---

## 🔒 REGRA ABSOLUTA

**Toda demanda DEVE seguir este template.**

**Demandas fora do template são FAIL estrutural.**

---

## 📋 ESTRUTURA OBRIGATÓRIA (11 SEÇÕES)

Toda demanda DEVE conter, nesta ordem:

1. **Cabeçalho canônico**
2. **🔒 END (Resultado Observável)**
3. **🚫 Regras Canônicas** (quando aplicável)
4. **✅ Critérios de Aceitação** (PASS / FAIL binários)
5. **🧠 Problemas Observados** (contexto, não tarefas)
6. **🚫 DO / DON'T**
7. **🧱 Bloqueios Estruturais**
8. **📋 TODO Canônico**
9. **❌ Fora de Escopo**
10. **📌 Status**
11. **🧭 Regra Final** (frase canônica de fechamento)

---

## 📝 TEMPLATE COMPLETO

```markdown
---
demanda_id: DEMANDA-XXX
title: [Título da Demanda]
type: [Bug / UX / Produto / Método]
altera_funcionalidade: [sim / não]
exige_f1: [sim / não]
status: [backlog / doing / done]
created_at: YYYY-MM-DD
created_by: [Nome]
executor: [Cursor / Manus / Outro]
---

# DEMANDA-XXX — [TÍTULO DA DEMANDA]

**Tipo:** [Bug / UX / Produto / Método]  
**Altera Funcionalidade:** [Sim / Não]  
**Exige F-1:** [Sim / Não]  
**Status:** [BACKLOG / DOING / DONE]

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado

Após a conclusão desta demanda:

- ✅ [Resultado observável 1]
- ✅ [Resultado observável 2]
- ✅ [Resultado observável 3]

**Resultado esperado do sistema:**

> [Frase única que resume o END]

---

## 🚫 Regras Canônicas

**[Tipo da Demanda]:**

> [Frase canônica explícita que governa esta demanda]

**Exemplos por tipo:**

- **Planejamento:**  
  > "Planejamento é artefato de primeira classe. Executor apenas executa."

- **UX:**  
  > "UX deve comunicar atividade contínua perceptível durante etapas longas, mesmo quando o percentual não muda."

- **Legibilidade:**  
  > "Se o usuário não vê o conteúdo imediatamente, o produto falhou."

- **Governança:**  
  > "Ausência de critério binário é FAIL estrutural."

- **Scroll (GLOBAL):**  
  > "Scroll interno é PROIBIDO. Conteúdo invisível ou cortado é BUG estrutural."

---

## ✅ Critérios de Aceitação (Binários)

### PASS

- ✅ [Critério binário 1]
- ✅ [Critério binário 2]
- ✅ [Critério binário 3]

### FAIL

- ❌ [Condição de falha 1]
- ❌ [Condição de falha 2]
- ❌ [Condição de falha 3]

---

## 🧠 Problemas Observados

**Contexto (não tarefas):**

[Descrever o problema observado empiricamente, não soluções]

**Causa raiz identificada:**

> [Frase única que resume a causa raiz]

---

## 🚫 DO / DON'T

### DO (fazer)

- ✅ [Ação permitida 1]
- ✅ [Ação permitida 2]

### DON'T (não fazer)

- ❌ [Ação proibida 1]
- ❌ [Ação proibida 2]

---

## 🧱 Bloqueios Estruturais

- 🔒 [Bloqueio 1: condição que impede execução]
- 🔒 [Bloqueio 2: condição que impede execução]
- 🔒 [Bloqueio 3: condição que impede execução]

---

## 📋 TODO Canônico

- [ ] [Etapa 1: descrição objetiva]
- [ ] [Etapa 2: descrição objetiva]
- [ ] [Etapa 3: descrição objetiva]

---

## ❌ Fora de Escopo

**Esta demanda NÃO inclui:**

- ❌ [Item fora de escopo 1]
- ❌ [Item fora de escopo 2]

---

## 📌 Status

**[BACKLOG / DOING / DONE]**

[Descrição do status atual]

---

## 🧭 Regra Final (Canônica)

> [Frase canônica de fechamento que resume o princípio da demanda]

---

**Governado por:** [Path do documento que governa]  
**Path Canônico:** [Path desta demanda]  
**Refs:** #[número da issue]
```

---

## 🔍 DETALHAMENTO DAS SEÇÕES

### 1. Cabeçalho Canônico (YAML Frontmatter)

**Obrigatório:**
- `demanda_id`: Identificador único (ex: DEMANDA-001)
- `title`: Título descritivo
- `type`: Bug / UX / Produto / Método
- `altera_funcionalidade`: sim / não
- `exige_f1`: sim / não
- `status`: backlog / doing / done
- `created_at`: Data de criação (YYYY-MM-DD)
- `created_by`: Nome do criador
- `executor`: Cursor / Manus / Outro

**Regra:**
> "Dúvida entre bug e UX é FAIL de planejamento."

---

### 2. 🔒 END (Resultado Observável)

**O que é:**
- Estado final esperado após conclusão da demanda
- Lista de resultados observáveis (não tarefas)
- Frase única que resume o END

**Obrigatório:**
- Pelo menos 3 resultados observáveis
- Frase de resumo do END

**Exemplo:**
```markdown
## 🔒 END (Resultado Observável)

Após a conclusão desta demanda:

- ✅ Usuário vê progresso perceptível durante etapas longas
- ✅ Percentual de progresso atualiza a cada 100ms
- ✅ Nenhum componente esconde conteúdo com scroll interno

**Resultado esperado do sistema:**

> UX comunica atividade contínua perceptível, eliminando percepção de travamento.
```

---

### 3. 🚫 Regras Canônicas

**O que é:**
- Frases canônicas explícitas que governam a demanda
- Princípios fundamentais que não podem ser violados

**Obrigatório:**
- Pelo menos uma frase canônica explícita
- Frase deve ser específica ao tipo da demanda

**Exemplos por tipo:**

| Tipo | Frase Canônica |
|------|----------------|
| Planejamento | "Planejamento é artefato de primeira classe. Executor apenas executa." |
| UX | "UX deve comunicar atividade contínua perceptível durante etapas longas, mesmo quando o percentual não muda." |
| Legibilidade | "Se o usuário não vê o conteúdo imediatamente, o produto falhou." |
| Governança | "Ausência de critério binário é FAIL estrutural." |
| Scroll (GLOBAL) | "Scroll interno é PROIBIDO. Conteúdo invisível ou cortado é BUG estrutural." |

---

### 4. ✅ Critérios de Aceitação (PASS / FAIL)

**O que é:**
- Critérios binários que determinam sucesso ou falha
- Não há espaço para interpretação

**Obrigatório:**
- Seção PASS com pelo menos 3 critérios
- Seção FAIL com pelo menos 3 condições

**Regra:**
> "Ausência de critério binário é FAIL estrutural."

**Exemplo:**
```markdown
## ✅ Critérios de Aceitação

### PASS

- ✅ Progresso atualiza a cada 100ms
- ✅ Nenhum scroll interno existe
- ✅ Conteúdo completo visível sem rolar

### FAIL

- ❌ Progresso congela por mais de 200ms
- ❌ Qualquer componente tem scroll interno
- ❌ Conteúdo cortado ou invisível
```

---

### 5. 🧠 Problemas Observados

**O que é:**
- Contexto empírico do problema
- Causa raiz identificada
- **NÃO é lista de tarefas**

**Obrigatório:**
- Descrição do problema observado
- Frase única que resume a causa raiz

**Exemplo:**
```markdown
## 🧠 Problemas Observados

Durante a execução do projeto CoverageSummarizer:

- Usuários reportaram "travamento" durante análise
- Progresso não atualizava por 30+ segundos
- Percepção de bug, mas sistema estava funcionando

**Causa raiz identificada:**

> UX não comunica atividade contínua durante etapas longas.
```

---

### 6. 🚫 DO / DON'T

**O que é:**
- Ações permitidas (DO)
- Ações proibidas (DON'T)

**Obrigatório:**
- Pelo menos 2 ações em cada seção

**Exemplo:**
```markdown
## 🚫 DO / DON'T

### DO (fazer)

- ✅ Atualizar progresso a cada 100ms
- ✅ Usar expansão vertical

### DON'T (não fazer)

- ❌ Usar scroll interno
- ❌ Esconder conteúdo
```

---

### 7. 🧱 Bloqueios Estruturais

**O que é:**
- Condições que impedem execução
- Bloqueios por design, não por disciplina

**Obrigatório:**
- Pelo menos 2 bloqueios

**Exemplo:**
```markdown
## 🧱 Bloqueios Estruturais

- 🔒 Cursor não executa sem F-1 aprovada
- 🔒 Nenhum componente pode ter scroll interno
- 🔒 Conteúdo invisível bloqueia PASS
```

---

### 8. 📋 TODO Canônico

**O que é:**
- Lista de etapas objetivas
- Ordem de execução

**Obrigatório:**
- Pelo menos 3 etapas
- Descrições objetivas (não ambíguas)

**Exemplo:**
```markdown
## 📋 TODO Canônico

- [ ] Adicionar timer de 100ms para atualização de progresso
- [ ] Remover scroll interno de todos os componentes
- [ ] Implementar expansão vertical automática
```

---

### 9. ❌ Fora de Escopo

**O que é:**
- Itens explicitamente excluídos
- Evita scope creep

**Obrigatório:**
- Pelo menos 2 itens

**Exemplo:**
```markdown
## ❌ Fora de Escopo

- ❌ Redesign completo da UI
- ❌ Otimização de performance do backend
```

---

### 10. 📌 Status

**O que é:**
- Estado atual da demanda
- Descrição do status

**Valores permitidos:**
- BACKLOG: Não autoriza execução
- DOING: Execução autorizada
- DONE: Concluída

**Exemplo:**
```markdown
## 📌 Status

**DOING**

Execução autorizada pelo CEO.
```

---

### 11. 🧭 Regra Final (Canônica)

**O que é:**
- Frase canônica de fechamento
- Resume o princípio da demanda

**Obrigatório:**
- Uma frase canônica

**Exemplo:**
```markdown
## 🧭 Regra Final

> "Se o usuário não vê o conteúdo imediatamente, o produto falhou."
```

---

## 🚨 REGRAS GLOBAIS

### Regra de UX Canônica (GLOBAL)

> **Scroll interno é PROIBIDO.**

- Nenhum componente pode esconder conteúdo
- Todo bloco deve expandir verticalmente
- Conteúdo invisível ou cortado é BUG estrutural
- Isso vale para:
  - UX refinements
  - bugs
  - produto
  - evidências

**Esta regra é GLOBAL e se aplica a todas as demandas.**

---

### Classificação Estrutural

Toda demanda DEVE declarar explicitamente:

- **Tipo:** Bug / UX / Produto / Método
- **Altera Funcionalidade:** Sim / Não
- **Exige F-1:** Sim / Não

**Regra:**
> "Dúvida entre bug e UX é FAIL de planejamento."

---

## 🔒 BLOQUEIOS ESTRUTURAIS

- 🔒 Manus não aceita demandas fora do template
- 🔒 Cursor não executa demandas fora do template
- 🔒 CEO não revisa demandas que não sigam o template
- 🔒 Template é fonte única da verdade

---

## 📌 FRASE CANÔNICA

> **"Se uma demanda precisa ser explicada, ela está errada. Se precisa ser revisada várias vezes, o método falhou."**

---

## 📜 DECLARAÇÃO DO CEO

Reconheço este template como canônico e obrigatório para o método END-FIRST v2.

Template Canônico de Demanda passa a governar:
- Criação de todas as demandas futuras
- Validação de demandas por Manus/Cursor
- Bloqueio estrutural de demandas fora do template

**Status:** CANÔNICO  
**Aplicação:** Imediata para todas as demandas  
**Versão:** 1.0

---

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Path Canônico:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`  
**Refs:** #13
