# PROVAS MÍNIMAS DE ROBUSTEZ — EXECUÇÃO LONGA E STREAMING

**Método:** END-FIRST v2  
**Versão:** 1.0  
**Data:** 2026-01-20  
**Origem:** DEMANDA-METODO-005 v2.0 (F3)  
**Status:** Ativo  

---

## 🎯 OBJETIVO DESTE DOCUMENTO

Este documento define **critérios documentais mínimos** de prova de robustez para demandas da **Classe A** (Execução Longa com Streaming e Persistência).

As provas são **explícitas, verificáveis e independentes de automação**.

---

## 📋 PRINCÍPIOS

1. **Prova é evidência, não opinião**
   - "Funcionou no meu teste" não é prova
   - "HTML 200" não é prova de robustez
   - "Testes antigos passam" não é prova de robustez

2. **Prova pode ser documental, teste ou contrato**
   - Não exige automação obrigatória
   - Exige explicitação do comportamento esperado
   - Exige verificação binária (PASS/FAIL)

3. **Distinção clara: teste funcional vs teste de robustez**
   - Teste funcional valida caminho feliz
   - Teste de robustez valida comportamento sob falha

---

## ✅ PROVAS ACEITAS

### 1. PROVA DE MONOTONICIDADE DE PROGRESSO

**Definição:**
> Progresso nunca regride. Se sistema reportou 10%, nunca reportará 5% posteriormente.

**Formas de prova aceitas:**

**A) Teste automatizado**
```
- Iniciar execução
- Capturar eventos de progresso
- Verificar: progress[i+1] >= progress[i] para todo i
- PASS se monotonicidade garantida
```

**B) Prova documental (contrato de API)**
```markdown
## Contrato de Progresso

- Campo: `progress` (número 0-100)
- Garantia: `progress` é monotônico crescente
- Violação: Se `progress` regredir, é bug crítico
- Evidência: Logs de execução mostram progresso sempre crescente
```

**C) Prova por inspeção de código**
```
- Variável `progress` é write-once ou append-only
- Não existe código que decrementa `progress`
- Estado de progresso é persistido antes de envio
```

**Critério de PASS:**
- ✅ Existe evidência explícita de que progresso não regride
- ✅ Evidência é verificável (teste, contrato, código)

**Critério de FAIL:**
- ❌ "Parece que não regride"
- ❌ "Nunca vi regredir"
- ❌ Ausência de evidência

---

### 2. PROVA DE PERSISTÊNCIA DE RESULTADO

**Definição:**
> Resultado não depende da conexão ativa para existir. Se stream quebrar, resultado não se perde.

**Formas de prova aceitas:**

**A) Teste automatizado**
```
- Iniciar execução
- Aguardar conclusão
- Desconectar stream
- Consultar resultado via API
- PASS se resultado está acessível
```

**B) Prova documental (contrato de API)**
```markdown
## Contrato de Persistência

- Endpoint: `GET /api/result/{id}`
- Garantia: Resultado persiste após conclusão
- Independência: Resultado não depende de stream ativo
- Evidência: Consulta pós-desconexão retorna resultado completo
```

**C) Prova por inspeção de código**
```
- Resultado é salvo em banco de dados/storage
- Salvamento ocorre antes de envio via stream
- Consulta de resultado não depende de conexão ativa
```

**Critério de PASS:**
- ✅ Existe evidência explícita de que resultado persiste
- ✅ Evidência é verificável (teste, contrato, código)

**Critério de FAIL:**
- ❌ "Resultado fica na memória"
- ❌ "Stream é a única forma de acessar resultado"
- ❌ Ausência de evidência

---

### 3. PROVA DE RETOMADA APÓS FALHA

**Definição:**
> Sistema sobrevive à queda de conexão do cliente. Execução continua mesmo se cliente desconectar.

**Formas de prova aceitas:**

**A) Teste automatizado**
```
- Iniciar execução
- Desconectar cliente durante execução
- Aguardar conclusão esperada
- Reconectar e consultar resultado
- PASS se execução completou e resultado está disponível
```

