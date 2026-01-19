# Proposta Metodológica — Gate Z11: END-USER SMOKE / FRONTEND

**Tipo:** Proposta de Atualização do Método  
**Data:** 2026-01-19  
**Status:** PROPOSTA (aguardando aprovação)

---

## 1. ANÁLISE DA FALHA ESTRUTURAL

### Por que o método permitiu declarar PASS com UI quebrada?

**Causa Raiz Identificada:**

1. **Gate Z9 (API + Frontend Observability)** valida:
   - Schema aceita campos opcionais
   - API retorna dados corretos
   - UI não quebra quando dados ausentes
   - **MAS NÃO valida se a UI está acessível e funcional**

2. **Gate Z10 (Code Quality)** valida:
   - TDD e Clean Code
   - Qualidade estrutural do código
   - **MAS NÃO valida experiência do usuário final**

3. **Regras Globais** exigem:
   - `pytest -q` 100% verde
   - Prova via testes + asserts
   - **MAS não exigem validação da experiência observável do usuário**

4. **Lacuna Estrutural:**
   - Nenhum gate valida se `http://localhost:8000/` está funcional para o usuário final
   - Nenhum gate bloqueia se CSS/JS retornam 404
   - Nenhum gate valida se a interface é utilizável

**Resultado:**
- Sistema pode passar todos os gates (Z0-Z10)
- Suite de testes pode estar 100% verde
- **MAS a experiência do usuário final pode estar quebrada**

---

## 2. PROPOSTA: GATE Z11 — END-USER SMOKE / FRONTEND

### Objetivo

Garantir que a experiência observável do usuário final está funcional antes de declarar qualquer gate como PASS.

**Regra Crítica:** Se a UI estiver quebrada para o usuário final, o sistema DEVE falhar estruturalmente antes de qualquer correção.

---

### END (Resultado Final Esperado)

**Para o Usuário Final:**
Ao acessar a interface web (`http://localhost:8000/` ou endpoint equivalente):
- Interface carrega completamente (HTML renderizado)
- Recursos estáticos carregam sem erro 404 (CSS, JS, imagens)
- Interface é visualmente correta (estilos aplicados)
- JavaScript funcional (interações básicas funcionam)
- Nenhum erro crítico no console do navegador

**Critério de Aceitação (BINÁRIO):**
- ✅ `curl http://localhost:8000/` retorna HTML válido (não 404, não 500)
- ✅ `curl http://localhost:8000/static/css/style.css` retorna CSS (não 404)
- ✅ `curl http://localhost:8000/static/js/app.js` retorna JS (não 404)
- ✅ Navegador acessa interface sem erros 404 no console
- ✅ Interface renderiza visualmente correta

---

### DONE WHEN (Binário, Sem Interpretação)

Gate Z11 é considerado PASS quando:

1. **HTML acessível:**
   ```bash
   curl -s http://localhost:8000/ | grep -q "<!DOCTYPE html>" && echo "PASS" || echo "FAIL"
   ```
   Retorna: `PASS`

2. **CSS acessível:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/style.css
   ```
   Retorna: `200` (não 404, não 500)

3. **JS acessível:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/js/app.js
   ```
   Retorna: `200` (não 404, não 500)

4. **Favicon acessível (se existir):**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/favicon.svg
   ```
   Retorna: `200` ou `204` (não 404)

5. **API Health responde:**
   ```bash
   curl -s http://localhost:8000/api/health | grep -q "healthy" && echo "PASS" || echo "FAIL"
   ```
   Retorna: `PASS`

**Regra:** Se QUALQUER um dos comandos acima retornar FAIL ou código HTTP diferente de 200/204, Gate Z11 = FAIL.

---

### PROIBIÇÕES CLARAS

Gate Z11 FALHA se:

- ❌ HTML retorna 404 ou 500
- ❌ CSS retorna 404 ou 500
- ❌ JS retorna 404 ou 500
- ❌ Interface não renderiza visualmente (estilos não aplicados)
- ❌ Console do navegador mostra erros 404 para recursos estáticos
- ❌ API Health não responde
- ❌ Qualquer recurso referenciado no HTML retorna 404

**Regra Crítica:** Gate Z11 falhou = PR bloqueado, mesmo com todos os outros gates (Z0-Z10) PASS.

---

### Prova Mínima Exigida

**Comandos Obrigatórios (executados via Docker):**

```bash
# 1. HTML acessível
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -5'

# 2. CSS acessível (código HTTP 200)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/style.css'

# 3. JS acessível (código HTTP 200)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/js/app.js'

# 4. Favicon (se existir)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/favicon.svg'

