---
document_id: ONTOLOGY_DECISIONS
type: canonical
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-08
governed_by: /METODO/PILAR_ENDFIRST.md
---

# Ontology Decisions

**Versão:** 2.1  
**Data:** 19 de Janeiro de 2026  
**Tipo:** Canônico (Ontologia Operacional)  
**Status:** Aprovado pelo CEO

**Histórico de versões:**
- v1.0 (2026-01-08): Versão inicial com estrutura base
- v1.1 (2026-01-08): OD-004 adicionada (DEMANDA ≠ PROJETO ≠ PRODUTO)
- v1.2 (2026-01-08): OD-005 adicionada (Toda Demanda pertence a um Produto) + OD-004 revisada
- v1.3 (2026-01-08): OD-006 adicionada (Execução é responsabilidade da Tecnologia - Cursor)
- v1.4 (2026-01-08): OD-007 adicionada (END é pré-condição absoluta)
- v1.5 (2026-01-08): OD-008 adicionada (Demandas para Manus também são demandas formais)
- v1.6 (2026-01-08): OD-009 adicionada (Disciplina Humana é Sinal de Falha de Design)
- v1.7 (2026-01-08): OD-010 adicionada (RESULTADO é entidade de primeira classe - backlog é derivado)
- v1.8 (2026-01-08): OD-011 adicionada (Entendimento sem mudança comportamental é fuga)
- v1.9 (2026-01-10): OD-011 estendida (Metacognição no caminho crítico)
- v2.0 (2026-01-19): OD-012 adicionada (Planejamento é artefato de primeira classe - END-FIRST v2)
- v2.1 (2026-01-19): OD-013 adicionada (Template de Demanda é Obrigatório)

---

## 🎯 OBJETIVO

Este documento consolida **decisões ontológicas** do ENDFIRST Ecosystem em **frases normativas** e **verdades operacionais**.

**Função:**
> Congelar aprendizado, não inovação.

**Princípio:**
> Nada de teoria. Nada de formalismo. Apenas regras já vividas.

---

## 📜 VERDADES ESTRUTURAIS

### 1. Sobre Aprovação

**"PR não é mecanismo de aprovação."**

PR (Pull Request) é mecanismo técnico de revisão de código. Aprovação é decisão governada registrada em APPROVAL_LOG.md. Os dois não são a mesma coisa.

**Consequência:** Commit pode estar em master e ainda não estar aprovado formalmente. Aprovação exige registro explícito no log.

---

**"Aprovação sem hash não existe."**

Toda aprovação deve referenciar um commit Git válido. Não existe aprovação "no ar" ou "prometida para depois".

**Consequência:** `commit: TBD` é proibido. Aprovação só pode apontar para commits existentes.

---

**"Documento aprovado sem log é inexistente."**

Se um documento não está registrado em APPROVAL_LOG.md, ele não está oficialmente aprovado, independente de quem disse que está.

**Consequência:** APPROVAL_LOG.md é fonte única de verdade para aprovações.

---

### 2. Sobre Commits

**"Checklist existe para impedir estados inválidos."**

COMMIT_GOVERNANCE_CHECKLIST.md não é burocracia. É proteção estrutural contra commits "quase conformes" que passam tecnicamente mas quebram governança.

**Consequência:** Se checklist não fecha, commit não pode ser considerado aprovado.

---

**"Commit aprovado sem log não existe."**

Análogo a "documento aprovado sem log". Se APPROVAL_LOG.md não foi atualizado no commit, a aprovação não aconteceu.

**Consequência:** Aprovação e mudança devem ser atômicas (mesmo commit).

---

**"TBD é proibido."**

`commit: TBD` significa "rastreabilidade quebrada". Não é permitido em nenhuma circunstância.

**Consequência:** Toda entrada no APPROVAL_LOG deve ter hash real desde o início.

---

### 3. Sobre Documentos

**"Documento sem YAML frontmatter não é governado."**

Metadados obrigatórios (document_id, type, status, approved_by, approved_at, governed_by) são a interface de governança. Sem eles, o documento não entra no sistema.

**Consequência:** Documentos sem YAML são tratados como rascunhos ou não governados.

---

**"Documento Tipo A governa outros documentos."**

Documentos canônicos (Tipo A) são soberanos. Outros documentos devem referenciar explicitamente qual canônico os governa.

**Consequência:** Hierarquia de governança é explícita, não implícita.

---

**"README é documento vivo, não promessa implícita."**

README deve separar "Estado Atual" (o que existe) de "Visão Futura" (o que ainda não existe). Não pode narrar futuro sem contrato explícito.

**Consequência:** README não mente sobre o estado do sistema.

---

### 4. Sobre Governança

**"Governança não depende de autoridade."**

Sistema de governança deve funcionar por regras verificáveis, não por quem tem autoridade para decidir.

**Consequência:** CEO pode ser bloqueado por checklist se commit não estiver conforme.

---

**"Governança não depende de memória."**

Decisões devem estar registradas em documentos, não na cabeça das pessoas.

**Consequência:** Se não está documentado, não aconteceu.

---

**"Governança não depende de boa vontade."**

Sistema deve impedir erros por design, não confiar que pessoas vão lembrar de fazer certo.

**Consequência:** Checklists, regras e validações automáticas são obrigatórios.

---

### 5. Sobre Ontologia

**"Ontologia operacional é executável, não declarativa."**

Ontologia não é um glossário bonito. É um conjunto de regras que impedem estados inválidos.

**Consequência:** Documentos como COMMIT_GOVERNANCE_CHECKLIST.md e APPROVAL_LOG_RULES.md são ontologia, mesmo sem se chamar "ontology".

---

**"Cada novo documento cria semântica."**

Todo documento governado adiciona significado ao sistema. Decisões novas devem ser ancoradas conscientemente.

**Consequência:** Crescimento de documentos deve ser intencional, não acidental.

---

**"Ontologia congela aprendizado, não inovação."**

Este documento (ONTOLOGY_DECISIONS.md) registra regras já vividas, não teorias futuras.

**Consequência:** Só entra aqui o que já foi testado e validado na prática.

---

## 🧠 DECISÕES ONTOLÓGICAS FORMAIS

### OD-004 — DEMANDA ≠ PROJETO ≠ PRODUTO

**ID:** OD-004  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-08

---

#### 🧠 DECISÃO

**Toda demanda DEVE estar vinculada a um produto.**  
**Nem toda demanda precisa estar vinculada a um projeto.**

No método ENDFIRST:
- **DEMANDA** é a unidade mínima soberana de resultado verificável
- **PRODUTO** é o eixo contínuo de valor, ownership e evolução (obrigatório)
- **PROJETO** é um contêiner temporário para acelerar mudanças em um produto (opcional)

Produto é obrigatório. Projeto é opcional.

---

#### 🎯 REGRA FORMAL

Toda demanda deve estar vinculada a:
1. **PRODUTO** (obrigatório) — eixo permanente de governança
2. **INTENÇÃO / RESULTADO** claro (obrigatório)
3. **PROJETO** (opcional) — contêiner temporário

Produto é obrigatório. Projeto é opcional.

Projetos:
- só são criados quando a realidade exige
- nunca por antecipação
- nunca como requisito burocrático

---

#### 🔍 DEFINIÇÕES OPERACIONAIS

**DEMANDA**
- Unidade mínima de trabalho governada por resultado
- Pode existir isoladamente
- Vive até o resultado ser produzido ou descartado

**PROJETO**
- Agrupamento temporário de múltiplas demandas
- Criado quando há coordenação, dependência ou risco sistêmico
- Não é obrigatório

**PRODUTO**
- Eixo contínuo de valor, ownership e evolução
- Tem dono
- Existe antes, durante e depois de projetos
- É obrigatório para toda demanda
- Ex.: ENDFIRST, LLM Orchestrator, Governança ENDFIRST

---

#### ❌ O QUE ESTA DECISÃO PROÍBE

- ❌ Criar demandas sem produto associado (trabalho órfão)
- ❌ Criar projetos "vazios" só para justificar demandas
- ❌ Bloquear demandas por ausência de projeto
- ❌ Confundir projeto (meio) com produto (identidade)
- ❌ Planejamento abstrato antes de resultado verificável

