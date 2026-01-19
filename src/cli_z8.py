#!/usr/bin/env python3
"""
Gate Z8 - Prova Real com PDF

Executa pipeline completo usando BookSummarizerRobust com PDF real,
gera evidências e valida critérios binários do Z8.
"""

import asyncio
import argparse
import sys
import json
from pathlib import Path
from typing import Tuple, List

# Adicionar src ao path para imports
# Dentro do Docker, working dir é /app, então src está em /app/src
# Fora do Docker, src está no mesmo diretório do script
script_dir = Path(__file__).parent
if (script_dir / "src").exists():
    # Estamos fora do Docker, adicionar src ao path
    sys.path.insert(0, str(script_dir))
else:
    # Estamos dentro do Docker, src já está no path
    sys.path.insert(0, "/app")

from summarizer_robust import BookSummarizerRobust
from exceptions import CoverageError

# Tentar usar document_reader primeiro, fallback para pdf_reader
try:
    from document_reader import read_pdf_to_markdown
    READ_PDF_FUNC = read_pdf_to_markdown
except ImportError:
    from pdf_reader import read_pdf_file
    READ_PDF_FUNC = read_pdf_file


def validate_z8(evidencias_dir: str = "/app/EVIDENCIAS") -> Tuple[bool, List[str]]:
    """
    Valida critérios binários do Gate Z8.
    
    Args:
        evidencias_dir: Diretório onde estão as evidências
        
    Returns:
        (is_pass, errors): Tupla com status de passagem e lista de erros
    """
    report_path = Path(evidencias_dir) / "coverage_report.json"
    
    if not report_path.exists():
        return False, ["coverage_report.json não encontrado"]
    
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Erro ao ler coverage_report.json: {e}"]
    
    errors = []
    
    # Critério 1: overall_coverage_percentage == 100.0
    summary = data.get('summary', {})
    overall = summary.get('overall_coverage_percentage', 0)
    if overall != 100.0:
        errors.append(f"overall_coverage_percentage = {overall}% (esperado: 100.0%)")
    
    # Critério 2: total_critical_items == total_covered
    total_items = summary.get('total_critical_items', 0)
    total_covered = summary.get('total_covered', 0)
    if total_items != total_covered:
        errors.append(f"total_critical_items ({total_items}) != total_covered ({total_covered})")
    
    # Critério 3: Para todo capítulo
    chapters = data.get('chapters', [])
    for ch in chapters:
        ch_num = ch.get('chapter_number', '?')
        
        # processed_chunks == total_chunks
        processed = ch.get('processed_chunks', 0)
        total = ch.get('total_chunks', 0)
        if processed != total:
            errors.append(f"Cap {ch_num}: processed_chunks ({processed}) != total_chunks ({total})")
        
        # missing_critical_item_ids é []
        missing = ch.get('missing_critical_item_ids', [])
        if missing:
            errors.append(f"Cap {ch_num}: missing_critical_item_ids = {missing} (esperado: [])")
    
    # Tripwire extra: soma de missing_critical_item_ids deve ser 0
    total_missing = sum(len(ch.get('missing_critical_item_ids', [])) for ch in chapters)
    if total_missing > 0:
        errors.append(f"Total de missing_critical_item_ids = {total_missing} (esperado: 0)")
    
    return len(errors) == 0, errors


async def main():
    """Função principal do CLI Z8."""
    parser = argparse.ArgumentParser(
        description='Gate Z8 - Prova Real com PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplo:
  python src/cli_z8.py --file /app/volumes/Dopamine_Nation_-_Anna_Lembke.pdf
        """
    )
    parser.add_argument(
        '--file',
        required=True,
        help='Caminho do PDF a ser processado'
    )
    parser.add_argument(
        '--evidencias-dir',
        default='/app/EVIDENCIAS',
        help='Diretório para salvar evidências (padrão: /app/EVIDENCIAS)'
    )
    
    args = parser.parse_args()
    
    # Verificar se arquivo existe
    pdf_path = Path(args.file)
    if not pdf_path.exists():
        print(f"❌ Erro: Arquivo não encontrado: {args.file}", file=sys.stderr)
        return 1
    
    # Ler PDF
    print(f"📖 Lendo PDF: {args.file}", file=sys.stderr)
    try:
        text = READ_PDF_FUNC(str(pdf_path))
        print(f"✅ PDF lido: {len(text)} caracteres, {len(text.split())} palavras", file=sys.stderr)
    except Exception as e:
        print(f"❌ Erro ao ler PDF: {e}", file=sys.stderr)
        return 1
    
    # Executar pipeline
    print(f"🚀 Iniciando pipeline robusto (Gate Z8)...", file=sys.stderr)
    print(f"📁 Evidências serão salvas em: {args.evidencias_dir}", file=sys.stderr)
    
    try:
        summarizer = BookSummarizerRobust(evidencias_dir=args.evidencias_dir)
        result = await summarizer.summarize_robust(text)
        
        print("✅ Pipeline executado com sucesso", file=sys.stderr)
        
        # Validar critérios binários Z8
        print("🔍 Validando critérios binários do Gate Z8...", file=sys.stderr)
        is_pass, errors = validate_z8(args.evidencias_dir)
        
        if not is_pass:
            print("❌ Gate Z8: FAIL - Critérios não atendidos:", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1
        else:
            print("✅ Gate Z8: PASS - Todos os critérios atendidos", file=sys.stderr)
            
            # Exibir métricas principais
            report_path = Path(args.evidencias_dir) / "coverage_report.json"
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            summary = data.get('summary', {})
            print("\n📊 Métricas principais:", file=sys.stderr)
            print(f"  - Overall Coverage: {summary.get('overall_coverage_percentage', 0)}%", file=sys.stderr)
            print(f"  - Total Chapters: {summary.get('total_chapters', 0)}", file=sys.stderr)
            print(f"  - Total Critical Items: {summary.get('total_critical_items', 0)}", file=sys.stderr)
            print(f"  - Total Covered: {summary.get('total_covered', 0)}", file=sys.stderr)
            print(f"  - Evidências: {args.evidencias_dir}", file=sys.stderr)
            
            return 0
            
    except CoverageError as e:
        print(f"❌ Gate Z8: FAIL - Quality Gate falhou: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
