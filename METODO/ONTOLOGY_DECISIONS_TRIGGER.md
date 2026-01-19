---
document_id: ONTOLOGY_DECISIONS_TRIGGER
type: operational
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-08
governed_by: /METODO/ONTOLOGY_DECISIONS.md
---

# Ontology Decisions Trigger

**Versão:** 1.0  
**Data:** 8 de Janeiro de 2026  
**Tipo:** Operacional (Processo)  
**Status:** Aprovado pelo CEO

---

## 🎯 OBJETIVO

Este documento define **quando e como** criar novas entradas em ONTOLOGY_DECISIONS.md.

**Função:**
> Impedir que ONTOLOGY_DECISIONS.md seja populado por ansiedade, teoria ou "boas práticas".

**Princípio:**
> Popular por cicatriz, não por prevenção.

---

## 📜 REGRA-MÃE (CRITÉRIO ZERO)

**Só entra no ONTOLOGY_DECISIONS.md aquilo que, se esquecido, faria o sistema voltar a errar.**

Se não cumprir isso → NÃO entra.

---

## ✅ GATILHO FORMAL (QUANDO CRIAR ENTRADA)

Uma nova entrada em ONTOLOGY_DECISIONS.md **só pode ser criada** quando **TODOS** os 5 critérios abaixo forem cumpridos:

---

### 1️⃣ Houve confusão real (não teórica)

**Pergunta de validação:**
> "Algo foi mal interpretado, feito 'quase certo', exigiu correção ou poderia voltar a acontecer?"

**Evidências válidas:**
- Commit de correção foi necessário
- Discussão sobre "o que isso significa"
- Decisão que gerou dúvida
- Interpretação ambígua que causou erro

**Exemplos válidos:**
- "PR ≠ aprovação" (confusão real: commit em master ≠ aprovado)
- "Checklist ≠ burocracia" (confusão real: checklist foi visto como obstáculo)
- "TBD é proibido" (confusão real: TBD apareceu 2x, exigiu correção 2x)

**❌ Não entra:**
- Conceitos óbvios
- Definições acadêmicas
- Termos que ninguém confundiu

---

### 2️⃣ A confusão gerou risco sistêmico

**Pergunta de validação:**
> "Se isso não for explicitado, o sistema pode quebrar de novo?"

**Se a resposta for NÃO → não entra.**

**Exemplos de risco real:**
- Aprovação sem rastro (quebra rastreabilidade)
- TBD persistente (quebra auditoria)
- README prometendo futuro (quebra confiança)
- Contagem fantasma (quebra estatísticas)

**❌ Não entra:**
- Erros localizados (afetam 1 arquivo)
- Preferências estéticas
- Convenções de nomenclatura

---

### 3️⃣ A decisão não é local, é transversal

**Pergunta de validação:**
> "Ela afeta mais de um documento, processo ou tipo de ator?"

**Tipos de ator:**
- CEO
- Manus (Agent)
- Cursor (AI)
- Contribuidor externo

**Exemplos transversais:**
- "PR ≠ aprovação" (afeta: commits, APPROVAL_LOG, README, processo)
- "Governança não depende de autoridade" (afeta: CEO, Manus, checklist, validação)

**❌ Não entra:**
- Decisão só de um arquivo
- Convenção estética
- Preferência pessoal

---

### 4️⃣ A decisão cria fronteira semântica clara

**Formato obrigatório:**
> "X NÃO é Y"

**Toda entrada precisa responder claramente:**
- O que X é
- O que Y é
- Por que confundir X com Y quebra o sistema

**Exemplos reais:**
- PR não é aprovação
- Governança não é Git
- Ontologia não é documentação
- Checklist não é burocracia
- Commit não é decisão

**❌ Não entra:**
- Explicações sem oposição clara
- Definições positivas ("X é...")
- Descrições genéricas

**Motivo:** Se não houver oposição clara → não é ontologia, é explicação.