---

#### ✅ O QUE ESTA DECISÃO GARANTE

- Clareza ontológica entre demanda, projeto e produto
- Produto como eixo permanente de governança
- Backlog sempre organizado por produto
- Ownership claro (produto define dono)
- Redução de burocracia precoce (projeto é opcional)
- Emergência natural de projetos
- Rastreabilidade limpa de produto → demanda → execução

---

#### 📌 EXEMPLO APLICADO

**DEMANDA-001 — LLM Orchestrator**
- É uma DEMANDA válida
- Pertence ao PRODUTO: "LLM Orchestrator"
- Não está em um PROJETO formal (fluxo contínuo)
- Produto já existe (mesmo que em v0)
- Projeto é opcional

---

#### 🧭 PRINCÍPIO

> Produto é o eixo permanente.  
> Demandas alteram produtos.  
> Projetos aceleram mudanças.  
> Produto é obrigatório. Projeto é opcional.

---

#### 📜 DECLARAÇÃO DO CEO

Reconheço esta decisão como canônica e obrigatória para o método ENDFIRST.

Esta decisão passa a governar:
- Criação de demandas
- Organização do backlog
- Leitura de DEMANDA-001 e futuras demandas

**Status:** CANÔNICA  
**Aplicação:** Imediata

---

### OD-005 — Toda Demanda pertence a um Produto

**ID:** OD-005  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-08

---

#### 🧠 DECISÃO

Toda DEMANDA deve estar vinculada a exatamente um PRODUTO.  
Uma DEMANDA pode ou não estar vinculada a um PROJETO.

---

#### 📝 RACIONAL

Produto é o eixo contínuo de valor, ownership e evolução.  
Projeto é um contêiner temporário para acelerar mudanças em um produto.  
Permitir demanda sem produto cria trabalho órfão, sem dono e sem direção estratégica.

---

#### 🔍 DEFINIÇÕES

**PRODUTO**
- É contínuo
- Tem dono
- Evolui no tempo
- Existe antes, durante e depois de projetos
- Ex.: ENDFIRST, LLM Orchestrator, Governança ENDFIRST

**PROJETO**
- É temporário
- Tem início e fim
- Serve para mudar o estado de um produto
- Pode conter várias demandas
- Pode não existir (produto em modo contínuo)

**DEMANDA**
- É a menor unidade governável de trabalho
- Sempre altera um produto
- Pode estar:
  - fora de projeto (fluxo contínuo), ou
  - dentro de um projeto (iniciativa estruturada)

---

#### ✅ IMPLICAÇÕES

- Não existe demanda sem produto
- Projeto é opcional
- Produto é obrigatório
- Backlog é sempre organizado por produto
- Projetos agrupam demandas, não definem identidade

---

#### 📌 EXEMPLOS

**Válidos:**
- DEMANDA-001 (LLM Orchestrator) → Produto: LLM Orchestrator → Projeto: opcional
- Ajuste de governança → Produto: ENDFIRST → Projeto: nenhum

**Inválidos (proibidos):**
- ❌ Demanda criada sem produto associado
- ❌ Demanda "solta" no backlog
- ❌ Trabalho sem dono

---

#### ❌ CONSEQUÊNCIAS PRÁTICAS

1. ❌ Não existe "demanda solta"
2. ❌ Não existe demanda sem produto
3. ✅ Existe demanda sem projeto
4. ✅ Projeto é um contêiner opcional
5. ✅ Produto é o eixo permanente de governança

**Isso resolve:**
- Confusão de backlog
- Confusão de ownership
- Confusão de prioridade
- Confusão entre execução e estratégia

---

#### 📜 DECLARAÇÃO DO CEO

> "Esta decisão não é opinião. É fundação ontológica do sistema. A partir de agora: qualquer demanda sem produto está errada por definição, projeto vira meio (não identidade), produto vira centro da governança."

**Status:** CANÔNICA  
**Aplicação:** Imediata

---

### OD-006 — Execução é sempre responsabilidade da Tecnologia (Cursor)

**ID:** OD-006  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-08

---

#### 🧠 DECISÃO

DEMANDA nunca é executada por quem escreve.  
DEMANDA nunca é executada pelo CEO.  
DEMANDA é sempre executada pelo executor designado.  
**No nosso sistema: Cursor.**

---

#### 📝 RACIONAL

O sistema autorizava a execução, mas não declarava explicitamente o executor canônico.  
Contrato de execução estava implícito, gerando ambiguidade sobre "quem executa".  
Implícito = fonte de dúvida.  
Explícito = elimina ambiguidade por design.

---

#### 🔍 DEFINIÇÕES

**EXECUTOR (Cursor)**
- Lê demandas do Git
- Implementa especificações
- Não decide
- Não autoriza
- Não especifica

**ESPECIFICADOR (Manus)**
- Escreve demandas
- Escreve specs
- Não executa
- Não autoriza

**AUTORIZADOR (CEO)**
- Autoriza execução
- Valida resultado
- Não executa
- Não especifica

---

#### ✅ IMPLICAÇÕES

- Toda DEMANDA DEVE ter campo `executor` no YAML
- Executor padrão: `cursor`
- Demanda sem executor → inválida
- Executor diferente de `cursor` → erro ontológico (por enquanto)
- Git é a fonte única de verdade
- Cursor lê do Git, não de mensagens

---

#### 📌 FLUXO CANÔNICO

1. CEO autoriza
2. Manus escreve/spec
3. Git é a fonte única
4. Cursor lê do Git
5. Cursor executa
6. Resultado volta para o Git

---

#### ❌ O QUE NÃO ACONTECE

- ❌ CEO não executa
- ❌ Manus não executa
- ❌ Cursor não decide
- ❌ Cursor não pergunta "quem executa?"
- ❌ Execução não depende de memória humana

---

#### 📜 FRASE CANÔNICA

> "Demandas são executadas por agentes de tecnologia, nunca por pessoas."

**Uso:**
- Onboarding
- Revisão
- Cultura
- Ontologia prática

---

#### 📜 DECLARAÇÃO DO CEO

> "O sistema está certo. A dúvida mostrou onde ele ainda estava silencioso. Vamos torná-lo explícito — e seguir."

**Status:** CANÔNICA  
**Aplicação:** Imediata

---

### OD-007 — END é pré-condição absoluta

**ID:** OD-007  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-08

---

#### 🧠 DECLARAÇÃO CANÔNICA

**END é pré-condição absoluta.**

**Nenhuma ação pode começar sem END documentado, versionado e aprovado no Git.**

---

#### 📝 RACIONAL

O sistema criou OD-006 (quem executa) e EXECUTION_MODEL.md (modelo de execução), mas o momento de entrada do executor ainda estava:
- Implícito
- Fora do método
- Dependente de "alguém explicar"

**Isso é um vazamento estrutural clássico.**

Se precisamos explicar como onboardar o Cursor, então o método ainda não está completo.

**Onboarding de Executor é parte do método, não um prompt ad-hoc.**

---

#### 🔍 DEFINIÇÕES

**END (Expected iN Document):**
- Documento que define **o que fazer** (DEMANDA)
- Documento que define **resultado esperado** (ENDFIRST_SPEC)
- Documento que define **critérios de sucesso** (ACCEPTANCE)
- Documento que define **como julgar** (FINAL_DECISION_TEMPLATE)
- Documento que define **como onboardar** (EXECUTOR_ONBOARDING_PROCESS)

**Pré-condição absoluta:**
- Nada começa sem END
- Nada é executado sem END
- Nada é julgado sem END
- END está no Git, não em mensagens
- END está versionado, não em memória
- END está aprovado, não em discussão

---

#### ⛔ PROIBIÇÕES EXPLÍCITAS

**❌ Começar pelo HOW**
- Proibido começar execução sem END documentado
- Proibido "fazer rápido" sem registrar END
- Proibido "testar" sem END aprovado

**❌ Onboarding sem END**
- Proibido onboardar executor sem END no Git
- Proibido explicar verbalmente o que fazer
- Proibido prompt improvisado fora do repositório

