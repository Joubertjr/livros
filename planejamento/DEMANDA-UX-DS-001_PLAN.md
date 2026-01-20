# PLANEJAMENTO CANÔNICO — DEMANDA-UX-DS-001: DESIGN SYSTEM MÍNIMO + COMPONENT LIBRARY

**Demanda:** DEMANDA-UX-DS-001_DESIGN_SYSTEM_MINIMO.md  
**Método:** END-FIRST v2  
**Data:** 2026-01-19  
**Status:** ✅ F-1 APROVADA  
**Aprovação:** 2026-01-19 (F-1 APROVADA)  
**Repositório:** https://github.com/Joubertjr/livros

---

## 🔒 END (Resultado Observável)

### Estado Final Esperado

**Para qualquer tela do produto (incluindo CoverageSummarizer):**
- Existe um Design System mínimo no repo com:
  - Tokens de spacing, tipografia, cores (incluindo estados), radius e sombras
  - Regras explícitas de uso ("não inventar valores soltos")
- Existe uma biblioteca de componentes base reutilizáveis:
  - Button, Input, Card, Badge/Tag de status, Alert, Progress, Accordion/Collapse, Table/List
- Qualquer nova UI passa a ser composição de componentes, não CSS ad-hoc
- UI final fica consistente e previsível (reduz "atrito de UI" e retrabalho)
- O sistema continua respeitando as regras canônicas:
  - Scroll interno proibido
  - Legibilidade imediata
  - Sem ruído técnico para usuário final
  - Progresso perceptível

**⚠️ Importante:**
Este END NÃO exige "ficar bonito"; exige consistência sistêmica.

---

## 🧭 FRASES CANÔNICAS (OBRIGATÓRIAS — NÃO NEGOCIÁVEIS)

Estas frases são canônicas, reutilizáveis e bloqueantes:

- **Design System:** "Sem tokens, todo pixel vira debate."
- **Composição:** "Tela não é CSS novo: tela é composição."
- **Consistência:** "Consistência remove opinião do loop."
- **Valores:** "Se um valor foi inventado 'no olho', o método falhou."
- **Scroll (GLOBAL):** "Scroll interno é PROIBIDO. Conteúdo invisível ou cortado é BUG estrutural."
- **Legibilidade (GLOBAL):** "Se o usuário não vê o conteúdo imediatamente, o produto falhou."

**Violação de qualquer frase canônica = FAIL automático da demanda.**

---

## ✅ Critérios de Aceitação (Binários)

### PASS

- ✅ Tokens definidos e usados (spacing/typo/colors/radius/shadow)
- ✅ Componentes base existem e são reutilizados
- ✅ Nenhum valor "mágico" fora dos tokens nos componentes/telas alteradas
- ✅ Estados (hover/focus/disabled/loading/error/success) definidos nos componentes
- ✅ UI final fica consistente e previsível
- ✅ Nova UI é composição de componentes, não CSS ad-hoc
- ✅ Gate Z11 permanece PASS
- ✅ Gate Z12 permanece PASS (se aplicável)
- ✅ Gate Z13 aplicável e satisfazível (UI/UX sistêmica)
- ✅ Evidência gerada (prints ou doc em `/EVIDENCIAS/ux/`)
- ✅ Nenhuma regressão funcional (Z0–Z11 continuam PASS)

### FAIL (AUTOMÁTICO)

- ❌ Componentes criados mas telas continuam "CSS solto"
- ❌ Tokens existem mas não são usados
- ❌ Valores mágicos espalhados
- ❌ Inconsistência entre botões/cards/inputs
- ❌ Regressão em Z11/Z12/Z13
- ❌ Scroll interno reaparece
- ❌ UX alterada sem F-1 aprovada
- ❌ Qualquer regressão funcional
- ❌ Gate Z11 quebrado
- ❌ Correção aplicada direto no código sem planejamento
- ❌ Violação de qualquer frase canônica

---

## 🚫 DO / DON'T

### DO (fazer)

