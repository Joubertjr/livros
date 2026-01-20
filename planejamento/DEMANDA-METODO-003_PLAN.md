# PLANEJAMENTO CANÔNICO — DEMANDA-METODO-003: GOVERNANÇA DO CICLO DE VIDA DE ARTEFATOS

**Demanda:** DEMANDA-METODO-003_GOVERNANCA_CICLO_VIDA_ARTEFATOS.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-19  
**Status:** ✅ F-1 APROVADA  
**Repositório:** https://github.com/Joubertjr/livros

---

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

**Clarificação Metodológica:**
- Criar documentos canônicos é parte da **governança conceitual** do método
- Paths específicos (ex: `/METODO/...`) são **implementação operacional** deste projeto
- O método governa **conceitos** (DEMANDA, F-1, Evidências, Histórico), não paths
- Outros projetos podem implementar a mesma governança com estrutura diferente

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS — NÃO NEGOCIÁVEIS)

Estas frases são canônicas, reutilizáveis e bloqueantes:

- **Ciclo de Vida:** "Artefatos com naturezas diferentes não podem ocupar o mesmo plano semântico."
- **Intenção vs Memória:** "Demanda não é histórico. Histórico não governa execução."
- **Planejamento:** "F-1 existe para governar execução, não para se perpetuar."
- **Evidência:** "Evidência prova o END; não substitui o END."
- **Clareza Cognitiva:** "Se é preciso explicar onde algo se encaixa, o método falhou."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

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
- ✅ Evidência conceitual gerada (documentação, não automação)

### FAIL (AUTOMÁTICO)

- ❌ Continuidade de ambiguidade entre planejamento, evidência e histórico
- ❌ Mistura conceitual entre artefatos ativos e memória
- ❌ Dependência de convenção tácita para entender organização
- ❌ Solução focada apenas em filesystem, sem governança conceitual
- ❌ Introdução de complexidade estrutural sem ganho cognitivo
- ❌ Alteração de comportamento operacional sem END claro
- ❌ Execução sem F-1 aprovada
- ❌ Violação de qualquer frase canônica

---

## 🚫 DO / DON'T

### DO (fazer)

- ✅ Tratar ciclo de vida como conceito de método
- ✅ Diferenciar intenção, execução, prova e memória
- ✅ Reduzir fricção cognitiva
- ✅ Manter independência de ferramenta e filesystem
- ✅ Usar Pilar END-FIRST como base
- ✅ Documentar governança conceitual
- ✅ Criar documentos canônicos (governança conceitual do método)

### DON'T (não fazer)

- ❌ Resolver apenas reorganizando pastas
- ❌ Criar convenções implícitas
- ❌ Misturar artefatos ativos com históricos
- ❌ Criar regras dependentes de um projeto específico
- ❌ Aumentar burocracia sem ganho cognitivo
- ❌ Alterar produto ou UX
- ❌ Criar novos gates automaticamente
- ❌ Alterar regras existentes sem evidência clara
- ❌ Implementar ferramentas ou automação (scripts, validações automáticas)
- ✅ Criar evidência documental (arquivos markdown) é permitido (é documentação, não automação)

---

## 🧱 BLOQUEIOS ESTRUTURAIS

- 🔒 F-1 obrigatório (demanda de método)
- 🔒 Nenhuma execução sem aprovação explícita
- 🔒 Não criar novos gates automaticamente
- 🔒 Não alterar regras existentes sem evidência clara
- 🔒 Governança conceitual precede implementação
- 🔒 END-FIRST v2 continua bloqueante
- 🔒 Nenhuma alteração de código ou estrutura de pastas

---

## 📋 TODO CANÔNICO (F0-F6)

### F0 — Revisar Plano (BLOQUEANTE — SEM EXECUÇÃO)

**END:** Plano aprovado e pronto para execução

**DONE WHEN:**
- ✅ Checklist completo verificado
- ✅ Nenhum comando executado
- ✅ Nenhum código alterado
- ✅ Declaração explícita: "F-1 APROVADA" (recebida do CEO em 2026-01-19)

**STATUS:** ✅ COMPLETA — F-1 aprovada e pronta para execução F1-F6

**PROIBIÇÕES:**
- ❌ Executar comandos
- ❌ Criar código
- ❌ "Validar rapidamente"

---

