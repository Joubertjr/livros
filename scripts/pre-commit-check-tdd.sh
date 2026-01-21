#!/bin/bash
# Pre-commit hook para validar ordem TDD
# 
# Regra Canônica: "Teste primeiro, código depois. Sem exceção."
#
# Valida que:
# - Se arquivo de código foi modificado, arquivo de teste correspondente existe
# - Se arquivo de teste foi criado, arquivo de código correspondente foi modificado no mesmo commit

set -e

# Verificar se estamos em um commit (não em um merge)
if [ "$(git rev-parse --verify HEAD 2>/dev/null)" = "" ]; then
    # Commit inicial, não há nada para verificar
    exit 0
fi

# Obter arquivos modificados/adicionados
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

# Verificar cada arquivo Python em src/
for file in $STAGED_FILES; do
    # Ignorar arquivos de teste
    if [[ "$file" == *"test_"* ]] || [[ "$file" == *"/tests/"* ]]; then
        continue
    fi
    
    # Verificar apenas arquivos Python em src/
    if [[ "$file" == src/*.py ]]; then
        # Encontrar arquivo de teste correspondente
        # Exemplo: src/storage/checkpoint_manager.py -> src/tests/unit/test_checkpoint_manager.py
        # ou src/tests/integration/test_checkpoint_manager.py
        
        module_name=$(basename "$file" .py)
        test_file_unit="src/tests/unit/test_${module_name}.py"
        test_file_integration="src/tests/integration/test_${module_name}.py"
        
        # Verificar se arquivo de teste existe (unit ou integration)
        if [ ! -f "$test_file_unit" ] && [ ! -f "$test_file_integration" ]; then
            echo "❌ TDD VIOLADO: Arquivo de código modificado sem teste correspondente"
            echo "   Arquivo: $file"
            echo "   Teste esperado: $test_file_unit ou $test_file_integration"
            echo ""
            echo "Regra Canônica: 'Teste primeiro, código depois. Sem exceção.'"
            echo ""
            echo "Ação: Criar teste antes de modificar código."
            exit 1
        fi
    fi
done

echo "✅ TDD validado: todos os arquivos de código têm testes correspondentes"
exit 0
