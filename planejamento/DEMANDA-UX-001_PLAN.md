# PLANEJAMENTO CANÔNICO — DEMANDA-UX-001: UX REFINEMENTS

**Demanda:** DEMANDA-UX-001_UX_REFINEMENTS.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-19  
**Status:** F-1 PENDENTE DE APROVAÇÃO  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado (UX Refinada)

**Para um usuário final acessando `http://localhost:8000/`:**
- Interface claramente compreensível sem contexto técnico
- Nenhum rótulo ambíguo ou confuso
- Feedback visual claro de estados (carregando, sucesso, erro)
- Resultados apresentados de forma legível e orientada à leitura
- UX consistente com o valor do produto: confiança, rastreabilidade e clareza
- Usuário **NUNCA** vê: IDs técnicos, hashes, marcadores internos, artefatos de engenharia
- Todo conteúdo é imediatamente visível
- Layout expande verticalmente conforme o conteúdo
- Scroll interno é proibido
- Progresso comunica atividade contínua perceptível, mesmo em etapas longas
- Nenhum elemento da UI gera dúvida do tipo: "isso é bug ou comportamento esperado?"

**Para o Desenvolvedor:**
- Interface continua funcional (Gate Z11 permanece PASS)
- Nenhuma regressão funcional (Z0–Z11 continuam PASS)
- Evidência UX gerada (prints ou PDF em `/EVIDENCIAS/ux/`)
- Suite de testes verde (`pytest -q` = 0 failed)

**⚠️ Importante:**
Este END não altera funcionalidade, apenas forma de apresentação e experiência.

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS — NÃO NEGOCIÁVEIS)

Estas frases são canônicas, reutilizáveis e bloqueantes:

- **Legibilidade:** "Se o usuário não vê o conteúdo imediatamente, o produto falhou."
- **Scroll:** "Scroll interno é bug estrutural, não escolha de UX."
- **Ruído Técnico:** "Usuário final nunca deve ver artefatos internos de engenharia."
- **Progresso:** "UX deve comunicar atividade contínua perceptível durante etapas longas, mesmo quando o percentual não muda."
- **Semântica:** "Métrica correta mas semanticamente ambígua é FAIL de UX."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## ✅ Critérios de Aceitação (Binários)

### PASS
- ✅ Usuário entende o que está vendo sem explicação externa
- ✅ Nenhum texto técnico desnecessário exposto ao usuário final
- ✅ Nenhum identificador técnico interno visível ([[RS:...]], hashes, IDs, chunks, markers)
- ✅ Todo conteúdo visível sem scroll interno
- ✅ Blocos expandem automaticamente conforme o conteúdo
- ✅ Estados vazios e mensagens fazem sentido
- ✅ Progresso comunica atividade contínua durante execuções longas
- ✅ Interface continua funcional (Gate Z11 permanece PASS)
- ✅ Nenhuma regressão funcional (Z0–Z11 continuam PASS)
- ✅ Evidência UX gerada (prints ou PDF em `/EVIDENCIAS/ux/`)

### FAIL (AUTOMÁTICO)
- ❌ UX alterada sem F-1 aprovada
- ❌ UI "mais bonita" porém menos clara
- ❌ Qualquer regressão funcional
- ❌ Gate Z11 quebrado
- ❌ Correção aplicada direto no código sem planejamento
- ❌ Marcadores técnicos internos visíveis ao usuário final
- ❌ Conteúdo oculto, cortado ou acessível apenas via scroll interno
- ❌ Usuário precisa "descobrir" que existe conteúdo escondido
- ❌ Métricas corretas porém semanticamente confusas sem explicação
- ❌ Progresso parece travado durante execução longa
- ❌ Usuário não sabe se o sistema está funcionando
- ❌ Violação de qualquer frase canônica

---

## 🚫 DO / DON'T

### DO
- ✅ Melhorar clareza textual (labels, mensagens, estados)
- ✅ Melhorar hierarquia visual (espaçamento, tipografia, cores)
- ✅ Melhorar feedback perceptível ao usuário (progresso, estados)
- ✅ Remover marcadores técnicos visíveis ao usuário final
- ✅ Garantir que blocos expandam verticalmente conforme conteúdo
- ✅ Adicionar feedback visual durante execuções longas
- ✅ Melhorar semântica de métricas confusas
- ✅ Manter rastreabilidade interna, sem vazar para UI
- ✅ Manter todos os gates PASS
- ✅ Gerar evidência UX (prints/PDF)

### DON'T
- ❌ Alterar pipeline de sumarização
- ❌ Alterar lógica de sumarização
- ❌ "Simplificar" removendo garantias
- ❌ Refatorar backend
- ❌ Introduzir scroll interno
- ❌ Quebrar Gate Z11
- ❌ Alterar funcionalidade existente
- ❌ Remover rastreabilidade interna (apenas ocultar da UI)

---

