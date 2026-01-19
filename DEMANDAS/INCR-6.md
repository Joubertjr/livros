# INCR-6 — Evidência automática

## END

`make evidence` gera tudo em `/EVIDENCIAS/`

## Descrição

Implementar comando `make evidence` que gera automaticamente evidências de execução do sistema. As evidências devem ser salvas em `/EVIDENCIAS/` e incluir informações sobre execuções, resultados e validações.

## Critérios de Aceitação

- [x] Comando `make evidence` funciona dentro do container
- [x] Gera evidências automaticamente em `/EVIDENCIAS/`
- [x] Evidências incluem informações de execução
- [x] Evidências incluem resultados de processamento
- [x] Evidências incluem validações do Quality Gate
- [x] Formato de evidências é estruturado e legível
- [x] Evidências são versionadas (se usando Git)
- [x] Comando pode ser executado a qualquer momento

## Tarefas Técnicas

1. ✅ Implementar comando `make evidence` no Makefile
2. ✅ Criar estrutura de evidências (formato JSON e texto estruturado)
3. ✅ Coletar informações de execução (timestamps, versão, configurações)
4. ✅ Coletar resultados de processamento (resumos gerados, estatísticas)
5. ✅ Coletar resultados de validação (Quality Gate)
6. ✅ Implementar geração de relatório formatado
7. ✅ Configurar volume Docker para evidências
8. ✅ Testar geração de evidências

## Notas

- Evidências devem ser úteis para validação e debugging
- Formato deve ser legível tanto por humanos quanto por máquinas
- Considerar incluir exemplos de resumos gerados
- Evidências ajudam a validar que o sistema está funcionando conforme especificado
