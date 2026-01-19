---
document_id: APPROVAL_LOG_RULES
type: operational
owner: Manus (Agent)
status: approved
approved_by: CEO
approved_at: 2026-01-08
governed_by: /METODO/ENDFIRST_DOCUMENT_GOVERNANCE.md
---

# Approval Log Rules

**Versão:** 1.0  
**Data:** 8 de Janeiro de 2026  
**Governado por:** ENDFIRST_DOCUMENT_GOVERNANCE.md  
**Status:** Operacional (Aprovado pelo CEO)

---

## 🎯 OBJETIVO

Este documento define **regras estruturais** para o APPROVAL_LOG.md que **matam estados inválidos por definição**.

**Função:**
> Transformar "esqueci de preencher" em erro impossível.

---

## 🚫 REGRAS OBRIGATÓRIAS

### Regra 1: `commit: TBD` é PROIBIDO

**Definição:**
> Nenhuma entrada no APPROVAL_LOG.md pode conter `commit: TBD`.

**Motivo:**
- TBD significa "rastreabilidade quebrada"
- Não é possível auditar aprovação sem commit hash
- Cria dívida técnica de governança

**Ação correta:**
- Preencher com hash real do commit que aprovou
- Se commit ainda não existe, NÃO criar entrada no log
- Aprovação só pode apontar para commits existentes

**Exceção:**
- ❌ NENHUMA. TBD é sempre inválido.

---

### Regra 2: Toda entrada deve conter hash real

**Definição:**
> A coluna `commit` deve sempre conter um hash Git válido de 7+ caracteres.

**Formato válido:**
```markdown
| document_id | ... | commit |
|-------------|-----|--------|
| DOC_001 | ... | [abc1234](https://github.com/user/repo/commit/abc1234) |
```

**Formato inválido:**
```markdown
| document_id | ... | commit |
|-------------|-----|--------|
| DOC_001 | ... | TBD |
| DOC_002 | ... | [pendente] |
| DOC_003 | ... | - |
```

**Verificação:**
- Hash deve existir no histórico Git
- Link deve apontar para commit real no GitHub
- Commit deve conter as mudanças referenciadas

---

### Regra 3: APPROVAL_LOG nunca pode "prever" commits futuros

**Definição:**
> Não é permitido registrar aprovação antes do commit existir.

**Sequência correta:**
1. Fazer mudanças nos documentos
2. Atualizar APPROVAL_LOG.md
3. Fazer commit (único, atômico)
4. Hash do commit aparece no APPROVAL_LOG

**Sequência incorreta:**
1. ❌ Atualizar APPROVAL_LOG com TBD
2. ❌ Fazer commit
3. ❌ "Depois eu volto e preencho o hash"

**Motivo:**
- Aprovação e mudança devem ser atômicas
- Log não pode estar em estado intermediário
- Rastreabilidade deve ser imediata

---

### Regra 4: Aprovação só pode apontar para commits existentes

**Definição:**
> Todo hash no APPROVAL_LOG deve ser verificável via `git log`.

**Verificação:**
```bash
# Hash deve existir
git log --oneline | grep abc1234

# Commit deve conter mudanças do documento
git show abc1234 -- path/to/document.md
```

**Ação se hash não existe:**
- ❌ Entrada é inválida
- ✅ Corrigir com commit real
- ✅ Ou remover entrada do log

---

### Regra 5: Totais devem ser derivados da lista real de documentos

**Definição:**
> Estatísticas no APPROVAL_LOG devem refletir contagem real, não estimativa.

**Cálculo correto:**
```bash
# Contar documentos governados
find . -name "*.md" -type f | grep -v node_modules | grep -v .git | wc -l
```

**Atualizar estatísticas:**
```markdown
## 📋 ESTATÍSTICAS

**Total de documentos no repositório:** [CONTAGEM_REAL]
**Aprovados:** [CONTAGEM_APPROVED]
**Pendentes:** [CONTAGEM_PENDING]
```

**Proibido:**
- ❌ Estimar total ("acho que são 17")
- ❌ Copiar número antigo sem verificar
- ❌ Incluir documentos que não existem

**Obrigatório:**
- ✅ Contar arquivos .md no repositório
- ✅ Verificar cada entrada do log
- ✅ Total = Aprovados + Pendentes + Obsoletos

---

## 📊 VALIDAÇÃO DE CONFORMIDADE

### Checklist de Validação do APPROVAL_LOG

