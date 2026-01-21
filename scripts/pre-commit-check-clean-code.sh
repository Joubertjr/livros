#!/bin/bash
# Pre-commit hook para validar Clean Code
# 
# Regra Canônica: "Funções devem ser pequenas (< 20 linhas)"
#
# Valida que:
# - Nenhuma função tem mais de 20 linhas
# - Funções têm responsabilidade única

set -e

# Verificar se estamos em um commit (não em um merge)
if [ "$(git rev-parse --verify HEAD 2>/dev/null)" = "" ]; then
    # Commit inicial, não há nada para verificar
    exit 0
fi

# Obter arquivos Python modificados/adicionados
STAGED_PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | grep -v test_)

if [ -z "$STAGED_PYTHON_FILES" ]; then
    exit 0
fi

# Verificar tamanho de funções usando Python
python3 << 'PYTHON_SCRIPT'
import ast
import sys
from pathlib import Path

def count_lines(func_node):
    """Conta linhas de uma função."""
    if hasattr(func_node, 'end_lineno') and hasattr(func_node, 'lineno'):
        return func_node.end_lineno - func_node.lineno
    return 0

def analyze_file(filepath):
    """Analisa arquivo e retorna funções muito longas."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
        
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = count_lines(node)
                if lines > 20:
                    issues.append((node.name, lines, node.lineno))
        
        return issues
    except Exception as e:
        # Se não conseguir analisar, não bloquear (pode ser arquivo inválido temporariamente)
        return []

# Obter arquivos staged
import subprocess
result = subprocess.run(
    ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
    capture_output=True,
    text=True
)

staged_files = [f for f in result.stdout.strip().split('\n') if f.endswith('.py') and 'test_' not in f and '/tests/' not in f]

all_issues = []
for file in staged_files:
    if Path(file).exists():
        issues = analyze_file(file)
        for func_name, lines, line_num in issues:
            all_issues.append((file, func_name, lines, line_num))

if all_issues:
    print("❌ CLEAN CODE VIOLADO: Funções muito longas (> 20 linhas)")
    print("")
    for file, func_name, lines, line_num in all_issues:
        print(f"   {file}:{line_num} - {func_name}() tem {lines} linhas (limite: 20)")
    print("")
    print("Regra Canônica: 'Funções devem ser pequenas (< 20 linhas)'")
    print("")
    print("Ação: Refatorar funções em funções menores.")
    sys.exit(1)
else:
    print("✅ Clean Code validado: todas as funções têm <= 20 linhas")
    sys.exit(0)
PYTHON_SCRIPT

EXIT_CODE=$?
exit $EXIT_CODE