**❌ Prompt, setup ou execução sem END registrado**
- Proibido executar demanda sem DEMANDA-XXX.md
- Proibido executar sem ENDFIRST_SPEC.md
- Proibido executar sem DEMANDA-XXX_ACCEPTANCE.md
- Proibido onboardar sem EXECUTOR_ONBOARDING_PROCESS.md

---

#### 🚫 EXEMPLOS PROIBIDOS (REAIS)

**Exemplo 1: Onboarding do Cursor sem END no Git**
- **Problema:** Prompt de onboarding criado fora do Git
- **Violação:** END não estava documentado, versionado e aprovado
- **Correção:** Criar EXECUTOR_ONBOARDING_PROCESS.md no Git

**Exemplo 2: Explicação verbal fora do repositório**
- **Problema:** "Explica para o Cursor o que fazer"
- **Violação:** END estava em mensagens, não no Git
- **Correção:** Tudo no Git, nada em mensagens

**Exemplo 3: Execução iniciada por contexto humano**
- **Problema:** Executor pergunta "o que fazer?"
- **Violação:** END não estava acessível ao executor
- **Correção:** Executor lê do Git, não de pessoas

---

#### ✅ IMPLICAÇÕES

**Para CEO:**
- Não autorizar execução sem END aprovado
- Não explicar verbalmente o que fazer
- Não criar "atalhos" fora do Git

**Para Manus:**
- Não especificar fora do Git
- Não criar processos improvisados
- Não documentar em mensagens

**Para Cursor:**
- Não executar sem ler END do Git
- Não perguntar "o que fazer?"
- Não aceitar instruções verbais

---

#### 📝 EXEMPLOS VÁLIDOS

**Exemplo 1: Onboarding correto**
- EXECUTOR_ONBOARDING_PROCESS.md existe no Git
- Executor lê documento
- Executor sabe o que fazer sem perguntar

**Exemplo 2: Execução correta**
- DEMANDA-001.md existe no Git
- ENDFIRST_SPEC_EF-2026-001.md existe no Git
- DEMANDA-001_ACCEPTANCE.md existe no Git
- Cursor lê e executa

**Exemplo 3: Julgamento correto**
- FINAL_DECISION_TEMPLATE.md existe no Git
- CEO lê e decide
- Decisão é registrada no Git

---

#### 🎯 ANTI-EXEMPLOS (PROIBIDOS)

**Anti-exemplo 1:**
> "Vou explicar para o Cursor o que fazer."

**Por que é proibido:**
- END não está no Git
- Depende de explicação oral
- Não é repetível

---

**Anti-exemplo 2:**
> "Vou criar um prompt rápido para onboardar."

**Por que é proibido:**
- END não está versionado
- Prompt improvisado
- Não é auditável

---

**Anti-exemplo 3:**
> "Vou começar a executar e documentar depois."

**Por que é proibido:**
- END não existe antes da execução
- Viola pré-condição absoluta
- Não é governado

---

#### 📜 FRASE CANÔNICA (CULTURA)

> **"END primeiro. HOW depois. Sempre."**

**Uso:**
- Cultura organizacional
- Onboarding de time
- Revisão de processos
- Decisões diárias

**Implicação:**
- Nada começa sem END
- END está no Git
- END é pré-condição, não sugestão

---

#### 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/EXECUTION_MODEL.md` (Modelo de execução)
- `/METODO/EXECUTOR_ONBOARDING_PROCESS.md` (Processo de onboarding)
- `/METODO/FINAL_DECISION_TEMPLATE.md` (Como CEO julga)
- `/METODO/PILAR_ENDFIRST.md` (Meta-pilar)

---

#### 📜 DECLARAÇÃO DO CEO

> "Se precisamos explicar como onboardar o Cursor, então o método ainda não está completo. OD-007 fecha o último vazamento estrutural do sistema: END é pré-condição absoluta, não opção."

**Data:** 2026-01-08  
**Responsável:** CEO (Joubert Jr)

---

### OD-008 — Demandas para Manus também são demandas formais

**ID:** OD-008  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-08

---

#### 🧠 DECLARAÇÃO CANÔNICA

**Toda solicitação ao Manus DEVE existir como DEMANDA no Git, com END explícito, escopo definido e critério de encerramento.**

**Manus não executa ordens fora do repositório.**

---

#### 📝 RACIONAL

O sistema criou `/DEMANDAS/` para Cursor, mas não criou equivalente para Manus.

**Problema identificado:**
- Manus estava recebendo ordens em mensagens
- Sem rastreabilidade
- Sem versionamento
- Sem END formal

**Consequência:**
- Manus vira "cabeça pensante informal"
- Decisões viram conversa
- END vira interpretação
- Sistema apodrece com o tempo

**Solução:**
- Criar `/DEMANDAS_MANUS/` no repositório
- Criar `TEMPLATE_DEMANDA_MANUS.md`
- Exigir END explícito em toda demanda para Manus
- Manus só executa demandas no Git

---

#### 🔍 DEFINIÇÕES

**DEMANDA_MANUS:**
- Solicitação formal ao Manus (Agent)
- Documento no Git (`/DEMANDAS_MANUS/DEMANDA_MANUS-XXX.md`)
- END explícito obrigatório
- Escopo definido
- Critério de encerramento
- Versionado
- Aprovado pelo CEO

**Tipos de demandas para Manus:**
1. **Ontologia** — Criar decisões ontológicas (OD-XXX)
2. **Método** — Criar processos do método
3. **Governança** — Criar documentos de governança
4. **Produto** — Especificar produtos, criar specs ENDFIRST

**Diferença: DEMANDAS vs DEMANDAS_MANUS:**

| Aspecto | /DEMANDAS/ | /DEMANDAS_MANUS/ |
|---------|------------|------------------|
| **Executor** | Cursor (tecnologia) | Manus (agent) |
| **Tipo de trabalho** | Código, implementação | Ontologia, método, governança, produto |
| **Resultado** | Sistema funcional | Documento, decisão, processo |
| **Template** | TEMPLATE_DEMANDA.md | TEMPLATE_DEMANDA_MANUS.md |

**Princípio comum:**
> Ambos seguem ENDFIRST. Ambos estão no Git. Ambos têm END explícito.

---

#### ⛔ PROIBIÇÕES EXPLÍCITAS

**❌ Manus executar ordens em mensagens**
- Proibido executar ordens fora do Git
- Proibido executar ordens verbais
- Proibido executar ordens sem END

**❌ CEO mandar ordem sem criar DEMANDA_MANUS**
- Proibido mandar ordem em mensagem
- Proibido explicar verbalmente o que fazer
- Proibido criar "atalhos" fora do Git

**❌ Demanda sem END explícito**
- Proibido criar DEMANDA_MANUS sem END
- Proibido executar sem resultado esperado definido
- Proibido "fazer rápido" sem registrar END

---

#### 🚫 EXEMPLOS PROIBIDOS (REAIS)

**Exemplo 1: CEO manda ordem em mensagem**
- **Problema:** "Crie a OD-007"
- **Violação:** Ordem fora do Git, sem END formal
- **Correção:** Criar DEMANDA_MANUS-001_OD-007.md no Git

**Exemplo 2: Manus executa sem END**
- **Problema:** Manus começa a criar OD-007 sem saber resultado esperado
- **Violação:** Sem END explícito
- **Correção:** Exigir END na DEMANDA_MANUS-001

**Exemplo 3: Demanda sem versionamento**
- **Problema:** Ordem dada verbalmente, não registrada
- **Violação:** Não está no Git
- **Correção:** Commitar demanda antes de executar

---

#### ✅ IMPLICAÇÕES

**Para CEO:**
- Não mandar ordens em mensagens
- Criar DEMANDA_MANUS-XXX.md antes de pedir execução
- Definir END explícito em toda demanda
- Commitar demanda no Git

**Para Manus:**
- Não executar ordens fora do Git
- Ler demanda do Git (não de mensagens)
- Exigir END explícito
- Não começar sem END

**Para o sistema:**
- Rastreabilidade 100%
- Versionamento de decisões
- END formal para todo trabalho
- Governança consistente