- ✅ Criar tokens e impor uso
- ✅ Criar componentes base reutilizáveis
- ✅ Priorizar acessibilidade (focus visível, contraste mínimo, navegação teclado)
- ✅ Auditar telas existentes para migrar minimamente
- ✅ Manter todos os gates PASS
- ✅ Manter regras canônicas de UX (scroll interno proibido, legibilidade imediata)
- ✅ Gerar evidência antes/depois

### DON'T (não fazer)

- ❌ Redesenhar produto inteiro
- ❌ Refatorar backend
- ❌ Criar 20 variações de botão
- ❌ Inserir scroll interno em qualquer lugar
- ❌ Alterar pipeline de sumarização
- ❌ "Simplificar" removendo garantias
- ❌ Quebrar Gate Z11
- ❌ Valores mágicos fora dos tokens

---

## 🧱 Bloqueios Estruturais

- 🔒 F-1 obrigatório (demanda de UX sistêmica complexa) — **ESTE DOCUMENTO**
- 🔒 Gate Z11 continua bloqueante
- 🔒 Gate Z12 continua bloqueante (se aplicável)
- 🔒 Gate Z13 aplicável e bloqueante (UI/UX sistêmica)
- 🔒 Nenhuma alteração sem evidência visual
- 🔒 Scroll interno = BUG estrutural (não negociável)
- 🔒 Tokens devem ser impostos, não opcionais

---

## 📋 TODO CANÔNICO (F0-F8)

### F0 — Revisar Plano (BLOQUEANTE — SEM EXECUÇÃO)

**END:** Plano aprovado e pronto para execução

**DONE WHEN:**
- Checklist completo verificado
- Nenhum comando executado
- Nenhum código alterado
- Declaração explícita: "F-1 aprovada"

**PROIBIÇÕES:**
- ❌ Executar comandos
- ❌ Criar código
- ❌ "Validar rapidamente"

---

### F1 — Definir Tokens do Design System

**END:** Arquivo de tokens CSS definido e documentado

**DONE WHEN:**
- Arquivo `frontends/web/css/tokens.css` criado
- Tokens definidos para:
  - Spacing (0.25rem, 0.5rem, 0.75rem, 1rem, 1.5rem, 2rem, 3rem, 4rem)
  - Tipografia (font-family, font-size, font-weight, line-height)
  - Cores (primary, secondary, success, error, warning, background, surface, border, text-primary, text-secondary)
  - Cores de estados (hover, focus, disabled, loading, error, success)
  - Radius (0.25rem, 0.5rem, 0.75rem, 1rem)
  - Sombras (shadow, shadow-lg, shadow-xl)
- Documentação de uso criada
- Nenhum valor mágico permitido fora dos tokens

**PROVA:**
```bash
# Verificar que tokens.css existe
docker compose exec app bash -c 'test -f /app/frontends/web/css/tokens.css && echo "OK: tokens.css existe" || echo "FAIL: tokens.css não existe"'

# Verificar que tokens são usados (grep por valores mágicos)
docker compose exec app bash -c 'grep -E "padding:\s*[0-9]+px|margin:\s*[0-9]+px|border-radius:\s*[0-9]+px" /app/frontends/web/css/style.css | head -5 || echo "OK: sem valores mágicos de spacing/radius"'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Sem tokens, todo pixel vira debate."
- "Se um valor foi inventado 'no olho', o método falhou."

---

### F2 — Criar Componentes Base (Lista Mínima)

**END:** Componentes base reutilizáveis implementados usando tokens

**DONE WHEN:**
- Componentes criados em `frontends/web/css/components.css`:
  - Button (com estados: default, hover, focus, disabled, loading)
  - Input (com estados: default, focus, error, disabled)
  - Card (com variações: default, elevated, outlined)
  - Badge/Tag (com variações: status-pass, status-fail, status-warning, status-info)
  - Alert (com variações: success, error, warning, info)
  - Progress (barra de progresso com animação)
  - Accordion/Collapse (expansível, sem scroll interno)
  - Table/List (estruturado, legível)
- Todos os componentes usam tokens (não valores mágicos)
- Estados definidos para cada componente
- Acessibilidade básica (focus visível, contraste mínimo)

**PROVA:**
```bash
# Verificar que components.css existe
docker compose exec app bash -c 'test -f /app/frontends/web/css/components.css && echo "OK: components.css existe" || echo "FAIL: components.css não existe"'

