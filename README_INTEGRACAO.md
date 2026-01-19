# ENDFIRST no projeto /livros — Integração mínima (CANÔNICA)

Este bundle adiciona o **END-FIRST v2** ao repositório **/livros**, para que o executor (Cursor) tenha uma referência **dentro do repo**.

## O que este ZIP contém
- `METODO/END_FIRST_V2.md` (copiado do repositório canônico endfirst-ecosystem)

## O que você deve fazer (ordem obrigatória)
1) **No repo /livros**, crie (se não existir) a pasta `METODO/`
2) Copie o arquivo `METODO/END_FIRST_V2.md` para dentro do repo
3) Faça commit com mensagem sugestão:
   - `docs: adiciona END-FIRST v2 ao repo (F-1 Planejamento Canônico)`
4) Atualize o `.cursorrules` do /livros para apontar explicitamente para:
   - `METODO/END_FIRST_V2.md`
   - Regra: **demanda complexa => exigir F-1 aprovado antes de executar**
5) (Opcional mas recomendado) Adicione no README um link curto:
   - `Método END-FIRST (v2): METODO/END_FIRST_V2.md`

## Regra de uso (para o Cursor)
- Se a tarefa envolve **múltiplos arquivos / fases / decisões**, o Cursor deve:
  - exigir documento F-1 (planejamento canônico) no repo
  - exigir a string literal: **"F-1 aprovada"**
  - só então executar

Se não existir F-1 aprovado quando necessário:
> "Esta demanda requer F-1 (Planejamento Canônico). Sem F-1 aprovada, não posso executar."
