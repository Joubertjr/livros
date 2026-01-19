# PLANEJAMENTO CANÔNICO — CoverageSummarizer (Projeto: livros)

**Método:** END-FIRST v2  
**Data:** 2026-01-19  
**Status:** F-1 APROVADA  
**Aprovação:** 2026-01-19 (F-1 APROVADA)  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final do Sistema CoverageSummarizer

**Para o Usuário Final:**
Ao acessar `http://localhost:8000/`:
- Interface web carrega completamente e é funcional
- CSS e JavaScript carregam sem erros 404
- Interface renderiza visualmente correta (estilos aplicados)
- Interações básicas funcionam (upload, processamento, visualização)
- Nenhum erro crítico no console do navegador
- API responde corretamente (`/api/health` retorna `{"status":"healthy"}`)

**Para o Desenvolvedor:**
- Sistema funciona completamente dentro do Docker
- Suite de testes verde (`pytest -q` = 0 failed)
- Gates Z0-Z11 validados e PASS
- Código segue TDD e Clean Code (Gate Z10)
- Evidências canônicas geradas e validadas
- Repositório sincronizado com GitHub (commits pushed)

**Integridade do Produto como um TODO:**
- Funcionamento técnico validado (Gates Z0-Z10)
- Experiência do usuário final validada (Gate Z11 - proposta)
- Qualidade estrutural garantida (TDD + Clean Code)
- Método END-FIRST v2 respeitado (sem correções fora de ordem)
- Documentação atualizada e coerente

---

## ✅ Critérios de Aceitação (Binários)

### PASS (Sistema Funcional)

**Critérios Técnicos:**
- ✅ `docker compose up --build` sobe sistema sem erros
- ✅ `docker compose exec app pytest -q` retorna `0 failed`
- ✅ Gates Z0-Z10 validados e PASS
- ✅ Gate Z11 validado e PASS (após implementação da proposta)

**Critérios de Experiência do Usuário:**
- ✅ `curl http://localhost:8000/` retorna HTML válido (não 404, não 500)
- ✅ `curl http://localhost:8000/static/css/style.css` retorna HTTP 200
- ✅ `curl http://localhost:8000/static/js/app.js` retorna HTTP 200
- ✅ `curl http://localhost:8000/api/health` retorna `{"status":"healthy"}`
- ✅ Navegador acessa interface sem erros 404 no console
- ✅ Interface renderiza visualmente correta (estilos aplicados)

**Critérios Metodológicos:**
- ✅ Nenhuma correção de produto aplicada sem DEMANDA + F-1 aprovada
- ✅ Gate Z11 implementado e validado (bloqueio estrutural ativo)
- ✅ Método END-FIRST v2 respeitado em todas as alterações

### FAIL (Sistema Quebrado)

**FAIL Automático se:**
- ❌ Interface web retorna 404 ou 500
- ❌ CSS ou JS retornam 404
- ❌ Console do navegador mostra erros 404 para recursos estáticos
- ❌ Suite de testes não está verde (`pytest -q` > 0 failed)
- ❌ Qualquer gate (Z0-Z11) falha
- ❌ Correção de produto aplicada sem DEMANDA + F-1 aprovada
- ❌ Gate Z11 não implementado (bloqueio estrutural ausente)

**Regra Crítica:** Se a UI estiver quebrada para o usuário final, o sistema DEVE falhar estruturalmente antes de qualquer correção.

---

## 🚫 DO / DON'T

### DO (Fazer)

**Durante Planejamento (F-1):**
- ✅ Criar documento de planejamento canônico
- ✅ Definir TODO canônico derivado do END
- ✅ Definir escopo DO/DON'T explícito
- ✅ Definir ordem de execução
- ✅ Definir critérios de FAIL
- ✅ Definir strings de prova (quando aplicável)
- ✅ Aguardar aprovação explícita ("F-1 aprovada")

**Durante Execução (após F-1 aprovada):**
- ✅ Executar conforme plano aprovado
- ✅ Validar cada etapa conforme critérios definidos
- ✅ Gerar evidências canônicas
- ✅ Reportar qualidade (testes, refatorações, nomes melhorados)
- ✅ Validar Gate Z11 antes de declarar qualquer gate como PASS

### DON'T (Não Fazer)

**Durante Planejamento (F-1):**
- ❌ Executar comandos
- ❌ Criar código
- ❌ Criar automações
- ❌ "Validar rapidamente"
- ❌ Interpretar regras durante execução
- ❌ Aplicar correções "óbvias"

**Durante Execução:**
- ❌ Alterar código sem DEMANDA + F-1 aprovada
- ❌ Corrigir UI / CSS / JS sem planejamento
- ❌ Aplicar hotfixes sem bloqueio estrutural
- ❌ Declarar PASS com UI quebrada
- ❌ Ignorar Gate Z11 (quando implementado)
- ❌ Fazer "refatoração silenciosa"
- ❌ Implementar sem testes (viola Gate Z10)

**Regra Absoluta:**
> "F-1 é planejamento, não execução. Executar durante F-1 é FAIL automático."

---

## 🧱 Bloqueios Estruturais

### Bloqueio 1: Gate Z11 (END-USER SMOKE)

**Status:** Proposta criada em `DEMANDAS/PROPOSAL_GATE_Z11_END_USER_SMOKE.md`

**Bloqueio:**
- Gate Z11 valida experiência observável do usuário final
- Se UI estiver quebrada, Gate Z11 = FAIL
- Gate Z11 falhou = PR bloqueado, mesmo com Z0-Z10 PASS