# Verificar que componentes usam tokens (não valores mágicos)
docker compose exec app bash -c 'grep -E "\.btn|\.input|\.card|\.badge|\.alert" /app/frontends/web/css/components.css | head -10'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Tela não é CSS novo: tela é composição."
- "Consistência remove opinião do loop."
- "Scroll interno é PROIBIDO."

---

### F3 — Migrar Tela Piloto (CoverageSummarizer)

**END:** Tela principal do CoverageSummarizer usa componentes, não CSS ad-hoc

**DONE WHEN:**
- `frontends/web/index.html` atualizado para usar classes de componentes
- `frontends/web/css/style.css` refatorado para usar tokens e componentes
- Nenhum valor mágico restante na tela piloto
- UI mantém funcionalidade (Gate Z11 continua PASS)
- Scroll interno não aparece

**PROVA:**
```bash
# Verificar que HTML usa classes de componentes
docker compose exec app bash -c 'grep -E "class=\"(btn|input|card|badge|alert|progress)" /app/frontends/web/index.html | head -5'

# Verificar Gate Z11
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1 && curl -s -o /dev/null -w "CSS: HTTP %{http_code}\n" http://localhost:8000/static/css/style.css'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Tela não é CSS novo: tela é composição."
- "Scroll interno é PROIBIDO."
- "Se o usuário não vê o conteúdo imediatamente, o produto falhou."

---

### F4 — Auditar e Migrar Telas Existentes (Mínimo)

**END:** Telas existentes migradas minimamente para usar tokens e componentes

**DONE WHEN:**
- `frontends/web/css/style.css` auditado
- Valores mágicos identificados e substituídos por tokens
- Componentes reutilizados onde aplicável
- Nenhuma regressão visual ou funcional
- Gate Z11 continua PASS

**PROVA:**
```bash
# Verificar ausência de valores mágicos
docker compose exec app bash -c 'grep -E "padding:\s*[0-9]+px|margin:\s*[0-9]+px|border-radius:\s*[0-9]+px|color:\s*#[0-9a-f]{3,6}" /app/frontends/web/css/style.css | grep -v "/*" | head -5 || echo "OK: sem valores mágicos"'

# Verificar Gate Z11
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Sem tokens, todo pixel vira debate."
- "Se um valor foi inventado 'no olho', o método falhou."

---

### F5 — Garantir Ausência Total de Scroll Interno

**END:** Nenhum componente ou tela possui scroll interno

**DONE WHEN:**
- Auditado todos os componentes para `overflow: hidden` ou `max-height` problemático
- Blocos expandem verticalmente conforme conteúdo
- Conteúdo sempre visível sem scroll oculto
- Gate Z11 continua PASS

**PROVA:**
```bash
# Verificar que não há overflow hidden problemático (exceto já corrigidos)
docker compose exec app bash -c 'grep -E "overflow.*hidden|max-height.*px" /app/frontends/web/css/components.css | grep -v "/*" | grep -v "#coverage\|#reliability\|#executive\|#chapter-toc" || echo "OK: sem overflow oculto problemático"'
```

**REGRAS CANÔNICAS APLICADAS:**
- "Scroll interno é PROIBIDO. Conteúdo invisível ou cortado é BUG estrutural."
- "Se o usuário não vê o conteúdo imediatamente, o produto falhou."

---

### F6 — Gerar Evidência UX (Antes/Depois)

**END:** Evidência visual gerada mostrando antes/depois

**DONE WHEN:**
- Arquivo `EVIDENCIAS/ux/design_system_proof.md` criado
- Documenta:
  - Tokens definidos
  - Componentes criados
  - Tela piloto migrada
  - Comparação antes/depois (se possível)
