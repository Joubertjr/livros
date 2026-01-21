# ORDENS DO CEO PARA O CURSOR

**Data:** 2026-01-21  
**Método:** END-FIRST v2  
**Status:** ATIVO (ORDENS OBRIGATÓRIAS)

---

## 🚫 ORDEM 1 — PARAR EXECUÇÃO DE PRODUTO AGORA

**❌ "Não execute nenhuma DEMANDA-PROD enquanto não houver F-1 aprovado."**

### Justificativa

Isso evita:
- Perda de progresso
- Retrabalho
- Bugs estruturais

### Regra Binária

```
SE demanda ∈ {PROD}
E F-1 não existe OU F-1 não está aprovada
ENTÃO EXECUÇÃO = BLOQUEADA
```

### Exceções

Nenhuma. Esta regra é absoluta.

---

## 🔍 ORDEM 2 — AUDITORIA TOTAL END-FIRST v2

**"Faça uma auditoria END-FIRST v2 do repositório livros."**

### Escopo Obrigatório da Auditoria

O Cursor deve gerar um relatório, contendo para **CADA DEMANDA**:

1. **Tipo:** PROD / METODO / UX / BUG
2. **Classe:** A / B / C / D / NÃO DEFINIDA
3. **Existe F-1?** (SIM / NÃO)
4. **Z10 é obrigatório?** (SIM / NÃO / NÃO DEFINIDO)
5. **Pode executar agora?** (SIM / BLOQUEADA)
6. **Risco de retrabalho?** (ALTO / MÉDIO / BAIXO)

### Critério de Auditoria

**Sem corrigir nada. Só mapear.**

O relatório deve ser salvo em `trns/AUDITORIA_ENDFIRST_V2.md`

---

## 📋 ORDEM 3 — PRIORIZAÇÃO CANÔNICA (NÃO OPINIÃO)

Depois da auditoria, o Cursor deve ordenar:

### Ordem Obrigatória de Resolução

1. **DEMANDA-METODO-006** (se existir)
   - Governa consumo do método, Cursor e onboarding
   - **NOTA:** DEMANDA-METODO-006 não encontrada no repositório. Verificar se foi criada ou se é referência a outra demanda.

2. **F-1 da DEMANDA-PROD-004**
   - Persistência progressiva e retomada
   - **Classe A** (execução longa + streaming + persistência)
   - **Z10 obrigatório**

3. **Execução da DEMANDA-PROD-004**
   - Com Z10, provas de robustez, checkpoints
   - **Só após F-1 aprovada**

4. **Só depois:**
   - Ajustes de UX
   - Refinamentos
   - Otimizações

---

## 🧭 ORDEM 4 — REGRA DE OURO PARA O CURSOR

**Esta regra deve ser colada literalmente no `.cursorrules`:**

> "Cursor: você não resolve 'todas as demandas'.
> Você resolve uma demanda por vez,
> somente se ela tiver END claro, classe definida e F-1 aprovado."

### Aplicação Binária

```
SE demanda não tem END claro
OU demanda não tem classe definida
OU demanda não tem F-1 aprovado (se exigir F-1)
ENTÃO EXECUÇÃO = BLOQUEADA
```

---

## 🚫 O QUE O CURSOR NÃO DEVE FAZER AGORA

❌ "Resolve tudo"  
❌ "Vai implementando"  
❌ "Depois a gente ajusta"  
❌ "Isso é simples"

**Tudo isso já custou retrabalho, e o método já mostrou isso.**

---

## 📌 STATUS DAS ORDENS

**Todas as ordens acima são OBRIGATÓRIAS e ATIVAS.**

**Violação de qualquer ordem = FAIL estrutural do projeto.**

---

**Documento criado:** 2026-01-21  
**Última atualização:** 2026-01-21  
**Governado por:** END-FIRST v2