### F1 — Mapear Conceitualmente o Ciclo de Vida

**END:** Ciclo DEMANDA → F-1 → Execução → Evidências → Histórico mapeado conceitualmente

**DONE WHEN:**
- Cada etapa do ciclo está explicitamente descrita
- Transições entre etapas estão claras
- Papel de cada artefato no ciclo está definido
- Documento conceitual criado (governança do método, não imposição de filesystem)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento existe (verificável: arquivo existe)
- ✅ Documento contém seção explícita descrevendo o ciclo DEMANDA → F-1 → Execução → Evidências → Histórico (verificável: grep por termos)
- ✅ Documento não menciona paths específicos (verificável: ausência de paths absolutos ou relativos)
- ✅ Documento menciona conceitos do método (DEMANDA, F-1, Evidências, Histórico) sem depender de estrutura de pastas (verificável: grep por conceitos)

**NOTA METODOLÓGICA:**
- A criação de documentos canônicos é parte da governança conceitual do método
- Paths específicos (ex: `/METODO/...`) são implementação operacional deste projeto
- O método em si não impõe estrutura de pastas; ele governa conceitos

**REGRAS CANÔNICAS APLICADAS:**
- "Artefatos com naturezas diferentes não podem ocupar o mesmo plano semântico."
- "Se é preciso explicar onde algo se encaixa, o método falhou."

---

### F2 — Definir Fronteiras Semânticas Entre Artefatos

**END:** Fronteiras semânticas entre DEMANDA, F-1, EVIDÊNCIAS e HISTÓRICO explicitamente definidas

**DONE WHEN:**
- Cada tipo de artefato tem:
  - Propósito único e claro
  - Momento de criação definido
  - Critério de transição para "não-ativo" explícito
- Fronteiras entre artefatos são inequívocas
- Documento de fronteiras semânticas criado (conceitual, independente de filesystem)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento existe (verificável: arquivo existe)
- ✅ Documento contém seção explícita para cada tipo de artefato (DEMANDA, F-1, EVIDÊNCIAS, HISTÓRICO) com propósito único (verificável: grep por cada tipo)
- ✅ Documento define critério de transição para "não-ativo" para cada tipo (verificável: grep por "transição" ou "não-ativo")
- ✅ Documento não menciona paths específicos (verificável: ausência de paths)

**REGRAS CANÔNICAS APLICADAS:**
- "Demanda não é histórico. Histórico não governa execução."
- "F-1 existe para governar execução, não para se perpetuar."
- "Evidência prova o END; não substitui o END."

---

### F3 — Identificar Pontos de Fricção Cognitiva Atuais

**END:** Pontos de fricção cognitiva no ciclo atual identificados e documentados

**DONE WHEN:**
- Análise do estado atual realizada (exemplos podem ser do projeto atual, mas método é genérico)
- Pontos onde organização gera confusão identificados
- Exemplos concretos de ambiguidade documentados
- Documento de análise criado (conceitual, com exemplos ilustrativos)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento existe (verificável: arquivo existe)
- ✅ Documento contém seção "Pontos de Fricção" ou equivalente listando ambiguidades identificadas (verificável: grep por "fricção" ou "ambiguidade")
- ✅ Documento não menciona paths específicos do projeto atual (verificável: ausência de paths)
- ✅ Exemplos (se houver) são marcados como "ilustrativos" ou "exemplo" (verificável: grep por "exemplo" ou "ilustrativo")

**REGRAS CANÔNICAS APLICADAS:**
- "Se é preciso explicar onde algo se encaixa, o método falhou."

---

### F4 — Validar Alinhamento com END-FIRST v2

**END:** Governança do ciclo de vida alinhada com END-FIRST v2

**DONE WHEN:**
- Documentos criados validam alinhamento com END-FIRST v2 (conceitual)
- Nenhuma contradição com Pilar END-FIRST identificada
- F-1 continua sendo artefato bloqueante
- Documento de validação criado (conceitual)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento existe (verificável: arquivo existe)
- ✅ Documento menciona explicitamente "END-FIRST v2" e "Pilar END-FIRST" (verificável: grep por termos)
- ✅ Documento declara explicitamente "F-1 continua sendo artefato bloqueante" (verificável: grep por "F-1" e "bloqueante")
- ✅ Documento não menciona paths específicos (verificável: ausência de paths)

