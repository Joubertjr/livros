# TEMPLATE F-1: PLANEJAMENTO CANÔNICO

**Status:** Template Oficial  
**Versão:** 1.0  
**Governado por:** `/METODO/END_FIRST_V2.md`  
**Uso obrigatório:** ✅ SIM (para demandas complexas)

**NOTA:** Este arquivo deve ser sincronizado para o repositório remoto `endfirst-ecosystem` para uso canônico.

---

## ESTRUTURA OBRIGATÓRIA

### 0️⃣ METADADOS

```yaml
demanda_id: ________
tipo: PROD / METODO / UX / BUG
classe: A / B / C / D
f1_criado_em: YYYY-MM-DD
f1_criado_por: ________
status: PENDENTE / APROVADO
```

---

### 6️⃣ VALIDAÇÃO DE TDD E CLEAN CODE (OBRIGATÓRIO)

**Regra Canônica:** "Teste primeiro, código depois. Sem exceção."
**Regra Canônica:** "Funções devem ser pequenas (< 20 linhas)."

#### Critérios Binários de Validação

**TDD:**
- [ ] Testes foram criados ANTES do código?
- [ ] Ciclo RED-GREEN-REFACTOR foi seguido?
- [ ] Todos os testes estão passando?

**Clean Code:**
- [ ] Todas as funções têm <= 20 linhas?
- [ ] Cada função tem responsabilidade única?
- [ ] Código foi refatorado para eliminar duplicação?

#### Bloqueio

**Fase não pode ser declarada completa sem:**
- ✅ Validação de TDD (testes antes de código)
- ✅ Validação de Clean Code (funções <= 20 linhas)
- ✅ Execução de `pytest -q` com todos os testes passando
- ✅ Validação de tamanho de funções (script ou linter)

**Violação = FAIL estrutural**

---

**Template canônico:** Deve ser sincronizado para `/METODO/TEMPLATE_F1_PLANEJAMENTO_CANONICO.md` no repositório remoto  
**Governado por:** END-FIRST v2
