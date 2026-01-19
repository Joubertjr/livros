# Plano: Book Summarizer - DEMANDA-000

## Objetivo

Criar estrutura inicial do projeto conforme especificação da DEMANDA-000, sem executar código ainda. Foco em documentação, estrutura Docker e cards de trabalho.

## Decisões Técnicas

- **Interface**: CLI (mais simples para MVP)
- **Entrada**: PDF (formato do exemplo fornecido)
- **Provider**: OpenAI

## Estrutura de Arquivos a Criar

### 1. Documentação da Demanda

- `DEMANDAS/DEMANDA-000_BOOK_SUMMARIZER.md` - Especificação completa do produto
- `DEMANDAS/DEMANDA-000_ACCEPTANCE.md` - Critérios de aceitação (CA-00 a CA-07)

### 2. Estrutura Base do Projeto

- `docker-compose.yml` - Configuração Docker (fundação)
- `Dockerfile` - Imagem base do container
- `.env.example` - Template de variáveis de ambiente
- `.cursorrules` - Regras e diretrizes para o Cursor
- `README.md` - Documentação inicial do projeto
- `Makefile` - Comandos auxiliares (incluindo `make evidence`)

### 3. Estrutura de Pastas

- `DEMANDAS/` - Documentação de demandas
- `EVIDENCIAS/` - Evidências geradas automaticamente
- `src/` - Código fonte (estrutura básica)
- `volumes/` - Volume Docker para exportações (MD/PDF)
- `planejamento/` - Planos de execução do projeto
- `plan-000.md` - Plano inicial (este arquivo será copiado para cá)

### 4. Cards de Trabalho

Cards para cada incremento:

- INCR-1: Fundação Docker + Hello Flow
- INCR-2: Pipeline de sumarização v1
- INCR-3: Rastreabilidade
- INCR-4: Quality Gate
- INCR-5: Export
- INCR-6: Evidência automática

## Detalhamento dos Arquivos

### DEMANDA-000_BOOK_SUMMARIZER.md

Conterá:

- END imutável
- Princípios inegociáveis
- Critérios de aceitação (referência)
- Arquitetura (restrições)
- Incrementos (INCR-1 a INCR-6)

### DEMANDA-000_ACCEPTANCE.md

Lista detalhada dos critérios:

- CA-00: Docker como gating absoluto
- CA-01: Entrada mínima funcional (PDF)
- CA-02: Tipos de resumo (curto/médio/longo + bullets + insights + referências)
- CA-03: Pipeline determinístico
- CA-04: Quality Gate automático
- CA-05: Rastreabilidade
- CA-06: Export (MD/PDF)
- CA-07: Evidência reproduzível

### docker-compose.yml

Configuração mínima inicial:

- Serviço principal (`app`)
- Volume para exportações
- Volume para evidências
- Variáveis de ambiente via `.env`

### Dockerfile

Base para processamento de PDFs e chamadas de IA:

- Python como base (para processamento de PDF e APIs de IA)
- Dependências: PyPDF2/pdfplumber, openai (biblioteca oficial)
- Estrutura preparada para CLI
- Nota: `.venv` existente não será usado no Docker (container terá seu próprio ambiente)

### .cursorrules

Regras e diretrizes para o Cursor seguir durante o desenvolvimento:

- Restrições Docker obrigatórias
- Padrões de código e estrutura

### planejamento/plan-000.md

Cópia deste plano de planejamento no projeto para rastreabilidade.

## Observações Importantes

- Não executar código ainda (apenas estrutura)
- Cards serão criados como markdown na pasta `DEMANDAS/`
- Técnica de resumo em camadas (chunking) será implementada nos incrementos seguintes
- Ambiente `.venv` já existe no projeto (não criar)
- Arquivos de exemplo já existem: `Dopamine_Nation_-_Anna_Lembke.md` e `Dopamine_Nation_-_Anna_Lembke.pdf` (usar como referência)

## Próximos Passos Após Validação

1. CEO valida estrutura
2. Início do INCR-1 (primeiro código funcional)
