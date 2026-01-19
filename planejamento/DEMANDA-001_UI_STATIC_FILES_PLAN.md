# Planejamento Canônico — DEMANDA-001: Correção de Arquivos Estáticos 404

**Demanda:** DEMANDA-001_UI_STATIC_FILES_404.md  
**Tipo:** Regularização Canônica (correção já aplicada)  
**Data:** 2026-01-19

---

## END (Resultado Final Esperado)

**Para o Usuário Final:**
Interface web totalmente funcional em `http://localhost:8000/`:
- CSS carrega sem erro 404
- JavaScript carrega sem erro 404
- Interface visualmente correta e utilizável

**Critério de Aceitação (BINÁRIO):**
- ✅ `curl http://localhost:8000/static/css/style.css` retorna CSS (não 404)
- ✅ `curl http://localhost:8000/static/js/app.js` retorna JS (não 404)
- ✅ Navegador não mostra erros 404 no console

---

## DO / DON'T

### DO (Obrigatório)
- Criar estrutura de diretórios `css/` e `js/` em `frontends/web/`
- Mover arquivos para estrutura esperada pelo HTML
- Validar via curl e navegador
- Documentar correção na demanda

### DON'T (Proibido)
- Alterar referências no HTML (já estão corretas)
- Modificar configuração do FastAPI (já está correta)
- Criar estrutura alternativa (usar estrutura padrão)

---

## Execução (Já Aplicada)

**Ação Técnica Executada:**
1. ✅ Criados diretórios `frontends/web/css/` e `frontends/web/js/`
2. ✅ Movido `style.css` → `css/style.css`
3. ✅ Movido `app.js` → `js/app.js`

**Validação:**
- ✅ `curl http://localhost:8000/static/css/style.css` retorna CSS
- ✅ `curl http://localhost:8000/static/js/app.js` retorna JS
- ✅ Interface funcional no navegador

---

## Evidência de Validação

**Comandos Executados:**
```bash
# Estrutura criada
mkdir -p frontends/web/css frontends/web/js

# Arquivos movidos
mv frontends/web/style.css frontends/web/css/style.css
mv frontends/web/app.js frontends/web/js/app.js

# Validação
curl http://localhost:8000/static/css/style.css  # ✅ Retorna CSS
curl http://localhost:8000/static/js/app.js      # ✅ Retorna JS
```

**Status:** ✅ PASS (correção aplicada e validada)

---

## Nota de Regularização

**⚠️ REGULARIZAÇÃO CANÔNICA:**

Esta correção foi aplicada ANTES da criação da demanda e do planejamento (violação do método END-FIRST v2).

**Ações de Regularização:**
1. ✅ Demanda criada (DEMANDA-001)
2. ✅ Planejamento canônico criado (este documento)
3. ✅ Correção mantida (não revertida)
4. ✅ Processo documentado

**Compromisso:**
Todas as correções futuras seguirão o método canônico:
- Demanda → Planejamento (F-1) → Execução

---

## Checklist Final

- [x] Demanda criada
- [x] Planejamento canônico criado
- [x] Correção aplicada e validada
- [x] Evidência de validação documentada
- [x] Regularização canônica concluída

**Status:** ✅ REGULARIZADO