---

#### 📝 EXEMPLOS VÁLIDOS

**Exemplo 1: Demanda para criar OD-007**
- DEMANDA_MANUS-001_OD-007_ENDFIRST_ABSOLUTO.md criada
- END explícito: "OD-007 criada, documentada e aprovada"
- Escopo definido
- Critério de encerramento claro
- Manus lê do Git e executa

**Exemplo 2: Demanda para criar processo**
- DEMANDA_MANUS-002_PROCESSO_XXX.md criada
- END explícito: "Processo XXX documentado e aprovado"
- Template usado: TEMPLATE_DEMANDA_MANUS.md
- Resultado no Git

**Exemplo 3: Demanda para especificar produto**
- DEMANDA_MANUS-003_SPEC_PRODUTO_YYY.md criada
- END explícito: "ENDFIRST_SPEC_EF-2026-003 criada e validada"
- Critérios de aceitação definidos
- CEO valida resultado

---

#### 🎯 ANTI-EXEMPLOS (PROIBIDOS)

**Anti-exemplo 1:**
> "Manus, crie a OD-007."

**Por que é proibido:**
- Ordem em mensagem
- Sem END formal
- Sem rastreabilidade

---

**Anti-exemplo 2:**
> "Vou explicar para o Manus o que fazer."

**Por que é proibido:**
- Explicação verbal
- Fora do Git
- Não é repetível

---

**Anti-exemplo 3:**
> "Manus, faça isso rápido sem documentar."

**Por que é proibido:**
- Sem END
- Sem versionamento
- Viola ENDFIRST

---

#### 📜 FRASE CANÔNICA (CULTURA)

> **"Se Cursor recebe demandas no Git, Manus TAMBÉM deve receber."**

**Uso:**
- Cultura organizacional
- Onboarding de time
- Revisão de processos
- Decisões diárias

**Implicação:**
- Manus não é "cabeça pensante informal"
- Manus é executor formal
- Manus recebe demandas no Git
- Manus segue ENDFIRST

---

#### 🔗 DOCUMENTOS RELACIONADOS

- `/DEMANDAS_MANUS/` (Diretório de demandas para Manus)
- `/DEMANDAS_MANUS/TEMPLATE_DEMANDA_MANUS.md` (Template oficial)
- `/DEMANDAS_MANUS/README.md` (Explicação do diretório)
- `/METODO/ONTOLOGY_DECISIONS.md` (OD-007: END é pré-condição absoluta)
- `/METODO/EXECUTION_MODEL.md` (Modelo de execução)
- `/METODO/PILAR_ENDFIRST.md` (Meta-pilar)

---

#### 📜 DECLARAÇÃO DO CEO

> "Se Cursor recebe demandas no Git, Manus TAMBÉM deve receber. Caso contrário, Manus vira 'cabeça pensante informal', decisões viram conversa, END vira interpretação, e o sistema apodrece com o tempo."

**Data:** 2026-01-08  
**Responsável:** CEO (Joubert Jr)

---

### OD-009 — Disciplina Humana é Sinal de Falha de Design

**ID:** OD-009  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-08  
**Categoria:** Princípio Transversal (aplica-se a TODO o sistema)

---

#### 🧠 DECLARAÇÃO CANÔNICA

**Qualquer processo que dependa de disciplina humana para evitar erro é ontologicamente inválido.**

**O método deve impedir o erro por design, não por atenção, cuidado ou boa intenção.**

---

#### 📝 RACIONAL

O problema nunca foi disciplina humana.

**Sempre que um sistema exige disciplina, ele está mal desenhado.**

O método ENDFIRST existe para eliminar a necessidade de disciplina por design.

**Princípio:**
> Se algo depende de disciplina humana para funcionar, está errado por definição.

**Implicação:**
- Disciplina é um sintoma de falha de design
- O método ENDFIRST existe para tornar o erro estruturalmente impossível
- Qualquer coisa que dependa de disciplina humana está proibida

---

#### ❌ O QUE ISSO ELIMINA

**Frases proibidas:**
- ❌ "Tem que lembrar de…"
- ❌ "É só tomar cuidado"
- ❌ "Normalmente a gente faz assim"
- ❌ "Confia que não vai errar"
- ❌ "As pessoas vão tomar cuidado"
- ❌ "Basta ter disciplina"
- ❌ "Precisa prestar atenção"

**Por que são proibidas:**
- Dependem de memória humana
- Dependem de boa intenção
- Dependem de atenção
- Não são estruturais
- Não escalam
- Não são auditáveis

---

#### ✅ O QUE ISSO EXIGE

**Soluções estruturais:**
- ✅ Campo obrigatório em template
- ✅ Regra explícita no processo
- ✅ Bloqueio estrutural
- ✅ Checklist que falha automaticamente
- ✅ Validação automática
- ✅ Sistema antifrágil (detecta e corrige)

**Princípio:**
> Se a única defesa do processo é "as pessoas vão tomar cuidado", o processo está errado.

---

#### 📝 EXEMPLOS REAIS (DO NOSSO SISTEMA)

**Exemplo 1: TBD aparecendo**
- **Problema:** TBD aparecia em APPROVAL_LOG.md
- **Causa raiz:** Dependia de "lembrar de atualizar"
- **Falha de design:** Sistema permitia TBD
- **Solução estrutural:** Sistema antifrágil detecta e corrige automaticamente

**Exemplo 2: Ordens fora do Git**
- **Problema:** Manus recebia ordens em mensagens
- **Causa raiz:** Dependia de "lembrar de criar DEMANDA"
- **Falha de design:** Sistema permitia ordens informais
- **Solução estrutural:** OD-008 (Manus só executa demandas no Git)

**Exemplo 3: Onboarding sem END**
- **Problema:** Onboarding do Cursor era prompt ad-hoc
- **Causa raiz:** Dependia de "lembrar de documentar"
- **Falha de design:** Sistema permitia onboarding fora do Git
- **Solução estrutural:** EXECUTOR_ONBOARDING_PROCESS.md + OD-007

**Exemplo 4: Commit sem validação**
- **Problema:** Push antes de CEO validar
- **Causa raiz:** Dependia de "lembrar de perguntar"
- **Falha de design:** Sistema não bloqueava push
- **Solução estrutural:** Processo explícito (commit → validar → push)

---

#### 🔍 FRONTEIRA SEMÂNTICA (X ≠ Y)

**Disciplina ≠ Processo**
- Disciplina: depende de memória humana
- Processo: estrutura que impede erro

**Atenção ≠ Governança**
- Atenção: esforço humano
- Governança: regra estrutural

**Boa intenção ≠ Sistema correto**
- Boa intenção: desejo de acertar
- Sistema correto: impossibilidade de errar

**Cuidado ≠ Design**
- Cuidado: comportamento humano
- Design: arquitetura que previne

---

#### ⛔ PROIBIÇÕES EXPLÍCITAS

**❌ Processo que depende de disciplina**
- Proibido criar processo que exige "lembrar"
- Proibido criar processo que exige "tomar cuidado"
- Proibido criar processo que exige "boa intenção"

**❌ Checklist sem validação automática**
- Proibido checklist que depende de "marcar manualmente"
- Proibido checklist que não falha automaticamente
- Proibido checklist que não é verificado pelo sistema

**❌ Template sem campo obrigatório**
- Proibido template que permite campo vazio
- Proibido template que depende de "lembrar de preencher"
- Proibido template sem validação estrutural

---

#### ✅ IMPLICAÇÕES

**Para CEO:**
- Não aceitar processo que depende de disciplina
- Rejeitar solução que exige "tomar cuidado"
- Exigir bloqueio estrutural

**Para Manus:**
- Não criar processo que depende de memória
- Não criar template sem validação
- Não criar checklist sem automação

**Para Cursor:**
- Não implementar solução que exige disciplina
- Não criar sistema que permite erro humano
- Não aceitar "basta ter cuidado" como defesa

**Para o sistema:**
- Erro humano = falha de design
- Disciplina = sintoma de problema
- Processo correto = erro impossível

---

#### 📝 EXEMPLOS VÁLIDOS

