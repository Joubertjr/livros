# PLANEJAMENTO CANÔNICO — DEMANDA-METODO-004: PROVA CONCEITUAL BINÁRIA E INTEGRAÇÃO CANÔNICA

**Demanda:** DEMANDA-METODO-004_PROVA_CONCEITUAL_BINARIA_INTEGRACAO_CANONICA.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-19  
**Status:** ⏸️ F-1 PENDENTE APROVAÇÃO  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para qualquer demanda de método (ex.: governança, ontologia, gates, princípios):**
- Existe uma definição **canônica, binária e inequívoca** de:
  - o que é **PROVA CONCEITUAL válida**
  - o que significa **INTEGRAÇÃO AO MÉTODO** (sem depender de interpretação humana)
- Um executor consegue concluir uma demanda de método sem retrabalho por:
  - ambiguidade de "autoexplicativo"
  - ambiguidade de "aplicável a qualquer projeto"
  - ambiguidade de "não depender de paths"
- Um revisor (CEO) consegue validar com **PASS/FAIL binário**, sem "leitura crítica extensa".

**Importante:**
Este END não cria automação, scripts, gates novos nem muda estrutura de pastas.
Ele governa **contrato textual**: definições e critérios binários.

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS — NÃO NEGOCIÁVEIS)

Estas frases são canônicas, reutilizáveis e bloqueantes:

- **Prova:** "Prova conceitual não é sensação de clareza; é critério verificável."
- **Integração:** "Integração ao método não é link; é referência canônica rastreável."
- **Encerramento:** "Se a conclusão depende de leitura humana extensa, o método falhou."
- **Fronteira:** "Conceito governa. Implementação exemplifica."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## ✅ CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)

### PASS

- ✅ O método contém uma definição canônica do que é **PROVA CONCEITUAL** (texto normativo)
- ✅ O método contém uma definição canônica do que é **INTEGRAÇÃO AO MÉTODO** (texto normativo)
- ✅ Ambas definições incluem **critérios binários** (PASS/FAIL) e **condições de FAIL automático**
- ✅ O método define **marcadores/âncoras textuais mínimas** que tornam a verificação objetiva (sem exigir ferramenta)
- ✅ A fronteira **conceito vs implementação** fica explícita e não depende de explicação verbal
- ✅ Nenhuma regra existente do END-FIRST v2 é enfraquecida
- ✅ Evidência documental criada em `/EVIDENCIAS/metodo/` mostrando aplicação em 1 caso real (ex.: DEMANDA-METODO-003)

### FAIL (AUTOMÁTICO)

- ❌ "Prova" permanecer definida como "autoexplicativo" sem critérios verificáveis
- ❌ "Integração" permanecer definida como "menciona algo" sem âncora rastreável
- ❌ Critérios dependerem de "bom senso" ou "leitura crítica" como mecanismo principal
- ❌ Confundir exemplos operacionais (paths, docker, comandos) com norma conceitual
- ❌ Criar automação, scripts ou novos gates como forma de "resolver" (fora de escopo)
- ❌ Alterar estrutura de pastas do projeto como substituto de governança
- ❌ Violação de qualquer frase canônica

---

## 🚫 DO / DON'T

### DO (fazer)

- ✅ Especificar definições normativas (canônicas)
- ✅ Tornar o encerramento binário e rastreável
- ✅ Manter independência de ferramenta
- ✅ Usar o Pilar END-FIRST como fonte de governança
- ✅ Criar documentos canônicos que definem conceitos (governança do método)
- ✅ Definir marcadores textuais verificáveis (grep-friendly)

### DON'T (não fazer)

- ❌ Criar automação para compensar ambiguidade conceitual
- ❌ Criar gate novo
- ❌ Resolver "na organização de pastas"
- ❌ Transformar isso em mudança de produto/UX
- ❌ Depender de ferramentas específicas para verificação
- ❌ Usar paths específicos nas definições canônicas

---

## 🧱 BLOQUEIOS ESTRUTURAIS

- 🔒 F-1 obrigatório (demanda de método)
- 🔒 Sem execução sem aprovação explícita
- 🔒 Sem automação/scripts
- 🔒 Sem mudança de estrutura de pastas
- 🔒 Sem criação de gate novo
- 🔒 END-FIRST v2 continua bloqueante

---

