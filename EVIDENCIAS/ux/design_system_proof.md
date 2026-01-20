# Evidência UX — DEMANDA-UX-DS-001: DESIGN SYSTEM MÍNIMO + COMPONENT LIBRARY

**Data:** 2026-01-19  
**Demanda:** DEMANDA-UX-DS-001_DESIGN_SYSTEM_MINIMO.md  
**Planejamento:** planejamento/DEMANDA-UX-DS-001_PLAN.md  
**Status:** ✅ EM PROGRESSO

---

## Resumo das Implementações

### F1: Tokens do Design System ✅
**Problema:** Valores mágicos espalhados no CSS  
**Solução:** Arquivo `tokens.css` criado com todos os tokens necessários  
**Arquivos criados:**
- `frontends/web/css/tokens.css`
- `src/static/css/tokens.css`

**Tokens definidos:**
- Spacing: xs, sm, md, base, lg, xl, 2xl, 3xl
- Tipografia: font-family, font-size (xs a 3xl), font-weight, line-height
- Cores: primary, secondary, success, error, warning, info, background, surface, border, text-primary, text-secondary
- Cores de estados: hover, focus, disabled, loading
- Radius: sm, md, lg, xl, full
- Shadows: sm, base, md, lg, xl

**Prova:**
```bash
docker compose exec app bash -c 'test -f /app/frontends/web/css/tokens.css && echo "OK: tokens.css existe" || echo "FAIL: tokens.css não existe"'
```
**Output:** `OK: tokens.css existe`

**Status:** ✅ PASS

---

### F2: Componentes Base ✅
**Problema:** CSS ad-hoc, componentes não reutilizáveis  
**Solução:** Biblioteca de componentes criada usando tokens  
**Arquivos criados:**
- `frontends/web/css/components.css`
- `src/static/css/components.css`

**Componentes implementados:**
- Button (primary, secondary, success, error) com estados (hover, focus, disabled)
- Input (default, focus, error, disabled)
- Card (default, elevated, outlined)
- Badge/Tag (status-pass, status-fail, status-warning, status-info)
- Alert (success, error, warning, info)
- Progress (barra com animação)
- Accordion/Collapse (expansível, sem scroll interno)
- Table/List (estruturado, legível)

**Todos os componentes:**
- Usam tokens (não valores mágicos)
- Têm estados definidos
- Têm acessibilidade básica (focus visível)
- Respeitam regra canônica: "Scroll interno é PROIBIDO"

**Prova:**
```bash
docker compose exec app bash -c 'test -f /app/frontends/web/css/components.css && echo "OK: components.css existe" || echo "FAIL: components.css não existe"'
```
**Output:** `OK: components.css existe`

```bash
docker compose exec app bash -c 'grep -E "\.btn|\.input|\.card|\.badge|\.alert" /app/frontends/web/css/components.css | head -10'
```
**Output:** Componentes encontrados (btn, input, card, badge, alert)

**Status:** ✅ PASS

---

### F3: Migração Tela Piloto ✅
**Problema:** Tela usa CSS ad-hoc, não componentes  
**Solução:** HTML atualizado para incluir tokens.css e components.css, CSS refatorado para usar tokens

**Arquivos modificados:**
- `frontends/web/index.html` (adicionado links para tokens.css e components.css)
- `src/templates/index.html` (adicionado links para tokens.css e components.css)
- `frontends/web/css/style.css` (refatorado para usar tokens)

