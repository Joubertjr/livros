# INCR-1 — Fundação Docker + Hello Flow

## END

- `docker compose up` sobe sistema
- UI/CLI responde
- Texto enviado gera "stub summary"

## Descrição

Primeiro incremento focado em estabelecer a fundação Docker e um fluxo básico de funcionamento. O sistema deve subir completamente via Docker e responder a entradas básicas, mesmo que apenas com um resumo stub (placeholder).

## Critérios de Aceitação

- [x] `docker compose up --build` sobe o sistema sem erros
- [x] Container fica rodando e acessível
- [x] CLI básica funciona dentro do container
- [x] Sistema aceita entrada de texto ou arquivo
- [x] Gera um resumo stub (placeholder) como resposta
- [x] Não requer instalação de dependências no host

## Tarefas Técnicas

1. ✅ Configurar Dockerfile com Python e dependências básicas
2. ✅ Configurar docker-compose.yml com volumes e variáveis de ambiente
3. ✅ Criar estrutura básica de CLI em `src/`
4. ✅ Implementar entrada básica (texto ou arquivo)
5. ✅ Implementar geração de resumo stub
6. ✅ Testar fluxo completo dentro do Docker

## Notas

- Este é um incremento de fundação, não precisa gerar resumos reais ainda
- Foco em validar que o Docker funciona e o fluxo básico está estabelecido
- O resumo stub pode ser apenas uma mensagem fixa confirmando que o sistema recebeu a entrada
