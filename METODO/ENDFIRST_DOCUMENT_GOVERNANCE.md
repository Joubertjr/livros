---
document_id: ENDFIRST_DOCUMENT_GOVERNANCE
type: canonical
owner: CEO (Joubert Jr)
status: approved
approved_by: CEO
approved_at: 2026-01-07
governed_by: /METODO/PILAR_ENDFIRST.md
spec_id: EF-2026-002
---

# ENDFIRST — Governança e Aprovação de Documentos

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Governado por:** ENDFIRST_SPEC_EF-2026-002  
**Status:** Canônico (Aprovado pelo CEO)

---

## 🎯 OBJETIVO

Este documento define o processo formal de governança e aprovação de **todos os documentos** no repositório ENDFIRST Ecosystem.

**Verdade estrutural:**
> Nenhum documento "existe oficialmente" sem passar por processo de aprovação explícito.

---

## 🚫 REGRA CRÍTICA: AUTO-APROVAÇÃO PROIBIDA

**Regra obrigatória:**
> Nenhum documento pode ser aprovado por quem o escreveu.

**Motivo:** Conflito de interesse estrutural.

**Consequência:** Documento aprovado por autor é **INVÁLIDO**.

**Aplicação:**
- Manus escreve → CEO aprova
- Cursor escreve → Manus valida, CEO aprova
- CEO escreve → Manus valida, CEO auto-aprova (única exceção)

**Exceção única:** CEO pode auto-aprovar documentos que escreveu (autoridade soberana).

**Todos os outros casos:** Auto-aprovação é PROIBIDA.

---

## 📂 CLASSIFICAÇÃO DE DOCUMENTOS

Todo documento no repositório deve ser classificado em um dos 3 tipos:

### Tipo A — Canônico (Soberano)

**Definição:** Documento soberano que governa outros documentos.

**Características:**
- Define regras, princípios ou templates oficiais
- Mudanças impactam todo o sistema
- Exige máxima integridade estrutural

**Processo de aprovação:**
1. Criar ENDFIRST_SPEC (obrigatório)
2. Validar Spec com CEO (Declaração Final de Passagem)
3. Implementar documento
4. CEO aprova explicitamente
5. Registrar em APPROVAL_LOG.md

**Exemplos:**
- `PILAR_ENDFIRST.md`
- `ENDFIRST_SPEC.md` (template)
- `ENDFIRST_DOCUMENT_GOVERNANCE.md` (este documento)

---

### Tipo B — Operacional

**Definição:** Documento que define processos, ferramentas ou implementações.

**Características:**
- Define "como fazer" algo
- Mudanças impactam execução
- Exige validação técnica

**Processo de aprovação:**
1. Criar documento seguindo template (se existir)
2. Preencher checklist próprio
3. Manus ou Cursor valida tecnicamente
4. CEO aprova se impactar governança
5. Registrar em APPROVAL_LOG.md

**Exemplos:**
- `ENDFIRST_PROCESS.md`
- `PROMPT_CURSOR.md`
- `TEMPLATE_DEMANDA.md`

---

### Tipo C — Exemplo / Apoio

**Definição:** Documento que exemplifica aplicação de templates ou fornece suporte.

**Características:**
- Demonstra uso de templates
- Documenta casos reais
- Não governa outros documentos

**Processo de aprovação:**
1. Seguir template correspondente
2. Validar conformidade (Manus ou Cursor)
3. Não exige aprovação do CEO
4. Registrar em APPROVAL_LOG.md

**Exemplos:**
- `ENDFIRST_SPEC_EF-2026-001_LLM_ORCHESTRATOR.md`
- `README.md` (/METODO/)
- `DEMANDA-001_LLM_ORCHESTRATOR.md`

---

## 📋 METADADOS OBRIGATÓRIOS

Todo documento deve ter **YAML frontmatter** no topo com 7 campos obrigatórios:

```yaml
---
document_id: [ID_UNICO]
type: canonical | operational | example
owner: [Nome do responsável]
status: draft | approved | obsolete
approved_by: [Nome do aprovador]
approved_at: [YYYY-MM-DD]
governed_by: [Path do documento que governa]
---
```

**Campos opcionais:**
```yaml
spec_id: [ID da ENDFIRST_SPEC que governa, se aplicável]
version: [Versão do documento]
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
```

---

## ✅ CRITÉRIOS DE APROVAÇÃO POR TIPO

### Tipo A (Canônico)

**Aprovador:** CEO (obrigatório)

**Checklist:**
- [ ] ENDFIRST_SPEC criada e validada
- [ ] Documento implementado conforme Spec
- [ ] CEO fez Declaração Final de Passagem
- [ ] Metadados YAML preenchidos
- [ ] Registrado em APPROVAL_LOG.md
- [ ] Commit com mensagem estruturada

**Bloqueio:** Não pode ser aprovado sem ENDFIRST_SPEC.

---

### Tipo B (Operacional)

**Aprovador:** Manus ou Cursor (técnico) + CEO (se impactar governança)