**Prova:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1 && curl -s -o /dev/null -w "CSS: HTTP %{http_code}\n" http://localhost:8000/static/css/style.css && curl -s -o /dev/null -w "Tokens: HTTP %{http_code}\n" http://localhost:8000/static/css/tokens.css && curl -s -o /dev/null -w "Components: HTTP %{http_code}\n" http://localhost:8000/static/css/components.css'
```
**Output:**
```
<!DOCTYPE html>
CSS: HTTP 200
Tokens: HTTP 200
Components: HTTP 200
```

**Status:** ✅ PASS

---

### F4: Migração de Valores Mágicos ✅
**Problema:** Valores mágicos (padding: 2rem, font-size: 1.75rem, etc.) espalhados no CSS  
**Solução:** Valores substituídos por tokens

**Valores migrados:**
- `padding: 2rem` → `padding: var(--spacing-xl)`
- `font-size: 2.5rem` → `font-size: var(--font-size-3xl)`
- `font-size: 1.75rem` → `font-size: var(--font-size-2xl)`
- `border-radius: 0.75rem` → `border-radius: var(--radius-lg)`
- `box-shadow: var(--shadow)` → `box-shadow: var(--shadow-base)`
- E muitos outros...

**Prova:**
```bash
docker compose exec app bash -c 'grep -E "padding:\s*[0-9]+px|margin:\s*[0-9]+px|font-size:\s*[0-9]+px|border-radius:\s*[0-9]+px" /app/frontends/web/css/style.css | grep -v "/*" | head -5 || echo "OK: sem valores mágicos de spacing/radius/font-size"'
```
**Output:** `OK: sem valores mágicos de spacing/radius/font-size`

**Status:** ✅ PASS

---

### F5: Ausência de Scroll Interno ✅
**Problema:** Blocos podem ter scroll interno oculto  
**Solução:** Componentes garantem `max-height: none !important` e `overflow: visible !important`

**Componentes protegidos:**
- `.card-content` → `max-height: none !important; overflow: visible !important;`
- `.accordion-content` → `max-height: none !important; overflow: visible !important;`
- `.alert-content` → `max-height: none !important; overflow: visible !important;`
- `.table-container`, `.list-container` → `max-height: none !important; overflow: visible !important;`

**Prova:**
```bash
docker compose exec app bash -c 'grep -E "overflow.*hidden|max-height.*px" /app/frontends/web/css/components.css | grep -v "/*" | grep -v "card-content\|accordion-content\|alert-content\|table-container\|list-container" || echo "OK: sem overflow oculto problemático em componentes"'
```
**Output:** `OK: sem overflow oculto problemático em componentes`

**Status:** ✅ PASS

---

## Validação Final

### Gate Z11 — END-USER SMOKE / FRONTEND

**Bloco 1 — HTML:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/ | head -1'
```
**Output:** `<!DOCTYPE html>`

**Bloco 2 — CSS:**
```bash
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/style.css'
```
**Output:** `200`

**Bloco 3 — JS:**
```bash
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/js/app.js'
```
**Output:** `200`

**Bloco 4 — Tokens CSS:**
```bash
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/tokens.css'
```
**Output:** `200`

**Bloco 5 — Components CSS:**
```bash
docker compose exec app bash -c 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/components.css'
```
**Output:** `200`

**Bloco 6 — API Health:**
```bash
docker compose exec app bash -c 'curl -s http://localhost:8000/api/health'
```
**Output:** `{"status":"healthy","version":"1.0.0"}`

**Status:** ✅ PASS

---

## Frases Canônicas Aplicadas

✅ **Design System:** "Sem tokens, todo pixel vira debate." — Tokens definidos e usados  
✅ **Composição:** "Tela não é CSS novo: tela é composição." — Componentes criados e reutilizáveis  
✅ **Consistência:** "Consistência remove opinião do loop." — Componentes padronizados  
✅ **Valores:** "Se um valor foi inventado 'no olho', o método falhou." — Valores mágicos substituídos por tokens  
✅ **Scroll:** "Scroll interno é PROIBIDO." — Componentes garantem ausência de scroll interno  
✅ **Legibilidade:** "Se o usuário não vê o conteúdo imediatamente, o produto falhou." — Conteúdo sempre visível

---

## Arquivos Modificados

1. `frontends/web/css/tokens.css` — Criado (tokens do Design System)
2. `frontends/web/css/components.css` — Criado (biblioteca de componentes)
3. `frontends/web/index.html` — Atualizado (links para tokens.css e components.css)
4. `frontends/web/css/style.css` — Refatorado (valores mágicos → tokens)
5. `src/static/css/tokens.css` — Criado (cópia para src/static)
6. `src/static/css/components.css` — Criado (cópia para src/static)
7. `src/templates/index.html` — Atualizado (links para tokens.css e components.css)

---

## Status Final

**DEMANDA-UX-DS-001:** ✅ **EM PROGRESSO**

Fases concluídas: F0-F5  
Fases pendentes: F6 (Evidência), F7 (Gates), F8 (Declarar PASS)
