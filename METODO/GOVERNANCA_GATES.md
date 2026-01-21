# GOVERNANÇA DE GATES — END-FIRST v2

**Método:** END-FIRST v2  
**Versão:** 1.0  
**Data:** 2026-01-20  
**Origem:** DEMANDA-METODO-005 v2.0 (F2)  
**Status:** Ativo  

---

## 🎯 OBJETIVO DESTE DOCUMENTO

Este documento define **quando gates específicos são obrigatórios** com base na **classificação de demandas**.

A obrigatoriedade é **binária, não opinativa e auditável**.

---

## 📋 PRINCÍPIOS DE GOVERNANÇA

1. **Obrigatoriedade é estrutural, não subjetiva**
   - Baseada na classe da demanda (ver `/METODO/CLASSIFICACAO_TIPOS_DEMANDA.md`)
   - Não baseada em "complexidade percebida"
   - Não baseada em "tempo disponível"

2. **Dispensa de gate exige justificativa explícita**
   - Ausência de decisão explícita = FAIL automático
   - Justificativa deve ser registrada na demanda
   - Justificativa deve ser aprovada pelo CEO ou arquiteto responsável

3. **Gates não são negociáveis por conveniência**
   - "Não tenho tempo" não é justificativa válida
   - "Parece simples" não é justificativa válida
   - "Já temos testes" não é justificativa válida

---

## 🔒 GATES OBRIGATÓRIOS POR CLASSE

### CLASSE A → Z10 OBRIGATÓRIO

**Classe A:** Execução Longa com Streaming e Persistência

**Gate obrigatório:** Z10 (Qualidade de Produto)

**Razão:**
- Classe A envolve estado distribuído (cliente + servidor)
- Falha de conexão é cenário real, não edge case
- Progresso que regride = bug crítico
- Resultado que se perde = promessa falsa

**Regra binária:**
```
SE demanda ∈ Classe A
ENTÃO Z10 é OBRIGATÓRIO
  OU dispensa explícita e registrada
```

**Dispensa válida requer:**
1. Justificativa técnica explícita
2. Aprovação do CEO ou arquiteto responsável
3. Registro na demanda (seção "Dispensa de Z10")
4. Análise de risco documentada

**Exemplos de justificativa válida:**
- ✅ "Sistema é read-only, sem persistência de estado"
- ✅ "Execução é síncrona, não há streaming"
- ✅ "Demanda é prova de conceito descartável"

**Exemplos de justificativa inválida:**
- ❌ "Não tenho tempo para Z10"
- ❌ "Parece simples, não precisa"
- ❌ "Já temos testes funcionais"

**Consequência de violação:**
- FAIL automático da demanda
- Demanda não pode ser declarada PASS/DONE
- Correção obrigatória antes de prosseguir

---

### CLASSE B → Z10 RECOMENDADO

**Classe B:** Operação Crítica de Negócio

**Gate recomendado:** Z10 (Qualidade de Produto)

**Razão:**
- Impacto financeiro ou de dados críticos
- Falha pode ter consequências graves
- Rollback/recovery são essenciais

**Regra:**
```
SE demanda ∈ Classe B
ENTÃO Z10 é RECOMENDADO
  (não obrigatório, mas fortemente sugerido)
```

**Dispensa não requer justificativa formal**, mas executor deve considerar:
- Testes de cenários de falha
- Estratégia de rollback
- Monitoramento de erros

---

### CLASSE C → Z11 OBRIGATÓRIO, Z13 OBRIGATÓRIO

**Classe C:** Interface de Usuário Complexa

**Gates obrigatórios:**
- Z11 (END-USER SMOKE)
- Z13 (UI/UX Sistêmica)

**Razão:**
- Múltiplos estados de UI exigem validação end-to-end
- Responsividade multi-dispositivo não é opcional
- Consistência visual é requisito de engenharia

**Regra binária:**
```
SE demanda ∈ Classe C
ENTÃO Z11 E Z13 são OBRIGATÓRIOS
  OU dispensa explícita e registrada
```

**Dispensa válida requer:**
1. Justificativa técnica explícita
2. Aprovação do CEO ou arquiteto responsável
3. Registro na demanda

---

### CLASSE D → Z10 RECOMENDADO

**Classe D:** Integração Externa

**Gate recomendado:** Z10 (Qualidade de Produto)

**Razão:**
- Dependência de serviço externo
- Timeout e falha de rede são cenários reais
- Fallback é essencial para resiliência

**Regra:**
```
SE demanda ∈ Classe D
ENTÃO Z10 é RECOMENDADO
  (não obrigatório, mas fortemente sugerido)
```

**Dispensa não requer justificativa formal**, mas executor deve considerar:
- Tratamento de timeout
- Fallback para falha de serviço externo
- Retry com backoff exponencial

---

## 🔒 GATES OBRIGATÓRIOS UNIVERSAIS

### Z12 — OBRIGATÓRIO PARA TODAS AS DEMANDAS

**Gate Z12 (Auditoria Canônica)** é obrigatório para **toda e qualquer demanda**, independentemente da classe.

**Razão:**
- Valida conformidade com o método END-FIRST
- Garante integridade da documentação
- Verifica coerência entre planejamento e execução

**Regra:**
```
PARA TODA demanda
  Z12 é OBRIGATÓRIO
  (sem exceções)
```

**Dispensa:** Não permitida

---

### Z13 — OBRIGATÓRIO PARA DEMANDAS COM UI

**Gate Z13 (UI/UX Sistêmica)** é obrigatório para **toda demanda que envolva UI/UX**.

