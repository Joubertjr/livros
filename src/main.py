#!/usr/bin/env python3
"""
CoverageSummarizer - DEMANDA-000
INCR-2: Pipeline de sumarização v1
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from summarizer import BookSummarizer
from pdf_reader import read_pdf_file
from exporter import export_summaries
from evidence_generator import EvidenceGenerator


def read_text_file(file_path: str) -> str:
    """Lê conteúdo de um arquivo de texto."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def format_summaries(summaries: dict) -> str:
    """
    Formata todos os resumos para exibição com rastreabilidade.
    
    Args:
        summaries: Dicionário com os resumos gerados e referências
    
    Returns:
        String formatada com todos os resumos e referências
    """
    from tracker import format_references
    
    output = []
    output.append("=" * 70)
    output.append("RESUMOS GERADOS - CoverageSummarizer (INCR-4: Quality Gate)")
    output.append("=" * 70)
    output.append("")
    
    # Informações de rastreabilidade
    if "tracker_info" in summaries:
        info = summaries["tracker_info"]
        output.append(f"📊 Informações do texto: {info.get('total_palavras', 'N/A')} palavras, {info.get('total_segmentos', 'N/A')} segmentos")
        output.append("")
    
    referencias = summaries.get("referencias", {})
    
    # Resumo Curto
    output.append("─" * 70)
    output.append("📝 RESUMO CURTO (até 100 palavras)")
    output.append("─" * 70)
    output.append(summaries.get("curto", "N/A"))
    if referencias.get("curto"):
        output.append("")
        output.append("📍 Referências no texto original:")
        for key, refs in list(referencias["curto"].items())[:3]:  # Limitar a 3 referências
            output.append(f"  • {key[:80]}...")
            output.append(format_references(refs))
    output.append("")
    
    # Resumo Médio
    output.append("─" * 70)
    output.append("📄 RESUMO MÉDIO (até 300 palavras)")
    output.append("─" * 70)
    output.append(summaries.get("medio", "N/A"))
    if referencias.get("medio"):
        output.append("")
        output.append("📍 Referências no texto original:")
        for key, refs in list(referencias["medio"].items())[:5]:  # Limitar a 5 referências
            output.append(f"  • {key[:80]}...")
            output.append(format_references(refs))
    output.append("")
    
    # Resumo Longo
    output.append("─" * 70)
    output.append("📚 RESUMO LONGO (até 500 palavras)")
    output.append("─" * 70)
    output.append(summaries.get("longo", "N/A"))
    if referencias.get("longo"):
        output.append("")
        output.append("📍 Referências no texto original:")
        for key, refs in list(referencias["longo"].items())[:7]:  # Limitar a 7 referências
            output.append(f"  • {key[:80]}...")
            output.append(format_references(refs))
    output.append("")
    
    # Bullet Points
    output.append("─" * 70)
    output.append("🔹 BULLET POINTS PRINCIPAIS")
    output.append("─" * 70)
    output.append(summaries.get("bullets", "N/A"))
    if referencias.get("bullets"):
        output.append("")
        output.append("📍 Referências no texto original:")
        for key, refs in list(referencias["bullets"].items())[:5]:  # Limitar a 5 referências
            output.append(f"  • {key[:80]}...")
            output.append(format_references(refs))
    output.append("")
    
    # Quality Gate Report
    if "validation_report" in summaries:
        output.append("")
        output.append(summaries["validation_report"])
    
    # Aviso se validação falhou
    if summaries.get("validation_failed"):
        output.append("")
        output.append("⚠️  AVISO: " + summaries.get("validation_message", "Validação falhou"))
    
    output.append("")
    output.append("=" * 70)
    output.append("✅ Processamento concluído")
    if "validation" in summaries:
        all_valid = all(is_valid for is_valid, _ in summaries["validation"].values())
        if all_valid:
            output.append("✅ Quality Gate: Todos os resumos aprovados")
        else:
            output.append("⚠️  Quality Gate: Alguns resumos falharam na validação")
    output.append("=" * 70)
    
    return "\n".join(output)


def generate_stub_summary(text: str, input_type: str = "texto") -> str:
    """
    Gera um resumo stub (placeholder) para validar o fluxo básico.
    
    Args:
        text: Texto ou conteúdo recebido
        input_type: Tipo de entrada ("texto" ou "arquivo")
    
    Returns:
        Resumo stub formatado
    """
    text_length = len(text)
    word_count = len(text.split()) if text else 0
    
    stub_summary = f"""
{'='*60}
RESUMO STUB - INCR-1
{'='*60}

Tipo de entrada: {input_type}
Tamanho do texto: {text_length} caracteres
Número de palavras: {word_count}

[STUB] Este é um resumo placeholder gerado pelo sistema.
[STUB] O sistema recebeu a entrada com sucesso.
[STUB] A geração de resumos reais será implementada no INCR-2.

Status: Sistema funcionando corretamente ✅
{'='*60}
"""
    return stub_summary