**Exemplo 1: Sistema antifrágil**
- TBD detectado automaticamente
- Sistema corrige sem intervenção humana
- Não depende de "lembrar"

**Exemplo 2: Campo obrigatório**
- Template exige END
- Sistema rejeita demanda sem END
- Não depende de "tomar cuidado"

**Exemplo 3: Processo explícito**
- Commit → validar → push
- Sistema bloqueia push sem validação
- Não depende de "boa intenção"

**Exemplo 4: OD-008**
- Manus só executa demandas no Git
- Sistema rejeita ordens em mensagens
- Não depende de "disciplina"

---

#### 🎯 ANTI-EXEMPLOS (PROIBIDOS)

**Anti-exemplo 1:**
> "Tem que lembrar de atualizar o APPROVAL_LOG."

**Por que é proibido:**
- Depende de memória humana
- Não é estrutural
- Falha de design

**Solução correta:**
- Sistema antifrágil detecta TBD
- Sistema corrige automaticamente

---

**Anti-exemplo 2:**
> "É só tomar cuidado para não fazer push antes de validar."

**Por que é proibido:**
- Depende de atenção
- Não é bloqueio estrutural
- Falha de design

**Solução correta:**
- Processo explícito: commit → validar → push
- Sistema exige validação antes de push

---

**Anti-exemplo 3:**
> "Normalmente a gente cria a DEMANDA antes de executar."

**Por que é proibido:**
- Depende de "normalmente"
- Não é regra estrutural
- Falha de design

**Solução correta:**
- OD-008: Manus só executa demandas no Git
- Sistema rejeita ordens fora do Git

---

#### 📜 FRASE CANÔNICA (CULTURA)

> **"Se algo depende de disciplina humana para funcionar, está errado por definição. Sistemas corretos impedem o erro por design."**

**Uso:**
- Cultura organizacional
- Onboarding de time
- Revisão de processos
- Decisões de design
- Corte de escopo

**Implicação:**
- Disciplina é sintoma de falha
- Processo correto não exige disciplina
- Sistema deve impedir erro, não confiar em atenção

---

#### 🚨 CRITÉRIO OBRIGATÓRIO DE REVISÃO

**Pergunta obrigatória em toda revisão:**

> **"Isso exige disciplina humana para não dar errado?"**

**Decisão:**
- Se SIM → ❌ REJEITADO
- Se NÃO → ✅ Pode seguir

**Nota obrigatória:**
> Se a única defesa do processo é "as pessoas vão tomar cuidado", o processo está errado.

**Aplica-se a:**
- Revisão de commits
- Revisão de demandas (Cursor e Manus)
- Revisão de processos
- Revisão de templates
- Revisão de governança

---

#### 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/COMMIT_GOVERNANCE_CHECKLIST.md` (Checklist de conformidade)
- `/METODO/ONTOLOGY_DECISIONS.md` (OD-004 a OD-008)
- `/METODO/PILAR_ENDFIRST.md` (Meta-pilar)
- `/README.md` (Frase canônica de cultura)

---

#### 📜 DECLARAÇÃO DO CEO

> "Disciplina é um sintoma de falha de design. O método ENDFIRST existe para tornar o erro estruturalmente impossível. A partir de agora, qualquer coisa que dependa de disciplina humana está proibida."

**Data:** 2026-01-08  
**Responsável:** CEO (Joubert Jr)

---

### OD-010 — RESULTADO é Entidade de Primeira Classe (Backlog é Derivado)

**ID:** OD-010  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-08  
**Categoria:** Princípio Transversal (aplica-se a TODO o sistema)

---

#### 🧠 DECLARAÇÃO CANÔNICA

**Nenhum backlog pode existir antes da definição formal do RESULTADO.**

**O sistema só pode ser organizado a partir do RESULTADO, nunca o contrário.**

**Frase canônica:**
> **"Backlog não cria resultado. Resultado cria backlog."**

---

#### 📝 RACIONAL

**O problema:**
Estamos tratando backlog como entidade primária.

**Mas no ENDFIRST, a hierarquia correta é:**

```
RESULTADO (END)
   ↓
CRITÉRIOS DE SUCESSO
   ↓
PROVAS OBSERVÁVEIS
   ↓
BACKLOG
   ↓
EXECUÇÃO
```

**Quando pulamos PROVAS OBSERVÁVEIS como entidade formal:**
- Backlog vira "plano"
- Execução vira "descoberta"
- Acompanhamento vira "interpretação"

**Isso quebra o método.**

---

#### 🎯 O QUE ENDFIRST REALMENTE EXIGE

**ENDFIRST não é:**
- ❌ "ter uma spec"
- ❌ "ter critérios"
- ❌ "ter um acceptance"

**ENDFIRST é:**
> "Nada existe enquanto o RESULTADO FINAL não estiver definido, versionado, governado e verificável."

**Mais forte:**
> "O sistema só pode ser organizado a partir do RESULTADO, nunca o contrário."

---

#### ❌ O QUE ISSO ELIMINA

**Frases proibidas:**
- ❌ "Vamos começar pelo backlog"
- ❌ "Primeiro organizamos as tarefas"
- ❌ "Depois vemos o resultado"
- ❌ "Vamos descobrindo o que entregar"
- ❌ "O backlog define o escopo"

**Por que são proibidas:**
- Invertem a hierarquia (PROCESS FIRST, não END FIRST)
- Backlog vira origem, não derivado
- Resultado vira descoberta, não pré-condição
- Viola pilar ENDFIRST

---

#### ✅ O QUE ISSO EXIGE

**RESULTADO como entidade de primeira classe:**
- ✅ Documento explícito: `/DEMANDAS/DEMANDA-XXX_RESULT.md`
- ✅ O que existe quando a demanda "termina"
- ✅ O que pode ser observado
- ✅ O que pode ser provado
- ✅ O que encerra a demanda

**Backlog como derivado:**
- ✅ Backlog é um mapa de provas
- ✅ Não é um plano de execução
- ✅ Cada item responde: "Qual parte do RESULTADO isto prova?"
- ✅ Se não prova nada → não entra no backlog

**Ordem obrigatória:**
1. ✅ Definir RESULTADO
2. ✅ Definir CRITÉRIOS DE SUCESSO
3. ✅ Definir PROVAS OBSERVÁVEIS
4. ✅ Derivar BACKLOG
5. ✅ Executar

---

#### 📝 EXEMPLOS REAIS (DO NOSSO SISTEMA)

**Exemplo 1: Erro que detectamos**
- **Problema:** Começamos a discutir backlog, Kanban, GitHub Projects
- **Causa raiz:** Antes de congelar o RESULTADO como objeto governável
- **Falha de design:** Agimos como PROCESS FIRST, não END FIRST
- **Solução estrutural:** OD-010 (RESULTADO primeiro, backlog depois)

**Exemplo 2: DEMANDA-001**
- **Problema:** DEMANDA-001 tinha ACCEPTANCE, mas não RESULT formal
- **Causa raiz:** Acceptance é parte, mas não é tudo
- **Falha de design:** Faltava entidade RESULT como objeto de primeira classe
- **Solução estrutural:** Criar DEMANDA-001_RESULT.md

---

#### 🔍 FRONTEIRA SEMÂNTICA (X ≠ Y)

**RESULTADO ≠ Acceptance**
- RESULTADO: O que existe quando termina
- Acceptance: Como CEO julga sucesso
- Acceptance é parte do RESULTADO, mas não é tudo

**RESULTADO ≠ Spec**
- RESULTADO: O que é entregue
- Spec: Como é construído
- Spec define HOW, RESULTADO define END

**Backlog ≠ Escopo**
- Backlog: Mapa de provas do RESULTADO
- Escopo: O que está dentro/fora
- RESULTADO define escopo, backlog deriva dele

**Processo ≠ Resultado**
- Processo: Como organizar execução
- Resultado: O que encerra demanda
- Processo não cria resultado, resultado cria processo

---

#### ⛔ PROIBIÇÕES EXPLÍCITAS