## 📋 TODO CANÔNICO (F0-F6)

### F0 — Revisar Plano (BLOQUEANTE — SEM EXECUÇÃO)

**END:** Plano aprovado e pronto para execução

**DONE WHEN:**
- ✅ Checklist completo verificado
- ✅ Nenhum comando executado
- ✅ Nenhum código alterado
- ✅ Declaração explícita: "F-1 APROVADA" (aguardando aprovação do CEO)

**STATUS:** ⏸️ PENDENTE APROVAÇÃO

**PROIBIÇÕES:**
- ❌ Executar comandos
- ❌ Criar código
- ❌ "Validar rapidamente"

---

### F1 — Mapear Ambiguidade Atual de "Prova Conceitual"

**END:** Ambiguidade atual de "prova conceitual" mapeada e documentada

**DONE WHEN:**
- Análise do uso atual de "prova conceitual" realizada
- Pontos onde "prova" é ambíguo identificados
- Exemplos concretos de ambiguidade documentados (ex.: DEMANDA-METODO-003)
- Documento de análise criado (conceitual)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento existe (verificável: arquivo existe)
- ✅ Documento contém seção "Ambiguidade Atual" ou equivalente listando problemas identificados (verificável: grep por "ambiguidade" ou "problema")
- ✅ Documento menciona pelo menos 2 exemplos concretos de uso ambíguo (verificável: grep por "exemplo" ou contagem de ocorrências)
- ✅ Documento não menciona paths específicos do projeto atual (verificável: ausência de paths)

**REGRAS CANÔNICAS APLICADAS:**
- "Prova conceitual não é sensação de clareza; é critério verificável."

---

### F2 — Mapear Ambiguidade Atual de "Integração ao Método"

**END:** Ambiguidade atual de "integração ao método" mapeada e documentada

**DONE WHEN:**
- Análise do uso atual de "integração ao método" realizada
- Pontos onde "integração" é ambíguo identificados
- Exemplos concretos de ambiguidade documentados (ex.: DEMANDA-METODO-003)
- Documento de análise criado (conceitual)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento existe (verificável: arquivo existe)
- ✅ Documento contém seção "Ambiguidade Atual" ou equivalente listando problemas identificados (verificável: grep por "ambiguidade" ou "problema")
- ✅ Documento menciona pelo menos 2 exemplos concretos de uso ambíguo (verificável: grep por "exemplo" ou contagem de ocorrências)
- ✅ Documento não menciona paths específicos do projeto atual (verificável: ausência de paths)

**REGRAS CANÔNICAS APLICADAS:**
- "Integração ao método não é link; é referência canônica rastreável."

---

### F3 — Definir Canonicamente: PROVA CONCEITUAL

**END:** Definição canônica de PROVA CONCEITUAL criada com critérios binários

**DONE WHEN:**
- Definição normativa de "prova conceitual" criada
- Critérios binários (PASS/FAIL) definidos
- Condições de FAIL automático especificadas
- Marcadores/âncoras textuais mínimas definidas
- Documento canônico criado (governança do método)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento canônico existe (verificável: arquivo existe)
- ✅ Documento contém seção "Definição Canônica" ou equivalente (verificável: grep por "definição" ou "canônica")
- ✅ Documento contém seção "Critérios Binários" ou equivalente listando condições PASS/FAIL (verificável: grep por "PASS" e "FAIL")
- ✅ Documento contém seção "Marcadores Textuais" ou equivalente listando strings verificáveis (verificável: grep por "marcador" ou "string")
- ✅ Documento contém seção "FAIL Automático" ou equivalente listando condições de falha (verificável: grep por "FAIL automático" ou "condição")
- ✅ Documento não menciona paths específicos (verificável: ausência de paths)

**REGRAS CANÔNICAS APLICADAS:**
- "Prova conceitual não é sensação de clareza; é critério verificável."
- "Se a conclusão depende de leitura humana extensa, o método falhou."

---

### F4 — Definir Canonicamente: INTEGRAÇÃO AO MÉTODO

**END:** Definição canônica de INTEGRAÇÃO AO MÉTODO criada com critérios binários

