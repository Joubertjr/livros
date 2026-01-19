#!/usr/bin/env python3
"""
Gera hash SHA256 dos artefatos canônicos do contrato do sistema.

Artefatos canônicos:
- CHECKLIST_Z_GATES.md (constituição do sistema)
- gates_manifest.json (contrato executável)

Gera arquivo CONTRACT_HASH.txt com hashes para verificação de integridade.
"""

import hashlib
from pathlib import Path
from datetime import datetime

def calculate_file_hash(file_path: Path) -> str:
    """Calcula hash SHA256 de um arquivo."""
    hash_obj = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def main():
    """Gera hash dos artefatos canônicos."""
    import sys
    project_root = Path(__file__).parent.parent
    
    checklist_path = project_root / "CHECKLIST_Z_GATES.md"
    manifest_path = project_root / "gates_manifest.json"
    output_path = project_root / "CONTRACT_HASH.txt"
    
    # Verificar se arquivos existem
    if not checklist_path.exists():
        print(f"Erro: {checklist_path} não encontrado", file=sys.stderr)
        return 1
    
    if not manifest_path.exists():
        print(f"Erro: {manifest_path} não encontrado", file=sys.stderr)
        return 1
    
    # Calcular hashes
    checklist_hash = calculate_file_hash(checklist_path)
    manifest_hash = calculate_file_hash(manifest_path)
    
    # Hash combinado (hash dos dois hashes concatenados)
    combined_content = f"{checklist_hash}{manifest_hash}"
    combined_hash = hashlib.sha256(combined_content.encode('utf-8')).hexdigest()
    
    # Gerar conteúdo do arquivo
    timestamp = datetime.now().isoformat()
    content = f"""Hash dos Artefatos Canônicos do Contrato
================================================

Data/Hora: {timestamp}

Artefatos Canônicos:
1. CHECKLIST_Z_GATES.md (constituição do sistema)
2. gates_manifest.json (contrato executável)

Hashes SHA256:
--------------
CHECKLIST_Z_GATES.md: {checklist_hash}
gates_manifest.json:  {manifest_hash}
Hash Combinado:        {combined_hash}

Verificação:
-----------
Para verificar integridade, execute:
  sha256sum CHECKLIST_Z_GATES.md gates_manifest.json

Os hashes devem corresponder aos valores acima.

Nota: Este arquivo é gerado automaticamente.
Qualquer alteração nos artefatos canônicos resultará em hash diferente.
"""
    
    # Salvar arquivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Hash gerado: {output_path}")
    print(f"   Checklist: {checklist_hash[:16]}...")
    print(f"   Manifest:  {manifest_hash[:16]}...")
    print(f"   Combinado: {combined_hash[:16]}...")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
