# INCR-5 — Export

## END

Export MD/PDF salvo em volume

## Descrição

Implementar funcionalidade de exportação dos resumos gerados em formatos Markdown e PDF. Os arquivos devem ser salvos no volume Docker configurado.

## Critérios de Aceitação

- [x] Exporta resumos em formato Markdown
- [x] Exporta resumos em formato PDF
- [x] Arquivos são salvos em `volumes/`
- [x] Nomes de arquivo são descritivos e únicos
- [x] PDF mantém formatação adequada
- [x] Markdown é bem formatado e legível
- [x] Exportação funciona para todos os tipos de resumo
- [x] Arquivos são acessíveis fora do container

## Tarefas Técnicas

1. ✅ Implementar geração de arquivo Markdown
2. ✅ Implementar geração de arquivo PDF (usando reportlab)
3. ✅ Criar templates de formatação
4. ✅ Implementar sistema de nomenclatura de arquivos
5. ✅ Configurar volume Docker para exportações
6. ✅ Adicionar opção de escolha de formato na CLI
7. ✅ Testar exportação de diferentes tipos de resumo

## Notas

- PDF deve incluir todos os tipos de resumo (curto, médio, longo, bullets, insights)
- Markdown deve ser bem formatado para leitura
- Considerar incluir metadados (data, livro processado, etc.)
