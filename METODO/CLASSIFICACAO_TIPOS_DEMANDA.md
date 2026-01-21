# CLASSIFICAÇÃO DE TIPOS DE DEMANDA

**Método:** END-FIRST v2  
**Versão:** 1.0  
**Data:** 2026-01-20  
**Origem:** DEMANDA-METODO-005 v2.0 (F1)  
**Status:** Ativo  

---

## 🎯 OBJETIVO DESTE DOCUMENTO

Este documento define **classificações canônicas de demandas** para determinar **quando gates específicos (ex: Z10) são obrigatórios**.

A classificação é **objetiva, verificável e independente de opinião**.

---

## 📋 PRINCÍPIOS DE CLASSIFICAÇÃO

1. **Classificação é estrutural, não subjetiva**
   - Baseada em características técnicas da demanda
   - Não baseada em "complexidade percebida"
   - Não baseada em "experiência do time"

2. **Classificação determina obrigatoriedade de gates**
   - Certas classes → certos gates obrigatórios
   - Dispensa de gate exige justificativa explícita e registrada

3. **Classificação é binária**
   - Demanda pertence ou não pertence a uma classe
   - Sem "meio-termo" ou "depende"

---

## 🏷️ CLASSES DE DEMANDA

### CLASSE A — Execução Longa com Streaming e Persistência

**Definição:**

Demanda pertence a esta classe se **todas** as condições abaixo são verdadeiras:

1. **Execução longa**
   - Processamento que leva mais de 5 segundos
   - OU processamento assíncrono (não retorna imediatamente)

2. **Streaming de progresso**
   - Sistema envia atualizações incrementais durante execução
   - Tecnologias: SSE (Server-Sent Events), WebSocket, polling progressivo
   - Usuário vê progresso em tempo real

3. **Persistência de resultado**
   - Resultado é armazenado após conclusão
   - Resultado pode ser consultado posteriormente
   - Resultado não depende da conexão ativa para existir

4. **Retomada ou consulta posterior**
   - Usuário pode desconectar e reconectar
   - OU usuário pode consultar resultado depois
   - Sistema garante que resultado não se perde

**Exemplos:**
- ✅ Processamento de log com SSE e histórico
- ✅ Geração de relatório com progresso e download posterior
- ✅ Análise de dados com streaming de status e resultado persistido
- ✅ Build/deploy com log em tempo real e resultado consultável

**Contra-exemplos:**
- ❌ API REST síncrona (retorna em < 1s)
- ❌ Consulta de banco de dados simples
- ❌ Upload de arquivo sem processamento
- ❌ Operação CRUD básica

---

### CLASSE B — Operação Crítica de Negócio

**Definição:**

Demanda pertence a esta classe se **qualquer** condição abaixo é verdadeira:

1. **Impacto financeiro direto**
   - Transação monetária
   - Cobrança/pagamento
   - Alteração de saldo/crédito

2. **Impacto em dados críticos**
   - Exclusão de dados
   - Alteração de permissões/acessos
   - Migração de dados

3. **Impacto em disponibilidade**
   - Mudança em infraestrutura
   - Alteração de configuração de produção
   - Deploy de componente crítico

**Exemplos:**
- ✅ Processamento de pagamento
- ✅ Exclusão de conta de usuário
- ✅ Migração de banco de dados
- ✅ Deploy de API principal

**Contra-exemplos:**
- ❌ Atualização de perfil de usuário
- ❌ Consulta de dados
- ❌ Geração de relatório não-financeiro

---

### CLASSE C — Interface de Usuário Complexa

**Definição:**

Demanda pertence a esta classe se **qualquer** condição abaixo é verdadeira:

1. **Múltiplos estados de UI**
   - Loading, erro, sucesso, vazio, parcial
   - Transições entre estados

2. **Interação rica**
   - Drag-and-drop
   - Edição inline
   - Validação em tempo real

3. **Responsividade multi-dispositivo**
   - Desktop, tablet, mobile
   - Orientação portrait/landscape

**Exemplos:**
- ✅ Dashboard com múltiplos widgets
- ✅ Editor de texto rico
- ✅ Formulário multi-etapa com validação

**Contra-exemplos:**
- ❌ Página estática de conteúdo
- ❌ Formulário simples (1-3 campos)
- ❌ Botão de ação única

---