**REGRAS CANÔNICAS APLICADAS:**
- "Planejamento é artefato de primeira classe. Executor apenas executa."

---

### F5 — Gerar Evidência Conceitual (Documentação Canônica)

**END:** Documentação canônica do ciclo de vida criada e integrada ao método

**DONE WHEN:**
- Documento canônico principal criado (governança conceitual)
- Documento integrado ao método (critério binário definido abaixo)
- Evidência de conformidade gerada (documental, não automação)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento canônico principal existe (verificável: arquivo existe)
- ✅ **INTEGRAÇÃO AO MÉTODO (Critério Binário):** Documento menciona explicitamente pelo menos um documento canônico do método por **nome** (não por path). Exemplos válidos: "END-FIRST v2", "Pilar END-FIRST", "Template Canônico de Demanda" (verificável: grep por nomes de documentos canônicos)
- ✅ Evidência documental existe (verificável: arquivo existe)
- ✅ Evidência lista status de cada fase F1-F6 (verificável: grep por "F1", "F2", etc.)

**DIFERENCIAÇÃO METODOLÓGICA:**
- **Evidência documental** (criar arquivos markdown): ✅ Permitido (é documentação)
- **Automação/ferramentas** (scripts, validações automáticas): ❌ Proibido

**REGRAS CANÔNICAS APLICADAS:**
- "Se é preciso explicar onde algo se encaixa, o método falhou."
- "Clareza cognitiva reduz necessidade de explicação humana"

---

### F6 — Declarar PASS

**END:** Demanda concluída e validada

**DONE WHEN:**
- Todos os documentos conceituais criados
- Evidência de conformidade gerada (documental)
- Nenhuma violação de frase canônica identificada
- Status atualizado para "✅ CONCLUÍDA"

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Todos os 4 documentos conceituais existem (verificável: 4 arquivos existem)
- ✅ Evidência documental existe (verificável: arquivo existe)
- ✅ Evidência declara status "✅ CONCLUÍDA" ou equivalente (verificável: grep por "CONCLUÍDA" ou "PASS")

**REGRAS CANÔNICAS APLICADAS:**
- "Quando o ciclo de vida é claro, a organização deixa de ser um problema."

---

## 📊 ESTRUTURA DE DOCUMENTOS A CRIAR

### SEPARAÇÃO METODOLÓGICA: Governança do Método vs Implementação Operacional

**ESCOPO DO MÉTODO (Governança Conceitual):**
- Criar documentos que definem conceitos do ciclo de vida
- Documentos são **independentes de filesystem**
- Documentos mencionam conceitos (DEMANDA, F-1, Evidências, Histórico), não paths
- Critérios de integração ao método são **binários e verificáveis** (mencionar documentos canônicos por nome, não por path)

**FORA DO ESCOPO DO MÉTODO (Implementação Operacional):**
- Onde criar os arquivos (paths específicos)
- Como organizar no filesystem
- Comandos para verificar existência
- Estrutura de pastas do projeto

**REGRA:** O método governa **o que criar** (conceitos). O projeto decide **onde criar** (paths).

1. **`GOVERNANCE_CYCLE_LIFECYCLE.md`** (Principal)
   - Mapeamento completo do ciclo DEMANDA → F-1 → Execução → Evidências → Histórico
   - Papel de cada artefato
   - Transições entre etapas
   - Critérios de "ativo vs histórico"

2. **`GOVERNANCE_ARTIFACT_BOUNDARIES.md`**
   - Fronteiras semânticas entre artefatos
   - Propósito único de cada tipo
   - Momento de criação
   - Critério de transição

3. **`GOVERNANCE_FRICTION_ANALYSIS.md`**
   - Análise de fricção cognitiva atual
   - Exemplos concretos de ambiguidade (marcados como ilustrativos)
   - Pontos de melhoria identificados

4. **`GOVERNANCE_ENDFIRST_ALIGNMENT.md`**
   - Validação de alinhamento com END-FIRST v2
   - Compatibilidade com Pilar END-FIRST
   - Integração com F-1

### Evidência (Documental, Não Automação)

5. **`governance_cycle_lifecycle_proof.md`**
   - Evidência de conformidade (documental)
   - Status de cada fase F1-F6
   - Declaração final de status

---

