#!/usr/bin/env python3
"""
Script de sincronização da pasta METODO/ do repositório endfirst-ecosystem.

Este script:
1. Clona/atualiza o repositório remoto temporariamente
2. Compara arquivos da pasta METODO/
3. Sincroniza apenas arquivos que mudaram
4. Mantém log de sincronização

Fonte de verdade: https://github.com/Joubertjr/endfirst-ecosystem
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
import hashlib


# Configurações
REPO_URL = "https://github.com/Joubertjr/endfirst-ecosystem.git"
METODO_SOURCE = "METODO"

# Detectar se está rodando no Docker ou no host
def get_metodo_target() -> Path:
    """Retorna caminho da pasta METODO/ dependendo do ambiente."""
    if os.path.exists("/app"):
        # Docker
        return Path("/app/METODO")
    else:
        # Host
        return Path(__file__).parent.parent / "METODO"

def get_sync_log_path() -> Path:
    """Retorna caminho do log de sincronização."""
    if os.path.exists("/app"):
        # Docker
        return Path("/app/EVIDENCIAS") / "metodo_sync_log.md"
    else:
        # Host
        return Path(__file__).parent.parent / "EVIDENCIAS" / "metodo_sync_log.md"

METODO_TARGET = get_metodo_target()
SYNC_LOG = get_sync_log_path()


def get_file_hash(file_path: Path) -> str:
    """Calcula hash SHA256 de um arquivo."""
    if not file_path.exists():
        return ""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def get_file_info(file_path: Path) -> dict:
    """Retorna informações sobre um arquivo."""
    if not file_path.exists():
        return {"exists": False}
    stat = file_path.stat()
    return {
        "exists": True,
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "hash": get_file_hash(file_path)
    }


def clone_or_update_repo(temp_dir: Path) -> Path:
    """Clona ou atualiza o repositório remoto."""
    repo_dir = temp_dir / "endfirst-ecosystem"
    
    if repo_dir.exists():
        print(f"🔄 Atualizando repositório existente...")
        subprocess.run(
            ["git", "pull", "origin", "master"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )
    else:
        print(f"📥 Clonando repositório remoto...")
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, str(repo_dir)],
            check=True,
            capture_output=True
        )
    
    return repo_dir


def find_metodo_files(directory: Path) -> List[Path]:
    """Encontra todos os arquivos na pasta METODO/ recursivamente."""
    metodo_dir = directory / METODO_SOURCE
    if not metodo_dir.exists():
        return []
    
    files = []
    for root, dirs, filenames in os.walk(metodo_dir):
        # Ignorar .git
        if '.git' in root:
            continue
        for filename in filenames:
            file_path = Path(root) / filename
            files.append(file_path)
    
    return files


def get_relative_path(file_path: Path, base_dir: Path) -> Path:
    """Retorna caminho relativo a partir do diretório base."""
    try:
        return file_path.relative_to(base_dir)
    except ValueError:
        return file_path


def sync_file(source: Path, target: Path, relative_path: Path) -> Tuple[bool, str]:
    """
    Sincroniza um arquivo individual.
    Retorna (atualizado, mensagem)
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    
    source_info = get_file_info(source)
    target_info = get_file_info(target)
    
    # Se arquivo não existe no destino ou hash é diferente
    if not target_info.get("exists") or source_info["hash"] != target_info["hash"]:
        shutil.copy2(source, target)
        action = "criado" if not target_info.get("exists") else "atualizado"
        return True, f"✅ {action}: {relative_path}"
    
    return False, f"⏭️  sem mudanças: {relative_path}"


def remove_orphaned_files(source_files: List[Path], target_dir: Path, source_base: Path) -> List[str]:
    """
    Remove arquivos que existem no destino mas não no source.
    Retorna lista de arquivos removidos.
    """
    removed = []
    
    # Criar conjunto de caminhos relativos do source
    source_relative = {
        get_relative_path(f, source_base): f
        for f in source_files
    }
    
    # Encontrar arquivos no destino
    if not target_dir.exists():
        return removed
    
    for root, dirs, filenames in os.walk(target_dir):
        for filename in filenames:
            target_file = Path(root) / filename
            relative = get_relative_path(target_file, target_dir)
            
            # Se arquivo não existe no source, remover
            if relative not in source_relative:
                target_file.unlink()
                removed.append(f"🗑️  removido: {relative}")
    
    return removed


def write_sync_log(updates: List[str], removed: List[str], timestamp: datetime):
    """Escreve log de sincronização."""
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    log_content = f"""# Log de Sincronização METODO/

**Data:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Fonte:** {REPO_URL}
**Destino:** {METODO_TARGET}

## Arquivos Atualizados/Criados

{chr(10).join(updates) if updates else '*Nenhum arquivo atualizado*'}

## Arquivos Removidos

{chr(10).join(removed) if removed else '*Nenhum arquivo removido*'}

## Resumo

- **Total atualizado/criado:** {len(updates)}
- **Total removido:** {len(removed)}
- **Status:** {'✅ Sincronização concluída' if (updates or removed) else '⏭️  Já está sincronizado'}

---
"""
    
    # Adicionar ao log existente (append)
    with open(SYNC_LOG, 'a', encoding='utf-8') as f:
        f.write(log_content)


def main():
    """Função principal de sincronização."""
    print("🚀 Iniciando sincronização da pasta METODO/...")
    print(f"📂 Destino: {METODO_TARGET}")
    print(f"🌐 Fonte: {REPO_URL}")
    print()
    
    timestamp = datetime.now()
    
    # Criar diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        try:
            # Clonar/atualizar repositório
            repo_dir = clone_or_update_repo(temp_path)
            source_metodo = repo_dir / METODO_SOURCE
            
            if not source_metodo.exists():
                print(f"❌ Erro: Pasta {METODO_SOURCE} não encontrada no repositório remoto")
                sys.exit(1)
            
            # Encontrar todos os arquivos no source
            source_files = find_metodo_files(repo_dir)
            print(f"📄 Encontrados {len(source_files)} arquivos no repositório remoto")
            
            # Sincronizar arquivos
            updates = []
            for source_file in source_files:
                relative_path = get_relative_path(source_file, source_metodo)
                target_file = METODO_TARGET / relative_path
                
                updated, message = sync_file(source_file, target_file, relative_path)
                if updated:
                    updates.append(message)
                    print(message)
            
            # Remover arquivos órfãos
            removed = remove_orphaned_files(source_files, METODO_TARGET, source_metodo)
            for msg in removed:
                print(msg)
            
            # Escrever log
            write_sync_log(updates, removed, timestamp)
            
            print()
            print(f"✅ Sincronização concluída!")
            print(f"📊 {len(updates)} arquivo(s) atualizado(s), {len(removed)} arquivo(s) removido(s)")
            print(f"📝 Log salvo em: {SYNC_LOG}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar git: {e}")
            if e.stdout:
                print(f"stdout: {e.stdout.decode()}")
            if e.stderr:
                print(f"stderr: {e.stderr.decode()}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