Para validar se APPROVAL_LOG.md está conforme:

**Verificação 1: Nenhum TBD**
```bash
grep -i "TBD" METODO/APPROVAL_LOG.md
# Resultado esperado: nenhuma linha encontrada
```

**Verificação 2: Todos os hashes são válidos**
```bash
# Extrair hashes do log
grep -oP '\[([a-f0-9]{7,})\]' METODO/APPROVAL_LOG.md

# Verificar cada hash existe
git log --oneline | grep [HASH]
```

**Verificação 3: Contagem bate com realidade**
```bash
# Contar documentos
find . -name "*.md" -type f | grep -v node_modules | grep -v .git | wc -l

# Comparar com total no log
grep "Total de documentos" METODO/APPROVAL_LOG.md
```

**Status:**
- ✅ CONFORME: Todas as verificações passam
- ❌ NÃO CONFORME: Uma ou mais verificações falham

---

## 🔄 PROCESSO DE CORREÇÃO

### Se APPROVAL_LOG estiver não conforme:

**Passo 1: Identificar problemas**
- Rodar checklist de validação
- Listar todas as inconsistências

**Passo 2: Corrigir inconsistências**
- Substituir TBD por hashes reais
- Recalcular totais
- Verificar sincronização com YAML

**Passo 3: Criar commit de correção**
- Mensagem: `fix(governance): corrigir [PROBLEMA] no APPROVAL_LOG`
- Incluir justificativa no commit message
- Registrar correção no histórico do log

**Passo 4: Validar novamente**
- Rodar checklist de validação
- Confirmar que todas as verificações passam

---

## 🧠 POR QUE ESTAS REGRAS EXISTEM

**Problema identificado:**
- TBD criava "dívida de governança"
- Contagens fantasma quebravam auditoria
- Correções retroativas frequentes

**Solução:**
- Regras estruturais que impedem estados inválidos
- Validação automatizável (grep, wc, git log)
- Governança verificável sem interpretação

**Resultado esperado:**
- ❌ TBD nunca mais aparece (Regra 1)
- ❌ Hashes inválidos não entram (Regra 2)
- ❌ Aprovações futuras não existem (Regra 3)
- ✅ Rastreabilidade perfeita (Regra 4)
- ✅ Estatísticas sempre corretas (Regra 5)

---

## 📚 DOCUMENTOS RELACIONADOS

- **APPROVAL_LOG.md** — Log de aprovações (governado por estas regras)
- **COMMIT_GOVERNANCE_CHECKLIST.md** — Checklist de conformidade de commits
- **ENDFIRST_DOCUMENT_GOVERNANCE.md** — Governança canônica

---

## 🔒 REGRA DE ENFORCEMENT

**Estas regras são obrigatórias, não opcionais.**

**Enforcement:**
1. **Manual:** Revisor verifica conformidade antes de aprovar commit
2. **Automatizado (futuro):** CI/CD valida regras automaticamente
3. **Auditoria:** CEO pode auditar conformidade a qualquer momento

**Penalidade por violação:**
- Commit é considerado NÃO CONFORME
- Deve ser corrigido com novo commit
- Não pode ser ignorado ou "aceito parcialmente"

---

## 📋 EXEMPLO DE APLICAÇÃO

### Antes (NÃO CONFORME):

```markdown
| TEMPLATE_DEMANDA | operational | approved | CEO | 2026-01-08 | ... | [TBD] |
| DOC_002 | example | approved | CEO | 2026-01-08 | ... | [pendente] |

**Total de documentos:** 17 (estimativa)
```

**Problemas:**
- ❌ TBD presente (Regra 1)
- ❌ "pendente" não é hash (Regra 2)
- ❌ Total é estimativa (Regra 5)

---

### Depois (CONFORME):

```markdown
| TEMPLATE_DEMANDA | operational | approved | CEO | 2026-01-08 | ... | [178e186](https://github.com/.../178e186) |
| DOC_002 | example | approved | CEO | 2026-01-08 | ... | [4b8957a](https://github.com/.../4b8957a) |

**Total de documentos:** 14 (contagem real)
```

**Conformidade:**
- ✅ Hashes reais (Regra 1, 2)
- ✅ Commits existem (Regra 4)
- ✅ Total verificável (Regra 5)

---

**Versão:** 1.0  
**Criado:** 8 de Janeiro de 2026  
**Criado por:** Manus (Agent)  
**Aprovado por:** CEO (Joubert Jr)  
**Status:** Operacional