**❌ Backlog antes de RESULTADO**
- Proibido criar backlog antes de definir RESULTADO
- Proibido organizar tarefas antes de congelar END
- Proibido começar pelo HOW

**❌ Execução sem RESULTADO formal**
- Proibido executar sem RESULT.md no Git
- Proibido "descobrir o resultado" durante execução
- Proibido "ajustar o END" depois de começar

**❌ Acompanhamento sem PROVAS OBSERVÁVEIS**
- Proibido acompanhar progresso sem provas definidas
- Proibido "interpretar" se está pronto
- Proibido julgar sucesso sem critérios prévios

---

#### ✅ IMPLICAÇÕES

**Para CEO:**
- Não aceitar demanda sem RESULT.md
- Rejeitar backlog antes de RESULTADO
- Exigir END formal antes de qualquer organização

**Para Manus:**
- Não criar processo antes de RESULTADO
- Não organizar backlog antes de END
- Não começar pelo HOW

**Para Cursor:**
- Não executar sem RESULT.md
- Não "descobrir" resultado durante execução
- Não aceitar demanda sem END formal

**Para o sistema:**
- RESULTADO é entidade de primeira classe
- Backlog é derivado
- END primeiro, HOW depois

---

#### 📝 EXEMPLOS VÁLIDOS

**Exemplo 1: DEMANDA-001 corrigida**
- DEMANDA-001_RESULT.md criado
- RESULTADO definido: "LLM Orchestrator funcional"
- PROVAS OBSERVÁVEIS: 7 critérios
- Backlog derivado das provas

**Exemplo 2: Ordem correta**
1. Criar RESULT.md
2. Definir PROVAS OBSERVÁVEIS
3. Derivar backlog
4. Executar

**Exemplo 3: Backlog como mapa de provas**
- Cada item do backlog responde: "Qual parte do RESULTADO isto prova?"
- Se não prova nada → não entra

---

#### 🎯 ANTI-EXEMPLOS (PROIBIDOS)

**Anti-exemplo 1:**
> "Vamos começar organizando o backlog, depois vemos o resultado."

**Por que é proibido:**
- Inverte hierarquia (PROCESS FIRST)
- Backlog vira origem
- Viola ENDFIRST

**Solução correta:**
- Definir RESULTADO primeiro
- Derivar backlog depois

---

**Anti-exemplo 2:**
> "Vamos descobrindo o que entregar durante a execução."

**Por que é proibido:**
- Resultado vira descoberta
- END não é pré-condição
- Viola OD-007

**Solução correta:**
- RESULTADO definido antes de executar
- END é pré-condição absoluta

---

**Anti-exemplo 3:**
> "O backlog define o escopo."

**Por que é proibido:**
- Backlog vira entidade primária
- RESULTADO vira derivado
- Viola OD-010

**Solução correta:**
- RESULTADO define escopo
- Backlog deriva do RESULTADO

---

#### 📜 FRASE CANÔNICA (CULTURA)

> **"Backlog não cria resultado. Resultado cria backlog. Processo não cria resultado. Resultado cria processo."**

**Uso:**
- Cultura organizacional
- Onboarding de time
- Revisão de demandas
- Decisões de planejamento
- Corte de escopo

**Implicação:**
- END FIRST, não PROCESS FIRST
- RESULTADO é entidade de primeira classe
- Backlog é derivado, não origem

---

#### 🚨 CRITÉRIO OBRIGATÓRIO DE REVISÃO

**Pergunta obrigatória em toda revisão:**

> **"O RESULTADO está definido, versionado e governável antes do backlog?"**

**Decisão:**
- Se NÃO → ❌ REJEITADO
- Se SIM → ✅ Pode seguir

**Nota obrigatória:**
> Se estamos discutindo backlog antes de congelar o resultado, o método falhou.

**Aplica-se a:**
- Revisão de demandas (Cursor e Manus)
- Revisão de planejamento
- Revisão de processos
- Revisão de organização

---

#### 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/PILAR_ENDFIRST.md` (Meta-pilar)
- `/METODO/ONTOLOGY_DECISIONS.md` (OD-004 a OD-009)
- `/DEMANDAS/DEMANDA-XXX_RESULT.md` (Template de RESULTADO)
- `/README.md` (Frase canônica de cultura)

---

#### 📜 DECLARAÇÃO DO CEO

> "Se estamos discutindo backlog antes de congelar o resultado, o método falhou. ENDFIRST significa que o sistema só se organiza depois que o fim está absolutamente claro. Processo não cria resultado. Resultado cria processo."

**Data:** 2026-01-08  
**Responsável:** CEO (Joubert Jr)

---

## OD-011 — Entendimento sem mudança comportamental é fuga

#### 📜 DECLARAÇÃO CANÔNICA

> **"Se o entendimento não muda comportamento pequeno imediatamente, ele é fuga."**

**Princípio:**
- Entendimento só é válido se forçar ou impedir ao menos um comportamento pequeno agora
- Se a mudança é "mais tarde", "quando amadurecer", "quando escalar" → ❌ inválido

**Regra absoluta:**
- Compreensão sem ação imediata = fuga sofisticada
- Consenso sem mudança = racionalização elegante
- Clareza sem impacto = ruído

---

#### ❌ PROIBIÇÕES EXPLÍCITAS

1. **Entendimento sem ação imediata**
   - Exemplo: "Agora ficou claro" sem mudança no Git
   - Consequência: Fuga sofisticada

2. **Documento que "explica" mas não muda nada**
   - Exemplo: Wiki educativa sem trava estrutural
   - Consequência: Conhecimento inútil

3. **Processo que depende de consciência/atenção**
   - Exemplo: "Agora todo mundo sabe"
   - Consequência: Viola OD-009 (disciplina humana)

4. **Cultura baseada em "todo mundo sabe"**
   - Exemplo: Conhecimento implícito, não versionado
   - Consequência: Viola OD-007 (END no Git)

---

#### ✅ EXEMPLOS VÁLIDOS

**Entendimento que muda comportamento:**
1. **OD-009 criada** → Checklist ganha critério obrigatório
2. **Template criado** → Campo obrigatório impede erro
3. **Regra formalizada** → Commit é rejeitado automaticamente
4. **Processo documentado** → Executor lê do Git, não pergunta

**Característica comum:**
- Mudança pequena, mas imediata
- Observável, não subjetiva
- Estrutural, não cultural

---

#### ❌ ANTI-EXEMPLOS (PROIBIDOS)

**Entendimento sem efeito:**
1. **"Agora entendi o método"** → Mas continua fazendo igual
2. **"Ficou claro"** → Mas nada muda no repositório
3. **"Todo mundo sabe"** → Mas não está no Git
4. **"Vamos ter cuidado"** → Depende de disciplina (viola OD-009)

**Característica comum:**
- Conforto intelectual
- Sem mudança observável
- Sem trava estrutural
- Fuga sofisticada

---

#### 📜 RACIONAL

Este princípio fecha o loop ontológico:

**OD-007:** END primeiro (não HOW)
**OD-009:** Processo > Disciplina
**OD-010:** RESULTADO é entidade de primeira classe
**OD-011:** Entendimento sem mudança é fuga

**Sem OD-011, o sistema ainda permite:**
- Compreensão sem ação
- Consenso sem mudança
- Clareza sem impacto

**Com OD-011:**
- Entendimento é inútil se não muda comportamento pequeno agora
- Ou muda o mundo — ou não entra

---

#### 🎯 IMPLICAÇÕES PRÁTICAS

**Para documentos:**
- Documento sem trava estrutural = fuga
- Wiki que não impede erro = inútil
- Explicação que não altera fluxo = ruído

**Para processos:**
- Processo que depende de "lembrar" = viola OD-009
- Processo que não muda comportamento = fuga

**Para decisões:**
- Decisão sem mudança imediata = não é decisão
- Consenso sem efeito observável = teatro

**Para comunicação:**
- Comunicação do método deve forçar uso correto
- Entendimento deve impedir erro estruturalmente
- Se pessoa "entendeu" mas faz errado = sistema falhou

---

#### 📜 FRASE CANÔNICA (CULTURA)

> **"Entendimento que não muda comportamento é fuga."**