**Razão:**
- Elimina subjetividade da avaliação de UI
- Garante consistência visual e funcional
- Transforma avaliação em checklist auditável

**Regra:**
```
SE demanda envolve UI/UX
ENTÃO Z13 é OBRIGATÓRIO
  (sem exceções)
```

**Dispensa:** Não permitida

---

## ✅ COMO APLICAR ESTA GOVERNANÇA

### Passo 1: Classificar a demanda

1. Ler `/METODO/CLASSIFICACAO_TIPOS_DEMANDA.md`
2. Verificar se demanda atende aos critérios de cada classe
3. Registrar classificação na demanda

### Passo 2: Identificar gates obrigatórios

1. Consultar este documento (`/METODO/GOVERNANCA_GATES.md`)
2. Identificar gates obrigatórios para a classe
3. Adicionar gates obrigatórios ao TODO da demanda

### Passo 3: Executar ou dispensar gates

**Se executar:**
- Seguir critérios de PASS/FAIL do gate
- Registrar evidência de execução
- Declarar PASS/FAIL

**Se dispensar:**
- Escrever justificativa técnica explícita
- Obter aprovação do CEO ou arquiteto responsável
- Registrar dispensa na demanda (seção "Dispensa de [Gate]")
- Documentar análise de risco

### Passo 4: Validar conformidade

- Ausência de decisão explícita = FAIL automático
- Gate obrigatório não executado e não dispensado = FAIL automático
- Demanda não pode ser declarada PASS/DONE até conformidade

---

## 🚫 ANTI-PADRÕES

### ❌ Não fazer

**1. "Não é complexo, então não precisa de Z10"**
- Classificação é estrutural, não subjetiva
- Se demanda ∈ Classe A → Z10 obrigatório

**2. "Já temos testes, então não precisa de Z10"**
- Testes funcionais ≠ provas de robustez
- Z10 exige provas específicas (ver `/METODO/PROVAS_MINIMAS_ROBUSTEZ.md`)

**3. "Vamos ver se quebra, depois a gente arruma"**
- Gates são preventivos, não reativos
- Classe A → Z10 obrigatório antes de PASS/DONE

**4. "Não tenho tempo para Z10"**
- Tempo não é justificativa válida
- Dispensa exige justificativa técnica e aprovação

**5. "CEO não está disponível para aprovar dispensa"**
- Ausência de aprovação = gate obrigatório
- Não executar gate obrigatório = FAIL automático

---

## 📊 EXEMPLOS PRÁTICOS

### Exemplo 1: DEMANDA-PROD-002

**Descrição:** "Implementar processamento de log com SSE e histórico"

**Classificação:**
- Execução longa? ✅
- Streaming? ✅ (SSE)
- Persistência? ✅ (histórico)
- Retomada? ✅ (consulta posterior)

**Classe:** A ✅

**Gates obrigatórios:**
- Z10 (Qualidade de Produto) ✅
- Z12 (Auditoria Canônica) ✅

**Resultado:**
- Z10 não foi executado na v1 da demanda
- Bug chegou ao usuário (progresso regrediu, resultado se perdeu)
- Violação de governança detectada retroativamente

**Ação corretiva:**
- DEMANDA-METODO-005 criada para corrigir lacuna do método
- Governança de gates formalizada neste documento

---

### Exemplo 2: Demanda hipotética — "Adicionar botão de logout"

**Descrição:** "Adicionar botão de logout na navbar"

**Classificação:**
- Execução longa? ❌
- Streaming? ❌
- Persistência? ❌
- UI? ✅ (simples)

**Classe:** Nenhuma (operação simples)

**Gates obrigatórios:**
- Z12 (Auditoria Canônica) ✅ (universal)
- Z13 (UI/UX Sistêmica) ❌ (UI não é complexa)

**Resultado:**
- Z10 não é obrigatório
- Z13 não é obrigatório (UI simples)
- Z12 é obrigatório (universal)

---

### Exemplo 3: Demanda hipotética — "Integração com Stripe"

**Descrição:** "Implementar pagamento via Stripe"

**Classificação:**
- Integração externa? ✅
- Operação crítica? ✅ (transação financeira)

**Classe:** B (Crítica) + D (Integração Externa)

**Gates obrigatórios:**
- Z12 (Auditoria Canônica) ✅ (universal)

**Gates recomendados:**
- Z10 (Qualidade de Produto) ✅ (fortemente recomendado)

**Resultado:**
- Z10 não é obrigatório, mas fortemente recomendado
- Executor deve considerar: timeout, fallback, retry, rollback

---

## 📊 METADADOS

**Versão:** 1.0  
**Criado em:** 2026-01-20  
**Origem:** DEMANDA-METODO-005 v2.0 (Fase F2)  
**Autor:** Manus Agent  
**Revisor:** CEO (pendente)  
**Status:** Ativo  
**Próxima revisão:** Após aplicação em 5+ demandas reais  

---

## 🔗 REFERÊNCIAS

- `/METODO/CLASSIFICACAO_TIPOS_DEMANDA.md` — Classificação de demandas por tipo
- `/METODO/PROVAS_MINIMAS_ROBUSTEZ.md` — Provas mínimas de robustez (a ser criado em F3)
- `/METODO/END_FIRST_V2.md` — Definição de gates Z12 e Z13
- `/METODO/GATE_Z13_UI_UX_SISTEMICA.md` — Definição detalhada de Z13
- `/DEMANDAS_MANUS/DEMANDA_METODO-005_ROBUSTEZ_EXECUCAO_LONGA.md` — Demanda origem