**DONE WHEN:**
- Definição normativa de "integração ao método" criada
- Critérios binários (PASS/FAIL) definidos
- Condições de FAIL automático especificadas
- Marcadores/âncoras textuais mínimas definidas
- Documento canônico criado (governança do método)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento canônico existe (verificável: arquivo existe)
- ✅ Documento contém seção "Definição Canônica" ou equivalente (verificável: grep por "definição" ou "canônica")
- ✅ Documento contém seção "Critérios Binários" ou equivalente listando condições PASS/FAIL (verificável: grep por "PASS" e "FAIL")
- ✅ Documento contém seção "Marcadores Textuais" ou equivalente listando strings verificáveis (verificável: grep por "marcador" ou "string")
- ✅ Documento contém seção "FAIL Automático" ou equivalente listando condições de falha (verificável: grep por "FAIL automático" ou "condição")
- ✅ Documento não menciona paths específicos (verificável: ausência de paths)

**REGRAS CANÔNICAS APLICADAS:**
- "Integração ao método não é link; é referência canônica rastreável."
- "Se a conclusão depende de leitura humana extensa, o método falhou."

---

### F5 — Definir Fronteira Conceito vs Implementação

**END:** Fronteira entre conceito (governança) e implementação (operacional) explicitamente definida

**DONE WHEN:**
- Fronteira conceito vs implementação explicitamente descrita
- Critérios para diferenciar norma conceitual de exemplo operacional definidos
- Documento de fronteira criado (conceitual)

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Documento existe (verificável: arquivo existe)
- ✅ Documento contém seção "Fronteira Conceito vs Implementação" ou equivalente (verificável: grep por "fronteira" ou "conceito")
- ✅ Documento define critérios para diferenciar norma de exemplo (verificável: grep por "critério" ou "diferenciação")
- ✅ Documento não menciona paths específicos (verificável: ausência de paths)

**REGRAS CANÔNICAS APLICADAS:**
- "Conceito governa. Implementação exemplifica."

---

### F6 — Integrar ao Método e Gerar Evidência

**END:** Definições canônicas integradas ao método e evidência documental criada

**DONE WHEN:**
- Definições canônicas integradas aos documentos apropriados do método
- Evidência documental criada aplicando as definições em 1 caso real (ex.: DEMANDA-METODO-003)
- Nenhuma violação de frase canônica identificada

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Definições canônicas mencionam explicitamente pelo menos um documento canônico do método por **nome** (não por path). Exemplos válidos: "END-FIRST v2", "Pilar END-FIRST", "Template Canônico de Demanda" (verificável: grep por nomes de documentos canônicos)
- ✅ Evidência documental existe (verificável: arquivo existe)
- ✅ Evidência aplica as definições canônicas em pelo menos 1 caso real (verificável: grep por nome de demanda real, ex.: "DEMANDA-METODO-003")
- ✅ Evidência declara status de cada fase F1-F6 (verificável: grep por "F1", "F2", etc.)

**INTEGRAÇÃO AO MÉTODO (Critério Binário):**
- ✅ Documento canônico criado menciona explicitamente pelo menos um documento canônico do método por **nome** (não por path). Exemplos válidos: "END-FIRST v2", "Pilar END-FIRST", "Template Canônico de Demanda" (verificável: grep por nomes de documentos canônicos)
- ✅ Documento canônico está referenciado em pelo menos um documento canônico existente do método (verificável: grep por nome do novo documento canônico em documentos do método)

**REGRAS CANÔNICAS APLICADAS:**
- "Integração ao método não é link; é referência canônica rastreável."
- "Se a conclusão depende de leitura humana extensa, o método falhou."

---

### F7 — Declarar PASS

**END:** Demanda concluída e validada

**DONE WHEN:**
- Todas as definições canônicas criadas
- Evidência de conformidade gerada (documental)
- Nenhuma violação de frase canônica identificada
- Status atualizado para "✅ CONCLUÍDA"

**PROVA CONCEITUAL (Documental - Binária):**
- ✅ Todos os documentos canônicos existem (verificável: arquivos existem)
- ✅ Evidência documental existe (verificável: arquivo existe)
- ✅ Evidência declara status "✅ CONCLUÍDA" ou equivalente (verificável: grep por "CONCLUÍDA" ou "PASS")

**REGRAS CANÔNICAS APLICADAS:**
- "Se prova e integração não são binárias, demandas de método viram retrabalho."

---

## 📊 ESTRUTURA DE DOCUMENTOS A CRIAR