# 5. API Health
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health'
```

**Evidência Obrigatória:**
- Output de cada comando acima colado em `EVIDENCIAS/gate_z11_end_user_smoke_proof.md`
- Cada comando deve retornar resultado esperado (PASS/200/healthy)
- Status final: `Status: PASS` ou `Status: FAIL`

---

### Checklist do Gate Z11

- [ ] Z11.0: HTML acessível em `http://localhost:8000/` (retorna HTML válido, não 404/500)
- [ ] Z11.1: CSS acessível em `/static/css/style.css` (HTTP 200, não 404)
- [ ] Z11.2: JS acessível em `/static/js/app.js` (HTTP 200, não 404)
- [ ] Z11.3: Favicon acessível (se existir) (HTTP 200 ou 204, não 404)
- [ ] Z11.4: API Health responde corretamente (`/api/health` retorna `{"status":"healthy"}`)
- [ ] Z11.5: Nenhum recurso estático referenciado no HTML retorna 404
- [ ] Z11.6: Evidência canônica gerada com outputs dos comandos

---

### Comando de Prova

```bash
# Validação completa do Gate Z11
docker compose exec app bash -c '
  echo "=== Z11.0: HTML ===" && \
  curl -s http://localhost:8000/ | head -1 && \
  echo "=== Z11.1: CSS ===" && \
  curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/static/css/style.css && \
  echo "=== Z11.2: JS ===" && \
  curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/static/js/app.js && \
  echo "=== Z11.4: Health ===" && \
  curl -s http://localhost:8000/api/health
'
```

**Critério de PASS:** Todos os comandos retornam resultado esperado (HTML válido, HTTP 200, healthy).

---

### Artifacts Esperados

- `EVIDENCIAS/gate_z11_end_user_smoke_proof.md` (evidência canônica com outputs)
- Comandos executados via Docker (não local)
- Status final: PASS ou FAIL

---

### Regra de Bloqueio Estrutural

**Gate Z11 é BLOQUEANTE:**

- Se Gate Z11 falhar, **TODOS os outros gates (Z0-Z10) são considerados INCOMPLETOS**
- Nenhum PR pode ser aprovado com Gate Z11 em FAIL
- Nenhuma correção de produto pode ser aplicada sem Gate Z11 PASS

**Ordem de Validação:**
1. Gates Z0-Z10 (validação técnica)
2. **Gate Z11 (validação de experiência do usuário final) — BLOQUEANTE**

Se Z11 falhar → sistema estruturalmente quebrado → PR bloqueado.

---

### Exceções e Casos Especiais

**Quando Gate Z11 não se aplica:**
- Sistema puramente CLI (sem interface web)
- Sistema em modo API-only (sem frontend)
- Desenvolvimento de backend isolado (sem frontend ativo)

**Regra:** Se o sistema expõe interface web (`http://localhost:8000/` ou equivalente), Gate Z11 é **OBRIGATÓRIO**.

---

### Integração com Método END-FIRST v2

**Gate Z11 reforça END-FIRST:**

- END observável do usuário final é validado estruturalmente
- Não é possível declarar "feito" sem validar experiência do usuário
- Correções de produto exigem Gate Z11 PASS antes de qualquer alteração

**Regra Canônica:**
> "Se a UI estiver quebrada para o usuário final, o sistema DEVE falhar estruturalmente antes de qualquer correção."

---

## 3. IMPACTO NO MÉTODO ATUAL

### Mudanças Necessárias

1. **CHECKLIST_Z_GATES.md:**
   - Adicionar Gate Z11 após Gate Z10
   - Atualizar "Regras Globais" para incluir validação de experiência do usuário

2. **gates_manifest.json:**
   - Adicionar entrada Z11 no array `gates` após Z10

3. **.cursorrules:**
   - Atualizar referência de "Z0→Z10" para "Z0→Z11"
   - Adicionar regra: "Gate Z11 é bloqueante para qualquer alteração de produto"

4. **README.md:**
   - Documentar Gate Z11 como validação estrutural de experiência do usuário

---

## 4. VALIDAÇÃO DA PROPOSTA

**Critérios de Aprovação da Proposta:**

- [ ] Proposta documenta claramente a falha estrutural identificada
- [ ] Gate Z11 tem END explícito e observável
- [ ] DONE WHEN é binário e verificável
- [ ] PROIBIÇÕES são claras e objetivas
- [ ] Prova mínima é executável via Docker
- [ ] Regra de bloqueio estrutural é explícita

**Status da Proposta:** ✅ COMPLETA (aguardando aprovação)

---

## 5. PRÓXIMOS PASSOS (Após Aprovação)

1. Aprovar esta proposta
2. Criar DEMANDA para implementação do Gate Z11
3. Criar F-1 (Planejamento Canônico) para implementação
4. Executar conforme método END-FIRST v2

---

**Fim da Proposta**