## 🧱 Bloqueios Estruturais
- 🔒 F-1 obrigatório (demanda de produto) — **ESTE DOCUMENTO**
- 🔒 Gate Z11 continua bloqueante
- 🔒 Nenhuma alteração sem evidência visual
- 🔒 UX ≠ estética → UX = clareza + confiança
- 🔒 Scroll interno = BUG estrutural
- 🔒 Violação de frase canônica = FAIL automático

---

## 📋 TODO Canônico (Sequencial e Bloqueante)

### F0 — Revisar Plano (BLOQUEANTE — SEM EXECUÇÃO)
**END:** Plano único, sem repetição, escopo fixo, provas definidas e padronizadas.

**Checklist obrigatório (marcar todos antes de avançar):**
- [ ] Escopo fixo declarado (UX Refinements apenas)
- [ ] Não existe passo opcional / "se quiser"
- [ ] Todas as fases têm END + DONE WHEN + PROOF
- [ ] Todos os PROOFs são via Docker (docker compose exec app bash -c ...)
- [ ] Gate Z11 validação definida
- [ ] Evidência UX obrigatória definida (prints/PDF em `/EVIDENCIAS/ux/`)
- [ ] Frases canônicas referenciadas em cada fase relevante

**DONE WHEN:** Declarar explicitamente "F0 aprovada" após checklist completo.

**PROOF:** Checklist acima preenchido no relatório (texto).

---

### F1 — Remover Marcadores Técnicos do Resumo
**END:** Usuário final nunca vê marcadores técnicos internos ([[RS:...]], hashes, IDs, chunks).

**Ação obrigatória:**
- Identificar onde marcadores técnicos são exibidos no resumo
- Remover ou sanitizar marcadores antes de exibir ao usuário
- Manter rastreabilidade interna (não remover do backend, apenas ocultar da UI)

**DONE WHEN:** 
- Nenhum marcador técnico visível na UI
- Resumo exibido sem artefatos de engenharia
- Rastreabilidade interna mantida (backend não alterado)

**PROOF (Docker):**
```bash
# Verificar que HTML não contém marcadores técnicos
docker compose exec app bash -c 'curl -s http://localhost:8000/ | grep -E "\[\[RS:|chunks:|hash" || echo "OK: nenhum marcador técnico encontrado"'
```

---

### F2 — Corrigir Métricas Semanticamente Confusas
**END:** Métricas exibidas são semanticamente claras ou têm explicação contextual.

**Ação obrigatória:**
- Identificar métricas confusas (ex.: "Original – 0 palavras")
- Melhorar labels ou adicionar explicação contextual
- Garantir que usuário entende o significado sem ambiguidade

**DONE WHEN:**
- Métricas exibidas são claras ou têm explicação
- Nenhuma métrica gera dúvida "é bug ou comportamento esperado?"

**PROOF (Docker):**
```bash
# Verificar que métricas confusas foram corrigidas
docker compose exec app bash -c 'curl -s http://localhost:8000/ | grep -E "Original.*0 palavras" || echo "OK: métrica confusa corrigida ou não encontrada"'
```

---

### F3 — Corrigir Blocos com Conteúdo Invisível (BUG UX)
**END:** Todo bloco com conteúdo expande verticalmente e é imediatamente visível.

**Ação obrigatória:**
- Identificar blocos com conteúdo invisível ou cortado (ex.: "Coverage & Evidence", "Confiabilidade do Resumo")
- Remover scroll interno, overflow oculto ou altura fixa que corta conteúdo
- Garantir que blocos expandem automaticamente conforme conteúdo
- CSS: remover `overflow: hidden`, `max-height` fixo, `scroll` interno

**DONE WHEN:**
- Nenhum bloco tem scroll interno
- Todo conteúdo é imediatamente visível
- Blocos expandem verticalmente conforme conteúdo

**PROOF (Docker):**
```bash
# Verificar que CSS não tem overflow hidden ou scroll interno problemático
docker compose exec app bash -c 'grep -E "overflow.*hidden|max-height.*px|overflow.*scroll" /app/frontends/web/css/style.css | grep -v "/*" || echo "OK: sem overflow oculto problemático"'

# Verificar que HTML não tem scroll interno
docker compose exec app bash -c 'curl -s http://localhost:8000/ | grep -E "overflow|scroll" || echo "OK: sem scroll interno no HTML"'
```

---

### F4 — Melhorar Feedback Durante Execuções Longas
**END:** Progresso comunica atividade contínua perceptível mesmo quando percentual não muda.

**Ação obrigatória:**
- Adicionar indicador visual de atividade durante execuções longas
- Exibir mensagem de progresso mais detalhada (ex.: "Processando capítulo X de Y...")
- Adicionar animação ou indicador pulsante quando percentual está estático
- Melhorar mensagens SSE para incluir detalhes de progresso

**DONE WHEN:**
- Usuário sabe que sistema está processando mesmo quando percentual não muda
- Feedback visual perceptível durante etapas longas