- Comandos de prova executados e outputs registrados

**PROVA:**
```bash
# Verificar que evidência existe
docker compose exec app bash -c 'test -f /app/EVIDENCIAS/ux/design_system_proof.md && echo "OK: evidência existe" || echo "FAIL: evidência não existe"'
```

---

### F7 — Validar Gates Z11, Z12, Z13 e Suite Verde

**END:** Todos os gates validados e suite verde

**DONE WHEN:**
- Gate Z11: PASS (HTML, CSS, JS, Health acessíveis)
- Gate Z12: PASS (se aplicável)
- Gate Z13: PASS (UI/UX sistêmica verificável)
- Suite verde: `pytest -q` = 0 failed

**PROVA:**
```bash
# Gate Z11
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1 && curl -s -o /dev/null -w "CSS: HTTP %{http_code}\n" http://localhost:8000/static/css/style.css && curl -s http://localhost:8000/api/health'

# Suite verde
docker compose exec app bash -c 'pytest -q 2>&1 | tail -1'
```

---

### F8 — Declarar PASS

**END:** Demanda concluída e validada

**DONE WHEN:**
- Todas as fases F1-F7 concluídas
- Todos os gates PASS
- Evidência gerada
- Commit final realizado
- Status atualizado para "✅ CONCLUÍDA"

---

## 🔍 ANÁLISE DO ESTADO ATUAL

### CSS Atual (`frontends/web/css/style.css`)

**Observações:**
- Já possui variáveis CSS (`:root` com cores, sombras)
- Valores mágicos presentes (ex: `padding: 2rem`, `font-size: 2.5rem`)
- Componentes não estruturados como biblioteca reutilizável
- Estilos misturados (base + componentes + utilitários)

**Oportunidades:**
- Extrair tokens das variáveis existentes
- Estruturar componentes como classes reutilizáveis
- Migrar valores mágicos para tokens

---

## 📊 STRINGS DE PROVA (Comandos Docker)

### F1 — Tokens:
```bash
docker compose exec app bash -c 'test -f /app/frontends/web/css/tokens.css && echo "OK" || echo "FAIL"'
```

### F2 — Componentes:
```bash
docker compose exec app bash -c 'test -f /app/frontends/web/css/components.css && echo "OK" || echo "FAIL"'
```

### F3 — Tela Piloto:
```bash
docker compose exec app bash -c 'grep -E "class=\"(btn|input|card)" /app/frontends/web/index.html | head -3'
```

### F4 — Valores Mágicos:
```bash
docker compose exec app bash -c 'grep -E "padding:\s*[0-9]+px" /app/frontends/web/css/style.css | head -3 || echo "OK: sem valores mágicos"'
```

### F5 — Scroll Interno:
```bash
docker compose exec app bash -c 'grep -E "overflow.*hidden" /app/frontends/web/css/components.css | grep -v "/*" || echo "OK: sem overflow oculto"'
```

### F6 — Evidência:
```bash
docker compose exec app bash -c 'test -f /app/EVIDENCIAS/ux/design_system_proof.md && echo "OK" || echo "FAIL"'
```

### F7 — Gates:
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health && pytest -q 2>&1 | tail -1'
```

---

## 🚨 CRITÉRIOS DE FAIL

### FAIL Automático se:
- ❌ Tokens criados mas não usados
- ❌ Componentes criados mas telas continuam CSS solto
- ❌ Valores mágicos restantes após migração
- ❌ Scroll interno reaparece
- ❌ Gate Z11 quebra
- ❌ Regressão funcional
- ❌ Execução sem F-1 aprovada

---

## 📌 Status

**✅ F-1 APROVADA** (2026-01-19)

Execução autorizada conforme planejamento.

---

**Governado por:** `/METODO/END_FIRST_V2.md`  
**Path Canônico:** `/planejamento/DEMANDA-UX-DS-001_PLAN.md`  
**Demanda:** `/DEMANDAS/DEMANDA-UX-DS-001_DESIGN_SYSTEM_MINIMO.md`