---

### 5️⃣ A decisão já está em uso (validada)

**Pergunta de validação:**
> "O sistema já opera com essa distinção correta?"

**Evidências válidas:**
- Conceito já apareceu em commits
- Já orientou decisões
- Já evitou erro
- Já foi usado em correção

**Importante:**
> ONTOLOGY_DECISIONS.md não cria conceitos novos. Ele cristaliza conceitos que já estão sendo usados corretamente.

**Você só escreve depois que:**
- O conceito já foi aplicado
- A distinção já foi feita
- O erro já foi evitado

**❌ Não entra:**
- Conceitos ainda não testados
- Ontologia "preventiva"
- Teoria sem validação prática

---

## 📋 FORMATO CANÔNICO DE UMA ENTRADA

Cada entrada deve ter **sempre** este formato:

```markdown
## OD-00X — <Decisão Ontológica>

### Confusão observada
(O que estava sendo confundido)

### Decisão ontológica
(A fronteira clara: X ≠ Y)

### Impacto sistêmico
(O que muda em governança, processo ou decisão)

### Evidência concreta
(Commits, incidentes, correções, decisões reais)

### Status
ADOTADA | OBRIGATÓRIA | IRREVERSÍVEL
```

**Se não conseguir preencher todas as seções → não entra.**

---

## 🚫 O QUE NUNCA DEVE ENTRAR

- ❌ Glossário de termos
- ❌ Definições de livro
- ❌ Repetição do README
- ❌ Repetição do PILAR
- ❌ "Boas práticas"
- ❌ Conceitos ainda não testados
- ❌ Ontologia "preventiva"
- ❌ Documentação para parecer madura

**Regra de ouro:**
> Se virar "bonito de ler", está errado.

---

## 🔄 PROCESSO DE CRIAÇÃO DE ENTRADA

### Passo 1: Identificar gatilho
**Quando:** Após commit de correção, discussão sobre significado, ou erro evitado.

**Pergunta:** "Isso poderia voltar a acontecer se não for explicitado?"

---

### Passo 2: Validar 5 critérios
**Checklist:**
- [ ] Houve confusão real?
- [ ] Gerou risco sistêmico?
- [ ] É transversal (não local)?
- [ ] Cria fronteira clara (X ≠ Y)?
- [ ] Já está em uso?

**Se TODOS os 5 critérios forem SIM → seguir para Passo 3.**

**Se algum critério for NÃO → NÃO criar entrada.**

---

### Passo 3: Preencher formato canônico
**Seções obrigatórias:**
1. Confusão observada
2. Decisão ontológica (X ≠ Y)
3. Impacto sistêmico
4. Evidência concreta (commits, links)
5. Status (ADOTADA/OBRIGATÓRIA/IRREVERSÍVEL)

**Se não conseguir preencher todas → NÃO criar entrada.**

---

### Passo 4: Propor ao CEO
**Formato:**
> "Proposta de entrada OD-00X: [Título]  
> Critérios validados: ✅ 5/5  
> Evidência: [commits/links]  
> Aprovação necessária?"

**CEO decide:**
- ✅ Aprovar → Criar entrada
- ❌ Rejeitar → Não criar entrada
- ⏸️ Aguardar → Esperar mais evidências

---

### Passo 5: Criar entrada
**Ação:**
1. Adicionar entrada em ONTOLOGY_DECISIONS.md
2. Atualizar APPROVAL_LOG.md
3. Fazer commit com mensagem estruturada
4. Registrar no histórico de mudanças

---

## 📊 MÉTRICAS DE SAÚDE

### Poucas entradas = Sistema forte
**Indicador:** < 10 entradas em 1 ano

**Significado:** Sistema tem poucos pontos de confusão estrutural.

---

### Muitas entradas = Design fraco
**Indicador:** > 20 entradas em 1 ano

**Significado:** Sistema tem muitos pontos de ambiguidade. Revisar design.