def process_input(text: str = None, file_path: str = None, use_real_summary: bool = True, 
                 export_formats: list = None, export_dir: str = "/app/volumes") -> Tuple[str, Dict]:
    """
    Processa entrada do usuário (texto ou arquivo) e gera resumos.
    
    Args:
        text: Texto direto fornecido pelo usuário
        file_path: Caminho para arquivo a ser processado
        use_real_summary: Se True, usa sumarização real (INCR-2), senão usa stub (INCR-1)
    
    Returns:
        Resumos gerados formatados
    """
    # Obter conteúdo
    if file_path:
        path = Path(file_path)
        if not path.exists():
            print(f"Erro: Arquivo não encontrado: {file_path}", file=sys.stderr)
            sys.exit(1)
        
        # Determinar tipo de arquivo
        if path.suffix.lower() == '.pdf':
            try:
                content = read_pdf_file(str(path))
            except Exception as e:
                print(f"Erro ao processar PDF: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            content = read_text_file(str(path))
    elif text:
        content = text
    else:
        print("Erro: É necessário fornecer texto ou arquivo.", file=sys.stderr)
        sys.exit(1)
    
    # Gerar resumos
    exported_files = {}
    
    if use_real_summary:
        try:
            print("Inicializando sumarizador...", file=sys.stderr)
            summarizer = BookSummarizer()
            print("Gerando resumos com Quality Gate...", file=sys.stderr)
            summaries = summarizer.generate_all_summaries(content, include_tracking=True, validate_quality=True)
            
            # Preparar metadados
            metadata = {
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "total_palavras": len(content.split())
            }
            if file_path:
                metadata["livro"] = Path(file_path).stem
            
            # Exportar se solicitado
            if export_formats:
                print(f"Exportando resumos para {', '.join(export_formats)}...", file=sys.stderr)
                base_name = Path(file_path).stem if file_path else "resumo_texto"
                exported_files = export_summaries(
                    summaries,
                    export_dir,
                    formats=export_formats,
                    base_name=base_name,
                    metadata=metadata
                )
                if exported_files:
                    print(f"✅ Arquivos exportados:", file=sys.stderr)
                    for fmt, path in exported_files.items():
                        print(f"   {fmt.upper()}: {path}", file=sys.stderr)
            
            # Gerar evidência automaticamente
            print("Gerando evidência de execução...", file=sys.stderr)
            evidence_gen = EvidenceGenerator()
            input_source = file_path if file_path else "texto direto"
            evidence_file = evidence_gen.generate_evidence(
                summaries,
                content,
                input_source,
                execution_info={
                    "exported_files": exported_files,
                    "export_formats": export_formats or []
                }
            )
            print(f"✅ Evidência gerada: {evidence_file}", file=sys.stderr)
            
            return format_summaries(summaries), exported_files
        except Exception as e:
            print(f"Erro ao gerar resumos: {e}", file=sys.stderr)
            print("Falling back para resumo stub...", file=sys.stderr)
            return generate_stub_summary(content, "texto" if text else "arquivo"), {}
    else:
        return generate_stub_summary(content, "texto" if text else "arquivo"), {}


def main():
    """Função principal da CLI."""
    parser = argparse.ArgumentParser(
        description='CoverageSummarizer - Sistema de resumo de livros (INCR-2)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Processar texto direto
  python src/main.py --text "Seu texto aqui"
  
  # Processar arquivo de texto
  python src/main.py --file livro.txt
  
  # Processar arquivo PDF
  python src/main.py --file livro.pdf
  
  # Usar resumo stub (modo de desenvolvimento)
  python src/main.py --text "teste" --stub
        """
    )
    
    # Grupo mutuamente exclusivo para entrada
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--text',
        type=str,
        help='Texto a ser processado'
    )
    input_group.add_argument(
        '--file',
        type=str,
        help='Caminho para arquivo a ser processado (texto ou PDF)'
    )
    
    parser.add_argument(
        '--stub',
        action='store_true',
        help='Usar resumo stub em vez de sumarização real (para testes)'
    )
    
    parser.add_argument(
        '--export',
        nargs='+',
        choices=['md', 'pdf'],
        help='Formatos para exportar (md, pdf, ou ambos)'
    )
    
    parser.add_argument(
        '--export-dir',
        type=str,
        default='/app/volumes',
        help='Diretório onde salvar arquivos exportados (padrão: /app/volumes)'
    )
    
    args = parser.parse_args()
    
    # Processar entrada e gerar resumos
    summary, exported_files = process_input(
        text=args.text,
        file_path=args.file,
        use_real_summary=not args.stub,
        export_formats=args.export,
        export_dir=args.export_dir
    )
    
    # Exibir resumos
    print(summary)
    
    # Informar sobre arquivos exportados
    if exported_files:
        print("\n" + "=" * 70)
        print("📁 ARQUIVOS EXPORTADOS")
        print("=" * 70)
        for fmt, path in exported_files.items():
            print(f"  {fmt.upper()}: {path}")
        print("=" * 70)


if __name__ == '__main__':
    main()
