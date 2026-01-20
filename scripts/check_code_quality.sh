#!/bin/bash
# Script de validação de qualidade de código (Gate Z10)
# Valida TDD + Clean Code automaticamente

set -e

echo "🔍 Validando Gate Z10 - TDD + Clean Code..."
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# 1. Validar testes passam
echo "📋 1. Validando testes (pytest)..."
if pytest -q > /tmp/pytest_output.txt 2>&1; then
    echo -e "${GREEN}✅ Testes passando${NC}"
    FAILED_COUNT=$(grep -o "[0-9]* failed" /tmp/pytest_output.txt | grep -o "[0-9]*" || echo "0")
    if [ "$FAILED_COUNT" != "0" ]; then
        echo -e "${RED}❌ $FAILED_COUNT testes falhando${NC}"
        FAILED=1
    fi
else
    echo -e "${RED}❌ Testes falhando${NC}"
    cat /tmp/pytest_output.txt | tail -20
    FAILED=1
fi
echo ""

# 2. Validar Flake8 (estilo e erros básicos)
echo "📋 2. Validando Flake8 (estilo e erros básicos)..."
if command -v flake8 &> /dev/null; then
    if flake8 src/ --count --statistics --show-source > /tmp/flake8_output.txt 2>&1; then
        echo -e "${GREEN}✅ Flake8: sem erros${NC}"
    else
        ERROR_COUNT=$(grep -c "^src/" /tmp/flake8_output.txt || echo "0")
        if [ "$ERROR_COUNT" -gt "0" ]; then
            echo -e "${YELLOW}⚠️  Flake8 encontrou $ERROR_COUNT problemas${NC}"
            cat /tmp/flake8_output.txt | head -30
            # Não falha o build, mas mostra avisos
        fi
    fi
else
    echo -e "${YELLOW}⚠️  Flake8 não instalado (pular)${NC}"
fi
echo ""

# 3. Validar funções grandes (> 50 linhas)
echo "📋 3. Validando funções grandes (> 50 linhas)..."
LARGE_FUNCTIONS=$(find src/ -name "*.py" -type f -exec grep -l "^def " {} \; | \
    xargs -I {} python3 -c "
import ast
import sys
with open('{}', 'r') as f:
    try:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if lines > 50:
                    print(f'{}:{node.lineno}:{node.name}:{lines} linhas')
    except:
        pass
" 2>/dev/null || true)

if [ -z "$LARGE_FUNCTIONS" ]; then
    echo -e "${GREEN}✅ Nenhuma função > 50 linhas${NC}"
else
    echo -e "${YELLOW}⚠️  Funções > 50 linhas encontradas:${NC}"
    echo "$LARGE_FUNCTIONS"
    # Não falha, mas mostra avisos (pode ser justificado)
fi
echo ""

# 4. Validar TODOs/HACKs/FIXMEs
echo "📋 4. Validando TODOs/HACKs/FIXMEs..."
TODOS=$(grep -rn "TODO\|HACK\|FIXME" src/ --include="*.py" 2>/dev/null | grep -v "^src/tests/" || true)
if [ -z "$TODOS" ]; then
    echo -e "${GREEN}✅ Nenhum TODO/HACK/FIXME encontrado${NC}"
else
    echo -e "${RED}❌ TODOs/HACKs/FIXMEs encontrados:${NC}"
    echo "$TODOS"
    FAILED=1
fi
echo ""

# 5. Validar testes de integração E2E
echo "📋 5. Validando testes de integração E2E..."
E2E_TESTS=$(find src/tests/integration -name "test_*e2e*.py" -o -name "test_*_e2e.py" 2>/dev/null || true)
if [ -z "$E2E_TESTS" ]; then
    echo -e "${YELLOW}⚠️  Nenhum teste E2E encontrado em src/tests/integration/test_*e2e*.py${NC}"
    # Não falha, mas avisa
else
    echo -e "${GREEN}✅ Testes E2E encontrados:${NC}"
    echo "$E2E_TESTS" | sed 's/^/  - /'
fi
echo ""

# Resumo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$FAILED" -eq "0" ]; then
    echo -e "${GREEN}✅ Gate Z10: PASS${NC}"
    exit 0
else
    echo -e "${RED}❌ Gate Z10: FAIL${NC}"
    exit 1
fi
