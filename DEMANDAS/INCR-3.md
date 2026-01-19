# INCR-3 — Rastreabilidade

## END

Cada saída aponta para trechos do texto

## Descrição

Implementar sistema de rastreabilidade onde cada parte do resumo referencia os trechos específicos do livro original. Isso garante que não existam resumos "soltos" ou não justificáveis.

## Critérios de Aceitação

- [x] Cada resumo referencia trechos do texto original
- [x] Referências incluem localização (página, capítulo, ou posição)
- [x] Sistema mantém mapeamento entre resumo e texto original
- [x] Usuário pode verificar origem de cada afirmação
- [x] Rastreabilidade funciona para todos os tipos de resumo
- [x] Referências são precisas e verificáveis

## Tarefas Técnicas

1. ✅ Implementar sistema de indexação de trechos do texto
2. ✅ Criar estrutura de dados para mapear resumo → trechos
3. ✅ Modificar prompts para incluir referências nos resumos
4. ✅ Adicionar metadados de localização (posição em palavras e %)
5. ✅ Implementar visualização de referências na saída
6. ✅ Validar precisão das referências

## Notas

- Referências podem ser por número de página, capítulo, ou posição no texto
- Sistema deve manter contexto suficiente para rastreabilidade
- Importante para validar qualidade e evitar alucinações