**Uso:**
- Cultura organizacional
- Revisão de documentos
- Revisão de processos
- Revisão de decisões
- Onboarding de time

**Implicação:**
- END FIRST, não conforto intelectual
- Mudança pequena, mas imediata
- Estrutural, não cultural

---

#### 🚨 CRITÉRIO OBRIGATÓRIO DE REVISÃO

**Pergunta obrigatória em toda revisão:**

> **"Que comportamento pequeno muda agora por causa disso?"**

**Decisão:**
- Sem resposta concreta → ❌ REJEITADO
- Se exigir disciplina humana → ❌ REJEITADO (OD-009)
- Se mudança é "mais tarde" → ❌ REJEITADO
- Se mudança é observável agora → ✅ Pode seguir

**Nota obrigatória:**
> Se algo "faz sentido" mas não muda nada, é fuga sofisticada.

**Aplica-se a:**
- Revisão de demandas (Cursor e Manus)
- Revisão de ODs
- Revisão de processos
- Revisão de documentos
- Revisão de comunicação do método

---

#### 🔗 DOCUMENTOS RELACIONADOS

- `/METODO/PILAR_ENDFIRST.md` (Meta-pilar)
- `/METODO/ONTOLOGY_DECISIONS.md` (OD-004 a OD-010)
- `/METODO/COMMIT_GOVERNANCE_CHECKLIST.md` (Critério obrigatório)
- `/README.md` (Frase canônica de cultura)

---

#### 📜 DECLARAÇÃO DO CEO

> "No ENDFIRST, entendimento é inútil se não muda comportamento pequeno agora. A partir de OD-011, qualquer coisa que apenas 'faça sentido' está proibida. Ou muda o mundo — ou não entra."

**Data:** 2026-01-08  
**Responsável:** CEO (Joubert Jr)

---

### 🚫 METACOGNIÇÃO NO CAMINHO CRÍTICO (EXTENSÃO ESTRUTURAL)

**Declaração canonica (reforço):**

> **"O método ENDFIRST existe para retirar a metacognição humana do caminho crítico. Se algo só funciona quando alguém percebe, nota ou ajusta, é estruturalmente inválido."**

**Proibições explícitas:**

- ❌ "se alguém perceber…"
- ❌ "ajusta se notar…"
- ❌ "depende de atenção/consciência"
- ❌ "quando alguém revisar com cuidado"

**Regra operacional absoluta:**

> **"Se um erro só é evitado quando alguém nota, o design falhou."**

**Princípio:**

- Metacognição é habilidade humana
- ENDFIRST é a decisão de não depender dela
- Bloqueio estrutural > Atenção humana
- Sistema pensa no lugar do humano no caminho crítico

**Racional:**

Metacognição no caminho crítico é a forma mais sofisticada de "entendimento sem mudança":

- Se o sistema exige que alguém "perceba" para não errar → viola OD-009 (disciplina humana)
- Se o sistema exige que alguém "reflita" para ajustar → viola OD-011 (entendimento sem mudança)
- Se o sistema exige "cuidado" para funcionar → design errado

**Exemplos reais:**

- ❌ Status verbal (depende de alguém notar inconsistência)
- ❌ Incremento sem card (depende de alguém perceber ausência)
- ❌ Critério sem evidência binária (depende de alguém avaliar)
- ✅ Kanban canônico (sistema impede status inventado)
- ✅ Commit sem card → rejeitado automaticamente
- ✅ Critério binário → passa ou falha, sem interpretação

**Frase guia:**

> **"Metacognição é habilidade humana. ENDFIRST é a decisão de não depender dela."**

---

## 🧠 ENTIDADES FUNDAMENTAIS

### Documento
**Definição:** Arquivo .md com YAML frontmatter obrigatório.

**Tipos:**
- **Canônico (A):** Governa outros documentos
- **Operacional (B):** Define processos
- **Exemplo (C):** Exemplifica templates

**Estados:**
- `approved` — Oficialmente aprovado
- `pending` — Aguardando aprovação
- `obsolete` — Obsoleto (não usar)

---

### Commit
**Definição:** Mudança atômica no repositório Git.

**Propriedades:**
- Hash (7+ caracteres)
- Mensagem (Conventional Commits)
- Autor
- Data

**Relação com Aprovação:** Aprovação deve referenciar commit existente.

---

### Aprovação
**Definição:** Decisão formal registrada em APPROVAL_LOG.md.

**Propriedades obrigatórias:**
- document_id
- type (A/B/C)
- status (approved/pending/obsolete)
- approved_by (nome)
- approved_at (YYYY-MM-DD)
- reason (justificativa)
- governed_by (path)
- commit (hash)

**Invariante:** Aprovação sem hash não existe.

---

### Checklist
**Definição:** Lista de verificações obrigatórias antes de declarar conformidade.

**Função:** Impedir estados inválidos.

**Exemplos:**
- COMMIT_GOVERNANCE_CHECKLIST.md
- Checklist B1-B11 do ENDFIRST_SPEC

---

## 🔗 RELAÇÕES FUNDAMENTAIS

### "governado por"
**Definição:** Documento A governa documento B.

**Propriedade:** Transitiva (se A governa B e B governa C, então A governa C indiretamente).

**Exemplo:**
```
PILAR_ENDFIRST.md (A)
    ↓ governa
ENDFIRST_SPEC.md (B)
    ↓ governa
ENDFIRST_SPEC_EF-2026-001 (C)
```

---

### "aprovado por"
**Definição:** Pessoa X aprovou documento Y.

**Propriedade:** Não transitiva (aprovação não se propaga).

**Registro:** APPROVAL_LOG.md

---

### "registrado em"
**Definição:** Aprovação de documento X está registrada em commit Y.

**Propriedade:** Bidirecional (commit → log, log → commit).

**Invariante:** Hash deve existir em ambos os lados.

---

## 🚫 ANTI-ESTADOS (IMPOSSÍVEIS POR DEFINIÇÃO)

### "Commit aprovado sem log"
**Definição:** Commit que altera documentos governados mas não atualiza APPROVAL_LOG.md.

**Status:** PROIBIDO

**Bloqueio:** COMMIT_GOVERNANCE_CHECKLIST.md

---

### "Aprovação com TBD"
**Definição:** Entrada no APPROVAL_LOG com `commit: TBD`.

**Status:** PROIBIDO

**Bloqueio:** APPROVAL_LOG_RULES.md Regra 1

---

### "Documento aprovado sem YAML"
**Definição:** Documento sem metadados obrigatórios mas marcado como aprovado.

**Status:** IMPOSSÍVEL

**Motivo:** Sem YAML, documento não entra no sistema de governança.

---

### "README que mente"
**Definição:** README que afirma existência de algo que não existe.

**Status:** PROIBIDO

**Bloqueio:** README v11.8+ (Estado Atual vs Visão Futura)

---

## 🔄 MECANISMOS DE CORREÇÃO

### Correção de TBD
**Gatilho:** Detectar `commit: TBD` no APPROVAL_LOG.

**Ação:**
1. Identificar commit real que aprovou o documento
2. Substituir TBD por hash real
3. Criar commit de correção
4. Registrar correção no histórico do log

**Exemplo:** Commit 5c294f0 corrigiu TBD do commit 2d47fab.

---

### Correção de Contagem
**Gatilho:** Total de documentos não bate com realidade.

**Ação:**
1. Contar arquivos .md no repositório
2. Atualizar estatísticas no APPROVAL_LOG
3. Criar commit de correção
4. Registrar correção no histórico do log

**Exemplo:** Commit 4b8957a corrigiu contagem de 17 para 14.

---

### Correção de Commit Não Conforme
**Gatilho:** Commit falha no COMMIT_GOVERNANCE_CHECKLIST.

**Ação:**
1. Identificar itens que falharam
2. Corrigir inconsistências
3. Criar commit de correção
4. Validar novamente com checklist

**Exemplo:** Commit 2d47fab falhou (TBD presente), corrigido por 5c294f0.

---

## 📊 INVARIANTES GLOBAIS

### Invariante 1: Rastreabilidade Bidirecional
**Definição:** Se APPROVAL_LOG referencia commit X, então commit X deve conter mudanças no documento aprovado.