**Implementação Pendente:**
- Gate Z11 deve ser adicionado ao `CHECKLIST_Z_GATES.md` após Z10
- Gate Z11 deve ser registrado no `gates_manifest.json`
- Gate Z11 deve ser validado antes de declarar qualquer alteração como concluída

### Bloqueio 2: END-FIRST v2 (F-1 Obrigatória)

**Bloqueio:**
- Demandas complexas exigem F-1 (Planejamento Canônico) aprovado
- Sem "F-1 aprovada", nenhuma execução é permitida
- Correções de produto (UI, frontend, assets) são demandas complexas

**Regra:**
> "Esta demanda requer F-1 (Planejamento Canônico). Sem F-1 aprovada, não posso executar."

### Bloqueio 3: Gate Z10 (TDD + Clean Code)

**Bloqueio:**
- Nenhuma implementação sem testes
- Funções ≤50 linhas (exceto wrapper/adapter documentado)
- Sem TODO/HACK/FIXME
- Sem refatoração silenciosa
- Gate Z10 falhou = PR bloqueado

### Bloqueio 4: Método Canônico

**Bloqueio:**
- Planejamento é artefato de primeira classe
- Executor apenas executa (não interpreta durante execução)
- Qualidade inclui produto como um TODO, não apenas testes

**Como Evitar "Arrumar Depois":**
- Gate Z11 valida experiência do usuário antes de declarar PASS
- F-1 obrigatória para correções de produto
- Bloqueio estrutural impede correções fora de ordem

---

## 📋 TODO Canônico

**Sequência derivada do END (sem interpretação):**

1. **F-1: Planejamento Canônico**
   - Criar este documento
   - Definir END, critérios, DO/DON'T, bloqueios, TODO
   - Aguardar aprovação explícita ("F-1 aprovada")

2. **Implementar Gate Z11 (após F-1 aprovada)**
   - Adicionar Gate Z11 ao `CHECKLIST_Z_GATES.md` após Z10
   - Registrar Z11 no `gates_manifest.json` (dentro do array, após Z10)
   - Atualizar `.cursorrules` (Z0→Z11)
   - Gerar evidência canônica do Gate Z11

3. **Validar Sistema Completo (após Gate Z11 implementado)**
   - Validar Gates Z0-Z10 (técnico)
   - Validar Gate Z11 (experiência do usuário)
   - Validar que UI está funcional (`http://localhost:8000/`)
   - Validar que CSS/JS carregam sem 404
   - Validar que API Health responde

4. **Sincronizar com GitHub (após validação completa)**
   - Push de commits pendentes
   - Verificar que repositório está atualizado

**Ordem de Execução:**
1. F-1 (este documento) → APROVAÇÃO
2. Implementação Gate Z11
3. Validação completa (Z0-Z11)
4. Sincronização GitHub

---

## ❌ Fora de Escopo

**Não será tratado nesta demanda:**

- Novas features de produto (fora do escopo)
- Melhorias de UX além de "funcional" (fora do escopo)
- Otimizações de performance (fora do escopo)
- Refatorações além do necessário para Gate Z10 (fora do escopo)
- Automações de CI/CD (fora do escopo)
- Scripts de qualidade automatizados (reservado para Z10.1 futuro)

**Escopo Fixo:**
- Implementar Gate Z11 (bloqueio estrutural)
- Validar que sistema está funcional end-to-end
- Garantir que método END-FIRST v2 está sendo respeitado

---

## 🔍 Contexto Crítico (Não Ignorar)

**Falha Estrutural Identificada:**

Já ocorreu neste projeto a situação em que:
- Gates Z0-Z10 passaram
- Evidências estavam verdes
- Suite de testes estava 100% verde
- **MAS a interface estava quebrada (CSS/JS 404)**
- **E uma correção foi feita sem planejamento aprovado**

**Causa Raiz:**
- Nenhum gate validava experiência do usuário final
- Nenhum bloqueio estrutural impedia correções fora de ordem
- Método permitia declarar PASS com produto quebrado

**Solução:**
- Gate Z11 (proposta criada) valida experiência do usuário
- F-1 obrigatória para correções de produto
- Bloqueio estrutural impede "arrumar depois"

---

## 📝 Strings de Prova

**Comandos de Validação (executados via Docker):**

```bash
# Gate Z11 - HTML acessível
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1'

# Gate Z11 - CSS acessível (HTTP 200)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/style.css'

# Gate Z11 - JS acessível (HTTP 200)
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/js/app.js'

# Gate Z11 - API Health
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health'

# Suite verde
docker compose exec app bash -c 'pytest -q'
```

**Strings Esperadas:**
- HTML: `<!DOCTYPE html>`
- CSS: HTTP código `200`
- JS: HTTP código `200`
- Health: `{"status":"healthy"}`
- pytest: `0 failed`

---

## 🎯 APROVAÇÃO

**Status:** PENDENTE DE APROVAÇÃO

**Checklist de Aprovação:**
- [x] TODO canônico existe
- [x] Escopo DO/DON'T explícito
- [x] Ordem de execução definida
- [x] Critérios de FAIL listados
- [x] Bloqueios estruturais documentados
- [x] Strings de prova definidas
- [x] Nenhum comando foi executado durante F-1
- [x] Nenhum código foi criado durante F-1

**Aguardando:**
- [ ] Declaração explícita: **"F-1 aprovada"**
- [ ] Aprovação do CEO ou arquiteto responsável

---

**F-1 PENDENTE DE APROVAÇÃO**