---

### Entrada por cicatriz
**Indicador:** Cada entrada tem commit de correção associado

**Significado:** Entradas são baseadas em aprendizado real, não teoria.

---

## 🧠 EXEMPLOS DE APLICAÇÃO

### Exemplo 1: TBD é proibido

**1️⃣ Confusão real?** ✅ SIM
- TBD apareceu em commits 2d47fab e 9793be8
- Exigiu correção em commits 5c294f0 e 10233c6

**2️⃣ Risco sistêmico?** ✅ SIM
- TBD quebra rastreabilidade
- Se não for explicitado, pode voltar a acontecer

**3️⃣ Transversal?** ✅ SIM
- Afeta: APPROVAL_LOG, commits, validação, auditoria

**4️⃣ Fronteira clara?** ✅ SIM
- "TBD NÃO é hash válido"
- "Aprovação sem hash NÃO existe"

**5️⃣ Já está em uso?** ✅ SIM
- APPROVAL_LOG_RULES.md Regra 1
- COMMIT_GOVERNANCE_CHECKLIST item 3
- 2 correções aplicadas

**Decisão:** ✅ CRIAR ENTRADA (todos os critérios cumpridos)

---

### Exemplo 2: Nomenclatura de branches

**1️⃣ Confusão real?** ❌ NÃO
- Ninguém confundiu
- Não houve erro

**2️⃣ Risco sistêmico?** ❌ NÃO
- Nomenclatura é convenção, não governa decisões

**3️⃣ Transversal?** ❌ NÃO
- Afeta apenas Git, não governança

**4️⃣ Fronteira clara?** ❌ NÃO
- Não há oposição semântica

**5️⃣ Já está em uso?** ❌ NÃO
- Não foi testado

**Decisão:** ❌ NÃO CRIAR ENTRADA (nenhum critério cumprido)

---

## 🔒 REGRA DE ENFORCEMENT

**Quem pode criar entradas:**
- CEO (decisão soberana)
- Manus (Agent) — com aprovação do CEO
- Cursor — com aprovação do CEO
- Contribuidor — com aprovação do CEO

**Quem NÃO pode criar entradas:**
- Ninguém sem aprovação do CEO

**Motivo:** Ontologia é decisão estrutural, não contribuição aberta.

---

## 📚 DOCUMENTOS RELACIONADOS

- **ONTOLOGY_DECISIONS.md** — Registro de decisões ontológicas (governado por este documento)
- **COMMIT_GOVERNANCE_CHECKLIST.md** — Checklist de conformidade
- **APPROVAL_LOG_RULES.md** — Regras anti-TBD
- **PILAR_ENDFIRST.md** — Meta-pilar soberano

---

## 🎯 DIRETRIZ FINAL DO CEO

**Citação oficial:**
> "Não vamos popular o ONTOLOGY_DECISIONS.md por ansiedade. Vamos popular por cicatriz. Cada entrada será rara, curta e irreversível. Poucas entradas = sistema forte. Muitas entradas = design fraco."

**Implicação:**
- Não criar entradas "preventivas"
- Não criar entradas "bonitas"
- Não criar entradas por completude
- **Criar apenas quando o sistema exigir**

---

## 📋 CHECKLIST DE VALIDAÇÃO

Antes de criar uma entrada, responder:

- [ ] Houve confusão real (não teórica)?
- [ ] A confusão gerou risco sistêmico?
- [ ] A decisão é transversal (não local)?
- [ ] A decisão cria fronteira clara (X ≠ Y)?
- [ ] A decisão já está em uso?
- [ ] Consegui preencher todas as seções do formato canônico?
- [ ] CEO aprovou a criação?

**Se TODOS os itens forem SIM → criar entrada.**

**Se algum item for NÃO → NÃO criar entrada.**

---

**Versão:** 1.0  
**Criado:** 8 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Status:** Operacional (Tipo B)