**Checklist:**
- [ ] Template seguido (se existir)
- [ ] Checklist próprio preenchido
- [ ] Validação técnica (Manus/Cursor)
- [ ] CEO aprova se impactar governança
- [ ] Metadados YAML preenchidos
- [ ] Registrado em APPROVAL_LOG.md

**Bloqueio:** Não pode ser aprovado sem validação técnica.

---

### Tipo C (Exemplo/Apoio)

**Aprovador:** Manus ou Cursor (conformidade)

**Checklist:**
- [ ] Template seguido corretamente
- [ ] Conformidade validada
- [ ] Metadados YAML preenchidos
- [ ] Registrado em APPROVAL_LOG.md

**Bloqueio:** Não pode ser aprovado sem seguir template.

---

## 📊 RASTRO DE DECISÃO

Todo documento aprovado deve ter entrada em `/METODO/APPROVAL_LOG.md` com:

- **document_id:** Identificador único
- **type:** Tipo (A, B ou C)
- **status:** Status atual
- **approved_by:** Quem aprovou
- **approved_at:** Quando aprovou
- **reason:** Por que foi aprovado
- **governed_by:** Documento que governa
- **commit:** Link para commit/PR

**Exemplo:**
```markdown
| document_id | type | status | approved_by | approved_at | reason | governed_by | commit |
|-------------|------|--------|-------------|-------------|--------|-------------|--------|
| PILAR_ENDFIRST | canonical | approved | CEO | 2026-01-07 | Núcleo operacional validado | Si mesmo | [80971a5] |
```

---

## 🔄 APROVAÇÕES RETROATIVAS

Documentos criados **antes** deste sistema de governança existir podem ser aprovados retroativamente, mas:

**Regras:**
1. CEO deve revisar explicitamente (não automático)
2. Documento deve ser classificado (Tipo A, B ou C)
3. Metadados YAML devem ser adicionados
4. Entrada em APPROVAL_LOG.md deve ser criada
5. Motivo da aprovação retroativa deve ser registrado

**Bloqueio:** Não pode marcar como "aprovado" sem revisão real.

---

## 🚫 ANTI-GAMING / PROTEÇÕES

### Proteção 1: Metadados não podem ser "preenchidos para passar"
CEO deve revisar e confirmar aprovação explicitamente.

### Proteção 2: Classificação não pode ser auto-atribuída
Manus ou CEO devem validar classificação de tipo.

### Proteção 3: Aprovações retroativas não podem ser automáticas
CEO deve revisar cada documento antigo explicitamente.

### Proteção 4: Status não pode mudar sem registro
Toda mudança de status exige entrada no APPROVAL_LOG.md.

### Proteção 5: Tipo A não pode ser criado sem ENDFIRST_SPEC
Bloquear criação de Canônicos sem passar pelo Pilar ENDFIRST.

---

## 🔗 INTEGRAÇÃO COM SISTEMA ANTIGO (13 Pilares)

**Decisão:** Pilar ENDFIRST governa tudo.

**Relação:**
- **Pilar ENDFIRST** → Define COMO criar especificações (meta-pilar)
- **13 Pilares** → Define O QUE incluir nas demandas (método operacional)

**Consequência:**
- `TEMPLATE_DEMANDA.md` (8 pilares) continua válido para demandas operacionais
- Mas demandas estratégicas devem passar pelo Pilar ENDFIRST primeiro
- Documentação dos "13 Pilares" vira backlog futuro (não verdade atual)

**Documento de integração:** `/METODO/INTEGRATION_13_PILARES.md` (a criar)

---

## 📊 AUDITORIA

**Frequência:** A cada 10 documentos novos OU 1x por mês (o que ocorrer primeiro)

**Checklist de auditoria:**
- [ ] Todos os documentos têm YAML frontmatter?
- [ ] Todos os documentos estão em APPROVAL_LOG.md?
- [ ] Status no YAML = Status no APPROVAL_LOG?
- [ ] Documentos Tipo A têm ENDFIRST_SPEC?
- [ ] Documentos Tipo B têm validação técnica?
- [ ] Documentos Tipo C seguem templates?

**Responsável:** Manus (Agent)

---

## 🎯 RESULTADO ESPERADO

Quando este documento estiver operacional, será verdade que:

1. ✅ Todo documento tem tipo explícito (Canônico, Operacional, Exemplo)
2. ✅ Todo documento tem metadados obrigatórios (7 campos)
3. ✅ Nenhum documento existe oficialmente sem aprovação explícita
4. ✅ Critérios de aprovação são diferentes por tipo
5. ✅ Existe rastro de decisão auditável (APPROVAL_LOG.md)

**Validação:**
> CEO consegue responder "todos os arquivos estão aprovados?" olhando log + metadados, sem interpretação.

---

## 📜 DECLARAÇÃO FINAL

**Este documento foi aprovado pelo CEO em 7 de Janeiro de 2026.**

**Status:** Canônico (Aprovado)  
**Governado por:** ENDFIRST_SPEC_EF-2026-002

---

**Versão:** 1.0  
**Data:** 7 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Próximo passo:** Implementar APPROVAL_LOG.md e padronizar YAML em todos os documentos
