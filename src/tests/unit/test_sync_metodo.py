"""
Testes unitários para o script de sincronização de METODO/.

Testa funções auxiliares do script sync_metodo.py.
"""

import pytest
import tempfile
import hashlib
from pathlib import Path
import sys

# Adicionar scripts ao path para importar
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))

from sync_metodo import get_file_hash, get_file_info, get_relative_path


def test_get_file_hash():
    """Testa cálculo de hash de arquivo."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = Path(f.name)
    
    try:
        hash1 = get_file_hash(temp_path)
        assert len(hash1) == 64  # SHA256 tem 64 caracteres hex
        assert hash1 != ""
        
        # Hash deve ser determinístico
        hash2 = get_file_hash(temp_path)
        assert hash1 == hash2
        
        # Hash deve mudar com conteúdo diferente
        temp_path.write_text("different content")
        hash3 = get_file_hash(temp_path)
        assert hash3 != hash1
    finally:
        temp_path.unlink()


def test_get_file_hash_nonexistent():
    """Testa hash de arquivo inexistente."""
    nonexistent = Path("/tmp/nonexistent_file_12345")
    hash_result = get_file_hash(nonexistent)
    assert hash_result == ""


def test_get_file_info():
    """Testa obtenção de informações de arquivo."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        temp_path = Path(f.name)
    
    try:
        info = get_file_info(temp_path)
        assert info["exists"] is True
        assert info["size"] > 0
        assert "mtime" in info
        assert "hash" in info
        assert len(info["hash"]) == 64
    finally:
        temp_path.unlink()


def test_get_file_info_nonexistent():
    """Testa informações de arquivo inexistente."""
    nonexistent = Path("/tmp/nonexistent_file_12345")
    info = get_file_info(nonexistent)
    assert info["exists"] is False


def test_get_relative_path():
    """Testa obtenção de caminho relativo."""
    base = Path("/app/METODO")
    file_path = Path("/app/METODO/templates/ENDFIRST_SPEC.md")
    
    relative = get_relative_path(file_path, base)
    assert relative == Path("templates/ENDFIRST_SPEC.md")
    
    # Teste com subdiretório
    file_path2 = Path("/app/METODO/examples/SPEC_001.md")
    relative2 = get_relative_path(file_path2, base)
    assert relative2 == Path("examples/SPEC_001.md")


def test_get_relative_path_same():
    """Testa caminho relativo quando arquivo está na raiz."""
    base = Path("/app/METODO")
    file_path = Path("/app/METODO/README.md")
    
    relative = get_relative_path(file_path, base)
    assert relative == Path("README.md")
