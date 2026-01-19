# DEMANDA-001: Correção de Arquivos Estáticos 404 (UI)

**Tipo:** Bug / Defeito de UX  
**Prioridade:** Alta (bloqueia uso da interface)  
**Data:** 2026-01-19  
**Status:** ✅ RESOLVIDO (correção aplicada, regularização canônica em andamento)

---

## END (Resultado Final Esperado)

**Para o Usuário Final:**
Ao acessar `http://localhost:8000/`, a interface web carrega completamente:
- CSS aplicado corretamente (sem erro 404)
- JavaScript funcional (sem erro 404)
- Interface utilizável e visualmente correta

**Critério de Aceitação (BINÁRIO):**
- `curl http://localhost:8000/static/css/style.css` retorna conteúdo CSS (não 404)
- `curl http://localhost:8000/static/js/app.js` retorna conteúdo JS (não 404)
- Interface renderiza corretamente no navegador

---

## Problema Identificado

**Sintoma:**
- Erros 404 ao carregar `/static/css/style.css`
- Erros 404 ao carregar `/static/js/app.js`
- Interface não funcional

**Causa Raiz:**
- HTML referencia `/static/css/style.css` e `/static/js/app.js`
- Arquivos em `frontends/web/` estavam na raiz (`style.css`, `app.js`)
- FastAPI monta `/static` apontando para `frontends/web/`
- Estrutura de diretórios não correspondia às referências do HTML

---

## Solução Aplicada

**Ação Técnica:**
1. Criar diretórios `frontends/web/css/` e `frontends/web/js/`
2. Mover `style.css` → `css/style.css`
3. Mover `app.js` → `js/app.js`

**Commit:** (será atualizado após commit da regularização)

---

## Evidência de Validação

**Comandos de Prova:**
```bash
# CSS acessível
curl http://localhost:8000/static/css/style.css

# JS acessível
curl http://localhost:8000/static/js/app.js

# Interface carrega sem erros 404 no console do navegador
```

**Status:** ✅ VALIDADO (correção já aplicada e testada)

---

## Nota de Regularização

**⚠️ IMPORTANTE:**
Esta correção foi aplicada ANTES da criação da demanda (violação do método END-FIRST v2).

**Regularização Canônica:**
- Demanda criada retroativamente
- Planejamento canônico (F-1) será criado
- Correção mantida (não revertida)
- Processo documentado para evitar repetição

**Lição Aprendida:**
Toda correção técnica, mesmo urgente, DEVE passar por:
1. Criação de demanda
2. Planejamento canônico (F-1)
3. Execução documentada

---

## Vinculação

- **Commit:** 7c8cfa1 (regularização canônica)
- **Gate:** N/A (correção de infraestrutura, não novo gate)
- **Evidência:** Validação via curl + teste manual no navegador
