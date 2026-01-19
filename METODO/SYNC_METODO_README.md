# Sincronização da Pasta METODO/

Este documento descreve como funciona a sincronização automática da pasta `METODO/` com o repositório remoto `endfirst-ecosystem`.

## 📋 Visão Geral

A pasta `METODO/` é sincronizada automaticamente com o repositório:
- **Fonte de verdade:** https://github.com/Joubertjr/endfirst-ecosystem
- **Pasta sincronizada:** `METODO/` (raiz do projeto)
- **Frequência:** Manual (executar quando necessário)

## 🚀 Como Usar

### Dentro do Docker (Recomendado)

```bash
# Sincronizar METODO/
docker compose exec app make sync-metodo
```

### Fora do Docker (Host)

```bash
# Sincronizar METODO/
python scripts/sync_metodo.py
```

## 🔄 O que o Script Faz

1. **Clona/Atualiza repositório remoto** temporariamente
2. **Compara arquivos** da pasta `METODO/` usando hash SHA256
3. **Sincroniza apenas arquivos que mudaram** (cria/atualiza)
4. **Remove arquivos órfãos** (arquivos que existem localmente mas não no remoto)
5. **Gera log de sincronização** em `EVIDENCIAS/metodo_sync_log.md`

## 📝 Log de Sincronização

O script gera um log em `EVIDENCIAS/metodo_sync_log.md` com:
- Data/hora da sincronização
- Lista de arquivos atualizados/criados
- Lista de arquivos removidos
- Resumo da operação

## ⚙️ Detalhes Técnicos

### Algoritmo de Sincronização

- **Hash SHA256:** Usado para detectar mudanças em arquivos
- **Comparação binária:** Garante detecção precisa de alterações
- **Preservação de estrutura:** Mantém subdiretórios e hierarquia

### Arquivos Ignorados

- `.git/` (pastas de controle de versão)
- Arquivos temporários do sistema

### Tratamento de Erros

- **Erro de rede:** Script falha com mensagem clara
- **Erro de permissão:** Verifica permissões de escrita
- **Repositório inacessível:** Informa URL e sugere verificação

## 🔒 Segurança

- **Temporário:** Repositório é clonado em diretório temporário (limpo automaticamente)
- **Somente leitura remota:** Apenas lê do repositório, nunca escreve
- **Validação:** Verifica existência da pasta `METODO/` no repositório antes de sincronizar

## 📊 Exemplo de Saída

```
🚀 Iniciando sincronização da pasta METODO/...
📂 Destino: /app/METODO
🌐 Fonte: https://github.com/Joubertjr/endfirst-ecosystem.git

📥 Clonando repositório remoto...
📄 Encontrados 25 arquivos no repositório remoto
✅ atualizado: PILAR_ENDFIRST.md
✅ atualizado: templates/ENDFIRST_SPEC.md
⏭️  sem mudanças: README.md
...

✅ Sincronização concluída!
📊 3 arquivo(s) atualizado(s), 0 arquivo(s) removido(s)
📝 Log salvo em: /app/EVIDENCIAS/metodo_sync_log.md
```

## 🛠️ Manutenção

### Atualizar Script

O script está em `scripts/sync_metodo.py`. Para modificá-lo:
1. Edite o arquivo
2. Teste localmente: `python scripts/sync_metodo.py`
3. Teste no Docker: `docker compose exec app make sync-metodo`

### Dependências

- **Python 3.11+**
- **Git** (instalado no Dockerfile)
- **Bibliotecas padrão:** `pathlib`, `hashlib`, `subprocess`, `shutil`

## 📚 Referências

- Repositório fonte: https://github.com/Joubertjr/endfirst-ecosystem
- Documentação ENDFIRST: `METODO/PILAR_ENDFIRST.md`
- Log de sincronizações: `EVIDENCIAS/metodo_sync_log.md`