**Verificação:**
```bash
git show [HASH] -- path/to/document.md
```

---

### Invariante 2: Consistência YAML ↔ Log
**Definição:** Metadados no YAML frontmatter devem estar sincronizados com APPROVAL_LOG.

**Verificação:** Comparar campos `status`, `approved_by`, `approved_at`, `governed_by`.

---

### Invariante 3: Totalização Correta
**Definição:** Total de documentos = Aprovados + Pendentes + Obsoletos.

**Verificação:**
```bash
find . -name "*.md" | wc -l
```

---

### Invariante 4: Hierarquia Acíclica
**Definição:** Relação "governado por" não pode ter ciclos.

**Exemplo inválido:**
```
A governa B
B governa C
C governa A  ← CICLO (proibido)
```

---

## 🧪 CASOS DE TESTE (VALIDAÇÃO)

### Teste 1: TBD é detectado
**Input:** Criar entrada com `commit: TBD`

**Resultado esperado:** Checklist falha, commit não é aprovado

**Status:** ✅ VALIDADO (commit 2d47fab)

---

### Teste 2: Contagem incorreta é detectada
**Input:** Afirmar "17 documentos" quando existem 14

**Resultado esperado:** Auditoria identifica discrepância

**Status:** ✅ VALIDADO (commit 4b8957a)

---

### Teste 3: Commit sem log é bloqueado
**Input:** Alterar documento sem atualizar APPROVAL_LOG

**Resultado esperado:** Checklist falha (item "APPROVAL_LOG atualizado?")

**Status:** ✅ VALIDADO (design do checklist)

---

## 📚 DOCUMENTOS RELACIONADOS

**Canônicos (Tipo A):**
- PILAR_ENDFIRST.md — Meta-pilar soberano
- ENDFIRST_DOCUMENT_GOVERNANCE.md — Governança documental
- ONTOLOGY_DECISIONS.md — Este documento

**Operacionais (Tipo B):**
- COMMIT_GOVERNANCE_CHECKLIST.md — Checklist de conformidade
- APPROVAL_LOG_RULES.md — Regras anti-TBD
- APPROVAL_LOG.md — Log de aprovações

**Exemplos (Tipo C):**
- ENDFIRST_SPEC_EF-2026-001 — LLM Orchestrator
- ENDFIRST_SPEC_EF-2026-002 — Governança Documental

---

## 🔒 REGRA DE ATUALIZAÇÃO

**Este documento só pode ser atualizado quando:**

1. **Gatilho formal dispara** (ver ONTOLOGY_DECISIONS_TRIGGER.md)
2. **Todos os 5 critérios são cumpridos:**
   - Houve confusão real
   - Gerou risco sistêmico
   - É transversal (não local)
   - Cria fronteira clara (X ≠ Y)
   - Já está em uso
3. **CEO aprova a entrada**

**Proibido adicionar:**
- ❌ Teoria sem validação prática
- ❌ Formalismo sem necessidade operacional
- ❌ Conceitos que não foram testados
- ❌ Ontologia "preventiva"
- ❌ Glossário de termos

**Motivo:** Ontologia congela aprendizado, não inovação.

**Processo completo:** Ver `/METODO/ONTOLOGY_DECISIONS_TRIGGER.md`

---

### OD-012 — Planejamento é artefato de primeira classe

**ID:** OD-012  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-19

---

#### 🧠 DECISÃO

Planejamento é artefato de primeira classe com END, DONE WHEN e critérios de FAIL explícitos.

Execução sem planejamento aprovado (F-1) é bloqueada estruturalmente para demandas complexas.

---

#### 📝 RACIONAL

Método END-FIRST atual permite execução sem planejamento aprovado, gerando:
- Interpretação durante execução
- Endurecimento tardio de regras
- Retrabalho sistemático
- Overhead cognitivo

**F-1 (Planejamento Canônico BLOQUEANTE)** corrige essa falha de design.

---

#### 🔍 DEFINIÇÕES

**F-1 (Planejamento Canônico)**
- Estágio obrigatório antes de qualquer execução (demandas complexas)
- Tem END explícito
- Tem DONE WHEN verificável
- Tem critérios de FAIL automáticos
- Bloqueia execução até aprovação

**PROIBIÇÕES (FAIL automático):**
- ❌ Executar comandos durante F-1
- ❌ Criar código durante F-1
- ❌ Criar automações durante F-1
- ❌ "Validar rapidamente"
- ❌ Interpretar regras durante execução

---

#### ✅ IMPLICAÇÕES

- Planejamento tem END próprio
- Executor (Cursor) não interpreta, apenas executa plano aprovado
- Arquitetura e governança são decididas antes de F-1
- Retrabalho de validação é eliminado por design
- F-1 é obrigatório para projetos complexos
- F-1 é opcional para demandas simples

---

#### 📌 FRASE CANÔNICA

> "Planejamento é artefato de primeira classe. Executor apenas executa."

---

#### 📜 EVIDÊNCIA

Proposta baseada em uso real do método com múltiplos ciclos de retrabalho documentados durante:
- Endurecimento tardio de regras
- Redefinição de escopo
- Validações repetidas

Não é opinião. É evidência empírica.

---

#### 🔗 REFERÊNCIA

**Documento canônico:** `/METODO/END_FIRST_V2.md`

---

#### 📜 DECLARAÇÃO DO CEO

> "Esta decisão cristaliza a evolução do método END-FIRST para v2. Planejamento deixa de ser processo informal e passa a ser artefato governado com END próprio. F-1 é bloqueio estrutural, não disciplina humana."

**Status:** CANÔNICA  
**Aplicação:** Imediata para demandas complexas

---

---

### OD-013 — Template de Demanda é Obrigatório

**ID:** OD-013  
**Status:** APROVADA  
**Aprovado por:** CEO (Joubert Jr)  
**Data:** 2026-01-19

---

#### 🧠 DECISÃO

Toda demanda deve seguir o Template Canônico de Demanda com 11 seções obrigatórias.

Demandas fora do template são FAIL estrutural.

---

#### 📝 RACIONAL

Método END-FIRST v2 permite demandas sem estrutura padronizada, gerando:
- Revisão manual recorrente
- Regras implícitas
- Frases canônicas perdidas
- Overhead cognitivo
- Ambiguidade entre bug/UX/produto

**Template Canônico** corrige essa falha de design.

---

#### 🔍 DEFINIÇÕES

**Template Canônico de Demanda:**
- Estrutura obrigatória de 11 seções
- Frases canônicas explícitas por tipo
- Regra de UX canônica (scroll interno proibido)
- Classificação estrutural (Bug/UX/Produto/Método)
- Documento oficial: `/METODO/TEMPLATE_DEMANDA_CANONICA.md`

**PROIBIÇÕES (FAIL estrutural):**
- ❌ Demandas sem estrutura do template
- ❌ Seções faltando
- ❌ Frases canônicas implícitas
- ❌ "Cada demanda é diferente"

---

#### ✅ IMPLICAÇÕES

- Toda demanda tem END explícito
- Toda demanda tem critérios binários
- Toda demanda tem bloqueios estruturais
- Toda demanda tem frases canônicas
- Revisão manual é eliminada por design
- Manus/Cursor rejeitam demandas fora do template

---

#### 📌 FRASE CANÔNICA

> "Se uma demanda precisa ser explicada, ela está errada. Se precisa ser revisada várias vezes, o método falhou."

---

#### 📜 EVIDÊNCIA

Proposta baseada em uso real do método (projeto CoverageSummarizer) com múltiplos ciclos de revisão documentados.

---

#### 🔗 REFERÊNCIA

**Documento canônico:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`

---

#### 📜 DECLARAÇÃO DO CEO

> "Esta decisão elimina ambiguidade na criação de demandas. Template Canônico é bloqueio estrutural, não disciplina humana. Demandas fora do template são FAIL por design."

**Status:** CANÔNICA  
**Aplicação:** Imediata para todas as demandas

---

**Versão:** 2.1  
**Criado:** 8 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Status:** Canônico (Tipo A)