### CLASSE D — Integração Externa

**Definição:**

Demanda pertence a esta classe se **qualquer** condição abaixo é verdadeira:

1. **Chamada a API externa**
   - Serviço de terceiros
   - API pública
   - Webhook externo

2. **Dependência de serviço externo**
   - Autenticação OAuth
   - Pagamento (Stripe, PayPal)
   - Armazenamento (S3, GCS)

3. **Sincronização com sistema externo**
   - CRM, ERP
   - Sistema legado
   - Banco de dados externo

**Exemplos:**
- ✅ Integração com Stripe
- ✅ Login via Google OAuth
- ✅ Upload para S3
- ✅ Sincronização com Salesforce

**Contra-exemplos:**
- ❌ Operação 100% interna
- ❌ Consulta a banco de dados próprio
- ❌ Lógica de negócio isolada

---

## 🔗 RELAÇÃO COM GATES

### Classe A → Z10 OBRIGATÓRIO

**Demandas da Classe A (Execução Longa com Streaming e Persistência) exigem obrigatoriamente:**

- **Gate Z10 (Qualidade de Produto)**
- **Provas mínimas de robustez** (ver `/METODO/PROVAS_MINIMAS_ROBUSTEZ.md`)

**Exceção:**
- Dispensa de Z10 exige justificativa explícita e registrada na demanda
- Ausência de decisão explícita = FAIL automático

**Razão:**
- Classe A envolve estado distribuído (cliente + servidor)
- Falha de conexão é cenário real, não edge case
- Progresso que regride = bug crítico
- Resultado que se perde = promessa falsa

---

### Classe B → Z10 RECOMENDADO

**Demandas da Classe B (Operação Crítica de Negócio) devem considerar:**

- Gate Z10 (Qualidade de Produto)
- Testes de cenários de falha
- Rollback/recovery

**Não obrigatório, mas fortemente recomendado.**

---

### Classe C → Z11 OBRIGATÓRIO

**Demandas da Classe C (Interface de Usuário Complexa) exigem:**

- Gate Z11 (UI/UX)
- Validação de estados de UI
- Testes de responsividade

---

### Classe D → Z10 RECOMENDADO

**Demandas da Classe D (Integração Externa) devem considerar:**

- Gate Z10 (Qualidade de Produto)
- Tratamento de timeout
- Fallback para falha de serviço externo

**Não obrigatório, mas fortemente recomendado.**

---

## ✅ CRITÉRIOS DE USO

### Como classificar uma demanda

1. **Ler definição de cada classe**
2. **Verificar se demanda atende aos critérios**
3. **Classificação é binária:** pertence ou não pertence
4. **Demanda pode pertencer a múltiplas classes**

### Exemplo prático

**DEMANDA-PROD-002:** "Implementar processamento de log com SSE e histórico"

**Verificação:**
- Execução longa? ✅ (processamento assíncrono)
- Streaming? ✅ (SSE)
- Persistência? ✅ (histórico)
- Retomada? ✅ (consulta posterior)

**Classificação:** Classe A ✅

**Consequência:** Z10 obrigatório

---

## 🚫 ANTI-PADRÕES

### ❌ Não fazer

- **"Parece simples, então não é Classe A"**
  - Classificação é estrutural, não subjetiva

- **"Já temos testes, então não precisa Z10"**
  - Testes funcionais ≠ provas de robustez

- **"Vamos ver se quebra, depois a gente arruma"**
  - Classe A → Z10 obrigatório, não opcional

- **"Não tenho tempo para Z10"**
  - Dispensa exige justificativa explícita e registrada

---

## 📊 METADADOS

**Versão:** 1.0  
**Criado em:** 2026-01-20  
**Origem:** DEMANDA-METODO-005 v2.0 (Fase F1)  
**Autor:** Manus Agent  
**Revisor:** CEO (pendente)  
**Status:** Ativo  
**Próxima revisão:** Após aplicação em 5+ demandas reais  

---

## 🔗 REFERÊNCIAS

- `/DEMANDAS_MANUS/DEMANDA_METODO-005_ROBUSTEZ_EXECUCAO_LONGA.md`
- `/METODO/PROVAS_MINIMAS_ROBUSTEZ.md` (a ser criado em F3)
- `/METODO/PILAR_ENDFIRST.md` (a ser atualizado em F5)