**B) Prova documental (arquitetura)**
```markdown
## Arquitetura de Retomada

- Execução é assíncrona (não depende de conexão ativa)
- Estado é persistido a cada etapa
- Cliente pode reconectar e consultar status
- Evidência: Diagrama de arquitetura mostra desacoplamento
```

**C) Prova por inspeção de código**
```
- Execução roda em background (worker, job queue)
- Estado é salvo periodicamente
- Desconexão do cliente não cancela execução
```

**Critério de PASS:**
- ✅ Existe evidência explícita de que execução sobrevive a desconexão
- ✅ Evidência é verificável (teste, arquitetura, código)

**Critério de FAIL:**
- ❌ "Execução é síncrona"
- ❌ "Desconexão cancela execução"
- ❌ Ausência de evidência

---

### 4. PROVA DE DURABILIDADE DE RESULTADO

**Definição:**
> Resultado não se perde após falha do stream. Cliente pode consultar resultado posteriormente.

**Formas de prova aceitas:**

**A) Teste automatizado**
```
- Iniciar execução
- Forçar falha de stream (kill connection)
- Aguardar conclusão esperada
- Consultar resultado via API
- PASS se resultado está acessível e completo
```

**B) Prova documental (contrato de API)**
```markdown
## Contrato de Durabilidade

- Endpoint: `GET /api/result/{id}`
- Garantia: Resultado persiste mesmo após falha de stream
- TTL: Resultado disponível por N dias/horas
- Evidência: Consulta pós-falha retorna resultado completo
```

**C) Prova por inspeção de código**
```
- Resultado é salvo em storage durável (DB, S3, etc.)
- Salvamento ocorre antes de envio via stream
- Falha de stream não impede salvamento
```

**Critério de PASS:**
- ✅ Existe evidência explícita de que resultado é durável
- ✅ Evidência é verificável (teste, contrato, código)

**Critério de FAIL:**
- ❌ "Resultado só existe durante stream"
- ❌ "Falha de stream perde resultado"
- ❌ Ausência de evidência

---

## ❌ PROVAS NÃO ACEITAS

### 1. "Funcionou no meu teste manual"

**Razão:** Não é reproduzível, não é verificável, não é auditável

**Alternativa:** Documentar teste manual como prova documental com evidência (screenshot, log)

---

### 2. "HTML 200"

**Razão:** Valida caminho feliz, não robustez

**Alternativa:** Teste de falha (desconexão, timeout, erro de rede)

---

### 3. "Testes antigos passam"

**Razão:** Testes funcionais ≠ testes de robustez

**Alternativa:** Criar testes específicos de robustez ou prova documental

---

### 4. "Parece robusto"

**Razão:** Opinião, não evidência

**Alternativa:** Prova explícita (teste, contrato, código)

---

### 5. "Nunca vi quebrar"

**Razão:** Ausência de evidência não é evidência de robustez

**Alternativa:** Teste de falha ou prova documental

---

## 📋 COMO APLICAR ESTAS PROVAS

### Passo 1: Identificar demanda Classe A

1. Consultar `/METODO/CLASSIFICACAO_TIPOS_DEMANDA.md`
2. Verificar se demanda pertence à Classe A
3. Se sim, provas mínimas são obrigatórias

### Passo 2: Escolher forma de prova

Para cada prova mínima (monotonicidade, persistência, retomada, durabilidade):

1. Escolher forma de prova: teste automatizado, prova documental ou inspeção de código
2. Executar prova
3. Registrar evidência na demanda

### Passo 3: Registrar evidência

**Na demanda, criar seção:**

```markdown
## Provas de Robustez (Z10)

### 1. Monotonicidade de Progresso
- **Forma de prova:** [Teste automatizado / Prova documental / Inspeção de código]
- **Evidência:** [Link para teste / Contrato de API / Trecho de código]
- **Resultado:** PASS / FAIL

### 2. Persistência de Resultado
- **Forma de prova:** [...]
- **Evidência:** [...]
- **Resultado:** PASS / FAIL

### 3. Retomada Após Falha
- **Forma de prova:** [...]
- **Evidência:** [...]
- **Resultado:** PASS / FAIL

### 4. Durabilidade de Resultado
- **Forma de prova:** [...]
- **Evidência:** [...]
- **Resultado:** PASS / FAIL
```