## 🔧 IMPLEMENTAÇÃO OPERACIONAL (Específica do Projeto "livros")

**⚠️ SEPARAÇÃO METODOLÓGICA:**
Esta seção é **implementação operacional** deste projeto específico.  
**NÃO é parte do método.** Outros projetos podem implementar de forma diferente.

**Paths onde os documentos serão criados neste projeto:**
- Documentos conceituais: `/METODO/` (implementação deste projeto)
- Evidência: `/EVIDENCIAS/metodo/` (implementação deste projeto)

**Comandos de verificação (opcional, específico deste projeto):**

```bash
# Exemplo F1 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_CYCLE_LIFECYCLE.md && echo "OK: documento existe" || echo "FAIL: documento não existe"'

# Exemplo F2 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_ARTIFACT_BOUNDARIES.md && echo "OK: documento existe" || echo "FAIL: documento não existe"'

# Exemplo F3 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_FRICTION_ANALYSIS.md && echo "OK: análise existe" || echo "FAIL: análise não existe"'

# Exemplo F4 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_ENDFIRST_ALIGNMENT.md && echo "OK: validação existe" || echo "FAIL: validação não existe"'

# Exemplo F5 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_CYCLE_LIFECYCLE.md && grep -q "END-FIRST v2\|Pilar END-FIRST\|Template Canônico" /app/METODO/GOVERNANCE_CYCLE_LIFECYCLE.md && echo "OK: documento integrado ao método" || echo "Verificar integração"'

# Exemplo F6 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_CYCLE_LIFECYCLE.md && test -f /app/METODO/GOVERNANCE_ARTIFACT_BOUNDARIES.md && test -f /app/EVIDENCIAS/metodo/governance_cycle_lifecycle_proof.md && echo "OK: todos os documentos existem" || echo "FAIL: documentos faltando"'
```

**⚠️ IMPORTANTE:** Estes comandos são **implementação operacional** deste projeto.  
**NÃO são parte do método.** O método define **provas conceituais binárias** (verificáveis por grep/existência de arquivo), não comandos Docker.

---

## 🚫 PROIBIÇÕES ESTRUTURAIS

- ❌ Nenhuma alteração de código
- ❌ Nenhuma reorganização de pastas
- ❌ Nenhuma criação de ferramentas
- ❌ Nenhuma automação
- ❌ Nenhuma alteração de gates existentes
- ❌ Nenhuma mudança em produto ou UX
- ❌ Nenhuma convenção implícita
- ❌ Nenhuma dependência de projeto específico

---

## ✅ REGRAS CANÔNICAS APLICADAS

- **Ciclo de Vida:** "Artefatos com naturezas diferentes não podem ocupar o mesmo plano semântico."
- **Intenção vs Memória:** "Demanda não é histórico. Histórico não governa execução."
- **Planejamento:** "F-1 existe para governar execução, não para se perpetuar."
- **Evidência:** "Evidência prova o END; não substitui o END."
- **Clareza Cognitiva:** "Se é preciso explicar onde algo se encaixa, o método falhou."

---

## 📌 STATUS

**✅ CONCLUÍDA**

**Aprovado por:** CEO (Joubert Jr)  
**Data de aprovação:** 2026-01-19  
**Data de conclusão:** 2026-01-19  
**Declaração canônica:** "F-1 APROVADA"

**Observações do CEO (não bloqueantes):**
1. Provas binárias via grep: considerar strings mínimas únicas do documento para maior robustez
2. Critério "não mencionar paths": já mitigado com "exemplos ilustrativos"

**Execução F1-F6:** ✅ COMPLETA

**Documentos criados:**
- `GOVERNANCE_CYCLE_LIFECYCLE.md`
- `GOVERNANCE_ARTIFACT_BOUNDARIES.md`
- `GOVERNANCE_FRICTION_ANALYSIS.md`
- `GOVERNANCE_ENDFIRST_ALIGNMENT.md`

**Evidência:** `/EVIDENCIAS/metodo/governance_cycle_lifecycle_proof.md`

---

## 🧭 REGRA FINAL (CANÔNICA)

> "Quando o ciclo de vida é claro, a organização deixa de ser um problema."

---

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Template:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`  
**Demanda:** `/DEMANDAS/DEMANDA-METODO-003_GOVERNANCA_CICLO_VIDA_ARTEFATOS.md`
