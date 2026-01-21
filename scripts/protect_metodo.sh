#!/bin/bash
# Script para tornar METODO/ somente leitura
# Proteção contra modificações locais

METODO_DIR="${1:-METODO}"

if [ ! -d "$METODO_DIR" ]; then
    echo "❌ Diretório $METODO_DIR não encontrado"
    exit 1
fi

echo "🔒 Aplicando proteção somente leitura em $METODO_DIR/..."

# Tornar todos os arquivos somente leitura
find "$METODO_DIR" -type f -exec chmod 444 {} \;

# Tornar diretórios somente leitura (sem permissão de escrita)
find "$METODO_DIR" -type d -exec chmod 555 {} \;

echo "✅ Proteção aplicada: $METODO_DIR/ é somente leitura"
echo "📝 Arquivos não podem ser modificados localmente"
echo "📝 Use 'make sync-metodo' para atualizar do repositório remoto"