**PROOF (Docker):**
```bash
# Verificar que JavaScript tem lógica de feedback durante execuções longas
docker compose exec app bash -c 'grep -E "keepalive|progress|activity|processando" /app/frontends/web/js/app.js | head -5'
```

---

### F5 — Gerar Evidência UX (Obrigatória)
**END:** Evidência visual gerada documentando antes/depois das melhorias UX.

**Ação obrigatória:**
- Criar diretório `/EVIDENCIAS/ux/` se não existir
- Gerar prints ou PDF mostrando:
  - Estado antes (marcadores técnicos, métricas confusas, blocos invisíveis)
  - Estado depois (sem marcadores, métricas claras, blocos visíveis)
  - Comparação de feedback durante execuções longas
- Documentar em `EVIDENCIAS/ux/UX_REFINEMENTS_PROOF.md`

**DONE WHEN:**
- Evidência visual gerada em `/EVIDENCIAS/ux/`
- Documento de prova criado com comparação antes/depois

**PROOF (Docker):**
```bash
# Verificar que evidência UX foi gerada
docker compose exec app bash -c 'ls -la /app/EVIDENCIAS/ux/ && echo "OK: evidência UX existe"'
```

---

### F6 — Validar Gate Z11 e Suite Verde
**END:** Gate Z11 continua PASS e suite de testes verde.

**Ação obrigatória:**
- Executar validação completa do Gate Z11 (HTML, CSS, JS, Health)
- Executar suite de testes (`pytest -q`)
- Confirmar que nenhuma regressão funcional foi introduzida

**DONE WHEN:**
- Gate Z11: todos os 6 blocos PASS
- Suite verde: `pytest -q` = 0 failed
- Nenhuma regressão funcional

**PROOF (Docker):**
```bash
# Validar Gate Z11
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1 && curl -s -o /dev/null -w "CSS: HTTP %{http_code}\n" http://localhost:8000/static/css/style.css && curl -s -o /dev/null -w "JS: HTTP %{http_code}\n" http://localhost:8000/static/js/app.js && curl -s http://localhost:8000/api/health'

# Suite verde
docker compose exec app bash -c 'pytest -q 2>&1 | tail -1'
```

---

## 📊 Strings de Prova (Comandos Docker)

Todos os comandos de prova devem ser executados via Docker:

```bash
# F1: Verificar ausência de marcadores técnicos
docker compose exec app bash -c 'curl -s http://localhost:8000/ | grep -E "\[\[RS:|chunks:|hash" || echo "OK: nenhum marcador técnico"'

# F2: Verificar métricas corrigidas
docker compose exec app bash -c 'curl -s http://localhost:8000/ | grep -E "Original.*0 palavras" || echo "OK: métrica corrigida"'

# F3: Verificar CSS sem overflow oculto problemático
docker compose exec app bash -c 'grep -E "overflow.*hidden|max-height.*px" /app/frontends/web/css/style.css | grep -v "/*" || echo "OK: sem overflow oculto"'

# F4: Verificar feedback de progresso
docker compose exec app bash -c 'grep -E "keepalive|progress|activity" /app/frontends/web/js/app.js | head -3'

# F5: Verificar evidência UX
docker compose exec app bash -c 'ls -la /app/EVIDENCIAS/ux/'

# F6: Validar Gate Z11 completo
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1 && curl -s -o /dev/null -w "CSS: %{http_code}\n" http://localhost:8000/static/css/style.css && curl -s -o /dev/null -w "JS: %{http_code}\n" http://localhost:8000/static/js/app.js && curl -s http://localhost:8000/api/health'

# F6: Suite verde
docker compose exec app bash -c 'pytest -q 2>&1 | tail -1'
```

---

## 🧭 Regras Canônicas Aplicadas

Cada fase deve respeitar as frases canônicas:

- **F1:** "Usuário final nunca deve ver artefatos internos de engenharia."
- **F2:** "Métrica correta mas semanticamente ambígua é FAIL de UX."
- **F3:** "Scroll interno é bug estrutural, não escolha de UX." + "Se o usuário não vê o conteúdo imediatamente, o produto falhou."
- **F4:** "UX deve comunicar atividade contínua perceptível durante etapas longas, mesmo quando o percentual não muda."

---

## ❌ Fora de Escopo
- Novas features
- Performance
- Mudanças no modelo
- Alterações no pipeline
- Refatorações estruturais
- Alteração de funcionalidade existente

---

## 📌 Status

**F-1 PENDENTE DE APROVAÇÃO**

Este planejamento **NÃO autoriza execução**.

Só pode ser executado após:
- Revisão completa do planejamento
- Aprovação explícita: **"F-1 APROVADA"**
- Ordem clara do CEO

---

## 🧭 Regra Final

**Produto já funciona.**  
Esta demanda existe para eliminar confusão, não para mudar lógica.

**"Se o usuário precisa rolar um bloco para descobrir conteúdo, o produto falhou."**