### SEPARAÇÃO METODOLÓGICA: Governança do Método vs Implementação Operacional

**ESCOPO DO MÉTODO (Governança Conceitual):**
- Criar documentos que definem conceitos de "prova conceitual" e "integração ao método"
- Documentos são **independentes de filesystem**
- Documentos mencionam conceitos, não paths
- Critérios de integração ao método são **binários e verificáveis** (mencionar documentos canônicos por nome, não por path)

**FORA DO ESCOPO DO MÉTODO (Implementação Operacional):**
- Onde criar os arquivos (paths específicos)
- Como organizar no filesystem
- Comandos para verificar existência
- Estrutura de pastas do projeto

**REGRA:** O método governa **o que criar** (conceitos). O projeto decide **onde criar** (paths).

1. **`GOVERNANCE_CONCEPTUAL_PROOF.md`** (Principal)
   - Definição canônica de PROVA CONCEITUAL
   - Critérios binários (PASS/FAIL)
   - Condições de FAIL automático
   - Marcadores textuais verificáveis

2. **`GOVERNANCE_METHOD_INTEGRATION.md`** (Principal)
   - Definição canônica de INTEGRAÇÃO AO MÉTODO
   - Critérios binários (PASS/FAIL)
   - Condições de FAIL automático
   - Marcadores textuais verificáveis

3. **`GOVERNANCE_CONCEPT_IMPLEMENTATION_BOUNDARY.md`**
   - Fronteira entre conceito (governança) e implementação (operacional)
   - Critérios para diferenciar norma de exemplo

4. **`GOVERNANCE_PROOF_AMBIGUITY_ANALYSIS.md`**
   - Análise de ambiguidade atual de "prova conceitual"
   - Exemplos concretos de uso ambíguo

5. **`GOVERNANCE_INTEGRATION_AMBIGUITY_ANALYSIS.md`**
   - Análise de ambiguidade atual de "integração ao método"
   - Exemplos concretos de uso ambíguo

### Evidência (Documental, Não Automação)

6. **`conceptual_proof_binary_integration_proof.md`**
   - Evidência de conformidade (documental)
   - Status de cada fase F1-F7
   - Aplicação das definições em caso real (ex.: DEMANDA-METODO-003)
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
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_PROOF_AMBIGUITY_ANALYSIS.md && echo "OK: documento existe" || echo "FAIL: documento não existe"'

# Exemplo F3 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_CONCEPTUAL_PROOF.md && grep -q "Definição Canônica\|Critérios Binários" /app/METODO/GOVERNANCE_CONCEPTUAL_PROOF.md && echo "OK: documento tem definição e critérios" || echo "Verificar conteúdo"'

# Exemplo F6 (apenas para este projeto)
docker compose exec app bash -c 'test -f /app/METODO/GOVERNANCE_CONCEPTUAL_PROOF.md && grep -q "END-FIRST v2\|Pilar END-FIRST\|Template Canônico" /app/METODO/GOVERNANCE_CONCEPTUAL_PROOF.md && echo "OK: documento integrado ao método" || echo "Verificar integração"'
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

- **Prova:** "Prova conceitual não é sensação de clareza; é critério verificável."
- **Integração:** "Integração ao método não é link; é referência canônica rastreável."
- **Encerramento:** "Se a conclusão depende de leitura humana extensa, o método falhou."
- **Fronteira:** "Conceito governa. Implementação exemplifica."

---

## 📌 STATUS

**⏸️ F-1 PENDENTE APROVAÇÃO**

**Aguardando aprovação de:** CEO (Joubert Jr)  
**Data de criação:** 2026-01-19  
**Declaração canônica:** Aguardando "F-1 APROVADA"

**Observações:**
- Este planejamento segue o padrão canônico estabelecido em DEMANDA-METODO-003
- As definições canônicas serão aplicadas retroativamente em DEMANDA-METODO-003 como evidência
- Nenhuma execução será iniciada sem aprovação explícita

---

## 🧭 REGRA FINAL (CANÔNICA)

> "Se prova e integração não são binárias, demandas de método viram retrabalho."

---

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Template:** `/METODO/TEMPLATE_DEMANDA_CANONICA.md`  
**Demanda:** DEMANDA-METODO-004_PROVA_CONCEITUAL_BINARIA_INTEGRACAO_CANONICA.md