### Passo 4: Validar conformidade

- Todas as 4 provas devem ter PASS
- Ausência de prova = FAIL automático
- Prova não aceita = FAIL automático

---

## 🎯 EXEMPLO PRÁTICO: DEMANDA-PROD-002

**Demanda:** "Implementar processamento de log com SSE e histórico"

**Classe:** A (Execução Longa + Streaming + Persistência)

**Provas mínimas obrigatórias:**

### 1. Monotonicidade de Progresso

**Forma de prova:** Teste automatizado

**Evidência:**
```typescript
test('progress is monotonic', async () => {
  const events = await captureSSEEvents('/api/process-log');
  for (let i = 1; i < events.length; i++) {
    expect(events[i].progress).toBeGreaterThanOrEqual(events[i-1].progress);
  }
});
```

**Resultado:** PASS ✅

---

### 2. Persistência de Resultado

**Forma de prova:** Prova documental (contrato de API)

**Evidência:**
```markdown
## API Contract

GET /api/result/{id}

Response:
{
  "id": "string",
  "status": "completed",
  "result": { ... },
  "created_at": "timestamp"
}

Guarantee: Result persists after SSE stream ends
```

**Resultado:** PASS ✅

---

### 3. Retomada Após Falha

**Forma de prova:** Inspeção de código

**Evidência:**
```typescript
// Execution runs in background worker
async function processLog(jobId: string) {
  await jobQueue.add('process-log', { jobId });
  // Execution continues even if client disconnects
}
```

**Resultado:** PASS ✅

---

### 4. Durabilidade de Resultado

**Forma de prova:** Teste automatizado

**Evidência:**
```typescript
test('result survives stream failure', async () => {
  const jobId = await startProcessing();
  await killSSEConnection(); // Force stream failure
  await waitForCompletion(jobId);
  const result = await fetch(`/api/result/${jobId}`);
  expect(result.status).toBe(200);
  expect(result.data).toBeDefined();
});
```

**Resultado:** PASS ✅

---

**Conclusão:** DEMANDA-PROD-002 com provas mínimas teria PASS em Z10 ✅

---

## 🚫 ANTI-PADRÕES

### ❌ Não fazer

**1. "Vou testar manualmente e ver se funciona"**
- Teste manual não é prova reproduzível
- Alternativa: Documentar teste manual como prova documental com evidência

**2. "Já temos testes, não precisa mais"**
- Testes funcionais ≠ testes de robustez
- Alternativa: Criar testes específicos de robustez

**3. "Vou fazer depois que entregar"**
- Provas são obrigatórias antes de PASS/DONE
- Alternativa: Planejar provas no F-1

**4. "Não sei como provar isso"**
- Escolher forma de prova: teste, contrato ou código
- Alternativa: Consultar este documento ou pedir ajuda

---

## 📊 METADADOS

**Versão:** 1.0  
**Criado em:** 2026-01-20  
**Origem:** DEMANDA-METODO-005 v2.0 (Fase F3)  
**Autor:** Manus Agent  
**Revisor:** CEO (pendente)  
**Status:** Ativo  
**Próxima revisão:** Após aplicação em 5+ demandas reais  

---

## 🔗 REFERÊNCIAS

- `/METODO/CLASSIFICACAO_TIPOS_DEMANDA.md` — Classificação de demandas (Classe A)
- `/METODO/GOVERNANCA_GATES.md` — Obrigatoriedade de Z10 para Classe A
- `/DEMANDAS_MANUS/DEMANDA_METODO-005_ROBUSTEZ_EXECUCAO_LONGA.md` — Demanda origem
- `/METODO/END_FIRST_V2.md` — Definição de gates
