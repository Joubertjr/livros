# INCR-2 — Pipeline de sumarização v1

## END

Dentro do Docker gera:
- curto / médio / longo
- bullets

## Descrição

Implementar o pipeline básico de sumarização usando OpenAI. O sistema deve processar o texto do livro e gerar resumos em três tamanhos diferentes (curto, médio, longo) além de bullet points.

## Critérios de Aceitação

- [x] Sistema processa texto completo do livro
- [x] Gera resumo curto (até 100 palavras)
- [x] Gera resumo médio (até 300 palavras)
- [x] Gera resumo longo (até 500 palavras)
- [x] Gera bullet points principais
- [x] Todas as gerações acontecem dentro do Docker
- [x] Usa OpenAI API para sumarização
- [x] Respostas são estruturadas e consistentes

## Tarefas Técnicas

1. ✅ Integrar biblioteca OpenAI no Docker
2. ✅ Implementar função de sumarização com prompts estruturados
3. ✅ Criar prompts específicos para cada tipo de resumo
4. ✅ Implementar processamento de texto longo (chunking se necessário)
5. ✅ Estruturar saída em formatos diferentes
6. ✅ Adicionar tratamento de erros da API

## Notas

- Usar técnica de chunking para livros grandes
- Prompts devem ser determinísticos (não escritos pelo usuário)
- Focar em qualidade básica, refinamentos vêm depois
